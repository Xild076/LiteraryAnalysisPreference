from __future__ import annotations

import argparse
import json
from pathlib import Path

from .inference import run_inference_on_dataset
from .prose_analysis import warm_etymology_cache
from .statistical_analysis import build_analysis_dataset, run_all_analyses
from .utility import SUPPORTED_MODELS
from .data_parser import load_input_dataset



def _default_path(name: str) -> str:
    return str(Path(__file__).resolve().parents[1] / "data" / name)



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Literary analysis pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    infer_parser = subparsers.add_parser("infer", help="Run model inference across the poem dataset")
    infer_parser.add_argument("--input", default=_default_path("input.csv"))
    infer_parser.add_argument("--output", default=_default_path("inference_results.csv"))
    infer_parser.add_argument("--models", nargs="+", default=list(SUPPORTED_MODELS))
    infer_parser.add_argument("--no-cache", action="store_true")

    stats_parser = subparsers.add_parser("stats", help="Build the analysis dataset and run statistical tests")
    stats_parser.add_argument("--input", default=_default_path("input.csv"))
    stats_parser.add_argument("--inference", default=_default_path("inference_results.csv"))
    stats_parser.add_argument("--analysis-csv", default=_default_path("analysis_dataset.csv"))
    stats_parser.add_argument("--output-json", default=_default_path("statistical_results.json"))

    warm_parser = subparsers.add_parser("warm-etymology-cache", help="Warm the permanent etymology cache")
    warm_parser.add_argument("--input", default=_default_path("input.csv"))
    warm_parser.add_argument("--refresh", action="store_true")
    warm_parser.add_argument("words", nargs="*")

    dataset_parser = subparsers.add_parser("build-analysis-dataset", help="Build the joined analysis dataset without running tests")
    dataset_parser.add_argument("--input", default=_default_path("input.csv"))
    dataset_parser.add_argument("--inference", default=_default_path("inference_results.csv"))
    dataset_parser.add_argument("--analysis-csv", default=_default_path("analysis_dataset.csv"))
    return parser



def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "infer":
        result_df = run_inference_on_dataset(args.input, args.output, args.models, check_cache=not args.no_cache)
        print(json.dumps({"rows": len(result_df), "output": args.output, "models": args.models}, indent=2))
        return
    if args.command == "stats":
        results = run_all_analyses(args.input, args.inference, args.output_json, args.analysis_csv)
        print(json.dumps({"output_json": args.output_json, "analysis_csv": args.analysis_csv, "sections": list(results.keys())}, indent=2))
        return
    if args.command == "warm-etymology-cache":
        if args.words:
            payload = args.words
        else:
            payload = load_input_dataset(args.input)["poem_text"].fillna("").tolist()
        result = warm_etymology_cache(payload, refresh=args.refresh)
        print(json.dumps(result, indent=2))
        return
    if args.command == "build-analysis-dataset":
        df = build_analysis_dataset(args.input, args.inference, args.analysis_csv)
        print(json.dumps({"rows": len(df), "analysis_csv": args.analysis_csv}, indent=2))
        return
    parser.error(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()
