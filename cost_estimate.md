# LLM Cost Estimate for Literary Analysis Project

## Corpus Basis

- Estimate source: `data/test_input.csv`
- Current repo state: `data/test_input.csv` contains 7 poems; `data/input.csv` currently contains 0 rows.
- Corpus totals: 4,480 characters, 861 words.
- Per-poem averages: 640 characters, 123 words.
- Token heuristic: approximately 4 characters per token, following Google's token guidance: <https://ai.google.dev/gemini-api/docs/tokens>
- Approximate raw poem text size: 160 input tokens per poem on average, with a range of about 94 to 266.

These estimates are for cold runs with no cache hits. Each poem triggers 3 calls per model:

1. Prior knowledge check
2. Literary devices inference
3. Score inference

Across 3 models, that is 9 API calls per poem.

## Average Input Tokens Per Poem Per Model

The numbers below include poem text, instructions, and the JSON schema appended by `run_model()`.

| Call | Legacy rationale pipeline | Implemented no-rationale pipeline |
| --- | ---: | ---: |
| Prior knowledge check | 274.43 | 274.43 |
| Literary devices | 396.14 | 392.00 |
| Scoring | 441.00 | 414.14 |
| **Total input per poem per model** | **1,111.57** | **1,080.57** |

## Representative Output Tokens Per Poem Per Model

These are estimated from compact valid JSON payloads, not the configured max-token caps.

| Call | Legacy rationale pipeline | Implemented no-rationale pipeline |
| --- | ---: | ---: |
| Prior knowledge check | 8 | 8 |
| Literary devices | 40 | 18 |
| Scoring | 60 | 28 |
| **Total output per poem per model** | **108** | **54** |

The input reduction from removing rationales is modest because prompt and schema overhead dominate this corpus. The output reduction is larger because the free-text rationales are gone.

## Pricing References

Current official pricing pages used for this estimate:

- OpenAI GPT-5.4: <https://openai.com/api/pricing/>
- Anthropic Claude Opus 4.6: <https://docs.anthropic.com/en/docs/about-claude/pricing>
- Google Gemini 3.1 Pro Preview: <https://ai.google.dev/pricing>

Rates used:

| Model | Input / 1M tokens | Output / 1M tokens |
| --- | ---: | ---: |
| GPT-5.4 | $2.50 | $15.00 |
| Claude Opus 4.6 | $5.00 | $25.00 |
| Gemini 3.1 Pro Preview | $2.00 | $12.00 |

## Cost Per Poem

### Legacy rationale pipeline

| Model | Cost per poem |
| --- | ---: |
| GPT-5.4 | $0.004399 |
| Claude Opus 4.6 | $0.008258 |
| Gemini 3.1 Pro Preview | $0.003519 |
| **All 3 models** | **$0.016176** |

### Implemented no-rationale pipeline

| Model | Cost per poem |
| --- | ---: |
| GPT-5.4 | $0.003511 |
| Claude Opus 4.6 | $0.006753 |
| Gemini 3.1 Pro Preview | $0.002809 |
| **All 3 models** | **$0.013073** |

Removing rationales lowers the estimated cold-run cost by about 19.18% on this corpus.

## Scale Estimates

### Legacy rationale pipeline

| Poem count | Estimated total |
| --- | ---: |
| 7 | $0.113231 |
| 100 | $1.62 |
| 1,000 | $16.18 |

### Implemented no-rationale pipeline

| Poem count | Estimated total |
| --- | ---: |
| 7 | $0.091514 |
| 100 | $1.31 |
| 1,000 | $13.07 |

## Notes

- These are approximation-grade planning numbers, not invoice-grade forecasts.
- They exclude retries, vendor-side prompt caching, and any future prompt or schema changes.
- The no-rationale estimate matches the code currently implemented in `src/inference.py`.
