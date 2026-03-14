from __future__ import annotations

import json
import math
import re
from itertools import combinations
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd
from scipy.stats import binomtest, chi2, friedmanchisquare, wilcoxon

from .artifacts import atomic_write_json, atomic_write_text
from .data_parser import STATUS_COMPLETED, load_inference_dataset, load_input_dataset, serialize_json_columns
from .inference import LITERARY_DEVICES
from .prose_analysis import compute_poem_features

try:
    import statsmodels.formula.api as smf
except ModuleNotFoundError:
    smf = None

ALPHA = 0.05
SCORE_METRICS = [
    "aggregate_score",
    "technical_craft_score",
    "structure_score",
    "diction_score",
    "originality_score",
    "impact_score",
]
SCORE_METRIC_LABELS = {
    "aggregate_score": "Aggregate Score",
    "technical_craft_score": "Technical Craft Score",
    "structure_score": "Structure Score",
    "diction_score": "Diction Score",
    "originality_score": "Originality Score",
    "impact_score": "Impact Score",
}
DEVICE_COLUMNS = {device: f"device_{re.sub(r'[^a-z0-9]+', '_', device.lower()).strip('_')}" for device in LITERARY_DEVICES}
DICTION_FEATURES = ["avg_word_length", "latinate_ratio", "type_token_ratio"]
AUTHOR_FEATURES = ["author_gender", "author_ethnicity", "author_nationality"]
POEM_ORIGIN_LABEL_COLUMN = "poem_origin_label"
POEM_ORIGIN_GROUP_COLUMN = "poem_origin_group"


def _require_statsmodels() -> None:
    if smf is None:
        raise RuntimeError("statsmodels is required for mixed-effects analyses")


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        numeric_value = float(value)
        if not math.isfinite(numeric_value):
            return None
        return numeric_value
    if pd.isna(value):
        return None
    return value


def _write_json(path: str | Path, payload: dict) -> None:
    atomic_write_json(path, _json_safe(payload))


def _write_markdown(path: str | Path, markdown_text: str) -> None:
    atomic_write_text(path, markdown_text)


def _emit_progress(
    progress_callback: Callable[[dict[str, Any]], None] | None,
    payload: dict[str, Any],
) -> None:
    if progress_callback is None:
        return
    try:
        progress_callback(payload)
    except Exception:
        # Progress hooks are best-effort and should not interrupt statistical work.
        return


def _adjust_pvalues_bh(results: list[dict], pvalue_key: str = "pvalue", adjusted_key: str = "adjusted_pvalue") -> list[dict]:
    valid = [(index, item[pvalue_key]) for index, item in enumerate(results) if item.get(pvalue_key) is not None]
    if not valid:
        return results
    order = sorted(valid, key=lambda item: item[1])
    adjusted = [None] * len(results)
    total = len(order)
    running_min = 1.0
    for rank, (index, pvalue) in enumerate(reversed(order), start=1):
        actual_rank = total - rank + 1
        candidate = min(running_min, pvalue * total / actual_rank)
        running_min = candidate
        adjusted[index] = min(candidate, 1.0)
    for index, value in enumerate(adjusted):
        results[index][adjusted_key] = value
    return results


def _format_pvalue(pvalue: float | None) -> str:
    if pvalue is None:
        return "N/A"
    if pvalue < 0.001:
        return "<0.001"
    return f"{pvalue:.3f}"


def _metric_label(metric: str) -> str:
    return SCORE_METRIC_LABELS.get(metric, metric.replace("_", " ").title())


def _significance_basis(row: dict) -> tuple[float | None, str]:
    if row.get("adjusted_pvalue") is not None:
        return float(row["adjusted_pvalue"]), "adjusted"
    if row.get("pvalue") is not None:
        return float(row["pvalue"]), "raw_unadjusted"
    return None, "none"


def _annotate_significance(rows: list[dict], alpha: float = ALPHA) -> list[dict]:
    for row in rows:
        pvalue, basis = _significance_basis(row)
        row["significance_basis"] = basis
        row["significant"] = bool(pvalue is not None and pvalue < alpha)
    return rows


def _significance_label(row: dict, alpha: float = ALPHA) -> str:
    pvalue, basis = _significance_basis(row)
    if pvalue is None:
        return "not testable"
    if pvalue < alpha:
        return f"significant at alpha={alpha:.2f} ({basis})"
    return f"not significant at alpha={alpha:.2f} ({basis})"


def _balanced_models(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str], list[str]]:
    analysis_df = df.copy()
    analysis_df["poem_id"] = analysis_df["poem_id"].astype(str)
    analysis_df["model"] = analysis_df["model"].astype(str)
    models = sorted(analysis_df["model"].dropna().unique().tolist())
    if not models:
        return analysis_df.iloc[0:0].copy(), [], []
    counts = analysis_df.groupby("poem_id").agg(model_count=("model", "nunique"), row_count=("model", "size"))
    balanced_ids = counts[(counts["model_count"] == len(models)) & (counts["row_count"] == len(models))].index.tolist()
    return analysis_df[analysis_df["poem_id"].isin(balanced_ids)].copy(), models, balanced_ids


def _normalize_analysis_df(df: pd.DataFrame) -> pd.DataFrame:
    analysis_df = df.copy()
    numeric_columns = [
        *SCORE_METRICS,
        *DICTION_FEATURES,
    ]
    for column in numeric_columns:
        if column in analysis_df.columns:
            analysis_df[column] = pd.to_numeric(analysis_df[column], errors="coerce")
    for feature in AUTHOR_FEATURES:
        if feature in analysis_df.columns:
            analysis_df[feature] = (
                analysis_df[feature]
                .fillna("anonymous")
                .astype(str)
                .str.strip()
                .replace({"": "anonymous", "nan": "anonymous", "None": "anonymous"})
                .str.lower()
            )
    if POEM_ORIGIN_LABEL_COLUMN in analysis_df.columns:
        analysis_df[POEM_ORIGIN_LABEL_COLUMN] = analysis_df[POEM_ORIGIN_LABEL_COLUMN].apply(
            lambda value: None if pd.isna(value) or str(value).strip() == "" else str(value).strip()
        )
    if POEM_ORIGIN_GROUP_COLUMN in analysis_df.columns:
        analysis_df[POEM_ORIGIN_GROUP_COLUMN] = analysis_df[POEM_ORIGIN_GROUP_COLUMN].apply(
            lambda value: None if pd.isna(value) or str(value).strip() == "" else str(value).strip().lower()
        )
    return analysis_df


def _origin_group_from_label(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    label = str(value).strip().lower()
    if not label:
        return None
    if label == "ai made":
        return "ai"
    return "non_ai"


def _prepare_analysis_input(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    analysis_df = _normalize_analysis_df(df)
    analysis_df = analysis_df[analysis_df["status"] == STATUS_COMPLETED].copy()
    analysis_df = analysis_df.dropna(subset=["poem_id", "model"])
    balanced_df, models, _ = _balanced_models(analysis_df)
    if balanced_df.empty:
        raise ValueError("No balanced completed poem-by-model rows are available for analysis")
    return balanced_df, models


def _prepare_metric_input(df: pd.DataFrame, metric: str) -> tuple[pd.DataFrame, list[str]]:
    analysis_df = _normalize_analysis_df(df)
    analysis_df = analysis_df[analysis_df["status"] == STATUS_COMPLETED].copy()
    analysis_df = analysis_df.dropna(subset=["poem_id", "model", metric])
    balanced_df, models, _ = _balanced_models(analysis_df)
    if balanced_df.empty:
        raise ValueError(f"No balanced completed poem-by-model rows are available for metric '{metric}'")
    return balanced_df, models


def _cochrans_q(matrix: np.ndarray) -> tuple[float | None, float | None, str | None]:
    if matrix.ndim != 2 or matrix.shape[0] < 2 or matrix.shape[1] < 2:
        return None, None, "insufficient_data"
    col_totals = matrix.sum(axis=0)
    row_totals = matrix.sum(axis=1)
    grand_total = col_totals.sum()
    denominator = matrix.shape[1] * grand_total - np.square(row_totals).sum()
    if denominator == 0:
        return None, None, "no_variation"
    statistic = float((matrix.shape[1] * (matrix.shape[1] - 1) * np.square(col_totals - (grand_total / matrix.shape[1])).sum()) / denominator)
    pvalue = float(chi2.sf(statistic, matrix.shape[1] - 1))
    return statistic, pvalue, None


def _mcnemar_test(x: np.ndarray, y: np.ndarray) -> dict:
    both_yes = int(np.sum((x == 1) & (y == 1)))
    x_only = int(np.sum((x == 1) & (y == 0)))
    y_only = int(np.sum((x == 0) & (y == 1)))
    both_no = int(np.sum((x == 0) & (y == 0)))
    discordant = x_only + y_only
    if discordant == 0:
        return {
            "status": "skipped",
            "statistic": None,
            "pvalue": None,
            "exact": True,
            "contingency_table": [[both_yes, x_only], [y_only, both_no]],
            "reason": "no_discordant_pairs",
        }
    if discordant < 25:
        pvalue = float(binomtest(min(x_only, y_only), n=discordant, p=0.5, alternative="two-sided").pvalue)
        statistic = None
        exact = True
    else:
        statistic = float(((x_only - y_only) ** 2) / discordant)
        pvalue = float(chi2.sf(statistic, 1))
        exact = False
    return {
        "status": "ok",
        "statistic": statistic,
        "pvalue": pvalue,
        "exact": exact,
        "contingency_table": [[both_yes, x_only], [y_only, both_no]],
    }


def _pair_direction(left_model: str, right_model: str, mean_difference: float | None) -> str:
    if mean_difference is None:
        return "direction unavailable"
    if mean_difference > 0:
        return f"{left_model} higher than {right_model}"
    if mean_difference < 0:
        return f"{left_model} lower than {right_model}"
    return "no directional difference"


def _pairwise_wilcoxon(pivot: pd.DataFrame, models: list[str]) -> list[dict]:
    results = []
    for left_model, right_model in combinations(models, 2):
        paired = pivot[[left_model, right_model]].dropna()
        if paired.empty:
            results.append(
                {
                    "pair": [left_model, right_model],
                    "left_model": left_model,
                    "right_model": right_model,
                    "status": "skipped",
                    "reason": "insufficient_data",
                    "n_pairs": 0,
                    "mean_difference": None,
                    "median_difference": None,
                    "pvalue": None,
                    "adjusted_pvalue": None,
                }
            )
            continue
        differences = paired[left_model] - paired[right_model]
        mean_difference = float(differences.mean())
        median_difference = float(differences.median())
        if np.allclose(differences.to_numpy(), 0.0):
            results.append(
                {
                    "pair": [left_model, right_model],
                    "left_model": left_model,
                    "right_model": right_model,
                    "status": "skipped",
                    "reason": "no_variation",
                    "n_pairs": int(len(paired)),
                    "mean_difference": mean_difference,
                    "median_difference": median_difference,
                    "pvalue": None,
                    "adjusted_pvalue": None,
                    "direction": _pair_direction(left_model, right_model, mean_difference),
                }
            )
            continue
        try:
            statistic, pvalue = wilcoxon(paired[left_model], paired[right_model], zero_method="wilcox")
        except ValueError:
            results.append(
                {
                    "pair": [left_model, right_model],
                    "left_model": left_model,
                    "right_model": right_model,
                    "status": "skipped",
                    "reason": "invalid_pairwise_input",
                    "n_pairs": int(len(paired)),
                    "mean_difference": mean_difference,
                    "median_difference": median_difference,
                    "pvalue": None,
                    "adjusted_pvalue": None,
                    "direction": _pair_direction(left_model, right_model, mean_difference),
                }
            )
            continue
        results.append(
            {
                "pair": [left_model, right_model],
                "left_model": left_model,
                "right_model": right_model,
                "status": "ok",
                "statistic": float(statistic),
                "pvalue": float(pvalue),
                "n_pairs": int(len(paired)),
                "mean_difference": mean_difference,
                "median_difference": median_difference,
                "direction": _pair_direction(left_model, right_model, mean_difference),
            }
        )
    _adjust_pvalues_bh(results)
    _annotate_significance(results, ALPHA)
    return results


def _fit_mixedlm(full_formula: str, reduced_formula: str, data: pd.DataFrame) -> dict:
    _require_statsmodels()
    reduced_result = None
    full_result = None
    last_error = None
    for method in ("lbfgs", "powell", "cg", "nm"):
        try:
            reduced_result = smf.mixedlm(reduced_formula, data=data, groups=data["poem_id"]).fit(reml=False, method=method, disp=False)
            full_result = smf.mixedlm(full_formula, data=data, groups=data["poem_id"]).fit(reml=False, method=method, disp=False)
            break
        except Exception as exc:
            last_error = exc
            reduced_result = None
            full_result = None
    if reduced_result is None or full_result is None:
        raise RuntimeError(str(last_error))
    statistic = max(0.0, float(2 * (full_result.llf - reduced_result.llf)))
    degrees_of_freedom = max(1, len(full_result.fe_params) - len(reduced_result.fe_params))
    coefficients = []
    for term in full_result.fe_params.index:
        coefficients.append(
            {
                "term": term,
                "estimate": float(full_result.fe_params[term]),
                "std_error": float(full_result.bse_fe[term]) if term in full_result.bse_fe.index else None,
                "pvalue": float(full_result.pvalues[term]) if term in full_result.pvalues.index else None,
            }
        )
    return {
        "statistic": statistic,
        "pvalue": float(chi2.sf(statistic, degrees_of_freedom)),
        "degrees_of_freedom": degrees_of_freedom,
        "coefficients": coefficients,
        "converged": bool(getattr(full_result, "converged", False)),
        "full_formula": full_formula,
        "reduced_formula": reduced_formula,
    }


def _interaction_result(full_formula: str, reduced_formula: str, data: pd.DataFrame, effect_prefix: str | None = None) -> dict:
    try:
        result = _fit_mixedlm(full_formula, reduced_formula, data)
    except Exception as exc:
        return {
            "status": "error",
            "reason": str(exc),
            "full_formula": full_formula,
            "reduced_formula": reduced_formula,
            "pvalue": None,
            "adjusted_pvalue": None,
        }
    coefficients = result["coefficients"]
    if effect_prefix is not None:
        coefficients = [item for item in coefficients if effect_prefix in item["term"]]
    return {
        "status": "ok",
        "statistic": result["statistic"],
        "pvalue": result["pvalue"],
        "degrees_of_freedom": result["degrees_of_freedom"],
        "coefficients": coefficients,
        "converged": result["converged"],
        "full_formula": full_formula,
        "reduced_formula": reduced_formula,
    }


def _extract_model_from_term(term: str) -> str | None:
    match = re.search(r"C\(model\)\[T\.([^\]]+)\]", term)
    if not match:
        return None
    return match.group(1)


def _interaction_direction_details(coefficients: list[dict]) -> list[dict]:
    details: list[dict] = []
    for item in coefficients:
        estimate = item.get("estimate")
        if estimate is None:
            continue
        numeric_estimate = float(estimate)
        model_name = _extract_model_from_term(str(item.get("term", "")))
        if numeric_estimate > 0:
            direction = "stronger positive association"
        elif numeric_estimate < 0:
            direction = "weaker or negative association"
        else:
            direction = "no directional interaction"
        details.append(
            {
                "term": str(item.get("term", "")),
                "model": model_name,
                "estimate": numeric_estimate,
                "direction": direction,
                "abs_estimate": abs(numeric_estimate),
            }
        )
    details.sort(key=lambda row: row["abs_estimate"], reverse=True)
    for row in details:
        row.pop("abs_estimate", None)
    return details


def _interaction_direction_summary(details: list[dict]) -> str:
    if not details:
        return "interaction direction unavailable"
    lead = details[0]
    model = lead.get("model") or "reference-comparison term"
    estimate = lead.get("estimate")
    direction = lead.get("direction")
    return f"Largest interaction term: {model} ({estimate:+.3f}) -> {direction}."


def build_analysis_dataset(
    input_csv: str,
    inference_csv: str,
    analysis_csv: str | None = None,
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
    sample_poems: int | None = None,
    sample_seed: int | None = None,
) -> pd.DataFrame:
    input_df = load_input_dataset(input_csv).copy()
    input_df["poem_id"] = input_df["poem_id"].astype(str)
    inference_df = load_inference_dataset(inference_csv)
    completed = inference_df[inference_df["status"] == STATUS_COMPLETED].copy()
    completed["poem_id"] = completed["poem_id"].astype(str)
    balanced_df, _, balanced_ids = _balanced_models(completed)
    if not balanced_ids:
        raise ValueError("No balanced completed poem-by-model rows are available for analysis")
    if sample_poems is not None and sample_poems > 0 and len(balanced_ids) > sample_poems:
        sampled_ids = (
            pd.Series(balanced_ids)
            .sample(n=sample_poems, random_state=sample_seed)
            .tolist()
        )
        sampled_set = set(str(poem_id) for poem_id in sampled_ids)
        balanced_df = balanced_df[balanced_df["poem_id"].astype(str).isin(sampled_set)].copy()
        balanced_ids = [poem_id for poem_id in balanced_ids if str(poem_id) in sampled_set]
    poem_context_columns = ["poem_id", "poem_text"]
    if POEM_ORIGIN_LABEL_COLUMN in input_df.columns:
        poem_context_columns.append(POEM_ORIGIN_LABEL_COLUMN)
    poem_text_df = input_df[input_df["poem_id"].isin(balanced_ids)][poem_context_columns].drop_duplicates("poem_id")
    feature_rows = []
    total_feature_rows = int(len(poem_text_df))
    _emit_progress(
        progress_callback,
        {
            "event": "feature_start",
            "stage": "stats",
            "step": "build_analysis_dataset",
            "completed_feature_rows": 0,
            "total_feature_rows": total_feature_rows,
        },
    )
    for index, row in enumerate(poem_text_df.itertuples(), start=1):
        feature_rows.append({"poem_id": row.poem_id, **compute_poem_features(row.poem_text)})
        _emit_progress(
            progress_callback,
            {
                "event": "feature_progress",
                "stage": "stats",
                "step": "build_analysis_dataset",
                "completed_feature_rows": index,
                "total_feature_rows": total_feature_rows,
            },
        )
    features_df = pd.DataFrame(feature_rows)
    analysis_df = balanced_df.merge(poem_text_df, on="poem_id", how="left")
    analysis_df = analysis_df.merge(features_df, on="poem_id", how="left")
    if POEM_ORIGIN_LABEL_COLUMN not in analysis_df.columns:
        analysis_df[POEM_ORIGIN_LABEL_COLUMN] = None
    analysis_df[POEM_ORIGIN_GROUP_COLUMN] = analysis_df[POEM_ORIGIN_LABEL_COLUMN].apply(_origin_group_from_label)
    analysis_df = _normalize_analysis_df(analysis_df)
    for device, column in DEVICE_COLUMNS.items():
        analysis_df[column] = analysis_df["literary_devices"].apply(lambda values: int(device in values))
    analysis_df = analysis_df.sort_values(["poem_id", "model"], kind="stable").reset_index(drop=True)
    if analysis_csv is not None:
        persistable = serialize_json_columns(analysis_df, ["literary_devices", "prior_knowledge_detected_models"])
        tmp_path = Path(f"{analysis_csv}.tmp")
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        persistable.to_csv(tmp_path, index=False)
        tmp_path.replace(Path(analysis_csv))
    return analysis_df


def _build_model_score_summary_for_metric(analysis_df: pd.DataFrame, metric: str) -> list[dict]:
    summary = (
        analysis_df.groupby("model", as_index=False)[metric]
        .agg(["mean", "median", "std", "min", "max", "count"])
        .reset_index()
    )
    rows: list[dict] = []
    for row in summary.itertuples(index=False):
        rows.append(
            {
                "metric": metric,
                "metric_label": _metric_label(metric),
                "model": str(row.model),
                "mean": float(row.mean),
                "median": float(row.median),
                "std_dev": float(0.0 if pd.isna(row.std) else row.std),
                "min": float(row.min),
                "max": float(row.max),
                "n": int(row.count),
            }
        )
    rows.sort(key=lambda item: item["mean"], reverse=True)
    return rows


def _run_metric_model_comparison(analysis_df: pd.DataFrame, metric: str, models: list[str]) -> dict:
    try:
        mixedlm_result = _fit_mixedlm(f"{metric} ~ C(model)", f"{metric} ~ 1", analysis_df)
        omnibus: dict[str, Any] = {
            "status": "ok",
            "method": "mixedlm",
            "models": models,
            "n_poems": int(analysis_df["poem_id"].nunique()),
            "n_rows": int(len(analysis_df)),
            "alpha": ALPHA,
            "pvalue_adjustment": "none",
            **mixedlm_result,
        }
    except Exception as exc:
        pivot = analysis_df.pivot(index="poem_id", columns="model", values=metric).reindex(columns=models).dropna()
        if pivot.shape[0] < 2:
            return {
                "status": "error",
                "method": "friedman",
                "alpha": ALPHA,
                "pvalue_adjustment": "benjamini_hochberg",
                "reason": f"mixedlm_failed: {exc}; insufficient balanced poems for Friedman fallback",
                "pairwise": [],
            }
        try:
            statistic, pvalue = friedmanchisquare(*(pivot[model].to_numpy() for model in models))
        except Exception as fallback_exc:
            return {
                "status": "error",
                "method": "friedman",
                "alpha": ALPHA,
                "pvalue_adjustment": "benjamini_hochberg",
                "reason": f"mixedlm_failed: {exc}; friedman_failed: {fallback_exc}",
                "pairwise": [],
            }
        omnibus = {
            "status": "ok",
            "method": "friedman",
            "models": models,
            "n_poems": int(pivot.shape[0]),
            "n_rows": int(len(analysis_df)),
            "alpha": ALPHA,
            "pvalue_adjustment": "none",
            "statistic": float(statistic),
            "pvalue": float(pvalue),
            "degrees_of_freedom": max(1, len(models) - 1),
            "mixedlm_error": str(exc),
            "coefficients": [],
        }

    pivot = analysis_df.pivot(index="poem_id", columns="model", values=metric).reindex(columns=models).dropna()
    pairwise = _pairwise_wilcoxon(pivot, models)
    omnibus["pairwise"] = pairwise
    omnibus["pairwise_pvalue_adjustment"] = "benjamini_hochberg"
    omnibus["significant"] = bool(omnibus.get("pvalue") is not None and float(omnibus["pvalue"]) < ALPHA)
    omnibus["significance_basis"] = "raw_unadjusted" if omnibus.get("pvalue") is not None else "none"
    return omnibus


def run_score_model_comparisons_by_metric(df: pd.DataFrame) -> dict:
    metrics_payload: dict[str, Any] = {}
    for metric in SCORE_METRICS:
        try:
            metric_df, models = _prepare_metric_input(df, metric)
        except ValueError as exc:
            metrics_payload[metric] = {
                "status": "error",
                "method": "mixedlm",
                "alpha": ALPHA,
                "pvalue_adjustment": "benjamini_hochberg",
                "reason": str(exc),
                "pairwise": [],
            }
            continue
        metrics_payload[metric] = _run_metric_model_comparison(metric_df, metric, models)
    return {
        "alpha": ALPHA,
        "pvalue_adjustment": "benjamini_hochberg",
        "metrics": metrics_payload,
    }


def run_score_summaries_by_metric(df: pd.DataFrame) -> dict:
    metrics_payload: dict[str, Any] = {}
    for metric in SCORE_METRICS:
        try:
            metric_df, _ = _prepare_metric_input(df, metric)
        except ValueError:
            metrics_payload[metric] = []
            continue
        metrics_payload[metric] = _build_model_score_summary_for_metric(metric_df, metric)
    return {
        "alpha": ALPHA,
        "pvalue_adjustment": "none",
        "metrics": metrics_payload,
    }


def run_device_detection_analysis(df: pd.DataFrame) -> dict:
    analysis_df, models = _prepare_analysis_input(df)
    results = []
    pivots: dict[str, pd.DataFrame] = {}
    for device, column in DEVICE_COLUMNS.items():
        pivot = analysis_df.pivot(index="poem_id", columns="model", values=column).reindex(columns=models).dropna()
        if pivot.empty or pivot.shape[0] < 2:
            results.append(
                {
                    "device": device,
                    "status": "skipped",
                    "reason": "insufficient_data",
                    "pvalue": None,
                    "adjusted_pvalue": None,
                    "n_poems": int(pivot.shape[0]),
                }
            )
            continue
        statistic, pvalue, reason = _cochrans_q(pivot.to_numpy(dtype=int))
        if reason is not None:
            results.append(
                {
                    "device": device,
                    "status": "skipped",
                    "reason": reason,
                    "pvalue": None,
                    "adjusted_pvalue": None,
                    "n_poems": int(pivot.shape[0]),
                }
            )
            continue
        detections_by_model = {model: int(pivot[model].sum()) for model in models}
        detection_rates_by_model = {model: float(pivot[model].mean()) for model in models}
        results.append(
            {
                "device": device,
                "status": "ok",
                "statistic": statistic,
                "pvalue": pvalue,
                "detections_by_model": detections_by_model,
                "detection_rates_by_model": detection_rates_by_model,
                "n_poems": int(pivot.shape[0]),
            }
        )
        pivots[device] = pivot

    _adjust_pvalues_bh(results)
    _annotate_significance(results, ALPHA)

    posthoc: dict[str, list[dict]] = {}
    for device, pivot in pivots.items():
        pairs: list[dict] = []
        for left_model, right_model in combinations(models, 2):
            pair_result = _mcnemar_test(
                pivot[left_model].to_numpy(dtype=int),
                pivot[right_model].to_numpy(dtype=int),
            )
            rate_difference = float(pivot[left_model].mean() - pivot[right_model].mean())
            pairs.append(
                {
                    "pair": [left_model, right_model],
                    "left_model": left_model,
                    "right_model": right_model,
                    "n_pairs": int(pivot.shape[0]),
                    "rate_difference": rate_difference,
                    "direction": _pair_direction(left_model, right_model, rate_difference),
                    **pair_result,
                }
            )
        _adjust_pvalues_bh(pairs)
        _annotate_significance(pairs, ALPHA)
        posthoc[device] = pairs

    return {
        "status": "ok",
        "method": "cochrans_q",
        "models": models,
        "n_poems": int(analysis_df["poem_id"].nunique()),
        "alpha": ALPHA,
        "pvalue_adjustment": "benjamini_hochberg",
        "posthoc_pvalue_adjustment": "benjamini_hochberg",
        "tests": results,
        "posthoc": posthoc,
    }


def _run_device_interactions_for_metric(df: pd.DataFrame, metric: str) -> dict:
    base_df, _ = _prepare_metric_input(df, metric)
    tests = []
    for device, column in DEVICE_COLUMNS.items():
        working_df = base_df.dropna(subset=[metric, column]).copy()
        working_df, models, _ = _balanced_models(working_df)
        if working_df.empty or len(models) < 2:
            tests.append({"device": device, "status": "skipped", "reason": "insufficient_data", "pvalue": None, "adjusted_pvalue": None})
            continue
        if working_df[column].nunique() < 2:
            tests.append({"device": device, "status": "skipped", "reason": "no_variation", "pvalue": None, "adjusted_pvalue": None})
            continue
        result = _interaction_result(
            f"{metric} ~ C(model) * {column}",
            f"{metric} ~ C(model) + {column}",
            working_df,
            effect_prefix=f":{column}",
        )
        result["models"] = models
        result["n_poems"] = int(working_df["poem_id"].nunique())
        result["n_rows"] = int(len(working_df))
        if result.get("status") == "ok":
            details = _interaction_direction_details(result.get("coefficients", []))
            result["direction_by_model"] = details
            result["direction_summary"] = _interaction_direction_summary(details)
        tests.append({"device": device, **result})
    _adjust_pvalues_bh(tests)
    _annotate_significance(tests, ALPHA)
    return {
        "status": "ok",
        "method": "mixedlm",
        "alpha": ALPHA,
        "pvalue_adjustment": "benjamini_hochberg",
        "metric": metric,
        "tests": tests,
    }


def _run_diction_interactions_for_metric(df: pd.DataFrame, metric: str) -> dict:
    base_df, _ = _prepare_metric_input(df, metric)
    tests = []
    for feature in DICTION_FEATURES:
        working_df = base_df[np.isfinite(base_df[feature])].copy()
        working_df, models, _ = _balanced_models(working_df)
        if working_df.empty or len(models) < 2:
            tests.append({"feature": feature, "status": "skipped", "reason": "insufficient_data", "pvalue": None, "adjusted_pvalue": None})
            continue
        if working_df[feature].nunique() < 2:
            tests.append({"feature": feature, "status": "skipped", "reason": "insufficient_variation", "pvalue": None, "adjusted_pvalue": None})
            continue
        result = _interaction_result(
            f"{metric} ~ C(model) * {feature}",
            f"{metric} ~ C(model) + {feature}",
            working_df,
            effect_prefix=f":{feature}",
        )
        result["models"] = models
        result["n_poems"] = int(working_df["poem_id"].nunique())
        result["n_rows"] = int(len(working_df))
        if result.get("status") == "ok":
            details = _interaction_direction_details(result.get("coefficients", []))
            result["direction_by_model"] = details
            result["direction_summary"] = _interaction_direction_summary(details)
        tests.append({"feature": feature, **result})
    _adjust_pvalues_bh(tests)
    _annotate_significance(tests, ALPHA)
    return {
        "status": "ok",
        "method": "mixedlm",
        "alpha": ALPHA,
        "pvalue_adjustment": "benjamini_hochberg",
        "metric": metric,
        "tests": tests,
    }


def _author_feature_sparse(df: pd.DataFrame, feature: str) -> bool:
    counts = df[["poem_id", feature]].drop_duplicates()[feature].value_counts()
    return counts.empty or (counts < 2).any()


def _run_author_interactions_for_metric(df: pd.DataFrame, metric: str) -> dict:
    base_df, _ = _prepare_metric_input(df, metric)
    tests = []
    for feature in AUTHOR_FEATURES:
        working_df = base_df.dropna(subset=[feature]).copy()
        working_df, models, _ = _balanced_models(working_df)
        if working_df.empty or len(models) < 2:
            tests.append({"feature": feature, "status": "skipped", "reason": "insufficient_data", "pvalue": None, "adjusted_pvalue": None})
            continue
        if working_df[feature].nunique() < 2:
            tests.append({"feature": feature, "status": "skipped", "reason": "insufficient_variation", "pvalue": None, "adjusted_pvalue": None})
            continue
        if _author_feature_sparse(working_df, feature):
            tests.append({"feature": feature, "status": "skipped", "reason": "sparse_categories", "pvalue": None, "adjusted_pvalue": None})
            continue
        result = _interaction_result(
            f"{metric} ~ C(model) * C({feature})",
            f"{metric} ~ C(model) + C({feature})",
            working_df,
            effect_prefix=":C(",
        )
        result["models"] = models
        result["n_poems"] = int(working_df["poem_id"].nunique())
        result["n_rows"] = int(len(working_df))
        if result.get("status") == "ok":
            details = _interaction_direction_details(result.get("coefficients", []))
            result["direction_by_model"] = details
            result["direction_summary"] = _interaction_direction_summary(details)
        tests.append({"feature": feature, **result})
    _adjust_pvalues_bh(tests)
    _annotate_significance(tests, ALPHA)
    return {
        "status": "ok",
        "method": "mixedlm",
        "alpha": ALPHA,
        "pvalue_adjustment": "benjamini_hochberg",
        "metric": metric,
        "tests": tests,
    }


def run_device_score_interactions_by_metric(df: pd.DataFrame) -> dict:
    metrics_payload: dict[str, Any] = {}
    for metric in SCORE_METRICS:
        try:
            metrics_payload[metric] = _run_device_interactions_for_metric(df, metric)
        except ValueError as exc:
            metrics_payload[metric] = {
                "status": "error",
                "method": "mixedlm",
                "metric": metric,
                "alpha": ALPHA,
                "pvalue_adjustment": "benjamini_hochberg",
                "reason": str(exc),
                "tests": [],
            }
    return {
        "alpha": ALPHA,
        "pvalue_adjustment": "benjamini_hochberg",
        "metrics": metrics_payload,
    }


def run_diction_score_interactions_by_metric(df: pd.DataFrame) -> dict:
    metrics_payload: dict[str, Any] = {}
    for metric in SCORE_METRICS:
        try:
            metrics_payload[metric] = _run_diction_interactions_for_metric(df, metric)
        except ValueError as exc:
            metrics_payload[metric] = {
                "status": "error",
                "method": "mixedlm",
                "metric": metric,
                "alpha": ALPHA,
                "pvalue_adjustment": "benjamini_hochberg",
                "reason": str(exc),
                "tests": [],
            }
    return {
        "alpha": ALPHA,
        "pvalue_adjustment": "benjamini_hochberg",
        "metrics": metrics_payload,
    }


def run_author_score_interactions_by_metric(df: pd.DataFrame) -> dict:
    metrics_payload: dict[str, Any] = {}
    for metric in SCORE_METRICS:
        try:
            metrics_payload[metric] = _run_author_interactions_for_metric(df, metric)
        except ValueError as exc:
            metrics_payload[metric] = {
                "status": "error",
                "method": "mixedlm",
                "metric": metric,
                "alpha": ALPHA,
                "pvalue_adjustment": "benjamini_hochberg",
                "reason": str(exc),
                "tests": [],
            }
    return {
        "alpha": ALPHA,
        "pvalue_adjustment": "benjamini_hochberg",
        "metrics": metrics_payload,
    }


def _prepare_ai_origin_metric_input(df: pd.DataFrame, metric: str) -> tuple[pd.DataFrame, list[str]]:
    analysis_df = _normalize_analysis_df(df)
    if POEM_ORIGIN_LABEL_COLUMN not in analysis_df.columns:
        raise ValueError("missing_origin_label")
    if POEM_ORIGIN_GROUP_COLUMN not in analysis_df.columns:
        analysis_df[POEM_ORIGIN_GROUP_COLUMN] = analysis_df[POEM_ORIGIN_LABEL_COLUMN].apply(_origin_group_from_label)
    analysis_df = analysis_df[analysis_df["status"] == STATUS_COMPLETED].copy()
    analysis_df = analysis_df.dropna(subset=["poem_id", "model", metric])
    analysis_df = analysis_df[analysis_df[POEM_ORIGIN_GROUP_COLUMN].isin(["ai", "non_ai"])].copy()
    if analysis_df.empty:
        raise ValueError("no_rows_with_origin_labels")
    if analysis_df[POEM_ORIGIN_GROUP_COLUMN].nunique() < 2:
        raise ValueError("insufficient_origin_groups")
    origin_counts = analysis_df[["poem_id", POEM_ORIGIN_GROUP_COLUMN]].drop_duplicates()[POEM_ORIGIN_GROUP_COLUMN].value_counts()
    if origin_counts.empty or (origin_counts < 2).any():
        raise ValueError("sparse_origin_groups")
    balanced_df, models, _ = _balanced_models(analysis_df)
    if balanced_df.empty:
        raise ValueError("no_balanced_origin_rows")
    if balanced_df[POEM_ORIGIN_GROUP_COLUMN].nunique() < 2:
        raise ValueError("insufficient_origin_groups_after_balance")
    return balanced_df, models


def _origin_gap_by_model(analysis_df: pd.DataFrame, metric: str, models: list[str]) -> dict[str, dict[str, float | int | None]]:
    gaps: dict[str, dict[str, float | int | None]] = {}
    for model in models:
        model_df = analysis_df[analysis_df["model"] == model]
        ai_series = model_df[model_df[POEM_ORIGIN_GROUP_COLUMN] == "ai"][metric]
        non_ai_series = model_df[model_df[POEM_ORIGIN_GROUP_COLUMN] == "non_ai"][metric]
        ai_mean = None if ai_series.empty else float(ai_series.mean())
        non_ai_mean = None if non_ai_series.empty else float(non_ai_series.mean())
        ai_minus_non_ai = None
        if ai_mean is not None and non_ai_mean is not None:
            ai_minus_non_ai = float(ai_mean - non_ai_mean)
        gaps[model] = {
            "ai_mean": ai_mean,
            "non_ai_mean": non_ai_mean,
            "ai_minus_non_ai": ai_minus_non_ai,
            "n_ai_poems": int(ai_series.shape[0]),
            "n_non_ai_poems": int(non_ai_series.shape[0]),
        }
    return gaps


def _pairwise_origin_gap_differences(analysis_df: pd.DataFrame, metric: str, models: list[str], gaps: dict[str, dict[str, float | int | None]]) -> list[dict]:
    pairwise_results: list[dict] = []
    for left_model, right_model in combinations(models, 2):
        left_gap = gaps.get(left_model, {}).get("ai_minus_non_ai")
        right_gap = gaps.get(right_model, {}).get("ai_minus_non_ai")
        gap_difference = None
        direction = "direction unavailable"
        if left_gap is not None and right_gap is not None:
            gap_difference = float(left_gap) - float(right_gap)
            direction = _pair_direction(left_model, right_model, gap_difference)
        subset = analysis_df[analysis_df["model"].isin([left_model, right_model])].copy()
        if subset.empty or subset[POEM_ORIGIN_GROUP_COLUMN].nunique() < 2:
            pairwise_results.append(
                {
                    "pair": [left_model, right_model],
                    "left_model": left_model,
                    "right_model": right_model,
                    "status": "skipped",
                    "reason": "insufficient_origin_groups",
                    "n_poems": int(subset["poem_id"].nunique()),
                    "n_rows": int(len(subset)),
                    "gap_difference": gap_difference,
                    "direction": direction,
                    "pvalue": None,
                    "adjusted_pvalue": None,
                }
            )
            continue
        interaction = _interaction_result(
            f"{metric} ~ C(model) * C({POEM_ORIGIN_GROUP_COLUMN})",
            f"{metric} ~ C(model) + C({POEM_ORIGIN_GROUP_COLUMN})",
            subset,
            effect_prefix=f":C({POEM_ORIGIN_GROUP_COLUMN})",
        )
        pairwise_results.append(
            {
                "pair": [left_model, right_model],
                "left_model": left_model,
                "right_model": right_model,
                "n_poems": int(subset["poem_id"].nunique()),
                "n_rows": int(len(subset)),
                "gap_difference": gap_difference,
                "direction": direction,
                **interaction,
            }
        )
    _adjust_pvalues_bh(pairwise_results)
    _annotate_significance(pairwise_results, ALPHA)
    return pairwise_results


def _run_ai_origin_interactions_for_metric(df: pd.DataFrame, metric: str) -> dict:
    try:
        working_df, models = _prepare_ai_origin_metric_input(df, metric)
    except ValueError as exc:
        return {
            "status": "skipped",
            "method": "mixedlm",
            "metric": metric,
            "alpha": ALPHA,
            "pvalue_adjustment": "benjamini_hochberg",
            "reason": str(exc),
            "pairwise": [],
            "ai_minus_non_ai_by_model": {},
        }

    omnibus = _interaction_result(
        f"{metric} ~ C(model) * C({POEM_ORIGIN_GROUP_COLUMN})",
        f"{metric} ~ C(model) + C({POEM_ORIGIN_GROUP_COLUMN})",
        working_df,
        effect_prefix=f":C({POEM_ORIGIN_GROUP_COLUMN})",
    )
    gaps = _origin_gap_by_model(working_df, metric, models)
    pairwise = _pairwise_origin_gap_differences(working_df, metric, models, gaps)

    result: dict[str, Any] = {
        "method": "mixedlm",
        "metric": metric,
        "alpha": ALPHA,
        "pvalue_adjustment": "benjamini_hochberg",
        "pairwise_pvalue_adjustment": "benjamini_hochberg",
        "models": models,
        "n_poems": int(working_df["poem_id"].nunique()),
        "n_rows": int(len(working_df)),
        "ai_minus_non_ai_by_model": gaps,
        "pairwise": pairwise,
        **omnibus,
    }
    if result.get("status") == "ok":
        result["direction_by_model"] = _interaction_direction_details(result.get("coefficients", []))
        result["direction_summary"] = _interaction_direction_summary(result.get("direction_by_model", []))
        result["significance_basis"] = "raw_unadjusted" if result.get("pvalue") is not None else "none"
        result["significant"] = bool(result.get("pvalue") is not None and float(result["pvalue"]) < ALPHA)
    else:
        result.setdefault("significance_basis", "none")
        result.setdefault("significant", False)
    return result


def run_ai_origin_score_interactions_by_metric(df: pd.DataFrame) -> dict:
    metrics_payload: dict[str, Any] = {}
    for metric in SCORE_METRICS:
        metrics_payload[metric] = _run_ai_origin_interactions_for_metric(df, metric)
    return {
        "alpha": ALPHA,
        "pvalue_adjustment": "benjamini_hochberg",
        "metrics": metrics_payload,
    }


def run_ai_origin_score_interactions(df: pd.DataFrame) -> dict:
    by_metric = run_ai_origin_score_interactions_by_metric(df)
    return by_metric.get("metrics", {}).get("aggregate_score", {"status": "error", "reason": "aggregate_score_not_available"})


def run_overall_score_analysis(df: pd.DataFrame) -> dict:
    by_metric = run_score_model_comparisons_by_metric(df)
    return by_metric.get("metrics", {}).get("aggregate_score", {"status": "error", "reason": "aggregate_score_not_available"})


def run_device_score_interactions(df: pd.DataFrame) -> dict:
    by_metric = run_device_score_interactions_by_metric(df)
    return by_metric.get("metrics", {}).get("aggregate_score", {"status": "error", "reason": "aggregate_score_not_available"})


def run_diction_score_interactions(df: pd.DataFrame) -> dict:
    by_metric = run_diction_score_interactions_by_metric(df)
    return by_metric.get("metrics", {}).get("aggregate_score", {"status": "error", "reason": "aggregate_score_not_available"})


def run_author_score_interactions(df: pd.DataFrame) -> dict:
    by_metric = run_author_score_interactions_by_metric(df)
    return by_metric.get("metrics", {}).get("aggregate_score", {"status": "error", "reason": "aggregate_score_not_available"})


def _render_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    if not rows:
        return ["No rows.", ""]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    return lines


def _render_score_summaries(section: dict[str, Any]) -> list[str]:
    lines = ["## Score Summaries By Metric", f"- Alpha: {section.get('alpha', ALPHA):.2f}", ""]
    metrics = section.get("metrics", {})
    for metric in SCORE_METRICS:
        rows = metrics.get(metric, [])
        lines.append(f"### {_metric_label(metric)} (`{metric}`)")
        table_rows = [
            [
                str(row.get("model", "N/A")),
                f"{float(row.get('mean', 0.0)):.3f}",
                f"{float(row.get('median', 0.0)):.3f}",
                f"{float(row.get('std_dev', 0.0)):.3f}",
                f"{float(row.get('min', 0.0)):.3f}",
                f"{float(row.get('max', 0.0)):.3f}",
                str(row.get("n", 0)),
            ]
            for row in rows
        ]
        lines.extend(
            _render_table(
                ["Model", "Mean", "Median", "Std Dev", "Min", "Max", "N"],
                table_rows,
            )
        )
    return lines


def _render_model_comparisons(section: dict[str, Any]) -> list[str]:
    lines = [
        "## Model Comparisons By Score Metric",
        f"- Alpha: {section.get('alpha', ALPHA):.2f}",
        f"- Pairwise p-value adjustment: {section.get('pvalue_adjustment', 'none')}",
        "",
    ]
    metrics = section.get("metrics", {})
    for metric in SCORE_METRICS:
        payload = metrics.get(metric, {})
        lines.append(f"### {_metric_label(metric)} (`{metric}`)")
        if payload.get("status") != "ok":
            lines.extend(
                [
                    f"- Status: {payload.get('status', 'error')}",
                    f"- Reason: {payload.get('reason', 'unknown')}",
                    "",
                ]
            )
            continue
        lines.extend(
            [
                f"- Method: `{payload.get('method', 'N/A')}`",
                f"- Omnibus p-value: {_format_pvalue(payload.get('pvalue'))}",
                f"- Omnibus significance: {_significance_label(payload, ALPHA)}",
                f"- Balanced poems: {payload.get('n_poems', 0)}",
                f"- Balanced rows: {payload.get('n_rows', 0)}",
                "",
                "#### Pairwise Model Differences",
            ]
        )
        pairwise_rows = []
        direction_lines = []
        for row in payload.get("pairwise", []):
            direction = str(row.get("direction", "direction unavailable"))
            if row.get("status") == "ok":
                direction_lines.append(
                    f"- {row.get('left_model')} vs {row.get('right_model')}: {direction}; "
                    f"mean paired difference = {float(row.get('mean_difference', 0.0)):+.3f}."
                )
            pairwise_rows.append(
                [
                    f"{row.get('left_model', 'N/A')} vs {row.get('right_model', 'N/A')}",
                    str(row.get("status", "N/A")),
                    str(row.get("n_pairs", "N/A")),
                    "N/A" if row.get("mean_difference") is None else f"{float(row.get('mean_difference')):+.3f}",
                    "N/A" if row.get("median_difference") is None else f"{float(row.get('median_difference')):+.3f}",
                    _format_pvalue(row.get("pvalue")),
                    _format_pvalue(row.get("adjusted_pvalue")),
                    "yes" if row.get("significant") else "no",
                    row.get("significance_basis", "none"),
                    direction,
                    row.get("reason", ""),
                ]
            )
        lines.extend(
            _render_table(
                [
                    "Pair",
                    "Status",
                    "N pairs",
                    "Mean diff (left-right)",
                    "Median diff",
                    "P",
                    "Adj P",
                    "Significant",
                    "Basis",
                    "Direction",
                    "Reason",
                ],
                pairwise_rows,
            )
        )
        lines.append("#### Direction Narrative")
        if direction_lines:
            lines.extend(direction_lines)
            lines.append("")
        else:
            lines.extend(["- No pairwise directional narrative available.", ""])
    return lines


def _render_device_detection(section: dict[str, Any]) -> list[str]:
    lines = [
        "## Device Detection Tests",
        f"- Alpha: {section.get('alpha', ALPHA):.2f}",
        f"- Device-level p-value adjustment: {section.get('pvalue_adjustment', 'none')}",
        f"- Posthoc p-value adjustment: {section.get('posthoc_pvalue_adjustment', 'none')}",
        "",
        "### Omnibus Device Tests",
    ]
    test_rows = []
    for row in section.get("tests", []):
        rate_snapshot = row.get("detection_rates_by_model", {})
        rate_text = ", ".join(f"{model}: {float(rate):.3f}" for model, rate in sorted(rate_snapshot.items()))
        test_rows.append(
            [
                str(row.get("device", "N/A")),
                str(row.get("status", "N/A")),
                str(row.get("n_poems", "N/A")),
                _format_pvalue(row.get("pvalue")),
                _format_pvalue(row.get("adjusted_pvalue")),
                "yes" if row.get("significant") else "no",
                row.get("significance_basis", "none"),
                rate_text,
                row.get("reason", ""),
            ]
        )
    lines.extend(
        _render_table(
            ["Device", "Status", "N poems", "P", "Adj P", "Significant", "Basis", "Rates by model", "Reason"],
            test_rows,
        )
    )

    lines.append("### Device Posthoc Pairwise Results")
    posthoc = section.get("posthoc", {})
    for device in sorted(posthoc.keys()):
        lines.append(f"#### {device}")
        pair_rows = []
        direction_lines = []
        for row in posthoc.get(device, []):
            pair_rows.append(
                [
                    f"{row.get('left_model', 'N/A')} vs {row.get('right_model', 'N/A')}",
                    str(row.get("status", "N/A")),
                    str(row.get("n_pairs", "N/A")),
                    "N/A" if row.get("rate_difference") is None else f"{float(row.get('rate_difference')):+.3f}",
                    _format_pvalue(row.get("pvalue")),
                    _format_pvalue(row.get("adjusted_pvalue")),
                    "yes" if row.get("significant") else "no",
                    row.get("significance_basis", "none"),
                    row.get("direction", ""),
                    row.get("reason", ""),
                ]
            )
            if row.get("status") == "ok":
                direction_lines.append(
                    f"- {row.get('left_model')} vs {row.get('right_model')}: {row.get('direction')}; "
                    f"detection-rate difference = {float(row.get('rate_difference', 0.0)):+.3f}."
                )
        lines.extend(
            _render_table(
                [
                    "Pair",
                    "Status",
                    "N pairs",
                    "Rate diff (left-right)",
                    "P",
                    "Adj P",
                    "Significant",
                    "Basis",
                    "Direction",
                    "Reason",
                ],
                pair_rows,
            )
        )
        lines.append("Direction Narrative")
        if direction_lines:
            lines.extend(direction_lines)
            lines.append("")
        else:
            lines.extend(["- No directional posthoc narrative available.", ""])
    if not posthoc:
        lines.extend(["No posthoc device tests available.", ""])
    return lines


def _render_interaction_section(
    title: str,
    section: dict[str, Any],
    label_key: str,
) -> list[str]:
    lines = [
        f"## {title}",
        f"- Alpha: {section.get('alpha', ALPHA):.2f}",
        f"- P-value adjustment: {section.get('pvalue_adjustment', 'none')}",
        "",
    ]
    metrics = section.get("metrics", {})
    for metric in SCORE_METRICS:
        payload = metrics.get(metric, {})
        lines.append(f"### {_metric_label(metric)} (`{metric}`)")
        if payload.get("status") != "ok":
            lines.extend(
                [
                    f"- Status: {payload.get('status', 'error')}",
                    f"- Reason: {payload.get('reason', 'unknown')}",
                    "",
                ]
            )
            continue
        table_rows = []
        direction_lines = []
        for row in payload.get("tests", []):
            table_rows.append(
                [
                    str(row.get(label_key, "N/A")),
                    str(row.get("status", "N/A")),
                    str(row.get("n_poems", "N/A")),
                    _format_pvalue(row.get("pvalue")),
                    _format_pvalue(row.get("adjusted_pvalue")),
                    "yes" if row.get("significant") else "no",
                    row.get("significance_basis", "none"),
                    row.get("direction_summary", ""),
                    row.get("reason", ""),
                ]
            )
            for detail in row.get("direction_by_model", []):
                model_name = detail.get("model") or "reference-comparison term"
                direction_lines.append(
                    f"- {row.get(label_key)}: {model_name} term `{detail.get('term')}` = {float(detail.get('estimate', 0.0)):+.3f} -> {detail.get('direction')}"
                )
        lines.extend(
            _render_table(
                [
                    label_key.replace("_", " ").title(),
                    "Status",
                    "N poems",
                    "P",
                    "Adj P",
                    "Significant",
                    "Basis",
                    "Direction summary",
                    "Reason",
                ],
                table_rows,
            )
        )
        lines.append("Direction Narrative")
        if direction_lines:
            lines.extend(direction_lines)
            lines.append("")
        else:
            lines.extend(["- No interaction-direction narrative available.", ""])
    return lines


def _render_ai_origin_interactions_section(section: dict[str, Any]) -> list[str]:
    lines = [
        "## AI-vs-Non-AI Preference Interactions By Metric",
        f"- Alpha: {section.get('alpha', ALPHA):.2f}",
        f"- Pairwise p-value adjustment: {section.get('pvalue_adjustment', 'none')}",
        "- Inferential claims here are based on cross-model interaction tests (omnibus and pairwise gap-difference tests) only.",
        "- Per-model AI-minus-Non-AI values below are descriptive effect summaries, not standalone significance tests.",
        "",
    ]
    metrics = section.get("metrics", {})
    for metric in SCORE_METRICS:
        payload = metrics.get(metric, {})
        lines.append(f"### {_metric_label(metric)} (`{metric}`)")
        if payload.get("status") != "ok":
            lines.extend(
                [
                    f"- Status: {payload.get('status', 'skipped')}",
                    f"- Reason: {payload.get('reason', 'unknown')}",
                    "",
                ]
            )
            continue
        lines.extend(
            [
                f"- Method: `{payload.get('method', 'N/A')}`",
                f"- Omnibus p-value: {_format_pvalue(payload.get('pvalue'))}",
                f"- Omnibus significance: {_significance_label(payload, ALPHA)}",
                "",
                "#### Descriptive AI-minus-Non-AI Gap By Model (Not a Standalone Test)",
            ]
        )
        gap_rows = []
        for model in payload.get("models", []):
            item = payload.get("ai_minus_non_ai_by_model", {}).get(model, {})
            gap_rows.append(
                [
                    model,
                    _format_pvalue(item.get("ai_mean")),
                    _format_pvalue(item.get("non_ai_mean")),
                    "N/A" if item.get("ai_minus_non_ai") is None else f"{float(item.get('ai_minus_non_ai')):+.3f}",
                    str(item.get("n_ai_poems", 0)),
                    str(item.get("n_non_ai_poems", 0)),
                ]
            )
        lines.extend(
            _render_table(
                ["Model", "AI mean", "Non-AI mean", "AI - Non-AI", "N AI", "N Non-AI"],
                gap_rows,
            )
        )

        lines.append("#### Pairwise Gap-Difference Interaction Tests")
        pair_rows = []
        direction_lines = []
        for row in payload.get("pairwise", []):
            pair_rows.append(
                [
                    f"{row.get('left_model', 'N/A')} vs {row.get('right_model', 'N/A')}",
                    str(row.get("status", "N/A")),
                    str(row.get("n_poems", "N/A")),
                    "N/A" if row.get("gap_difference") is None else f"{float(row.get('gap_difference')):+.3f}",
                    _format_pvalue(row.get("pvalue")),
                    _format_pvalue(row.get("adjusted_pvalue")),
                    "yes" if row.get("significant") else "no",
                    row.get("significance_basis", "none"),
                    row.get("direction", ""),
                    row.get("reason", ""),
                ]
            )
            if row.get("status") == "ok":
                direction_lines.append(
                    f"- {row.get('left_model')} vs {row.get('right_model')}: {row.get('direction')}; "
                    f"gap-difference (AI-minus-Non-AI) = {float(row.get('gap_difference', 0.0)):+.3f}."
                )
        lines.extend(
            _render_table(
                ["Pair", "Status", "N poems", "Gap diff", "P", "Adj P", "Significant", "Basis", "Direction", "Reason"],
                pair_rows,
            )
        )
        lines.append("Direction Narrative")
        if direction_lines:
            lines.extend(direction_lines)
            lines.append("")
        else:
            lines.extend(["- No pairwise origin-gap directional narrative available.", ""])
    return lines


def _format_significance_evidence(row: dict) -> str:
    pvalue, basis = _significance_basis(row)
    if pvalue is None:
        return "N/A"
    label = "Adj P" if basis == "adjusted" else "P"
    return f"{label}={_format_pvalue(pvalue)} ({basis})"


def _collect_significant_result_categories(results: dict[str, Any]) -> dict[str, list[list[str]]]:
    categories: dict[str, list[list[str]]] = {
        "Score Model Comparisons": [],
        "Device Detection": [],
        "Device x Model Score Interactions": [],
        "Diction x Model Score Interactions": [],
        "Author x Model Score Interactions": [],
        "AI-vs-Non-AI Gap-Difference Interactions": [],
    }

    score_metrics = results.get("score_model_comparisons_by_metric", {}).get("metrics", {})
    for metric, payload in score_metrics.items():
        if payload.get("status") == "ok" and payload.get("significant"):
            categories["Score Model Comparisons"].append(
                [
                    f"Omnibus `{metric}` (all models)",
                    _format_significance_evidence(payload),
                    "At least one model differs on this score metric.",
                ]
            )
        for pair in payload.get("pairwise", []):
            if pair.get("status") == "ok" and pair.get("significant"):
                mean_difference = pair.get("mean_difference")
                mean_diff_text = "N/A" if mean_difference is None else f"{float(mean_difference):+.3f}"
                categories["Score Model Comparisons"].append(
                    [
                        f"Pairwise `{metric}`: {pair.get('left_model')} vs {pair.get('right_model')}",
                        _format_significance_evidence(pair),
                        f"{pair.get('direction', 'direction unavailable')}; mean diff={mean_diff_text}.",
                    ]
                )

    for row in results.get("device_detection", {}).get("tests", []):
        if row.get("status") == "ok" and row.get("significant"):
            rate_snapshot = row.get("detection_rates_by_model", {})
            if rate_snapshot:
                ranked = sorted(rate_snapshot.items(), key=lambda item: float(item[1]), reverse=True)
                top_model, top_rate = ranked[0]
                low_model, low_rate = ranked[-1]
                direction_text = f"Highest detection: {top_model} ({float(top_rate):.3f}); lowest: {low_model} ({float(low_rate):.3f})."
            else:
                direction_text = "Detection-rate breakdown unavailable."
            categories["Device Detection"].append(
                [
                    f"Omnibus device `{row.get('device')}`",
                    _format_significance_evidence(row),
                    direction_text,
                ]
            )
    for device, rows in results.get("device_detection", {}).get("posthoc", {}).items():
        for row in rows:
            if row.get("status") == "ok" and row.get("significant"):
                rate_difference = row.get("rate_difference")
                rate_diff_text = "N/A" if rate_difference is None else f"{float(rate_difference):+.3f}"
                categories["Device Detection"].append(
                    [
                        f"Pairwise device `{device}`: {row.get('left_model')} vs {row.get('right_model')}",
                        _format_significance_evidence(row),
                        f"{row.get('direction', 'direction unavailable')}; rate diff={rate_diff_text}.",
                    ]
                )

    interaction_sections = (
        ("device_score_interactions_by_metric", "device", "Device x Model Score Interactions"),
        ("diction_score_interactions_by_metric", "feature", "Diction x Model Score Interactions"),
        ("author_score_interactions_by_metric", "feature", "Author x Model Score Interactions"),
    )
    for section_name, label_key, category_name in interaction_sections:
        metrics = results.get(section_name, {}).get("metrics", {})
        for metric, payload in metrics.items():
            for row in payload.get("tests", []):
                if row.get("status") == "ok" and row.get("significant"):
                    categories[category_name].append(
                        [
                            f"`{metric}` / `{row.get(label_key)}`",
                            _format_significance_evidence(row),
                            row.get("direction_summary", "interaction direction unavailable"),
                        ]
                    )

    origin_metrics = results.get("ai_origin_score_interactions_by_metric", {}).get("metrics", {})
    for metric, payload in origin_metrics.items():
        if payload.get("status") == "ok" and payload.get("significant"):
            categories["AI-vs-Non-AI Gap-Difference Interactions"].append(
                [
                    f"Omnibus `{metric}` (model x origin)",
                    _format_significance_evidence(payload),
                    "Models differ in AI-minus-Non-AI gap size.",
                ]
            )
        for pair in payload.get("pairwise", []):
            if pair.get("status") == "ok" and pair.get("significant"):
                gap_difference = pair.get("gap_difference")
                gap_diff_text = "N/A" if gap_difference is None else f"{float(gap_difference):+.3f}"
                categories["AI-vs-Non-AI Gap-Difference Interactions"].append(
                    [
                        f"Pairwise `{metric}`: {pair.get('left_model')} vs {pair.get('right_model')}",
                        _format_significance_evidence(pair),
                        f"{pair.get('direction', 'direction unavailable')}; gap diff={gap_diff_text}.",
                    ]
                )

    return {category: rows for category, rows in categories.items() if rows}


def _render_significant_results_section(results: dict[str, Any]) -> list[str]:
    lines = [
        "## Significant Results Only",
        "- This section contains only statistically significant findings.",
        f"- Decision rule: alpha = {results.get('alpha', ALPHA):.2f}, using adjusted p-values when available.",
        "- AI-vs-Non-AI claims here are only cross-model gap-difference tests (interaction tests), not within-model preference tests.",
        "",
    ]
    categories = _collect_significant_result_categories(results)
    if not categories:
        lines.append("- No significant results at alpha=0.05.")
        lines.append("")
        return lines

    total_rows = sum(len(rows) for rows in categories.values())
    lines.extend([f"- Significant findings: {total_rows}", ""])
    category_order = [
        "Score Model Comparisons",
        "Device Detection",
        "Device x Model Score Interactions",
        "Diction x Model Score Interactions",
        "Author x Model Score Interactions",
        "AI-vs-Non-AI Gap-Difference Interactions",
    ]
    for category in category_order:
        rows = categories.get(category, [])
        if not rows:
            continue
        lines.append(f"### {category}")
        lines.extend(_render_table(["Result", "Evidence", "Direction"], rows))
    return lines


def _collect_skipped_or_error_rows(results: dict[str, Any]) -> list[str]:
    lines: list[str] = []

    for section_name in (
        "device_detection",
        "device_score_interactions",
        "diction_score_interactions",
        "author_score_interactions",
        "ai_origin_score_interactions",
    ):
        section = results.get(section_name, {})
        for item in section.get("tests", []):
            status = item.get("status")
            if status in {"skipped", "error"}:
                label = item.get("device") or item.get("feature") or "unknown"
                lines.append(f"- `{section_name}` / `{label}`: status={status}; reason={item.get('reason', 'unknown')}")

    by_metric_sections = (
        "score_model_comparisons_by_metric",
        "device_score_interactions_by_metric",
        "diction_score_interactions_by_metric",
        "author_score_interactions_by_metric",
        "ai_origin_score_interactions_by_metric",
    )
    for section_name in by_metric_sections:
        section = results.get(section_name, {})
        metrics = section.get("metrics", {}) if isinstance(section, dict) else {}
        for metric, payload in metrics.items():
            if payload.get("status") in {"error", "skipped"}:
                lines.append(
                    f"- `{section_name}` / `{metric}`: status={payload.get('status')}; reason={payload.get('reason', 'unknown')}"
                )
            for item in payload.get("tests", []):
                status = item.get("status")
                if status in {"skipped", "error"}:
                    label = item.get("device") or item.get("feature") or "unknown"
                    lines.append(
                        f"- `{section_name}` / `{metric}` / `{label}`: status={status}; reason={item.get('reason', 'unknown')}"
                    )
            for pair in payload.get("pairwise", []):
                status = pair.get("status")
                if status in {"skipped", "error"}:
                    left = pair.get("left_model", "?")
                    right = pair.get("right_model", "?")
                    lines.append(
                        f"- `{section_name}` / `{metric}` / `{left} vs {right}`: status={status}; reason={pair.get('reason', 'unknown')}"
                    )

    device_posthoc = results.get("device_detection", {}).get("posthoc", {})
    for device, rows in device_posthoc.items():
        for row in rows:
            status = row.get("status")
            if status in {"skipped", "error"}:
                lines.append(
                    f"- `device_detection.posthoc` / `{device}` / `{row.get('left_model', '?')} vs {row.get('right_model', '?')}`: "
                    f"status={status}; reason={row.get('reason', 'unknown')}"
                )

    return lines


def render_results_markdown(results: dict) -> str:
    metadata = results.get("metadata", {})
    lines = [
        "# Literary Analysis Report",
        "",
        "## Dataset Snapshot",
        f"- Input CSV: `{metadata.get('input_csv', 'N/A')}`",
        f"- Inference CSV: `{metadata.get('inference_csv', 'N/A')}`",
        f"- Analysis CSV: `{metadata.get('analysis_csv', 'N/A')}`",
        f"- Output JSON: `{metadata.get('output_json', 'N/A')}`",
        f"- Output Markdown: `{metadata.get('report_md', 'N/A')}`",
        f"- Poems analyzed: {metadata.get('n_poems', 0)}",
        f"- Model rows: {metadata.get('n_rows', 0)}",
        f"- Models: {', '.join(metadata.get('models', [])) or 'N/A'}",
        "",
        "## Statistical Decision Rule",
        f"- Alpha: {results.get('alpha', ALPHA):.2f}",
        "- Classification rule: significant / non-significant only.",
        "- Significance uses adjusted p-values when available; raw p-values are explicitly marked as unadjusted.",
        "",
        "## AP Stats Interpretation Guide",
        "- A p-value is the probability of seeing data at least this extreme if there were truly no model difference.",
        "- Repeated-measures tests are used because each poem is evaluated by multiple models; poem-level pairing must be preserved.",
        "- Adjusted p-values are needed when many tests are run so false positives stay controlled.",
        f"- Significance threshold is alpha = {results.get('alpha', ALPHA):.2f}; values below alpha are significant, otherwise non-significant.",
        "- Direction is read from paired differences (score/device rates) or from interaction-term signs.",
        "- AI-vs-Non-AI interaction null: the AI-minus-Non-AI score gap is the same across models.",
        "- AI-vs-Non-AI interaction alternative: at least one model has a different AI-minus-Non-AI gap.",
        "- Positive AI-minus-Non-AI means that model scores AI poems higher on average (descriptive only, not a standalone significance test).",
        "- Statistical significance for AI-vs-Non-AI claims is determined only by cross-model interaction tests.",
        "",
    ]

    if results.get("status") == "error":
        error = results.get("error", {})
        lines.extend(
            [
                "## Run Status",
                "- Status: error",
                f"- Failure point: `{error.get('stage', 'unknown')}`",
                f"- Message: {error.get('message', 'Unknown error')}",
                "",
                "## Caveats",
                "- Statistical analyses could not be completed for this run.",
                "- Check inference completeness: each poem must have one completed row per model.",
                "- Fix the issue, then re-run using the same `--run-id` to preserve run lineage.",
                "",
            ]
        )
        return "\n".join(lines)

    lines.extend(_render_significant_results_section(results))

    lines.extend(_render_score_summaries(results.get("score_summaries_by_metric", {})))
    lines.extend(_render_model_comparisons(results.get("score_model_comparisons_by_metric", {})))
    lines.extend(_render_device_detection(results.get("device_detection", {})))
    lines.extend(_render_interaction_section("Device x Model Score Interactions By Metric", results.get("device_score_interactions_by_metric", {}), "device"))
    lines.extend(_render_interaction_section("Diction Feature x Model Score Interactions By Metric", results.get("diction_score_interactions_by_metric", {}), "feature"))
    lines.extend(_render_interaction_section("Author Variable x Model Score Interactions By Metric", results.get("author_score_interactions_by_metric", {}), "feature"))
    lines.extend(_render_ai_origin_interactions_section(results.get("ai_origin_score_interactions_by_metric", {})))

    lines.append("## Skipped And Error Rows")
    skipped_rows = _collect_skipped_or_error_rows(results)
    if skipped_rows:
        lines.extend(skipped_rows)
    else:
        lines.append("- No skipped or error rows.")
    lines.append("")

    lines.extend(
        [
            "## Caveats",
            "- P-values indicate evidence against the null; they do not measure practical effect size on their own.",
            "- Mixed-effects and non-parametric fallbacks are inferential models and do not prove causation.",
            "",
        ]
    )
    return "\n".join(lines)


def run_all_analyses(
    input_csv: str,
    inference_csv: str,
    output_json: str,
    analysis_csv: str | None = None,
    report_md: str | None = None,
    sample_poems: int | None = None,
    sample_seed: int | None = None,
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
) -> dict:
    resolved_analysis_csv = analysis_csv or str(Path(output_json).with_name("analysis_dataset.csv"))
    resolved_report_md = report_md or str(Path(output_json).with_suffix(".md"))
    metadata = {
        "input_csv": str(input_csv),
        "inference_csv": str(inference_csv),
        "analysis_csv": str(resolved_analysis_csv),
        "output_json": str(output_json),
        "report_md": str(resolved_report_md),
        "sample_poems": sample_poems,
        "sample_seed": sample_seed,
    }

    steps = [
        "build_analysis_dataset",
        "score_summaries_by_metric",
        "score_model_comparisons_by_metric",
        "device_detection",
        "device_score_interactions_by_metric",
        "diction_score_interactions_by_metric",
        "author_score_interactions_by_metric",
        "ai_origin_score_interactions_by_metric",
        "persist_results",
    ]
    total_steps = len(steps)
    completed_steps = 0
    active_step = "run_all_analyses"

    _emit_progress(
        progress_callback,
        {
            "event": "start",
            "stage": "stats",
            "step": active_step,
            "completed_steps": completed_steps,
            "total_steps": total_steps,
            "metadata": metadata,
        },
    )

    def _step_start(step_name: str) -> None:
        nonlocal active_step
        active_step = step_name
        _emit_progress(
            progress_callback,
            {
                "event": "step_start",
                "stage": "stats",
                "step": step_name,
                "completed_steps": completed_steps,
                "total_steps": total_steps,
            },
        )

    def _step_complete(step_name: str, **extra: Any) -> None:
        nonlocal completed_steps
        completed_steps += 1
        _emit_progress(
            progress_callback,
            {
                "event": "step_complete",
                "stage": "stats",
                "step": step_name,
                "completed_steps": completed_steps,
                "total_steps": total_steps,
                **extra,
            },
        )

    try:
        _step_start("build_analysis_dataset")
        analysis_df = build_analysis_dataset(
            input_csv,
            inference_csv,
            resolved_analysis_csv,
            progress_callback=progress_callback,
            sample_poems=sample_poems,
            sample_seed=sample_seed,
        )
        _step_complete(
            "build_analysis_dataset",
            n_rows=int(len(analysis_df)),
            n_poems=int(analysis_df["poem_id"].nunique()),
        )

        _step_start("score_summaries_by_metric")
        score_summaries_by_metric = run_score_summaries_by_metric(analysis_df)
        _step_complete("score_summaries_by_metric")

        _step_start("score_model_comparisons_by_metric")
        score_model_comparisons_by_metric = run_score_model_comparisons_by_metric(analysis_df)
        _step_complete("score_model_comparisons_by_metric")

        _step_start("device_detection")
        device_detection = run_device_detection_analysis(analysis_df)
        _step_complete("device_detection")

        _step_start("device_score_interactions_by_metric")
        device_score_interactions_by_metric = run_device_score_interactions_by_metric(analysis_df)
        _step_complete("device_score_interactions_by_metric")

        _step_start("diction_score_interactions_by_metric")
        diction_score_interactions_by_metric = run_diction_score_interactions_by_metric(analysis_df)
        _step_complete("diction_score_interactions_by_metric")

        _step_start("author_score_interactions_by_metric")
        author_score_interactions_by_metric = run_author_score_interactions_by_metric(analysis_df)
        _step_complete("author_score_interactions_by_metric")

        _step_start("ai_origin_score_interactions_by_metric")
        ai_origin_score_interactions_by_metric = run_ai_origin_score_interactions_by_metric(analysis_df)
        _step_complete("ai_origin_score_interactions_by_metric")

        results = {
            "alpha": ALPHA,
            "metadata": {
                **metadata,
                "n_poems": int(analysis_df["poem_id"].nunique()),
                "n_rows": int(len(analysis_df)),
                "models": sorted(analysis_df["model"].astype(str).unique().tolist()),
                "score_metrics": list(SCORE_METRICS),
            },
            "score_summaries_by_metric": score_summaries_by_metric,
            "score_model_comparisons_by_metric": score_model_comparisons_by_metric,
            "device_detection": device_detection,
            "device_score_interactions_by_metric": device_score_interactions_by_metric,
            "diction_score_interactions_by_metric": diction_score_interactions_by_metric,
            "author_score_interactions_by_metric": author_score_interactions_by_metric,
            "ai_origin_score_interactions_by_metric": ai_origin_score_interactions_by_metric,
            # Compatibility aliases (aggregate_score slices).
            "model_score_summary": score_summaries_by_metric.get("metrics", {}).get("aggregate_score", []),
            "overall_score": score_model_comparisons_by_metric.get("metrics", {}).get("aggregate_score", {}),
            "device_score_interactions": device_score_interactions_by_metric.get("metrics", {}).get("aggregate_score", {}),
            "diction_score_interactions": diction_score_interactions_by_metric.get("metrics", {}).get("aggregate_score", {}),
            "author_score_interactions": author_score_interactions_by_metric.get("metrics", {}).get("aggregate_score", {}),
            "ai_origin_score_interactions": ai_origin_score_interactions_by_metric.get("metrics", {}).get("aggregate_score", {}),
        }

        _step_start("persist_results")
        _write_json(output_json, results)
        _write_markdown(resolved_report_md, render_results_markdown(results))
        _step_complete("persist_results")

        _emit_progress(
            progress_callback,
            {
                "event": "complete",
                "stage": "stats",
                "step": "persist_results",
                "completed_steps": completed_steps,
                "total_steps": total_steps,
                "output_json": str(output_json),
                "report_md": str(resolved_report_md),
            },
        )
        return results
    except Exception as exc:
        error_results = {
            "status": "error",
            "alpha": ALPHA,
            "metadata": {
                **metadata,
                "n_poems": 0,
                "n_rows": 0,
                "models": [],
                "score_metrics": list(SCORE_METRICS),
            },
            "error": {
                "stage": "run_all_analyses",
                "step": active_step,
                "message": str(exc),
                "exception_type": type(exc).__name__,
            },
        }
        _write_json(output_json, error_results)
        _write_markdown(resolved_report_md, render_results_markdown(error_results))
        _emit_progress(
            progress_callback,
            {
                "event": "error",
                "stage": "stats",
                "step": active_step,
                "completed_steps": completed_steps,
                "total_steps": total_steps,
                "error": str(exc),
                "output_json": str(output_json),
                "report_md": str(resolved_report_md),
            },
        )
        raise RuntimeError(str(exc)) from exc
