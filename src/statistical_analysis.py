from __future__ import annotations

import json
import math
import re
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import binomtest, chi2, friedmanchisquare, wilcoxon

from .data_parser import STATUS_COMPLETED, load_inference_dataset, load_input_dataset, serialize_json_columns
from .inference import LITERARY_DEVICES
from .prose_analysis import compute_poem_features

try:
    import statsmodels.formula.api as smf
except ModuleNotFoundError:
    smf = None

DEVICE_COLUMNS = {device: f"device_{re.sub(r'[^a-z0-9]+', '_', device.lower()).strip('_')}" for device in LITERARY_DEVICES}
DICTION_FEATURES = ["avg_word_length", "latinate_ratio", "type_token_ratio"]
AUTHOR_FEATURES = ["author_gender", "author_ethnicity", "author_nationality"]



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
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(_json_safe(payload), indent=2), encoding="utf-8")



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
        "technical_craft_score",
        "structure_score",
        "diction_score",
        "originality_score",
        "impact_score",
        "aggregate_score",
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
    return analysis_df



def _prepare_analysis_input(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    analysis_df = _normalize_analysis_df(df)
    analysis_df = analysis_df[analysis_df["status"] == STATUS_COMPLETED].copy()
    analysis_df = analysis_df.dropna(subset=["aggregate_score", "poem_id", "model"])
    balanced_df, models, _ = _balanced_models(analysis_df)
    if balanced_df.empty:
        raise ValueError("No balanced completed poem-by-model rows are available for analysis")
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
        "statistic": statistic,
        "pvalue": pvalue,
        "exact": exact,
        "contingency_table": [[both_yes, x_only], [y_only, both_no]],
    }



def _pairwise_wilcoxon(pivot: pd.DataFrame, models: list[str]) -> list[dict]:
    results = []
    pairs = list(combinations(models, 2))
    for left_model, right_model in pairs:
        paired = pivot[[left_model, right_model]].dropna()
        if paired.empty or np.allclose(paired[left_model].to_numpy(), paired[right_model].to_numpy()):
            results.append({"pair": [left_model, right_model], "statistic": None, "pvalue": None, "adjusted_pvalue": None, "reason": "no_variation"})
            continue
        try:
            statistic, pvalue = wilcoxon(paired[left_model], paired[right_model], zero_method="wilcox")
        except ValueError:
            results.append({"pair": [left_model, right_model], "statistic": None, "pvalue": None, "adjusted_pvalue": None, "reason": "invalid_pairwise_input"})
            continue
        results.append({
            "pair": [left_model, right_model],
            "statistic": float(statistic),
            "pvalue": float(pvalue),
            "adjusted_pvalue": float(min(pvalue * len(pairs), 1.0)),
        })
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
        return {"status": "error", "reason": str(exc), "full_formula": full_formula, "reduced_formula": reduced_formula}
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



def build_analysis_dataset(input_csv: str, inference_csv: str, analysis_csv: str | None = None) -> pd.DataFrame:
    input_df = load_input_dataset(input_csv).copy()
    input_df["poem_id"] = input_df["poem_id"].astype(str)
    inference_df = load_inference_dataset(inference_csv)
    completed = inference_df[inference_df["status"] == STATUS_COMPLETED].copy()
    completed["poem_id"] = completed["poem_id"].astype(str)
    balanced_df, _, balanced_ids = _balanced_models(completed)
    if not balanced_ids:
        raise ValueError("No balanced completed poem-by-model rows are available for analysis")
    poem_text_df = input_df[input_df["poem_id"].isin(balanced_ids)][["poem_id", "poem_text"]].drop_duplicates("poem_id")
    feature_rows = []
    for row in poem_text_df.itertuples():
        feature_rows.append({"poem_id": row.poem_id, **compute_poem_features(row.poem_text)})
    features_df = pd.DataFrame(feature_rows)
    analysis_df = balanced_df.merge(poem_text_df, on="poem_id", how="left")
    analysis_df = analysis_df.merge(features_df, on="poem_id", how="left")
    analysis_df = _normalize_analysis_df(analysis_df)
    for device, column in DEVICE_COLUMNS.items():
        analysis_df[column] = analysis_df["literary_devices"].apply(lambda values: int(device in values))
    analysis_df = analysis_df.sort_values(["poem_id", "model"], kind="stable").reset_index(drop=True)
    if analysis_csv is not None:
        output_path = Path(analysis_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        persistable = serialize_json_columns(analysis_df, ["literary_devices", "prior_knowledge_detected_models"])
        persistable.to_csv(output_path, index=False)
    return analysis_df



def run_overall_score_analysis(df: pd.DataFrame) -> dict:
    analysis_df, models = _prepare_analysis_input(df)
    try:
        mixedlm_result = _fit_mixedlm("aggregate_score ~ C(model)", "aggregate_score ~ 1", analysis_df)
        return {
            "status": "ok",
            "method": "mixedlm",
            "models": models,
            "n_poems": int(analysis_df["poem_id"].nunique()),
            "n_rows": int(len(analysis_df)),
            **mixedlm_result,
        }
    except Exception as exc:
        pivot = analysis_df.pivot(index="poem_id", columns="model", values="aggregate_score").reindex(columns=models).dropna()
        if pivot.shape[0] < 2:
            return {"status": "error", "method": "friedman", "reason": f"mixedlm_failed: {exc}; insufficient balanced poems for Friedman fallback"}
        try:
            statistic, pvalue = friedmanchisquare(*(pivot[model].to_numpy() for model in models))
        except Exception as fallback_exc:
            return {"status": "error", "method": "friedman", "reason": f"mixedlm_failed: {exc}; friedman_failed: {fallback_exc}"}
        posthoc = _pairwise_wilcoxon(pivot, models) if pvalue < 0.05 else []
        return {
            "status": "ok",
            "method": "friedman",
            "models": models,
            "n_poems": int(pivot.shape[0]),
            "n_rows": int(len(analysis_df)),
            "statistic": float(statistic),
            "pvalue": float(pvalue),
            "mixedlm_error": str(exc),
            "posthoc": posthoc,
        }



def run_device_detection_analysis(df: pd.DataFrame) -> dict:
    analysis_df, models = _prepare_analysis_input(df)
    results = []
    posthoc = {}
    for device, column in DEVICE_COLUMNS.items():
        pivot = analysis_df.pivot(index="poem_id", columns="model", values=column).reindex(columns=models).dropna()
        if pivot.empty or pivot.shape[0] < 2:
            results.append({"device": device, "status": "skipped", "reason": "insufficient_data", "pvalue": None})
            continue
        statistic, pvalue, reason = _cochrans_q(pivot.to_numpy(dtype=int))
        if reason is not None:
            results.append({"device": device, "status": "skipped", "reason": reason, "pvalue": None})
            continue
        results.append({
            "device": device,
            "status": "ok",
            "statistic": statistic,
            "pvalue": pvalue,
            "detections_by_model": {model: int(pivot[model].sum()) for model in models},
            "n_poems": int(pivot.shape[0]),
        })
        posthoc[device] = pivot
    _adjust_pvalues_bh(results)
    pairwise_results = {}
    for item in results:
        if item.get("status") != "ok" or item.get("adjusted_pvalue") is None or item["adjusted_pvalue"] >= 0.05:
            continue
        pivot = posthoc[item["device"]]
        pairs = []
        pair_count = len(list(combinations(models, 2)))
        for left_model, right_model in combinations(models, 2):
            pair_result = _mcnemar_test(pivot[left_model].to_numpy(dtype=int), pivot[right_model].to_numpy(dtype=int))
            adjusted_pvalue = None if pair_result["pvalue"] is None else float(min(pair_result["pvalue"] * pair_count, 1.0))
            pairs.append({"pair": [left_model, right_model], **pair_result, "adjusted_pvalue": adjusted_pvalue})
        pairwise_results[item["device"]] = pairs
    return {
        "status": "ok",
        "method": "cochrans_q",
        "models": models,
        "n_poems": int(analysis_df["poem_id"].nunique()),
        "tests": results,
        "posthoc": pairwise_results,
    }



def run_device_score_interactions(df: pd.DataFrame) -> dict:
    analysis_df, _ = _prepare_analysis_input(df)
    tests = []
    for device, column in DEVICE_COLUMNS.items():
        working_df = analysis_df.dropna(subset=["aggregate_score", column])
        if working_df[column].nunique() < 2:
            tests.append({"device": device, "status": "skipped", "reason": "no_variation", "pvalue": None})
            continue
        result = _interaction_result(
            f"aggregate_score ~ C(model) * {column}",
            f"aggregate_score ~ C(model) + {column}",
            working_df,
            effect_prefix=f":{column}",
        )
        tests.append({"device": device, **result})
    _adjust_pvalues_bh(tests)
    return {"status": "ok", "method": "mixedlm", "tests": tests}



def run_diction_score_interactions(df: pd.DataFrame) -> dict:
    analysis_df, _ = _prepare_analysis_input(df)
    tests = []
    for feature in DICTION_FEATURES:
        working_df = analysis_df[np.isfinite(analysis_df[feature])].copy()
        if working_df.empty or working_df[feature].nunique() < 2:
            tests.append({"feature": feature, "status": "skipped", "reason": "insufficient_variation", "pvalue": None})
            continue
        result = _interaction_result(
            f"aggregate_score ~ C(model) * {feature}",
            f"aggregate_score ~ C(model) + {feature}",
            working_df,
            effect_prefix=f":{feature}",
        )
        tests.append({"feature": feature, **result})
    _adjust_pvalues_bh(tests)
    return {"status": "ok", "method": "mixedlm", "tests": tests}



def _author_feature_sparse(df: pd.DataFrame, feature: str) -> bool:
    counts = df[["poem_id", feature]].drop_duplicates()[feature].value_counts()
    return counts.empty or (counts < 2).any()



def run_author_score_interactions(df: pd.DataFrame) -> dict:
    analysis_df, _ = _prepare_analysis_input(df)
    tests = []
    for feature in AUTHOR_FEATURES:
        if analysis_df[feature].nunique() < 2:
            tests.append({"feature": feature, "status": "skipped", "reason": "insufficient_variation", "pvalue": None})
            continue
        if _author_feature_sparse(analysis_df, feature):
            tests.append({"feature": feature, "status": "skipped", "reason": "sparse_categories", "pvalue": None})
            continue
        result = _interaction_result(
            f"aggregate_score ~ C(model) * C({feature})",
            f"aggregate_score ~ C(model) + C({feature})",
            analysis_df,
            effect_prefix=":C(",
        )
        tests.append({"feature": feature, **result})
    _adjust_pvalues_bh(tests)
    return {"status": "ok", "method": "mixedlm", "tests": tests}



def run_all_analyses(input_csv: str, inference_csv: str, output_json: str, analysis_csv: str | None = None) -> dict:
    resolved_analysis_csv = analysis_csv or str(Path(output_json).with_name("analysis_dataset.csv"))
    analysis_df = build_analysis_dataset(input_csv, inference_csv, resolved_analysis_csv)
    results = {
        "metadata": {
            "input_csv": str(input_csv),
            "inference_csv": str(inference_csv),
            "analysis_csv": str(resolved_analysis_csv),
            "output_json": str(output_json),
            "n_poems": int(analysis_df["poem_id"].nunique()),
            "n_rows": int(len(analysis_df)),
            "models": sorted(analysis_df["model"].unique().tolist()),
        },
        "overall_score": run_overall_score_analysis(analysis_df),
        "device_detection": run_device_detection_analysis(analysis_df),
        "device_score_interactions": run_device_score_interactions(analysis_df),
        "diction_score_interactions": run_diction_score_interactions(analysis_df),
        "author_score_interactions": run_author_score_interactions(analysis_df),
    }
    _write_json(output_json, results)
    return results
