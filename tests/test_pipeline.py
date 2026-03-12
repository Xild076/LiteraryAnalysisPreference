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

from src.data_parser import load_input_dataset
from src.inference import run_inference_on_dataset
from src.prose_analysis import FAILED_LOOKUPS, _lookup_word_origin, check_word_origin, warm_etymology_cache
from src import prose_analysis
from src.statistical_analysis import build_analysis_dataset, run_all_analyses


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
                    "literary_devices_rationale": "",
                    "literary_devices": ["metaphor"],
                    "score_rationale": "",
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
                        "literary_devices_rationale": "",
                        "literary_devices": json.dumps(["metaphor"] if metaphor else []),
                        "score_rationale": "",
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
            self.assertTrue(results_json.exists())

    def test_cli_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_csv, inference_csv = self._write_synthetic_dataset(tmp)
            analysis_csv = tmp / "analysis.csv"
            results_json = tmp / "results.json"
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
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("output_json", stats_result.stdout)
            warm_result = subprocess.run(
                [sys.executable, "-m", "src.main", "warm-etymology-cache", "illumination", "illumination"],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn('"unique_words": 1', warm_result.stdout)


if __name__ == "__main__":
    unittest.main()
