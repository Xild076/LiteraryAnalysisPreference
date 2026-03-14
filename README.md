# LiteraryAnalysis

Basic pipeline for comparing how multiple LLMs analyze poems, then running statistics on score and literary-device differences.

## How It Works

1. Inference stage (`infer`):
- Reads poem rows from CSV.
- Runs each selected model on each poem.
- Checks prior-knowledge leakage first.
- Extracts literary devices and 5 score dimensions.
- Saves/merges results to an inference CSV.

2. Statistics stage (`stats`):
- Builds a balanced analysis dataset (only poem/model combinations that are complete).
- Runs omnibus + pairwise model comparisons by score metric.
- Runs device detection tests and posthoc pairwise tests.
- Runs interaction tests (device, diction, author features x model).
- Writes JSON and Markdown reports.

3. Artifacts:
- Each run can be tracked in a run folder with a manifest and outputs.
- Cache metadata includes source fingerprint + poem cache key to avoid duplicate work across repeats.

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Run inference:

```bash
python src/main.py infer \
	--input data/input.csv \
	--output data/inference_results.csv \
	--models qwen/qwen3.5-397b-a17b openai/gpt-oss-120b nemotron-3-super-120b-a12b
```

Run statistics:

```bash
python src/main.py stats \
	--input data/input.csv \
	--inference data/inference_results.csv \
	--analysis-csv data/analysis_dataset.csv \
	--output-json data/statistical_results.json
```

Optional sampling:

```bash
# Inference sampling
python src/main.py infer --sample-size 50 --sample-seed 42 ...

# Stats sampling
python src/main.py stats --sample-poems 50 --sample-seed 42 ...
```

## Preliminary Significant Reports
- This section contains only statistically significant findings.
- Decision rule: alpha = 0.05, using adjusted p-values when available.
- AI-vs-Non-AI claims here are only cross-model gap-difference tests (interaction tests), not within-model preference tests.
- Note that the author demographic related information within the full preliminary report is invalid.

- Significant findings: 185

### Score Model Comparisons
| Result | Evidence | Direction |
| --- | --- | --- |
| Omnibus `aggregate_score` (all models) | P=<0.001 (raw_unadjusted) | At least one model differs on this score metric. |
| Pairwise `aggregate_score`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; mean diff=+10.920. |
| Pairwise `aggregate_score`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; mean diff=+3.284. |
| Pairwise `aggregate_score`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; mean diff=-7.636. |
| Omnibus `technical_craft_score` (all models) | P=<0.001 (raw_unadjusted) | At least one model differs on this score metric. |
| Pairwise `technical_craft_score`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; mean diff=+2.054. |
| Pairwise `technical_craft_score`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=0.027 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; mean diff=+0.103. |
| Pairwise `technical_craft_score`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; mean diff=-1.950. |
| Omnibus `structure_score` (all models) | P=<0.001 (raw_unadjusted) | At least one model differs on this score metric. |
| Pairwise `structure_score`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; mean diff=+1.567. |
| Pairwise `structure_score`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; mean diff=-0.326. |
| Pairwise `structure_score`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; mean diff=-1.893. |
| Omnibus `diction_score` (all models) | P=<0.001 (raw_unadjusted) | At least one model differs on this score metric. |
| Pairwise `diction_score`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; mean diff=+2.820. |
| Pairwise `diction_score`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; mean diff=+1.337. |
| Pairwise `diction_score`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; mean diff=-1.483. |
| Omnibus `originality_score` (all models) | P=<0.001 (raw_unadjusted) | At least one model differs on this score metric. |
| Pairwise `originality_score`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; mean diff=+1.506. |
| Pairwise `originality_score`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; mean diff=+1.100. |
| Pairwise `originality_score`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; mean diff=-0.406. |
| Omnibus `impact_score` (all models) | P=<0.001 (raw_unadjusted) | At least one model differs on this score metric. |
| Pairwise `impact_score`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; mean diff=+2.973. |
| Pairwise `impact_score`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; mean diff=+1.069. |
| Pairwise `impact_score`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; mean diff=-1.904. |

### Device Detection
| Result | Evidence | Direction |
| --- | --- | --- |
| Omnibus device `metaphor` | Adj P=<0.001 (adjusted) | Highest detection: nemotron-3-super-120b-a12b (0.920); lowest: qwen/qwen3.5-397b-a17b (0.667). |
| Omnibus device `simile` | Adj P=<0.001 (adjusted) | Highest detection: qwen/qwen3.5-397b-a17b (0.337); lowest: nemotron-3-super-120b-a12b (0.215). |
| Omnibus device `personification` | Adj P=<0.001 (adjusted) | Highest detection: openai/gpt-oss-120b (0.981); lowest: qwen/qwen3.5-397b-a17b (0.923). |
| Omnibus device `symbolism` | Adj P=<0.001 (adjusted) | Highest detection: openai/gpt-oss-120b (0.831); lowest: qwen/qwen3.5-397b-a17b (0.368). |
| Omnibus device `allusion` | Adj P=<0.001 (adjusted) | Highest detection: openai/gpt-oss-120b (0.149); lowest: qwen/qwen3.5-397b-a17b (0.065). |
| Omnibus device `hyperbole` | Adj P=<0.001 (adjusted) | Highest detection: openai/gpt-oss-120b (0.192); lowest: nemotron-3-super-120b-a12b (0.046). |
| Omnibus device `understatement` | Adj P=0.012 (adjusted) | Highest detection: nemotron-3-super-120b-a12b (0.034); lowest: openai/gpt-oss-120b (0.000). |
| Omnibus device `irony` | Adj P=0.003 (adjusted) | Highest detection: openai/gpt-oss-120b (0.054); lowest: qwen/qwen3.5-397b-a17b (0.011). |
| Omnibus device `paradox` | Adj P=0.008 (adjusted) | Highest detection: nemotron-3-super-120b-a12b (0.149); lowest: qwen/qwen3.5-397b-a17b (0.069). |
| Omnibus device `alliteration` | Adj P=<0.001 (adjusted) | Highest detection: nemotron-3-super-120b-a12b (0.969); lowest: qwen/qwen3.5-397b-a17b (0.498). |
| Omnibus device `assonance` | Adj P=<0.001 (adjusted) | Highest detection: nemotron-3-super-120b-a12b (0.969); lowest: qwen/qwen3.5-397b-a17b (0.418). |
| Omnibus device `consonance` | Adj P=<0.001 (adjusted) | Highest detection: nemotron-3-super-120b-a12b (0.667); lowest: qwen/qwen3.5-397b-a17b (0.142). |
| Omnibus device `rhyme` | Adj P=<0.001 (adjusted) | Highest detection: nemotron-3-super-120b-a12b (0.686); lowest: openai/gpt-oss-120b (0.402). |
| Omnibus device `internal rhyme` | Adj P=<0.001 (adjusted) | Highest detection: nemotron-3-super-120b-a12b (0.625); lowest: qwen/qwen3.5-397b-a17b (0.023). |
| Omnibus device `euphony` | Adj P=<0.001 (adjusted) | Highest detection: nemotron-3-super-120b-a12b (0.349); lowest: openai/gpt-oss-120b (0.073). |
| Omnibus device `cacophony` | Adj P=0.030 (adjusted) | Highest detection: openai/gpt-oss-120b (0.042); lowest: qwen/qwen3.5-397b-a17b (0.015). |
| Omnibus device `repetition` | Adj P=<0.001 (adjusted) | Highest detection: openai/gpt-oss-120b (0.923); lowest: nemotron-3-super-120b-a12b (0.617). |
| Omnibus device `anaphora` | Adj P=<0.001 (adjusted) | Highest detection: nemotron-3-super-120b-a12b (0.406); lowest: qwen/qwen3.5-397b-a17b (0.234). |
| Omnibus device `parallelism` | Adj P=<0.001 (adjusted) | Highest detection: openai/gpt-oss-120b (0.881); lowest: qwen/qwen3.5-397b-a17b (0.552). |
| Omnibus device `enjambment` | Adj P=<0.001 (adjusted) | Highest detection: openai/gpt-oss-120b (0.981); lowest: qwen/qwen3.5-397b-a17b (0.215). |
| Omnibus device `caesura` | Adj P=<0.001 (adjusted) | Highest detection: openai/gpt-oss-120b (0.686); lowest: qwen/qwen3.5-397b-a17b (0.023). |
| Omnibus device `refrain` | Adj P=<0.001 (adjusted) | Highest detection: nemotron-3-super-120b-a12b (0.379); lowest: qwen/qwen3.5-397b-a17b (0.176). |
| Omnibus device `meter` | Adj P=<0.001 (adjusted) | Highest detection: nemotron-3-super-120b-a12b (0.322); lowest: openai/gpt-oss-120b (0.069). |
| Omnibus device `rhythm` | Adj P=<0.001 (adjusted) | Highest detection: nemotron-3-super-120b-a12b (0.383); lowest: openai/gpt-oss-120b (0.107). |
| Omnibus device `stanza` | Adj P=<0.001 (adjusted) | Highest detection: nemotron-3-super-120b-a12b (0.644); lowest: qwen/qwen3.5-397b-a17b (0.253). |
| Omnibus device `lineation` | Adj P=<0.001 (adjusted) | Highest detection: nemotron-3-super-120b-a12b (0.648); lowest: qwen/qwen3.5-397b-a17b (0.096). |
| Omnibus device `juxtaposition` | Adj P=<0.001 (adjusted) | Highest detection: qwen/qwen3.5-397b-a17b (0.667); lowest: openai/gpt-oss-120b (0.203). |
| Pairwise device `metaphor`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.253. |
| Pairwise device `metaphor`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.218. |
| Pairwise device `simile`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; rate diff=-0.123. |
| Pairwise device `simile`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; rate diff=-0.111. |
| Pairwise device `personification`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=0.019 (adjusted) | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; rate diff=-0.038. |
| Pairwise device `personification`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.057. |
| Pairwise device `symbolism`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=0.001 (adjusted) | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; rate diff=-0.096. |
| Pairwise device `symbolism`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.368. |
| Pairwise device `symbolism`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.464. |
| Pairwise device `allusion`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=0.034 (adjusted) | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; rate diff=-0.042. |
| Pairwise device `allusion`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=0.029 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.042. |
| Pairwise device `allusion`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.084. |
| Pairwise device `hyperbole`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; rate diff=-0.146. |
| Pairwise device `hyperbole`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; rate diff=-0.096. |
| Pairwise device `hyperbole`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=0.047 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.050. |
| Pairwise device `understatement`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=0.012 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; rate diff=+0.034. |
| Pairwise device `irony`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=0.003 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.042. |
| Pairwise device `paradox`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=0.002 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.080. |
| Pairwise device `alliteration`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; rate diff=+0.218. |
| Pairwise device `alliteration`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.471. |
| Pairwise device `alliteration`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.253. |
| Pairwise device `assonance`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; rate diff=+0.410. |
| Pairwise device `assonance`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.552. |
| Pairwise device `assonance`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.142. |
| Pairwise device `consonance`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; rate diff=+0.349. |
| Pairwise device `consonance`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.525. |
| Pairwise device `consonance`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.176. |
| Pairwise device `rhyme`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; rate diff=+0.284. |
| Pairwise device `rhyme`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.153. |
| Pairwise device `rhyme`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; rate diff=-0.130. |
| Pairwise device `internal rhyme`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; rate diff=+0.364. |
| Pairwise device `internal rhyme`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.602. |
| Pairwise device `internal rhyme`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.238. |
| Pairwise device `euphony`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; rate diff=+0.276. |
| Pairwise device `euphony`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.257. |
| Pairwise device `repetition`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; rate diff=-0.307. |
| Pairwise device `repetition`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=0.004 (adjusted) | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; rate diff=-0.088. |
| Pairwise device `repetition`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.218. |
| Pairwise device `anaphora`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.172. |
| Pairwise device `anaphora`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.157. |
| Pairwise device `parallelism`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; rate diff=-0.142. |
| Pairwise device `parallelism`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.188. |
| Pairwise device `parallelism`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.330. |
| Pairwise device `enjambment`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; rate diff=-0.115. |
| Pairwise device `enjambment`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.651. |
| Pairwise device `enjambment`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.766. |
| Pairwise device `caesura`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; rate diff=-0.356. |
| Pairwise device `caesura`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.307. |
| Pairwise device `caesura`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.663. |
| Pairwise device `refrain`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; rate diff=+0.165. |
| Pairwise device `refrain`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.203. |
| Pairwise device `meter`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; rate diff=+0.253. |
| Pairwise device `meter`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=0.011 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.088. |
| Pairwise device `meter`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; rate diff=-0.165. |
| Pairwise device `rhythm`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; rate diff=+0.276. |
| Pairwise device `rhythm`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.226. |
| Pairwise device `stanza`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; rate diff=+0.088. |
| Pairwise device `stanza`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.391. |
| Pairwise device `stanza`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.303. |
| Pairwise device `lineation`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; rate diff=+0.192. |
| Pairwise device `lineation`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.552. |
| Pairwise device `lineation`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; rate diff=+0.360. |
| Pairwise device `juxtaposition`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; rate diff=+0.460. |
| Pairwise device `juxtaposition`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; rate diff=-0.464. |

### Device x Model Score Interactions
| Result | Evidence | Direction |
| --- | --- | --- |
| `aggregate_score` / `rhyme` | Adj P=0.005 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-2.028) -> weaker or negative association. |
| `aggregate_score` / `juxtaposition` | Adj P=0.021 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (+1.319) -> stronger positive association. |
| `diction_score` / `apostrophe` | Adj P=0.007 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.539) -> weaker or negative association. |
| `diction_score` / `consonance` | Adj P=0.006 (adjusted) | Largest interaction term: openai/gpt-oss-120b (-0.558) -> weaker or negative association. |
| `diction_score` / `rhyme` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.058) -> weaker or negative association. |
| `diction_score` / `internal rhyme` | Adj P=<0.001 (adjusted) | Largest interaction term: openai/gpt-oss-120b (-0.795) -> weaker or negative association. |
| `diction_score` / `repetition` | Adj P=<0.001 (adjusted) | Largest interaction term: openai/gpt-oss-120b (-0.881) -> weaker or negative association. |
| `diction_score` / `anaphora` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.693) -> weaker or negative association. |
| `diction_score` / `parallelism` | Adj P=0.033 (adjusted) | Largest interaction term: openai/gpt-oss-120b (-0.575) -> weaker or negative association. |
| `diction_score` / `caesura` | Adj P=0.037 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.399) -> stronger positive association. |
| `diction_score` / `refrain` | Adj P=0.008 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.570) -> weaker or negative association. |
| `diction_score` / `meter` | Adj P=0.026 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.513) -> weaker or negative association. |
| `diction_score` / `stanza` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.685) -> weaker or negative association. |
| `diction_score` / `lineation` | Adj P=<0.001 (adjusted) | Largest interaction term: openai/gpt-oss-120b (-0.600) -> weaker or negative association. |
| `diction_score` / `juxtaposition` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.533) -> stronger positive association. |
| `originality_score` / `simile` | Adj P=0.008 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.416) -> stronger positive association. |
| `originality_score` / `irony` | Adj P=0.008 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.831) -> weaker or negative association. |
| `originality_score` / `alliteration` | Adj P=0.008 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.493) -> weaker or negative association. |
| `originality_score` / `rhyme` | Adj P=0.007 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.536) -> weaker or negative association. |
| `originality_score` / `internal rhyme` | Adj P=0.033 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.196) -> weaker or negative association. |
| `impact_score` / `metaphor` | Adj P=0.026 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.680) -> weaker or negative association. |
| `impact_score` / `apostrophe` | Adj P=0.033 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.357) -> weaker or negative association. |
| `impact_score` / `alliteration` | Adj P=0.007 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.542) -> weaker or negative association. |
| `impact_score` / `assonance` | Adj P=0.010 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.382) -> weaker or negative association. |
| `impact_score` / `rhyme` | Adj P=0.013 (adjusted) | Largest interaction term: openai/gpt-oss-120b (+0.278) -> stronger positive association. |
| `impact_score` / `euphony` | Adj P=0.007 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.730) -> weaker or negative association. |
| `impact_score` / `refrain` | Adj P=0.032 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.468) -> weaker or negative association. |
| `impact_score` / `juxtaposition` | Adj P=0.011 (adjusted) | Largest interaction term: openai/gpt-oss-120b (-0.443) -> weaker or negative association. |

### Diction x Model Score Interactions
| Result | Evidence | Direction |
| --- | --- | --- |
| `aggregate_score` / `latinate_ratio` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-4.829) -> weaker or negative association. |
| `structure_score` / `latinate_ratio` | Adj P=0.040 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.510) -> weaker or negative association. |
| `diction_score` / `avg_word_length` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.991) -> stronger positive association. |
| `diction_score` / `latinate_ratio` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.345) -> weaker or negative association. |
| `diction_score` / `type_token_ratio` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (+2.656) -> stronger positive association. |
| `originality_score` / `avg_word_length` | Adj P=0.038 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.576) -> stronger positive association. |
| `originality_score` / `latinate_ratio` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.377) -> weaker or negative association. |
| `originality_score` / `type_token_ratio` | Adj P=0.038 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (+1.427) -> stronger positive association. |
| `impact_score` / `latinate_ratio` | Adj P=0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.956) -> weaker or negative association. |

### AI-vs-Non-AI Gap-Difference Interactions
| Result | Evidence | Direction |
| --- | --- | --- |
| Omnibus `aggregate_score` (model x origin) | P=<0.001 (raw_unadjusted) | Models differ in AI-minus-Non-AI gap size. |
| Pairwise `aggregate_score`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; gap diff=-3.545. |
| Pairwise `aggregate_score`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; gap diff=-3.138. |
| Omnibus `technical_craft_score` (model x origin) | P=<0.001 (raw_unadjusted) | Models differ in AI-minus-Non-AI gap size. |
| Pairwise `technical_craft_score`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=0.022 (adjusted) | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; gap diff=-0.258. |
| Pairwise `technical_craft_score`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; gap diff=-0.528. |
| Pairwise `technical_craft_score`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=0.043 (adjusted) | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; gap diff=-0.270. |
| Omnibus `diction_score` (model x origin) | P=<0.001 (raw_unadjusted) | Models differ in AI-minus-Non-AI gap size. |
| Pairwise `diction_score`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; gap diff=-0.497. |
| Pairwise `diction_score`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; gap diff=-1.496. |
| Pairwise `diction_score`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; gap diff=-0.998. |
| Omnibus `originality_score` (model x origin) | P=<0.001 (raw_unadjusted) | Models differ in AI-minus-Non-AI gap size. |
| Pairwise `originality_score`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; gap diff=-0.919. |
| Pairwise `originality_score`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; gap diff=-0.820. |
| Omnibus `impact_score` (model x origin) | P=<0.001 (raw_unadjusted) | Models differ in AI-minus-Non-AI gap size. |
| Pairwise `impact_score`: nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | Adj P=0.038 (adjusted) | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; gap diff=+0.237. |
| Pairwise `impact_score`: nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; gap diff=-0.658. |
| Pairwise `impact_score`: openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | Adj P=<0.001 (adjusted) | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; gap diff=-0.895. |
