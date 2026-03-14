# Test Intent Matrix

This file maps behavioral requirements to tests, so each test has an explicit purpose tied to user-visible outcomes.

## Data Loading And Compatibility

- Input headers are normalized and required fields are preserved.
  - `LoaderTests.test_load_input_dataset_strips_headers`
- Legacy inference CSVs (including removed rationale columns) still load.
  - `LoaderTests.test_load_inference_dataset_accepts_legacy_rationale_columns`

## Inference Saving And Resume Behavior

- Resume mode preserves existing completed rows and adds only missing work.
  - `InferenceTests.test_inference_resume_preserves_existing_rows`
- New inference outputs exclude rationale columns in memory and persisted CSV.
  - `InferenceTests.test_inference_resume_preserves_existing_rows`

## Parsing And Model Routing

- Model routing dispatches to the expected backend.
  - `UtilityRoutingTests.test_run_model_routes_gemma_to_nvidia`
  - `UtilityRoutingTests.test_run_model_routes_new_nvidia_models`
  - `UtilityRoutingTests.test_run_model_routes_gemini_to_google`
  - `UtilityRoutingTests.test_run_model_routes_gpt_to_openai`
- NVIDIA fallback and retry behavior handle vendor-specific response patterns.
  - `UtilityRoutingTests.test_run_nvidia_models_retries_with_prefixed_name`
  - `UtilityRoutingTests.test_run_nvidia_models_gemma_tries_google_prefix`
  - `UtilityRoutingTests.test_run_nvidia_models_namespaced_model_has_no_prefix_fallbacks`
  - `UtilityRoutingTests.test_run_nvidia_models_accepts_object_content_parts`
  - `UtilityRoutingTests.test_run_nvidia_models_retries_on_length_with_more_tokens`
- Two-tier exponential retry/backoff behavior escalates waits for timeout and 429-class failures.
  - `UtilityRoutingTests.test_run_nvidia_models_rate_limit_uses_two_tier_exponential_backoff_without_retry_after`
  - `UtilityRoutingTests.test_run_model_timeout_retries_use_long_tier_backoff`
  - `UtilityRoutingTests.test_run_model_disable_retries_uses_single_backend_attempt`
- JSON parse handling recovers wrapped/split outputs and only retries truncation-style failures.
  - `UtilityRoutingTests.test_run_model_retries_after_truncated_json`
  - `UtilityRoutingTests.test_run_model_does_not_retry_after_trailing_text_recovery`
  - `UtilityRoutingTests.test_parse_output_json_extracts_wrapped_json`
  - `UtilityRoutingTests.test_parse_output_json_ignores_trailing_text`
  - `UtilityRoutingTests.test_parse_output_json_merges_adjacent_objects`
  - `UtilityRoutingTests.test_parse_output_json_error_includes_schema_name`

## Artifact Management And Atomic Persistence

- Explicit run IDs map to deterministic run folders.
  - `ArtifactManagerTests.test_when_run_id_is_explicit_then_run_directory_is_deterministic`
- Missing run IDs generate timestamped unique run folders.
  - `ArtifactManagerTests.test_when_run_id_is_omitted_then_generated_id_has_expected_shape`
- Stage manifests and latest-run pointer are updated on writes.
  - `ArtifactManagerTests.test_when_stage_is_recorded_then_manifest_and_latest_pointer_are_updated`
- Atomic write failures do not corrupt existing artifacts.
  - `ArtifactManagerTests.test_when_atomic_write_fails_then_existing_file_remains_unchanged`

## Human-Readable Reporting

- Markdown report contains plain-language interpretation sections for successful runs.
  - `ReportRenderingTests.test_when_results_include_findings_then_markdown_is_human_readable`
- Markdown report includes a dedicated significant-only section and explicit no-significant fallback text.
  - `ReportRenderingTests.test_when_no_rows_are_significant_then_markdown_says_so`
- Markdown report explains failure states for non-expert readers.
  - `ReportRenderingTests.test_when_results_are_error_state_then_markdown_explains_failure`
- Error runs still persist JSON + Markdown artifacts before raising.
  - `StatsOutputPersistenceTests.test_when_stats_cannot_run_then_error_json_and_markdown_are_still_saved`

## Run Linking And Full-Pipeline Organization

- Shared `run_id` links `infer` and `stats` artifacts into one run folder.
  - `PipelineRunLinkingTests.test_when_infer_then_stats_share_run_id_then_outputs_are_grouped`
- Missing `run_id` creates separate command-local runs.
  - `PipelineRunLinkingTests.test_when_run_id_is_omitted_then_each_invocation_gets_distinct_run_folder`

## Statistical Pipeline And CLI

- Statistical analyses detect planted effects in synthetic paired data.
  - `StatisticalAnalysisTests.test_stats_pipeline_detects_planted_effects`
- AI-vs-non-AI interaction analysis detects model-specific preference gaps and reports directionality.
  - `StatisticalAnalysisTests.test_ai_origin_interaction_detects_model_specific_preferences`
- AI-vs-non-AI section is skipped (without failing the run) when origin labels are unavailable.
  - `StatisticalAnalysisTests.test_ai_origin_interaction_is_skipped_when_origin_label_missing`
- CLI smoke checks include new run-artifact flags and report output.
  - `StatisticalAnalysisTests.test_cli_smoke`
