from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import warnings
from pathlib import Path
from unittest import mock

import pandas as pd
from pydantic import BaseModel

from src.artifacts import RunArtifactsManager, atomic_write_text
from src.data_parser import load_inference_dataset, load_input_dataset
from src.inference import check_prior_knowledge, run_inference_on_dataset
from src.pipeline_orchestrator import run_infer_stage, run_stats_stage
from src.prose_analysis import FAILED_LOOKUPS, _lookup_word_origin, check_word_origin, warm_etymology_cache
from src import prose_analysis
from src.statistical_analysis import build_analysis_dataset, render_results_markdown, run_all_analyses
from src.utility import parse_output_json, run_model, run_nvidia_models


class LoaderTests(unittest.TestCase):
    def test_load_input_dataset_strips_headers(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "input.csv"
            csv_path.write_text(
                "poem_id, poem_text, poem_fetch_url, poem_genre, year_of_publish, author_name, author_age, author_gender, author_ethnicity, author_nationality\n"
                "1,hello,url,lyric,2000,Author,30,female,group,nation\n",
                encoding="utf-8",
            )
            df = load_input_dataset(csv_path)
            self.assertEqual(df.columns.tolist()[0], "poem_id")
            self.assertIn("poem_text", df.columns)

    def test_load_inference_dataset_accepts_legacy_rationale_columns(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "inference.csv"
            pd.DataFrame(
                [
                    {
                        "poem_id": "1",
                        "model": "gpt-5.4",
                        "status": "completed",
                        "skip_reason": "",
                        "prior_knowledge_detected_models": json.dumps([]),
                        "poem_fetch_url": "https://example.com/1",
                        "poem_genre": "lyric",
                        "year_of_publish": 2000,
                        "author_name": "Author",
                        "author_age": 30,
                        "author_gender": "female",
                        "author_ethnicity": "group",
                        "author_nationality": "nation",
                        "literary_devices_rationale": "legacy explanation",
                        "literary_devices": json.dumps(["metaphor"]),
                        "score_rationale": "legacy scoring explanation",
                        "technical_craft_score": 5,
                        "structure_score": 5,
                        "diction_score": 5,
                        "originality_score": 5,
                        "impact_score": 5,
                        "aggregate_score": 25,
                    }
                ]
            ).to_csv(csv_path, index=False)

            df = load_inference_dataset(csv_path)

            self.assertEqual(df.loc[0, "literary_devices"], ["metaphor"])
            self.assertNotIn("literary_devices_rationale", df.columns)
            self.assertNotIn("score_rationale", df.columns)


class ArtifactManagerTests(unittest.TestCase):
    def test_when_run_id_is_explicit_then_run_directory_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = RunArtifactsManager(Path(tmpdir) / "runs")
            context = manager.prepare_run("batch-001")
            self.assertEqual(context.run_id, "batch-001")
            self.assertEqual(context.run_dir.resolve(), (Path(tmpdir) / "runs" / "batch-001").resolve())
            self.assertTrue((context.run_dir / "manifest.json").exists())

    def test_when_run_id_is_omitted_then_generated_id_has_expected_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = RunArtifactsManager(Path(tmpdir) / "runs")
            context = manager.prepare_run()
            self.assertRegex(context.run_id, r"^run-\d{8}T\d{6}Z-[0-9a-f]{8}$")

    def test_when_stage_is_recorded_then_manifest_and_latest_pointer_are_updated(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            runs_dir = Path(tmpdir) / "runs"
            manager = RunArtifactsManager(runs_dir)
            context = manager.prepare_run("batch-xyz")
            manifest_path = manager.record_stage(
                context,
                "infer",
                "ok",
                {"rows": 5, "outputs": {"run_output_csv": str(context.run_dir / "inference_results.csv")}},
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["stages"]["infer"]["status"], "ok")
            self.assertEqual(manifest["stages"]["infer"]["rows"], 5)
            latest = json.loads((runs_dir / "latest_run.json").read_text(encoding="utf-8"))
            self.assertEqual(latest["run_id"], "batch-xyz")
            self.assertEqual(latest["stage_statuses"]["infer"], "ok")

    def test_when_atomic_write_fails_then_existing_file_remains_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "artifact.txt"
            target.write_text("original", encoding="utf-8")
            with mock.patch("src.artifacts.os.replace", side_effect=OSError("simulated_failure")):
                with self.assertRaises(OSError):
                    atomic_write_text(target, "new text")
            self.assertEqual(target.read_text(encoding="utf-8"), "original")
            leftovers = [path for path in Path(tmpdir).iterdir() if path.name.startswith(".artifact.txt.")]
            self.assertEqual(leftovers, [])


class ReportRenderingTests(unittest.TestCase):
    def test_when_results_include_findings_then_markdown_is_human_readable(self) -> None:
        payload = {
            "alpha": 0.05,
            "metadata": {
                "input_csv": "input.csv",
                "inference_csv": "inference.csv",
                "analysis_csv": "analysis.csv",
                "output_json": "results.json",
                "report_md": "results.md",
                "n_poems": 7,
                "n_rows": 21,
                "models": ["a", "b", "c"],
            },
            "score_summaries_by_metric": {
                "alpha": 0.05,
                "pvalue_adjustment": "none",
                "metrics": {
                    "aggregate_score": [
                        {"model": "a", "mean": 38.0, "median": 38.0, "std_dev": 1.2, "min": 36.0, "max": 40.0, "n": 7}
                    ],
                    "technical_craft_score": [],
                    "structure_score": [],
                    "diction_score": [],
                    "originality_score": [],
                    "impact_score": [],
                },
            },
            "score_model_comparisons_by_metric": {
                "alpha": 0.05,
                "pvalue_adjustment": "benjamini_hochberg",
                "metrics": {
                    "aggregate_score": {
                        "status": "ok",
                        "method": "mixedlm",
                        "pvalue": 0.03,
                        "significant": True,
                        "significance_basis": "raw_unadjusted",
                        "n_poems": 7,
                        "n_rows": 21,
                        "pairwise": [
                            {
                                "left_model": "a",
                                "right_model": "b",
                                "status": "ok",
                                "mean_difference": 0.6,
                                "median_difference": 0.5,
                                "pvalue": 0.04,
                                "adjusted_pvalue": 0.04,
                                "significant": True,
                                "significance_basis": "adjusted",
                                "direction": "a higher than b",
                                "n_pairs": 7,
                            }
                        ],
                    },
                    "technical_craft_score": {"status": "error", "reason": "insufficient_data", "pairwise": []},
                    "structure_score": {"status": "error", "reason": "insufficient_data", "pairwise": []},
                    "diction_score": {"status": "error", "reason": "insufficient_data", "pairwise": []},
                    "originality_score": {"status": "error", "reason": "insufficient_data", "pairwise": []},
                    "impact_score": {"status": "error", "reason": "insufficient_data", "pairwise": []},
                },
            },
            "device_detection": {
                "alpha": 0.05,
                "pvalue_adjustment": "benjamini_hochberg",
                "posthoc_pvalue_adjustment": "benjamini_hochberg",
                "tests": [{"device": "metaphor", "status": "ok", "adjusted_pvalue": 0.02, "significant": True, "significance_basis": "adjusted"}],
                "posthoc": {
                    "metaphor": [
                        {
                            "left_model": "a",
                            "right_model": "b",
                            "status": "ok",
                            "rate_difference": 0.3,
                            "pvalue": 0.02,
                            "adjusted_pvalue": 0.02,
                            "significant": True,
                            "significance_basis": "adjusted",
                            "direction": "a higher than b",
                            "n_pairs": 7,
                        }
                    ]
                },
            },
            "device_score_interactions_by_metric": {
                "alpha": 0.05,
                "pvalue_adjustment": "benjamini_hochberg",
                "metrics": {
                    "aggregate_score": {
                        "status": "ok",
                        "tests": [{"device": "imagery", "status": "ok", "adjusted_pvalue": 0.02, "significant": True, "significance_basis": "adjusted", "direction_summary": "Largest interaction term: a (+0.200) -> stronger positive association."}],
                    },
                    "technical_craft_score": {"status": "error", "reason": "insufficient_data", "tests": []},
                    "structure_score": {"status": "error", "reason": "insufficient_data", "tests": []},
                    "diction_score": {"status": "error", "reason": "insufficient_data", "tests": []},
                    "originality_score": {"status": "error", "reason": "insufficient_data", "tests": []},
                    "impact_score": {"status": "error", "reason": "insufficient_data", "tests": []},
                },
            },
            "diction_score_interactions_by_metric": {
                "alpha": 0.05,
                "pvalue_adjustment": "benjamini_hochberg",
                "metrics": {
                    "aggregate_score": {
                        "status": "ok",
                        "tests": [{"feature": "avg_word_length", "status": "ok", "adjusted_pvalue": 0.03, "significant": True, "significance_basis": "adjusted", "direction_summary": "Largest interaction term: b (-0.120) -> weaker or negative association."}],
                    },
                    "technical_craft_score": {"status": "error", "reason": "insufficient_data", "tests": []},
                    "structure_score": {"status": "error", "reason": "insufficient_data", "tests": []},
                    "diction_score": {"status": "error", "reason": "insufficient_data", "tests": []},
                    "originality_score": {"status": "error", "reason": "insufficient_data", "tests": []},
                    "impact_score": {"status": "error", "reason": "insufficient_data", "tests": []},
                },
            },
            "author_score_interactions_by_metric": {
                "alpha": 0.05,
                "pvalue_adjustment": "benjamini_hochberg",
                "metrics": {
                    "aggregate_score": {
                        "status": "ok",
                        "tests": [{"feature": "author_gender", "status": "skipped", "reason": "sparse_categories", "adjusted_pvalue": None, "significant": False, "significance_basis": "none"}],
                    },
                    "technical_craft_score": {"status": "error", "reason": "insufficient_data", "tests": []},
                    "structure_score": {"status": "error", "reason": "insufficient_data", "tests": []},
                    "diction_score": {"status": "error", "reason": "insufficient_data", "tests": []},
                    "originality_score": {"status": "error", "reason": "insufficient_data", "tests": []},
                    "impact_score": {"status": "error", "reason": "insufficient_data", "tests": []},
                },
            },
            "ai_origin_score_interactions_by_metric": {
                "alpha": 0.05,
                "pvalue_adjustment": "benjamini_hochberg",
                "metrics": {
                    "aggregate_score": {
                        "status": "ok",
                        "method": "mixedlm",
                        "pvalue": 0.01,
                        "significant": True,
                        "significance_basis": "raw_unadjusted",
                        "models": ["a", "b", "c"],
                        "ai_minus_non_ai_by_model": {
                            "a": {"ai_mean": 40.0, "non_ai_mean": 37.0, "ai_minus_non_ai": 3.0, "n_ai_poems": 4, "n_non_ai_poems": 3},
                            "b": {"ai_mean": 38.0, "non_ai_mean": 37.0, "ai_minus_non_ai": 1.0, "n_ai_poems": 4, "n_non_ai_poems": 3},
                            "c": {"ai_mean": 36.0, "non_ai_mean": 37.0, "ai_minus_non_ai": -1.0, "n_ai_poems": 4, "n_non_ai_poems": 3},
                        },
                        "pairwise": [
                            {
                                "left_model": "a",
                                "right_model": "b",
                                "status": "ok",
                                "n_poems": 7,
                                "gap_difference": 2.0,
                                "pvalue": 0.04,
                                "adjusted_pvalue": 0.04,
                                "significant": True,
                                "significance_basis": "adjusted",
                                "direction": "a higher than b",
                            }
                        ],
                    },
                    "technical_craft_score": {"status": "skipped", "reason": "insufficient_data", "pairwise": []},
                    "structure_score": {"status": "skipped", "reason": "insufficient_data", "pairwise": []},
                    "diction_score": {"status": "skipped", "reason": "insufficient_data", "pairwise": []},
                    "originality_score": {"status": "skipped", "reason": "insufficient_data", "pairwise": []},
                    "impact_score": {"status": "skipped", "reason": "insufficient_data", "pairwise": []},
                },
            },
        }
        markdown = render_results_markdown(payload)
        self.assertIn("## Dataset Snapshot", markdown)
        self.assertIn("## Significant Results Only", markdown)
        self.assertIn("## Model Comparisons By Score Metric", markdown)
        self.assertIn("## Device Detection Tests", markdown)
        self.assertIn("## AI-vs-Non-AI Preference Interactions By Metric", markdown)
        self.assertIn("## AP Stats Interpretation Guide", markdown)
        self.assertIn("AI-vs-Non-AI interaction null", markdown)
        self.assertIn("AI-vs-Non-AI claims here are only cross-model gap-difference tests", markdown)
        self.assertIn("### AI-vs-Non-AI Gap-Difference Interactions", markdown)
        self.assertIn("## Caveats", markdown)
        self.assertIn("significant at alpha=0.05", markdown)
        self.assertNotIn("suggestive evidence", markdown)

    def test_when_results_are_error_state_then_markdown_explains_failure(self) -> None:
        payload = {
            "status": "error",
            "metadata": {"input_csv": "input.csv", "inference_csv": "inference.csv", "analysis_csv": "analysis.csv", "output_json": "out.json", "report_md": "out.md"},
            "error": {"stage": "run_all_analyses", "message": "No balanced completed poem-by-model rows are available for analysis"},
        }
        markdown = render_results_markdown(payload)
        self.assertIn("## Run Status", markdown)
        self.assertIn("No balanced completed poem-by-model rows are available for analysis", markdown)

    def test_when_no_rows_are_significant_then_markdown_says_so(self) -> None:
        payload = {
            "alpha": 0.05,
            "metadata": {
                "input_csv": "input.csv",
                "inference_csv": "inference.csv",
                "analysis_csv": "analysis.csv",
                "output_json": "results.json",
                "report_md": "results.md",
                "n_poems": 4,
                "n_rows": 12,
                "models": ["a", "b", "c"],
            },
            "score_summaries_by_metric": {"alpha": 0.05, "pvalue_adjustment": "none", "metrics": {metric: [] for metric in ("aggregate_score", "technical_craft_score", "structure_score", "diction_score", "originality_score", "impact_score")}},
            "score_model_comparisons_by_metric": {
                "alpha": 0.05,
                "pvalue_adjustment": "benjamini_hochberg",
                "metrics": {
                    "aggregate_score": {"status": "ok", "pvalue": 0.40, "significant": False, "significance_basis": "raw_unadjusted", "pairwise": []},
                    "technical_craft_score": {"status": "skipped", "reason": "insufficient_data", "pairwise": []},
                    "structure_score": {"status": "skipped", "reason": "insufficient_data", "pairwise": []},
                    "diction_score": {"status": "skipped", "reason": "insufficient_data", "pairwise": []},
                    "originality_score": {"status": "skipped", "reason": "insufficient_data", "pairwise": []},
                    "impact_score": {"status": "skipped", "reason": "insufficient_data", "pairwise": []},
                },
            },
            "device_detection": {"tests": [], "posthoc": {}},
            "device_score_interactions_by_metric": {"metrics": {metric: {"status": "skipped", "tests": []} for metric in ("aggregate_score", "technical_craft_score", "structure_score", "diction_score", "originality_score", "impact_score")}},
            "diction_score_interactions_by_metric": {"metrics": {metric: {"status": "skipped", "tests": []} for metric in ("aggregate_score", "technical_craft_score", "structure_score", "diction_score", "originality_score", "impact_score")}},
            "author_score_interactions_by_metric": {"metrics": {metric: {"status": "skipped", "tests": []} for metric in ("aggregate_score", "technical_craft_score", "structure_score", "diction_score", "originality_score", "impact_score")}},
            "ai_origin_score_interactions_by_metric": {"metrics": {metric: {"status": "skipped", "pairwise": []} for metric in ("aggregate_score", "technical_craft_score", "structure_score", "diction_score", "originality_score", "impact_score")}},
        }
        markdown = render_results_markdown(payload)
        self.assertIn("## Significant Results Only", markdown)
        self.assertIn("- No significant results at alpha=0.05.", markdown)


class PipelineRunLinkingTests(unittest.TestCase):
    def test_when_infer_then_stats_share_run_id_then_outputs_are_grouped(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            runs_dir = tmp / "runs"
            input_csv = tmp / "input.csv"
            input_csv.write_text(
                "poem_id,poem_text,poem_fetch_url,poem_genre,year_of_publish,author_name,author_age,author_gender,author_ethnicity,author_nationality\n"
                "1,text,url,lyric,2000,Author,30,female,group,nation\n",
                encoding="utf-8",
            )
            requested_inference = tmp / "inference_results.csv"
            default_inference = str(requested_inference)
            run_id = "batch-link"

            def fake_infer(_: str, output_csv: str, __: list[str], check_cache: bool = True) -> pd.DataFrame:
                self.assertTrue(check_cache)
                output_path = Path(output_csv)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                pd.DataFrame([{"poem_id": "1", "status": "completed"}]).to_csv(output_path, index=False)
                return pd.DataFrame([{"poem_id": "1"}])

            expected_run_inference = runs_dir / run_id / "inference_results.csv"

            def fake_stats(
                input_csv_arg: str,
                inference_csv_arg: str,
                output_json_arg: str,
                analysis_csv_arg: str | None = None,
                report_md: str | None = None,
            ) -> dict:
                self.assertEqual(Path(input_csv_arg), input_csv)
                self.assertEqual(Path(inference_csv_arg).resolve(), expected_run_inference.resolve())
                assert analysis_csv_arg is not None
                assert report_md is not None
                Path(analysis_csv_arg).parent.mkdir(parents=True, exist_ok=True)
                pd.DataFrame([{"poem_id": "1", "model": "a", "aggregate_score": 10}]).to_csv(analysis_csv_arg, index=False)
                Path(output_json_arg).write_text(json.dumps({"metadata": {}, "overall_score": {}, "device_detection": {}, "device_score_interactions": {}, "diction_score_interactions": {}, "author_score_interactions": {}}), encoding="utf-8")
                Path(report_md).write_text("# Report\n", encoding="utf-8")
                return {
                    "metadata": {"input_csv": input_csv_arg},
                    "overall_score": {},
                    "device_detection": {},
                    "device_score_interactions": {},
                    "diction_score_interactions": {},
                    "author_score_interactions": {},
                }

            with mock.patch("src.pipeline_orchestrator.run_inference_on_dataset", side_effect=fake_infer):
                infer_payload = run_infer_stage(
                    input_csv=str(input_csv),
                    output_csv=str(requested_inference),
                    models=["gpt-5.4"],
                    check_cache=True,
                    runs_dir=str(runs_dir),
                    run_id=run_id,
                    default_output_csv=default_inference,
                )

            with mock.patch("src.pipeline_orchestrator.run_all_analyses", side_effect=fake_stats):
                stats_payload = run_stats_stage(
                    input_csv=str(input_csv),
                    inference_csv=default_inference,
                    analysis_csv=str(tmp / "analysis_dataset.csv"),
                    output_json=str(tmp / "statistical_results.json"),
                    report_md=None,
                    runs_dir=str(runs_dir),
                    run_id=run_id,
                    default_inference_csv=default_inference,
                    default_analysis_csv=str(tmp / "analysis_dataset.csv"),
                    default_output_json=str(tmp / "statistical_results.json"),
                )

            run_dir = runs_dir / run_id
            self.assertEqual(infer_payload["run_id"], run_id)
            self.assertEqual(stats_payload["run_id"], run_id)
            self.assertTrue((run_dir / "inference_results.csv").exists())
            self.assertTrue((run_dir / "analysis_dataset.csv").exists())
            self.assertTrue((run_dir / "statistical_results.json").exists())
            self.assertTrue((run_dir / "statistical_report.md").exists())
            latest = json.loads((runs_dir / "latest_run.json").read_text(encoding="utf-8"))
            self.assertEqual(latest["run_id"], run_id)
            self.assertEqual(latest["stage_statuses"]["infer"], "ok")
            self.assertEqual(latest["stage_statuses"]["stats"], "ok")

    def test_when_run_id_is_omitted_then_each_invocation_gets_distinct_run_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            runs_dir = tmp / "runs"
            input_csv = tmp / "input.csv"
            output_csv = tmp / "inference.csv"
            input_csv.write_text(
                "poem_id,poem_text,poem_fetch_url,poem_genre,year_of_publish,author_name,author_age,author_gender,author_ethnicity,author_nationality\n"
                "1,text,url,lyric,2000,Author,30,female,group,nation\n",
                encoding="utf-8",
            )

            def fake_infer(_: str, output_csv_arg: str, __: list[str], check_cache: bool = True) -> pd.DataFrame:
                Path(output_csv_arg).parent.mkdir(parents=True, exist_ok=True)
                pd.DataFrame([{"poem_id": "1", "status": "completed"}]).to_csv(output_csv_arg, index=False)
                return pd.DataFrame([{"poem_id": "1"}])

            with mock.patch("src.pipeline_orchestrator.run_inference_on_dataset", side_effect=fake_infer):
                first = run_infer_stage(
                    input_csv=str(input_csv),
                    output_csv=str(output_csv),
                    models=["gpt-5.4"],
                    check_cache=True,
                    runs_dir=str(runs_dir),
                    run_id=None,
                    default_output_csv=str(output_csv),
                )
                second = run_infer_stage(
                    input_csv=str(input_csv),
                    output_csv=str(output_csv),
                    models=["gpt-5.4"],
                    check_cache=True,
                    runs_dir=str(runs_dir),
                    run_id=None,
                    default_output_csv=str(output_csv),
                )

            self.assertNotEqual(first["run_id"], second["run_id"])
            self.assertTrue((runs_dir / first["run_id"] / "manifest.json").exists())
            self.assertTrue((runs_dir / second["run_id"] / "manifest.json").exists())


class InferenceTests(unittest.TestCase):
    def test_inference_resume_preserves_existing_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_csv = tmp / "input.csv"
            output_csv = tmp / "inference.csv"
            pd.DataFrame(
                [
                    {
                        "poem_id": "1",
                        "poem_text": "sun wind rain",
                        "poem_fetch_url": "https://example.com/1",
                        "poem_genre": "lyric",
                        "year_of_publish": 2001,
                        "author_name": "Author 1",
                        "author_age": 30,
                        "author_gender": "female",
                        "author_ethnicity": "group_a",
                        "author_nationality": "nation_a",
                    },
                    {
                        "poem_id": "2",
                        "poem_text": "stone cloud fire",
                        "poem_fetch_url": "https://example.com/2",
                        "poem_genre": "lyric",
                        "year_of_publish": 2002,
                        "author_name": "Author 2",
                        "author_age": 31,
                        "author_gender": "male",
                        "author_ethnicity": "group_b",
                        "author_nationality": "nation_b",
                    },
                ]
            ).to_csv(input_csv, index=False)
            existing_row = pd.DataFrame(
                [
                    {
                        "poem_id": "1",
                        "model": "model-a",
                        "status": "completed",
                        "skip_reason": "",
                        "prior_knowledge_detected_models": json.dumps([]),
                        "poem_fetch_url": "https://example.com/1",
                        "poem_genre": "lyric",
                        "year_of_publish": 2001,
                        "author_name": "Author 1",
                        "author_age": 30,
                        "author_gender": "female",
                        "author_ethnicity": "group_a",
                        "author_nationality": "nation_a",
                        "literary_devices_rationale": "",
                        "literary_devices": json.dumps(["metaphor"]),
                        "score_rationale": "",
                        "technical_craft_score": 5,
                        "structure_score": 5,
                        "diction_score": 5,
                        "originality_score": 5,
                        "impact_score": 5,
                        "aggregate_score": 25,
                    }
                ]
            )
            existing_row.to_csv(output_csv, index=False)

            def fake_run_single_inference(poem_dict: dict, model: str) -> dict:
                base = 30 if poem_dict["poem_id"] == "1" else 20
                return {
                    "poem_id": str(poem_dict["poem_id"]),
                    "model": model,
                    "status": "completed",
                    "skip_reason": "",
                    "prior_knowledge_detected_models": [],
                    "poem_fetch_url": poem_dict["poem_fetch_url"],
                    "poem_genre": poem_dict["poem_genre"],
                    "year_of_publish": poem_dict["year_of_publish"],
                    "author_name": poem_dict["author_name"],
                    "author_age": poem_dict["author_age"],
                    "author_gender": poem_dict["author_gender"],
                    "author_ethnicity": poem_dict["author_ethnicity"],
                    "author_nationality": poem_dict["author_nationality"],
                    "literary_devices": ["metaphor"],
                    "technical_craft_score": base // 5,
                    "structure_score": base // 5,
                    "diction_score": base // 5,
                    "originality_score": base // 5,
                    "impact_score": base // 5,
                    "aggregate_score": base,
                }

            with mock.patch("src.inference.check_prior_knowledge", return_value=False) as mocked_check:
                with mock.patch("src.inference.run_single_inference", side_effect=fake_run_single_inference):
                    result_df = run_inference_on_dataset(input_csv, output_csv, ["model-a", "model-b"], check_cache=True)

            completed = result_df[result_df["status"] == "completed"]
            self.assertEqual(len(completed), 4)
            original_row = completed[(completed["poem_id"] == "1") & (completed["model"] == "model-a")].iloc[0]
            self.assertEqual(original_row["aggregate_score"], 25)
            self.assertEqual(mocked_check.call_count, 2)
            self.assertNotIn("literary_devices_rationale", result_df.columns)
            self.assertNotIn("score_rationale", result_df.columns)

            persisted_df = pd.read_csv(output_csv)
            self.assertNotIn("literary_devices_rationale", persisted_df.columns)
            self.assertNotIn("score_rationale", persisted_df.columns)

    def test_inference_emits_terminal_complete_progress_event(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_csv = tmp / "input.csv"
            output_csv = tmp / "inference.csv"
            pd.DataFrame(
                [
                    {
                        "poem_id": "1",
                        "poem_text": "sun wind rain",
                        "poem_fetch_url": "https://example.com/1",
                        "poem_genre": "lyric",
                        "year_of_publish": 2001,
                        "author_name": "Author 1",
                        "author_age": 30,
                        "author_gender": "female",
                        "author_ethnicity": "group_a",
                        "author_nationality": "nation_a",
                    }
                ]
            ).to_csv(input_csv, index=False)

            events: list[dict] = []

            def fake_run_single_inference(poem_dict: dict, model: str) -> dict:
                return {
                    "poem_id": str(poem_dict["poem_id"]),
                    "model": model,
                    "status": "completed",
                    "skip_reason": "",
                    "prior_knowledge_detected_models": [],
                    "poem_fetch_url": poem_dict["poem_fetch_url"],
                    "poem_genre": poem_dict["poem_genre"],
                    "year_of_publish": poem_dict["year_of_publish"],
                    "author_name": poem_dict["author_name"],
                    "author_age": poem_dict["author_age"],
                    "author_gender": poem_dict["author_gender"],
                    "author_ethnicity": poem_dict["author_ethnicity"],
                    "author_nationality": poem_dict["author_nationality"],
                    "literary_devices": ["metaphor"],
                    "technical_craft_score": 6,
                    "structure_score": 6,
                    "diction_score": 6,
                    "originality_score": 6,
                    "impact_score": 6,
                    "aggregate_score": 30,
                }

            with mock.patch("src.inference.check_prior_knowledge", return_value=False):
                with mock.patch("src.inference.run_single_inference", side_effect=fake_run_single_inference):
                    run_inference_on_dataset(
                        input_csv,
                        output_csv,
                        ["model-a"],
                        check_cache=False,
                        progress_callback=events.append,
                    )

            self.assertTrue(any(event.get("event") == "start" for event in events))
            self.assertTrue(any(event.get("event") == "complete" for event in events))

    def test_inference_emits_terminal_error_progress_event(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_csv = tmp / "input.csv"
            output_csv = tmp / "inference.csv"
            pd.DataFrame(
                [
                    {
                        "poem_id": "1",
                        "poem_text": "sun wind rain",
                        "poem_fetch_url": "https://example.com/1",
                        "poem_genre": "lyric",
                        "year_of_publish": 2001,
                        "author_name": "Author 1",
                        "author_age": 30,
                        "author_gender": "female",
                        "author_ethnicity": "group_a",
                        "author_nationality": "nation_a",
                    }
                ]
            ).to_csv(input_csv, index=False)

            events: list[dict] = []

            with mock.patch("src.inference.check_prior_knowledge", return_value=False):
                with mock.patch("src.inference.run_single_inference", side_effect=RuntimeError("boom")):
                    result_df = run_inference_on_dataset(
                        input_csv,
                        output_csv,
                        ["model-a"],
                        check_cache=False,
                        progress_callback=events.append,
                    )

            model_error_events = [event for event in events if event.get("event") == "model_error"]
            self.assertEqual(len(model_error_events), 1)
            self.assertIn("boom", str(model_error_events[0].get("error", "")))
            self.assertTrue(any(event.get("event") == "complete" for event in events))
            self.assertEqual(result_df.iloc[0]["status"], "failed_model_inference")
            persisted = load_inference_dataset(output_csv)
            self.assertEqual(persisted.iloc[0]["status"], "failed_model_inference")

    def test_prior_knowledge_timeout_is_treated_as_no_detection(self) -> None:
        poem = {
            "poem_id": "1",
            "poem_text": "text",
            "author_name": "Author",
        }
        with mock.patch("src.inference.run_model", side_effect=RuntimeError("Request timed out.")):
            detected = check_prior_knowledge(poem, "qwen/qwen3.5-397b-a17b")
        self.assertFalse(detected)

    def test_prior_knowledge_uses_no_token_budget(self) -> None:
        poem = {
            "poem_id": "1",
            "poem_text": "text",
            "author_name": "Author",
        }
        with mock.patch("src.inference.run_model", return_value={"author_name": "I don't know"}) as mocked_run_model:
            check_prior_knowledge(poem, "openai/gpt-oss-120b")
        self.assertIsNone(mocked_run_model.call_args.kwargs["max_tokens"])
        self.assertFalse(mocked_run_model.call_args.kwargs["disable_retries"])


class EtymologyCacheTests(unittest.TestCase):
    def setUp(self) -> None:
        _lookup_word_origin.cache_clear()
        FAILED_LOOKUPS.clear()

    def tearDown(self) -> None:
        _lookup_word_origin.cache_clear()
        FAILED_LOOKUPS.clear()

    def test_etymology_cache_persists_and_refreshes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / "etymology.sqlite"
            with mock.patch.object(prose_analysis, "CACHE_PATH", cache_path):
                with mock.patch("src.prose_analysis._fetch_etymonline_entry", return_value=("https://example.com", "from Latin root")) as mocked_fetch:
                    first = check_word_origin("illumination", refresh=True)
                self.assertEqual(first["origin_group"], "latinate")
                self.assertEqual(mocked_fetch.call_count, 1)
                with mock.patch("src.prose_analysis._fetch_etymonline_entry", side_effect=RuntimeError("should not fetch")) as cached_fetch:
                    second = check_word_origin("illumination")
                self.assertEqual(second["source"], "etymonline")
                self.assertEqual(cached_fetch.call_count, 0)
                with mock.patch("src.prose_analysis._fetch_etymonline_entry", return_value=("https://example.com/2", "from Old English root")):
                    refreshed = check_word_origin("illumination", refresh=True)
                self.assertEqual(refreshed["origin_group"], "germanic")

    def test_warm_etymology_cache_uses_unique_words(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / "etymology.sqlite"
            with mock.patch.object(prose_analysis, "CACHE_PATH", cache_path):
                with mock.patch("src.prose_analysis._fetch_etymonline_entry", return_value=("https://example.com", "from Latin root")) as mocked_fetch:
                    result = warm_etymology_cache(["illumination illumination", "illumination"])
                self.assertEqual(result["unique_words"], 1)
                self.assertEqual(mocked_fetch.call_count, 1)


class UtilityRoutingTests(unittest.TestCase):
    class _Schema(BaseModel):
        value: int

    class _SplitSchema(BaseModel):
        left: int
        right: int

    def test_run_model_routes_gemma_to_nvidia(self) -> None:
        with mock.patch("src.utility.run_nvidia_models", return_value='{"value": 1}') as mocked_nvidia:
            with mock.patch("src.utility.parse_output_json", return_value={"value": 1}) as mocked_parse:
                result = run_model("ping", self._Schema, "gemma-3-27b-it")
        self.assertEqual(result, {"value": 1})
        mocked_nvidia.assert_called_once()
        mocked_parse.assert_called_once()

    def test_run_model_routes_gemini_to_google(self) -> None:
        with mock.patch("src.utility.run_google_models", return_value='{"value": 2}') as mocked_google:
            with mock.patch("src.utility.parse_output_json", return_value={"value": 2}) as mocked_parse:
                result = run_model("ping", self._Schema, "gemini-3.1-pro-preview")
        self.assertEqual(result, {"value": 2})
        mocked_google.assert_called_once()
        mocked_parse.assert_called_once()

    def test_run_model_routes_gpt_to_openai(self) -> None:
        with mock.patch("src.utility.run_openai_models", return_value='{"value": 3}') as mocked_openai:
            with mock.patch("src.utility.parse_output_json", return_value={"value": 3}) as mocked_parse:
                result = run_model("ping", self._Schema, "gpt-5.3")
        self.assertEqual(result, {"value": 3})
        mocked_openai.assert_called_once()
        mocked_parse.assert_called_once()

    def test_run_model_routes_new_nvidia_models(self) -> None:
        for model_name in (
            "qwen/qwen3.5-397b-a17b",
            "deepseek-ai/deepseek-v3.2",
            "openai/gpt-oss-120b",
            "moonshotai/kimi-k2-instruct",
        ):
            with self.subTest(model=model_name):
                with mock.patch("src.utility.run_nvidia_models", return_value='{"value": 9}') as mocked_nvidia:
                    with mock.patch("src.utility.parse_output_json", return_value={"value": 9}) as mocked_parse:
                        result = run_model("ping", self._Schema, model_name)
                self.assertEqual(result, {"value": 9})
                mocked_nvidia.assert_called_once()
                mocked_parse.assert_called_once()

    def test_run_nvidia_models_retries_with_prefixed_name(self) -> None:
        class FakeNotFound(Exception):
            pass

        response = mock.Mock()
        choice = mock.Mock()
        choice.message.content = '{"value": 4}'
        response.choices = [choice]

        client = mock.Mock()
        client.chat.completions.create.side_effect = [FakeNotFound("missing"), response]

        with mock.patch("openai.NotFoundError", FakeNotFound):
            with mock.patch("openai.OpenAI", return_value=client):
                with mock.patch("src.utility.NVIDIA_API_KEY", "dummy"):
                    output = run_nvidia_models("ping", "nemotron-3-nano-30b-a3b")

        self.assertEqual(output, '{"value": 4}')
        attempted = [call.kwargs["model"] for call in client.chat.completions.create.call_args_list]
        self.assertEqual(attempted, ["nvidia/nemotron-3-nano-30b-a3b", "nemotron-3-nano-30b-a3b"])
        first_call = client.chat.completions.create.call_args_list[0].kwargs
        self.assertEqual(first_call.get("extra_body"), {"chat_template_kwargs": {"enable_thinking": False}})

    def test_run_nvidia_models_gemma_tries_google_prefix(self) -> None:
        class FakeNotFound(Exception):
            pass

        response = mock.Mock()
        choice = mock.Mock()
        choice.message.content = '{"value": 5}'
        response.choices = [choice]

        client = mock.Mock()
        client.chat.completions.create.side_effect = [FakeNotFound("missing"), FakeNotFound("missing"), response]

        with mock.patch("openai.NotFoundError", FakeNotFound):
            with mock.patch("openai.OpenAI", return_value=client):
                with mock.patch("src.utility.NVIDIA_API_KEY", "dummy"):
                    output = run_nvidia_models("ping", "gemma-3-27b-it")

        self.assertEqual(output, '{"value": 5}')
        attempted = [call.kwargs["model"] for call in client.chat.completions.create.call_args_list]
        self.assertEqual(attempted, ["google/gemma-3-27b-it", "gemma-3-27b-it", "nvidia/gemma-3-27b-it"])

    def test_run_nvidia_models_namespaced_model_has_no_prefix_fallbacks(self) -> None:
        response = mock.Mock()
        choice = mock.Mock()
        choice.message.content = '{"value": 12}'
        response.choices = [choice]

        client = mock.Mock()
        client.chat.completions.create.return_value = response

        with mock.patch("openai.OpenAI", return_value=client):
            with mock.patch("src.utility.NVIDIA_API_KEY", "dummy"):
                output = run_nvidia_models("ping", "deepseek-ai/deepseek-v3.2")

        self.assertEqual(output, '{"value": 12}')
        attempted = [call.kwargs["model"] for call in client.chat.completions.create.call_args_list]
        self.assertEqual(attempted, ["deepseek-ai/deepseek-v3.2"])
        first_call = client.chat.completions.create.call_args_list[0].kwargs
        self.assertEqual(first_call.get("extra_body"), {"chat_template_kwargs": {"thinking": False}})

    def test_run_nvidia_models_gpt_oss_disables_thinking(self) -> None:
        response = mock.Mock()
        choice = mock.Mock()
        choice.message.content = '{"value": 13}'
        response.choices = [choice]

        client = mock.Mock()
        client.chat.completions.create.return_value = response

        with mock.patch("openai.OpenAI", return_value=client):
            with mock.patch("src.utility.NVIDIA_API_KEY", "dummy"):
                output = run_nvidia_models("ping", "openai/gpt-oss-120b")

        self.assertEqual(output, '{"value": 13}')
        self.assertEqual(client.chat.completions.create.call_count, 1)
        first_call = client.chat.completions.create.call_args_list[0].kwargs
        self.assertEqual(first_call.get("extra_body"), {"chat_template_kwargs": {"enable_thinking": False}})

    def test_run_nvidia_models_rate_limit_retries_with_pause(self) -> None:
        class FakeRateLimit(Exception):
            def __init__(self) -> None:
                super().__init__("Error code: 429 - {'status': 429, 'title': 'Too Many Requests'}")
                self.status_code = 429
                self.response = mock.Mock()
                self.response.status_code = 429
                self.response.headers = {"retry-after": "0.25"}

        response = mock.Mock()
        choice = mock.Mock()
        choice.message.content = '{"value": 14}'
        response.choices = [choice]

        client = mock.Mock()
        client.chat.completions.create.side_effect = [FakeRateLimit(), response]

        with mock.patch("openai.OpenAI", return_value=client):
            with mock.patch("src.utility.NVIDIA_API_KEY", "dummy"):
                with mock.patch("src.utility.random.uniform", return_value=0.0):
                    with mock.patch("src.utility.time.sleep") as mocked_sleep:
                        output = run_nvidia_models("ping", "openai/gpt-oss-120b")

        self.assertEqual(output, '{"value": 14}')
        self.assertEqual(client.chat.completions.create.call_count, 2)
        mocked_sleep.assert_called_once_with(0.25)

    def test_run_nvidia_models_rate_limit_uses_two_tier_exponential_backoff_without_retry_after(self) -> None:
        class FakeRateLimit(Exception):
            def __init__(self) -> None:
                super().__init__("Error code: 429 - {'status': 429, 'title': 'Too Many Requests'}")
                self.status_code = 429
                self.response = mock.Mock()
                self.response.status_code = 429
                self.response.headers = {}

        response = mock.Mock()
        choice = mock.Mock()
        choice.message.content = '{"value": 17}'
        response.choices = [choice]

        client = mock.Mock()
        client.chat.completions.create.side_effect = [
            FakeRateLimit(),
            FakeRateLimit(),
            FakeRateLimit(),
            FakeRateLimit(),
            FakeRateLimit(),
            response,
        ]

        with mock.patch("openai.OpenAI", return_value=client):
            with mock.patch("src.utility.NVIDIA_API_KEY", "dummy"):
                with mock.patch("src.utility.random.uniform", return_value=0.0):
                    with mock.patch("src.utility.time.sleep") as mocked_sleep:
                        output = run_nvidia_models("ping", "openai/gpt-oss-120b")

        self.assertEqual(output, '{"value": 17}')
        self.assertEqual(client.chat.completions.create.call_count, 6)
        self.assertEqual([call.args[0] for call in mocked_sleep.call_args_list], [2.0, 4.0, 12.0, 24.0, 48.0])

    def test_run_nvidia_models_qwen_timeout_tries_fallback_variants(self) -> None:
        class FakeTimeout(Exception):
            pass

        client = mock.Mock()
        client.chat.completions.create.side_effect = [
            FakeTimeout("Request timed out."),
            FakeTimeout("Request timed out."),
            FakeTimeout("Request timed out."),
        ]

        with mock.patch("openai.OpenAI", return_value=client):
            with mock.patch("src.utility.NVIDIA_API_KEY", "dummy"):
                with self.assertRaisesRegex(RuntimeError, "Request timed out"):
                    run_nvidia_models("ping", "qwen/qwen3.5-397b-a17b")

        self.assertEqual(client.chat.completions.create.call_count, 3)
        first_call = client.chat.completions.create.call_args_list[0].kwargs
        self.assertEqual(first_call.get("extra_body"), {
            "top_k": 20,
            "repetition_penalty": 1.0,
            "chat_template_kwargs": {"enable_thinking": False},
        })

    def test_run_nvidia_models_accepts_object_content_parts(self) -> None:
        class ContentPart:
            def __init__(self, text: str) -> None:
                self.text = text

        response = mock.Mock()
        choice = mock.Mock()
        choice.message.content = [ContentPart('{"value": 6}')]
        response.choices = [choice]

        client = mock.Mock()
        client.chat.completions.create.return_value = response

        with mock.patch("openai.OpenAI", return_value=client):
            with mock.patch("src.utility.NVIDIA_API_KEY", "dummy"):
                output = run_nvidia_models("ping", "nemotron-3-nano-30b-a3b")

        self.assertEqual(output, '{"value": 6}')

    def test_run_nvidia_models_retries_on_length_with_same_tokens(self) -> None:
        first_response = mock.Mock()
        first_choice = mock.Mock()
        first_choice.message.content = None
        first_choice.finish_reason = "length"
        first_response.choices = [first_choice]

        second_response = mock.Mock()
        second_choice = mock.Mock()
        second_choice.message.content = '{"value": 7}'
        second_choice.finish_reason = "stop"
        second_response.choices = [second_choice]

        client = mock.Mock()
        client.chat.completions.create.side_effect = [first_response, second_response]

        with mock.patch("openai.OpenAI", return_value=client):
            with mock.patch("src.utility.NVIDIA_API_KEY", "dummy"):
                output = run_nvidia_models("ping", "nemotron-3-nano-30b-a3b", max_tokens=40)

        self.assertEqual(output, '{"value": 7}')
        budgets = [call.kwargs["max_tokens"] for call in client.chat.completions.create.call_args_list]
        self.assertEqual(budgets, [40, 40])

    def test_run_model_retries_after_truncated_json(self) -> None:
        with mock.patch("src.utility.run_openai_models", side_effect=['{"value": "truncated', '{"value": 8}']) as mocked_openai:
            result = run_model("ping", self._Schema, "gpt-5.3", max_tokens=100)
        self.assertEqual(result, {"value": 8})
        budgets = [call.args[3] for call in mocked_openai.call_args_list]
        self.assertEqual(budgets, [100, 100])

    def test_run_model_retries_after_schema_echo_json(self) -> None:
        schema_echo = '{"type":"object","properties":{"value":{"type":"integer"}},"required":["value"]}'
        with mock.patch("src.utility.run_openai_models", side_effect=[schema_echo, '{"value": 8}']) as mocked_openai:
            result = run_model("ping", self._Schema, "gpt-5.3", max_tokens=100)
        self.assertEqual(result, {"value": 8})
        budgets = [call.args[3] for call in mocked_openai.call_args_list]
        self.assertEqual(budgets, [100, 100])
        second_prompt = mocked_openai.call_args_list[1].args[0]
        self.assertIn("Previous output returned JSON schema metadata", second_prompt)

    def test_run_model_retries_after_empty_backend_error(self) -> None:
        with mock.patch(
            "src.utility.run_nvidia_models",
            side_effect=[RuntimeError("NVIDIA returned empty content for model 'openai/gpt-oss-120b'"), '{"value": 8}'],
        ) as mocked_nvidia:
            result = run_model("ping", self._Schema, "openai/gpt-oss-120b", max_tokens=100)
        self.assertEqual(result, {"value": 8})
        budgets = [call.args[3] for call in mocked_nvidia.call_args_list]
        self.assertEqual(budgets, [100, 100])
        allow_retry_flags = [call.kwargs.get("allow_token_retry") for call in mocked_nvidia.call_args_list]
        self.assertEqual(allow_retry_flags, [False, False])

    def test_run_model_retries_after_rate_limit_backend_error(self) -> None:
        with mock.patch(
            "src.utility.run_nvidia_models",
            side_effect=[RuntimeError("Error code: 429 - {'status': 429, 'title': 'Too Many Requests'}"), '{"value": 8}'],
        ) as mocked_nvidia:
            with mock.patch("src.utility.random.uniform", return_value=0.0):
                with mock.patch("src.utility.time.sleep") as mocked_sleep:
                    result = run_model("ping", self._Schema, "openai/gpt-oss-120b", max_tokens=100)
        self.assertEqual(result, {"value": 8})
        self.assertEqual(mocked_nvidia.call_count, 2)
        mocked_sleep.assert_called_once_with(0.8)

    def test_run_model_timeout_retries_use_long_tier_backoff(self) -> None:
        with mock.patch(
            "src.utility.run_nvidia_models",
            side_effect=[
                RuntimeError("Request timed out."),
                RuntimeError("Request timed out."),
                RuntimeError("Request timed out."),
                '{"value": 8}',
            ],
        ) as mocked_nvidia:
            with mock.patch("src.utility.random.uniform", return_value=0.0):
                with mock.patch("src.utility.time.sleep") as mocked_sleep:
                    result = run_model("ping", self._Schema, "openai/gpt-oss-120b", max_tokens=100)
        self.assertEqual(result, {"value": 8})
        self.assertEqual(mocked_nvidia.call_count, 4)
        self.assertEqual([call.args[0] for call in mocked_sleep.call_args_list], [0.8, 1.6, 12.0])

    def test_run_model_disable_retries_uses_single_backend_attempt(self) -> None:
        with mock.patch("src.utility.run_openai_models", side_effect=RuntimeError("timed out")) as mocked_openai:
            with self.assertRaisesRegex(RuntimeError, "timed out"):
                run_model("ping", self._Schema, "gpt-5.3", disable_retries=True)
        self.assertEqual(mocked_openai.call_count, 1)

    def test_run_model_does_not_retry_after_trailing_text_recovery(self) -> None:
        with mock.patch("src.utility.run_openai_models", return_value='{"value": 10}\nDone.') as mocked_openai:
            result = run_model("ping", self._Schema, "gpt-5.3", max_tokens=100)
        self.assertEqual(result, {"value": 10})
        self.assertEqual(mocked_openai.call_count, 1)

    def test_parse_output_json_extracts_wrapped_json(self) -> None:
        parsed = parse_output_json("Model output:\n```json\n{\"value\": 9}\n```\nDone.", self._Schema)
        self.assertEqual(parsed, {"value": 9})

    def test_parse_output_json_ignores_trailing_text(self) -> None:
        parsed = parse_output_json("{\"value\": 11}\nSummary complete.", self._Schema)
        self.assertEqual(parsed, {"value": 11})

    def test_parse_output_json_merges_adjacent_objects(self) -> None:
        parsed = parse_output_json("{\"left\": 1}\n\n{\"right\": 2}", self._SplitSchema)
        self.assertEqual(parsed, {"left": 1, "right": 2})

    def test_parse_output_json_flags_schema_echo(self) -> None:
        with self.assertRaisesRegex(ValueError, "schema_echo_json: Failed to parse output as JSON for _Schema"):
            parse_output_json('{"type":"object","properties":{"value":{"type":"integer"}},"required":["value"]}', self._Schema)

    def test_parse_output_json_error_includes_schema_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "json_parse_error: Failed to parse output as JSON for _Schema"):
            parse_output_json("not json at all", self._Schema)


class StatsOutputPersistenceTests(unittest.TestCase):
    def test_when_stats_cannot_run_then_error_json_and_markdown_are_still_saved(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_csv = tmp / "input.csv"
            inference_csv = tmp / "inference.csv"
            output_json = tmp / "results.json"
            output_md = tmp / "results.md"
            analysis_csv = tmp / "analysis.csv"

            pd.DataFrame(
                [
                    {
                        "poem_id": "1",
                        "poem_text": "text",
                        "poem_fetch_url": "https://example.com/1",
                        "poem_genre": "lyric",
                        "year_of_publish": 2000,
                        "author_name": "Author",
                        "author_age": 30,
                        "author_gender": "female",
                        "author_ethnicity": "group",
                        "author_nationality": "nation",
                    }
                ]
            ).to_csv(input_csv, index=False)

            pd.DataFrame(
                [
                    {
                        "poem_id": "1",
                        "model": "screening",
                        "status": "skipped_prior_knowledge",
                        "skip_reason": "prior_knowledge_detected",
                        "prior_knowledge_detected_models": json.dumps(["gpt-5.4"]),
                        "poem_fetch_url": "https://example.com/1",
                        "poem_genre": "lyric",
                        "year_of_publish": 2000,
                        "author_name": "Author",
                        "author_age": 30,
                        "author_gender": "female",
                        "author_ethnicity": "group",
                        "author_nationality": "nation",
                        "literary_devices": json.dumps([]),
                        "technical_craft_score": pd.NA,
                        "structure_score": pd.NA,
                        "diction_score": pd.NA,
                        "originality_score": pd.NA,
                        "impact_score": pd.NA,
                        "aggregate_score": pd.NA,
                    }
                ]
            ).to_csv(inference_csv, index=False)

            with self.assertRaises(RuntimeError):
                run_all_analyses(
                    str(input_csv),
                    str(inference_csv),
                    str(output_json),
                    str(analysis_csv),
                    report_md=str(output_md),
                )

            self.assertTrue(output_json.exists())
            self.assertTrue(output_md.exists())
            payload = json.loads(output_json.read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "error")
            self.assertIn("No balanced completed poem-by-model rows are available for analysis", payload["error"]["message"])
            markdown = output_md.read_text(encoding="utf-8")
            self.assertIn("## Run Status", markdown)
            self.assertIn("No balanced completed poem-by-model rows are available for analysis", markdown)


class StatisticalAnalysisTests(unittest.TestCase):
    def _suppress_stats_warnings(self):
        return warnings.catch_warnings()

    def _write_synthetic_dataset(self, tmp: Path) -> tuple[Path, Path]:
        models = ["gpt-5.4", "claude-opus-4-6", "gemini-3.1-pro-preview"]
        input_rows = []
        inference_rows = []
        for idx in range(1, 25):
            poem_id = str(idx)
            is_long = idx % 2 == 0
            female = idx % 3 == 0
            poem_text = "illumination civilization resonance " * 8 if is_long else "sun wind rain stone " * 8
            input_rows.append(
                {
                    "poem_id": poem_id,
                    "poem_text": poem_text,
                    "poem_fetch_url": f"https://example.com/{idx}",
                    "poem_genre": "lyric",
                    "year_of_publish": 2000 + idx,
                    "author_name": f"Author {idx}",
                    "author_age": 30 + idx,
                    "author_gender": "female" if female else "male",
                    "author_ethnicity": "group_a" if idx % 2 == 0 else "group_b",
                    "author_nationality": "nation_a" if idx % 4 < 2 else "nation_b",
                }
            )
            base = 18 + (idx % 5)
            for model in models:
                metaphor = (model == "gpt-5.4" and is_long) or (model == "claude-opus-4-6" and idx % 4 == 0) or (model == "gemini-3.1-pro-preview" and idx % 8 == 0)
                aggregate = base
                if model == "gpt-5.4":
                    aggregate += 8 + (8 if is_long else 0) + (6 if female else 0) + (6 if metaphor else 0)
                elif model == "claude-opus-4-6":
                    aggregate += 1 + (2 if is_long else 0) + (1 if female else 0) + (1 if metaphor else 0)
                else:
                    aggregate += (-6) + (1 if is_long else 0) + (1 if metaphor else 0)
                inference_rows.append(
                    {
                        "poem_id": poem_id,
                        "model": model,
                        "status": "completed",
                        "skip_reason": "",
                        "prior_knowledge_detected_models": json.dumps([]),
                        "poem_fetch_url": f"https://example.com/{idx}",
                        "poem_genre": "lyric",
                        "year_of_publish": 2000 + idx,
                        "author_name": f"Author {idx}",
                        "author_age": 30 + idx,
                        "author_gender": "female" if female else "male",
                        "author_ethnicity": "group_a" if idx % 2 == 0 else "group_b",
                        "author_nationality": "nation_a" if idx % 4 < 2 else "nation_b",
                        "literary_devices": json.dumps(["metaphor"] if metaphor else []),
                        "technical_craft_score": aggregate // 5,
                        "structure_score": aggregate // 5,
                        "diction_score": aggregate // 5,
                        "originality_score": aggregate // 5,
                        "impact_score": aggregate // 5,
                        "aggregate_score": aggregate,
                    }
                )
        input_csv = tmp / "input.csv"
        inference_csv = tmp / "inference.csv"
        pd.DataFrame(input_rows).to_csv(input_csv, index=False)
        pd.DataFrame(inference_rows).to_csv(inference_csv, index=False)
        return input_csv, inference_csv

    def _write_origin_interaction_dataset(self, tmp: Path) -> tuple[Path, Path]:
        models = ["gpt-5.4", "claude-opus-4-6", "gemini-3.1-pro-preview"]
        input_rows = []
        inference_rows = []
        for idx in range(1, 41):
            poem_id = str(idx)
            is_ai_origin = idx % 2 == 0
            origin_label = "AI made" if is_ai_origin else "public-domain anthology"
            poem_text = ("synthetic radiant syntax " if is_ai_origin else "stone river wind ") * 8
            input_rows.append(
                {
                    "poem_id": poem_id,
                    "poem_text": poem_text,
                    "poem_fetch_url": f"https://example.com/origin/{idx}",
                    "poem_genre": "lyric",
                    "year_of_publish": 1990 + idx,
                    "author_name": f"Origin Author {idx}",
                    "author_age": 20 + idx,
                    "author_gender": "female" if idx % 3 == 0 else "male",
                    "author_ethnicity": "group_a" if idx % 2 == 0 else "group_b",
                    "author_nationality": "nation_a" if idx % 4 < 2 else "nation_b",
                    "poem_origin_label": origin_label,
                }
            )
            base = 28 + (idx % 4)
            for model in models:
                if model == "gpt-5.4":
                    aggregate = base + (8 if is_ai_origin else 0)
                elif model == "claude-opus-4-6":
                    aggregate = base + (2 if is_ai_origin else 0)
                else:
                    aggregate = base + (-4 if is_ai_origin else 2)
                component = aggregate / 5.0
                inference_rows.append(
                    {
                        "poem_id": poem_id,
                        "model": model,
                        "status": "completed",
                        "skip_reason": "",
                        "prior_knowledge_detected_models": json.dumps([]),
                        "poem_fetch_url": f"https://example.com/origin/{idx}",
                        "poem_genre": "lyric",
                        "year_of_publish": 1990 + idx,
                        "author_name": f"Origin Author {idx}",
                        "author_age": 20 + idx,
                        "author_gender": "female" if idx % 3 == 0 else "male",
                        "author_ethnicity": "group_a" if idx % 2 == 0 else "group_b",
                        "author_nationality": "nation_a" if idx % 4 < 2 else "nation_b",
                        "literary_devices": json.dumps(["imagery"] if is_ai_origin else []),
                        "technical_craft_score": component,
                        "structure_score": component,
                        "diction_score": component,
                        "originality_score": component,
                        "impact_score": component,
                        "aggregate_score": aggregate,
                    }
                )
        input_csv = tmp / "input_origin.csv"
        inference_csv = tmp / "inference_origin.csv"
        pd.DataFrame(input_rows).to_csv(input_csv, index=False)
        pd.DataFrame(inference_rows).to_csv(inference_csv, index=False)
        return input_csv, inference_csv

    def test_stats_pipeline_detects_planted_effects(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_csv, inference_csv = self._write_synthetic_dataset(tmp)
            analysis_csv = tmp / "analysis.csv"
            results_json = tmp / "results.json"
            analysis_df = build_analysis_dataset(input_csv, inference_csv, analysis_csv)
            self.assertFalse(analysis_df.empty)
            with self._suppress_stats_warnings():
                warnings.simplefilter("ignore")
                results = run_all_analyses(input_csv, inference_csv, results_json, analysis_csv)
            self.assertEqual(results["overall_score"]["status"], "ok")
            self.assertEqual(results["device_detection"]["tests"][0]["device"], "metaphor")
            self.assertLess(results["device_detection"]["tests"][0]["adjusted_pvalue"], 0.05)
            self.assertEqual(results["device_score_interactions"]["tests"][0]["status"], "ok")
            self.assertLess(results["device_score_interactions"]["tests"][0]["adjusted_pvalue"], 0.05)
            avg_word_length = next(item for item in results["diction_score_interactions"]["tests"] if item["feature"] == "avg_word_length")
            self.assertEqual(avg_word_length["status"], "ok")
            self.assertLess(avg_word_length["adjusted_pvalue"], 0.05)
            author_gender = next(item for item in results["author_score_interactions"]["tests"] if item["feature"] == "author_gender")
            self.assertEqual(author_gender["status"], "ok")
            self.assertLess(author_gender["adjusted_pvalue"], 0.05)
            metric_keys = {
                "aggregate_score",
                "technical_craft_score",
                "structure_score",
                "diction_score",
                "originality_score",
                "impact_score",
            }
            self.assertEqual(set(results["score_summaries_by_metric"]["metrics"].keys()), metric_keys)
            self.assertEqual(set(results["score_model_comparisons_by_metric"]["metrics"].keys()), metric_keys)
            self.assertEqual(set(results["device_score_interactions_by_metric"]["metrics"].keys()), metric_keys)
            self.assertEqual(set(results["diction_score_interactions_by_metric"]["metrics"].keys()), metric_keys)
            self.assertEqual(set(results["author_score_interactions_by_metric"]["metrics"].keys()), metric_keys)
            self.assertEqual(set(results["ai_origin_score_interactions_by_metric"]["metrics"].keys()), metric_keys)
            self.assertEqual(results["overall_score"], results["score_model_comparisons_by_metric"]["metrics"]["aggregate_score"])
            self.assertEqual(results["model_score_summary"], results["score_summaries_by_metric"]["metrics"]["aggregate_score"])
            self.assertEqual(results["device_score_interactions"], results["device_score_interactions_by_metric"]["metrics"]["aggregate_score"])
            self.assertEqual(results["diction_score_interactions"], results["diction_score_interactions_by_metric"]["metrics"]["aggregate_score"])
            self.assertEqual(results["author_score_interactions"], results["author_score_interactions_by_metric"]["metrics"]["aggregate_score"])
            self.assertEqual(results["ai_origin_score_interactions"], results["ai_origin_score_interactions_by_metric"]["metrics"]["aggregate_score"])
            self.assertTrue(results_json.exists())

    def test_ai_origin_interaction_detects_model_specific_preferences(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_csv, inference_csv = self._write_origin_interaction_dataset(tmp)
            analysis_csv = tmp / "analysis_origin.csv"
            results_json = tmp / "results_origin.json"
            with self._suppress_stats_warnings():
                warnings.simplefilter("ignore")
                results = run_all_analyses(input_csv, inference_csv, results_json, analysis_csv)

            metric_payload = results["ai_origin_score_interactions_by_metric"]["metrics"]["aggregate_score"]
            self.assertEqual(metric_payload["status"], "ok")
            self.assertTrue(metric_payload["significant"])
            self.assertEqual(metric_payload["significance_basis"], "raw_unadjusted")

            by_model = metric_payload["ai_minus_non_ai_by_model"]
            self.assertGreater(float(by_model["gpt-5.4"]["ai_minus_non_ai"]), 0.0)
            self.assertGreater(float(by_model["claude-opus-4-6"]["ai_minus_non_ai"]), 0.0)
            self.assertLess(float(by_model["gemini-3.1-pro-preview"]["ai_minus_non_ai"]), 0.0)

            pair = next(
                row
                for row in metric_payload["pairwise"]
                if {row["left_model"], row["right_model"]} == {"gpt-5.4", "gemini-3.1-pro-preview"}
            )
            self.assertEqual(pair["status"], "ok")
            self.assertIsNotNone(pair["adjusted_pvalue"])
            self.assertTrue(pair["significant"])
            self.assertEqual(pair["significance_basis"], "adjusted")
            if float(pair["gap_difference"]) > 0:
                self.assertIn("higher", str(pair["direction"]))
            elif float(pair["gap_difference"]) < 0:
                self.assertIn("lower", str(pair["direction"]))
            self.assertEqual(
                results["ai_origin_score_interactions"],
                results["ai_origin_score_interactions_by_metric"]["metrics"]["aggregate_score"],
            )

    def test_ai_origin_interaction_is_skipped_when_origin_label_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_csv, inference_csv = self._write_synthetic_dataset(tmp)
            analysis_csv = tmp / "analysis.csv"
            results_json = tmp / "results.json"
            with self._suppress_stats_warnings():
                warnings.simplefilter("ignore")
                results = run_all_analyses(input_csv, inference_csv, results_json, analysis_csv)

            origin_metrics = results["ai_origin_score_interactions_by_metric"]["metrics"]
            self.assertEqual(len(origin_metrics), 6)
            for payload in origin_metrics.values():
                self.assertEqual(payload["status"], "skipped")
                self.assertIn("origin", str(payload.get("reason", "")))

    def test_significance_policy_and_directionality_are_consistent(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_csv, inference_csv = self._write_synthetic_dataset(tmp)
            analysis_csv = tmp / "analysis.csv"
            results_json = tmp / "results.json"
            with self._suppress_stats_warnings():
                warnings.simplefilter("ignore")
                results = run_all_analyses(input_csv, inference_csv, results_json, analysis_csv)

            self.assertEqual(results["alpha"], 0.05)

            aggregate_pairwise = results["score_model_comparisons_by_metric"]["metrics"]["aggregate_score"]["pairwise"]
            for row in aggregate_pairwise:
                if row.get("status") != "ok":
                    continue
                mean_diff = float(row["mean_difference"])
                direction = str(row.get("direction", ""))
                if mean_diff > 0:
                    self.assertIn("higher", direction)
                elif mean_diff < 0:
                    self.assertIn("lower", direction)
                else:
                    self.assertIn("no directional difference", direction)
                if row.get("adjusted_pvalue") is not None:
                    self.assertEqual(row.get("significance_basis"), "adjusted")
                    self.assertEqual(bool(row.get("significant")), float(row["adjusted_pvalue"]) < 0.05)

            for row in results["device_detection"].get("tests", []):
                if row.get("adjusted_pvalue") is not None:
                    self.assertEqual(bool(row.get("significant")), float(row["adjusted_pvalue"]) < 0.05)

            for family in (
                "device_score_interactions_by_metric",
                "diction_score_interactions_by_metric",
                "author_score_interactions_by_metric",
            ):
                for metric_payload in results[family]["metrics"].values():
                    for test_row in metric_payload.get("tests", []):
                        if test_row.get("adjusted_pvalue") is not None:
                            self.assertEqual(bool(test_row.get("significant")), float(test_row["adjusted_pvalue"]) < 0.05)
                        for detail in test_row.get("direction_by_model", []):
                            estimate = float(detail["estimate"])
                            direction = str(detail.get("direction", ""))
                            if estimate > 0:
                                self.assertIn("stronger positive", direction)
                            elif estimate < 0:
                                self.assertIn("weaker or negative", direction)

    def test_markdown_report_includes_ap_stats_full_metrics_and_no_suggestive_language(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_csv, inference_csv = self._write_synthetic_dataset(tmp)
            analysis_csv = tmp / "analysis.csv"
            results_json = tmp / "results.json"
            with self._suppress_stats_warnings():
                warnings.simplefilter("ignore")
                results = run_all_analyses(input_csv, inference_csv, results_json, analysis_csv)

            markdown = render_results_markdown(results)
            self.assertIn("## Significant Results Only", markdown)
            self.assertIn("## AP Stats Interpretation Guide", markdown)
            self.assertIn("alpha = 0.05", markdown)
            self.assertIn("AI-vs-Non-AI interaction null", markdown)
            self.assertIn("## AI-vs-Non-AI Preference Interactions By Metric", markdown)
            self.assertIn("## Model Comparisons By Score Metric", markdown)
            for metric in (
                "aggregate_score",
                "technical_craft_score",
                "structure_score",
                "diction_score",
                "originality_score",
                "impact_score",
            ):
                self.assertIn(f"`{metric}`", markdown)
            self.assertNotIn("suggestive", markdown.lower())
            self.assertIn("## Skipped And Error Rows", markdown)

    def test_cli_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_csv, inference_csv = self._write_synthetic_dataset(tmp)
            analysis_csv = tmp / "analysis.csv"
            results_json = tmp / "results.json"
            script_help_result = subprocess.run([sys.executable, "src/main.py", "--help"], capture_output=True, text=True, check=True)
            self.assertIn("Literary analysis pipeline", script_help_result.stdout)
            help_result = subprocess.run([sys.executable, "-m", "src.main", "--help"], capture_output=True, text=True, check=True)
            self.assertIn("Literary analysis pipeline", help_result.stdout)
            stats_result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "src.main",
                    "stats",
                    "--input",
                    str(input_csv),
                    "--inference",
                    str(inference_csv),
                    "--analysis-csv",
                    str(analysis_csv),
                    "--output-json",
                    str(results_json),
                    "--runs-dir",
                    str(tmp / "runs"),
                    "--run-id",
                    "smoke-run",
                    "--report-md",
                    str(tmp / "custom_report.md"),
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("output_json", stats_result.stdout)
            self.assertIn("run_id", stats_result.stdout)
            self.assertTrue((tmp / "custom_report.md").exists())
            self.assertTrue((tmp / "runs" / "smoke-run" / "manifest.json").exists())
            warm_result = subprocess.run(
                [sys.executable, "-m", "src.main", "warm-etymology-cache", "illumination", "illumination"],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn('"unique_words": 1', warm_result.stdout)


if __name__ == "__main__":
    unittest.main()
