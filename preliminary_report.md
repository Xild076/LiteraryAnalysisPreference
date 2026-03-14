# Literary Analysis Report

## Dataset Snapshot
- Input CSV: `/Users/harry/Documents/Python_Projects/LiteraryAnalysis/data/input_280.csv`
- Inference CSV: `/Users/harry/Documents/Python_Projects/LiteraryAnalysis/data/inference_results_280.csv`
- Analysis CSV: `/Users/harry/Documents/Python_Projects/LiteraryAnalysis/data/analysis_dataset_280.csv`
- Output JSON: `/Users/harry/Documents/Python_Projects/LiteraryAnalysis/data/statistical_results_280.json`
- Output Markdown: `/Users/harry/Documents/Python_Projects/LiteraryAnalysis/data/statistical_results_280.md`
- Poems analyzed: 261
- Model rows: 783
- Models: nemotron-3-super-120b-a12b, openai/gpt-oss-120b, qwen/qwen3.5-397b-a17b

## Statistical Decision Rule
- Alpha: 0.05
- Classification rule: significant / non-significant only.
- Significance uses adjusted p-values when available; raw p-values are explicitly marked as unadjusted.

## Significant Results Only
- This section contains only statistically significant findings.
- Decision rule: alpha = 0.05, using adjusted p-values when available.
- AI-vs-Non-AI claims here are only cross-model gap-difference tests (interaction tests), not within-model preference tests.

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

### Author x Model Score Interactions
| Result | Evidence | Direction |
| --- | --- | --- |
| `aggregate_score` / `author_gender` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-3.545) -> weaker or negative association. |
| `aggregate_score` / `author_ethnicity` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-3.545) -> weaker or negative association. |
| `aggregate_score` / `author_nationality` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-3.545) -> weaker or negative association. |
| `technical_craft_score` / `author_gender` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.528) -> weaker or negative association. |
| `technical_craft_score` / `author_ethnicity` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.528) -> weaker or negative association. |
| `technical_craft_score` / `author_nationality` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.528) -> weaker or negative association. |
| `diction_score` / `author_gender` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.496) -> weaker or negative association. |
| `diction_score` / `author_ethnicity` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.496) -> weaker or negative association. |
| `diction_score` / `author_nationality` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.496) -> weaker or negative association. |
| `originality_score` / `author_gender` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.919) -> weaker or negative association. |
| `originality_score` / `author_ethnicity` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.919) -> weaker or negative association. |
| `originality_score` / `author_nationality` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.919) -> weaker or negative association. |
| `impact_score` / `author_gender` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.658) -> weaker or negative association. |
| `impact_score` / `author_ethnicity` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.658) -> weaker or negative association. |
| `impact_score` / `author_nationality` | Adj P=<0.001 (adjusted) | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.658) -> weaker or negative association. |

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

## Score Summaries By Metric
- Alpha: 0.05

### Aggregate Score (`aggregate_score`)
| Model | Mean | Median | Std Dev | Min | Max | N |
| --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b | 37.441 | 36.000 | 3.392 | 26.000 | 43.000 | 261 |
| qwen/qwen3.5-397b-a17b | 34.157 | 35.000 | 5.473 | 22.000 | 43.000 | 261 |
| openai/gpt-oss-120b | 26.521 | 26.000 | 3.876 | 18.000 | 38.000 | 261 |

### Technical Craft Score (`technical_craft_score`)
| Model | Mean | Median | Std Dev | Min | Max | N |
| --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b | 7.398 | 7.000 | 0.584 | 6.000 | 8.000 | 261 |
| qwen/qwen3.5-397b-a17b | 7.295 | 7.000 | 0.993 | 5.000 | 9.000 | 261 |
| openai/gpt-oss-120b | 5.345 | 5.000 | 0.901 | 3.000 | 8.000 | 261 |

### Structure Score (`structure_score`)
| Model | Mean | Median | Std Dev | Min | Max | N |
| --- | --- | --- | --- | --- | --- | --- |
| qwen/qwen3.5-397b-a17b | 7.176 | 7.000 | 0.749 | 5.000 | 9.000 | 261 |
| nemotron-3-super-120b-a12b | 6.851 | 7.000 | 0.677 | 5.000 | 8.000 | 261 |
| openai/gpt-oss-120b | 5.284 | 5.000 | 0.767 | 3.000 | 8.000 | 261 |

### Diction Score (`diction_score`)
| Model | Mean | Median | Std Dev | Min | Max | N |
| --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b | 8.314 | 8.000 | 0.719 | 5.000 | 9.000 | 261 |
| qwen/qwen3.5-397b-a17b | 6.977 | 7.000 | 1.462 | 4.000 | 9.000 | 261 |
| openai/gpt-oss-120b | 5.494 | 5.000 | 1.066 | 4.000 | 8.000 | 261 |

### Originality Score (`originality_score`)
| Model | Mean | Median | Std Dev | Min | Max | N |
| --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b | 6.900 | 7.000 | 1.115 | 4.000 | 9.000 | 261 |
| qwen/qwen3.5-397b-a17b | 5.801 | 6.000 | 1.483 | 3.000 | 9.000 | 261 |
| openai/gpt-oss-120b | 5.395 | 6.000 | 1.256 | 3.000 | 8.000 | 261 |

### Impact Score (`impact_score`)
| Model | Mean | Median | Std Dev | Min | Max | N |
| --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b | 7.977 | 8.000 | 0.940 | 5.000 | 10.000 | 261 |
| qwen/qwen3.5-397b-a17b | 6.908 | 7.000 | 1.301 | 4.000 | 9.000 | 261 |
| openai/gpt-oss-120b | 5.004 | 5.000 | 0.839 | 3.000 | 8.000 | 261 |

## Model Comparisons By Score Metric
- Alpha: 0.05
- Pairwise p-value adjustment: benjamini_hochberg

### Aggregate Score (`aggregate_score`)
- Method: `mixedlm`
- Omnibus p-value: <0.001
- Omnibus significance: significant at alpha=0.05 (raw_unadjusted)
- Balanced poems: 261
- Balanced rows: 783

#### Pairwise Model Differences
| Pair | Status | N pairs | Mean diff (left-right) | Median diff | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +10.920 | +11.000 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +3.284 | +3.000 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -7.636 | -8.000 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

#### Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; mean paired difference = +10.920.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; mean paired difference = +3.284.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; mean paired difference = -7.636.

### Technical Craft Score (`technical_craft_score`)
- Method: `mixedlm`
- Omnibus p-value: <0.001
- Omnibus significance: significant at alpha=0.05 (raw_unadjusted)
- Balanced poems: 261
- Balanced rows: 783

#### Pairwise Model Differences
| Pair | Status | N pairs | Mean diff (left-right) | Median diff | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +2.054 | +2.000 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.103 | +0.000 | 0.027 | 0.027 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -1.950 | -2.000 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

#### Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; mean paired difference = +2.054.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; mean paired difference = +0.103.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; mean paired difference = -1.950.

### Structure Score (`structure_score`)
- Method: `mixedlm`
- Omnibus p-value: <0.001
- Omnibus significance: significant at alpha=0.05 (raw_unadjusted)
- Balanced poems: 261
- Balanced rows: 783

#### Pairwise Model Differences
| Pair | Status | N pairs | Mean diff (left-right) | Median diff | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +1.567 | +2.000 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.326 | +0.000 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -1.893 | -2.000 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

#### Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; mean paired difference = +1.567.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; mean paired difference = -0.326.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; mean paired difference = -1.893.

### Diction Score (`diction_score`)
- Method: `mixedlm`
- Omnibus p-value: <0.001
- Omnibus significance: significant at alpha=0.05 (raw_unadjusted)
- Balanced poems: 261
- Balanced rows: 783

#### Pairwise Model Differences
| Pair | Status | N pairs | Mean diff (left-right) | Median diff | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +2.820 | +3.000 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +1.337 | +1.000 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -1.483 | -2.000 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

#### Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; mean paired difference = +2.820.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; mean paired difference = +1.337.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; mean paired difference = -1.483.

### Originality Score (`originality_score`)
- Method: `mixedlm`
- Omnibus p-value: <0.001
- Omnibus significance: significant at alpha=0.05 (raw_unadjusted)
- Balanced poems: 261
- Balanced rows: 783

#### Pairwise Model Differences
| Pair | Status | N pairs | Mean diff (left-right) | Median diff | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +1.506 | +1.000 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +1.100 | +1.000 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.406 | +0.000 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

#### Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; mean paired difference = +1.506.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; mean paired difference = +1.100.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; mean paired difference = -0.406.

### Impact Score (`impact_score`)
- Method: `mixedlm`
- Omnibus p-value: <0.001
- Omnibus significance: significant at alpha=0.05 (raw_unadjusted)
- Balanced poems: 261
- Balanced rows: 783

#### Pairwise Model Differences
| Pair | Status | N pairs | Mean diff (left-right) | Median diff | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +2.973 | +3.000 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +1.069 | +1.000 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -1.904 | -2.000 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

#### Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; mean paired difference = +2.973.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; mean paired difference = +1.069.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; mean paired difference = -1.904.

## Device Detection Tests
- Alpha: 0.05
- Device-level p-value adjustment: benjamini_hochberg
- Posthoc p-value adjustment: benjamini_hochberg

### Omnibus Device Tests
| Device | Status | N poems | P | Adj P | Significant | Basis | Rates by model | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metaphor | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.920, openai/gpt-oss-120b: 0.885, qwen/qwen3.5-397b-a17b: 0.667 |  |
| simile | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.215, openai/gpt-oss-120b: 0.226, qwen/qwen3.5-397b-a17b: 0.337 |  |
| personification | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.943, openai/gpt-oss-120b: 0.981, qwen/qwen3.5-397b-a17b: 0.923 |  |
| symbolism | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.736, openai/gpt-oss-120b: 0.831, qwen/qwen3.5-397b-a17b: 0.368 |  |
| imagery | ok | 261 | 0.368 | 0.390 | no | adjusted | nemotron-3-super-120b-a12b: 1.000, openai/gpt-oss-120b: 0.996, qwen/qwen3.5-397b-a17b: 1.000 |  |
| allusion | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.107, openai/gpt-oss-120b: 0.149, qwen/qwen3.5-397b-a17b: 0.065 |  |
| apostrophe | ok | 261 | 0.918 | 0.918 | no | adjusted | nemotron-3-super-120b-a12b: 0.257, openai/gpt-oss-120b: 0.261, qwen/qwen3.5-397b-a17b: 0.264 |  |
| hyperbole | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.046, openai/gpt-oss-120b: 0.192, qwen/qwen3.5-397b-a17b: 0.142 |  |
| understatement | ok | 261 | 0.009 | 0.012 | yes | adjusted | nemotron-3-super-120b-a12b: 0.034, openai/gpt-oss-120b: 0.000, qwen/qwen3.5-397b-a17b: 0.015 |  |
| irony | ok | 261 | 0.002 | 0.003 | yes | adjusted | nemotron-3-super-120b-a12b: 0.023, openai/gpt-oss-120b: 0.054, qwen/qwen3.5-397b-a17b: 0.011 |  |
| paradox | ok | 261 | 0.006 | 0.008 | yes | adjusted | nemotron-3-super-120b-a12b: 0.149, openai/gpt-oss-120b: 0.100, qwen/qwen3.5-397b-a17b: 0.069 |  |
| oxymoron | ok | 261 | 0.108 | 0.135 | no | adjusted | nemotron-3-super-120b-a12b: 0.038, openai/gpt-oss-120b: 0.038, qwen/qwen3.5-397b-a17b: 0.011 |  |
| metonymy | ok | 261 | 0.247 | 0.270 | no | adjusted | nemotron-3-super-120b-a12b: 0.008, openai/gpt-oss-120b: 0.011, qwen/qwen3.5-397b-a17b: 0.000 |  |
| synecdoche | ok | 261 | 0.135 | 0.158 | no | adjusted | nemotron-3-super-120b-a12b: 0.008, openai/gpt-oss-120b: 0.015, qwen/qwen3.5-397b-a17b: 0.000 |  |
| allegory | ok | 261 | 0.607 | 0.624 | no | adjusted | nemotron-3-super-120b-a12b: 0.004, openai/gpt-oss-120b: 0.004, qwen/qwen3.5-397b-a17b: 0.000 |  |
| alliteration | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.969, openai/gpt-oss-120b: 0.751, qwen/qwen3.5-397b-a17b: 0.498 |  |
| assonance | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.969, openai/gpt-oss-120b: 0.559, qwen/qwen3.5-397b-a17b: 0.418 |  |
| consonance | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.667, openai/gpt-oss-120b: 0.318, qwen/qwen3.5-397b-a17b: 0.142 |  |
| rhyme | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.686, openai/gpt-oss-120b: 0.402, qwen/qwen3.5-397b-a17b: 0.533 |  |
| internal rhyme | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.625, openai/gpt-oss-120b: 0.261, qwen/qwen3.5-397b-a17b: 0.023 |  |
| onomatopoeia | ok | 261 | 0.125 | 0.151 | no | adjusted | nemotron-3-super-120b-a12b: 0.084, openai/gpt-oss-120b: 0.054, qwen/qwen3.5-397b-a17b: 0.061 |  |
| euphony | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.349, openai/gpt-oss-120b: 0.073, qwen/qwen3.5-397b-a17b: 0.092 |  |
| cacophony | ok | 261 | 0.023 | 0.030 | yes | adjusted | nemotron-3-super-120b-a12b: 0.015, openai/gpt-oss-120b: 0.042, qwen/qwen3.5-397b-a17b: 0.015 |  |
| repetition | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.617, openai/gpt-oss-120b: 0.923, qwen/qwen3.5-397b-a17b: 0.705 |  |
| anaphora | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.406, openai/gpt-oss-120b: 0.391, qwen/qwen3.5-397b-a17b: 0.234 |  |
| epistrophe | ok | 261 | 0.205 | 0.232 | no | adjusted | nemotron-3-super-120b-a12b: 0.027, openai/gpt-oss-120b: 0.015, qwen/qwen3.5-397b-a17b: 0.034 |  |
| parallelism | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.739, openai/gpt-oss-120b: 0.881, qwen/qwen3.5-397b-a17b: 0.552 |  |
| enjambment | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.866, openai/gpt-oss-120b: 0.981, qwen/qwen3.5-397b-a17b: 0.215 |  |
| caesura | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.330, openai/gpt-oss-120b: 0.686, qwen/qwen3.5-397b-a17b: 0.023 |  |
| refrain | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.379, openai/gpt-oss-120b: 0.215, qwen/qwen3.5-397b-a17b: 0.176 |  |
| meter | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.322, openai/gpt-oss-120b: 0.069, qwen/qwen3.5-397b-a17b: 0.234 |  |
| rhythm | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.383, openai/gpt-oss-120b: 0.107, qwen/qwen3.5-397b-a17b: 0.157 |  |
| stanza | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.644, openai/gpt-oss-120b: 0.556, qwen/qwen3.5-397b-a17b: 0.253 |  |
| lineation | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.648, openai/gpt-oss-120b: 0.456, qwen/qwen3.5-397b-a17b: 0.096 |  |
| juxtaposition | ok | 261 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b: 0.663, openai/gpt-oss-120b: 0.203, qwen/qwen3.5-397b-a17b: 0.667 |  |

### Device Posthoc Pairwise Results
#### allegory
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.000 | 1.000 | 1.000 | no | adjusted | no directional difference |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.004 | 1.000 | 1.000 | no | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.004 | 1.000 | 1.000 | no | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: no directional difference; detection-rate difference = +0.000.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.004.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.004.

#### alliteration
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.218 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.471 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.253 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.218.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.471.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.253.

#### allusion
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.042 | 0.034 | 0.034 | yes | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.042 | 0.019 | 0.029 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.084 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; detection-rate difference = -0.042.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.042.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.084.

#### anaphora
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.015 | 0.606 | 0.606 | no | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.172 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.157 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.015.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.172.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.157.

#### apostrophe
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.004 | 0.847 | 1.000 | no | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.008 | 0.839 | 1.000 | no | adjusted | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.004 | 1.000 | 1.000 | no | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; detection-rate difference = -0.004.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.008.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.004.

#### assonance
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.410 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.552 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.142 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.410.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.552.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.142.

#### cacophony
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.027 | 0.065 | 0.098 | no | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.000 | 1.000 | 1.000 | no | adjusted | no directional difference |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.027 | 0.039 | 0.098 | no | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; detection-rate difference = -0.027.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: no directional difference; detection-rate difference = +0.000.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.027.

#### caesura
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.356 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.307 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.663 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; detection-rate difference = -0.356.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.307.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.663.

#### consonance
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.349 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.525 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.176 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.349.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.525.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.176.

#### enjambment
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.115 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.651 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.766 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; detection-rate difference = -0.115.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.651.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.766.

#### epistrophe
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.011 | 0.453 | 0.680 | no | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.008 | 0.727 | 0.727 | no | adjusted | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.019 | 0.180 | 0.539 | no | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.011.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.008.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.019.

#### euphony
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.276 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.257 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.019 | 0.369 | 0.369 | no | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.276.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.257.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.019.

#### hyperbole
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.146 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.096 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.050 | 0.047 | 0.047 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; detection-rate difference = -0.146.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.096.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.050.

#### imagery
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.004 | 1.000 | 1.000 | no | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | skipped | 261 | +0.000 | N/A | N/A | no | none | no directional difference | no_discordant_pairs |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.004 | 1.000 | 1.000 | no | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.004.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.004.

#### internal rhyme
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.364 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.602 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.238 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.364.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.602.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.238.

#### irony
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.031 | 0.077 | 0.115 | no | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.011 | 0.375 | 0.375 | no | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.042 | <0.001 | 0.003 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; detection-rate difference = -0.031.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.011.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.042.

#### juxtaposition
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.460 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.004 | 0.909 | 0.909 | no | adjusted | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.464 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.460.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.004.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.464.

#### lineation
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.192 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.552 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.360 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.192.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.552.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.360.

#### metaphor
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.034 | 0.128 | 0.128 | no | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.253 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.218 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.034.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.253.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.218.

#### meter
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.253 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.088 | 0.011 | 0.011 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.165 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.253.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.088.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.165.

#### metonymy
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.004 | 1.000 | 1.000 | no | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.008 | 0.500 | 0.750 | no | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.011 | 0.250 | 0.750 | no | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; detection-rate difference = -0.004.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.008.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.011.

#### onomatopoeia
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.031 | 0.134 | 0.269 | no | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.023 | 0.180 | 0.269 | no | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.008 | 0.791 | 0.791 | no | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.031.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.023.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.008.

#### oxymoron
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.000 | 1.000 | 1.000 | no | adjusted | no directional difference |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.027 | 0.092 | 0.138 | no | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.027 | 0.092 | 0.138 | no | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: no directional difference; detection-rate difference = +0.000.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.027.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.027.

#### paradox
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.050 | 0.074 | 0.111 | no | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.080 | <0.001 | 0.002 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.031 | 0.194 | 0.194 | no | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.050.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.080.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.031.

#### parallelism
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.142 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.188 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.330 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; detection-rate difference = -0.142.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.188.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.330.

#### personification
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.038 | 0.013 | 0.019 | yes | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.019 | 0.267 | 0.267 | no | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.057 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; detection-rate difference = -0.038.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.019.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.057.

#### refrain
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.165 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.203 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.038 | 0.052 | 0.052 | no | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.165.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.203.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.038.

#### repetition
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.307 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.088 | 0.004 | 0.004 | yes | adjusted | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.218 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; detection-rate difference = -0.307.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.088.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.218.

#### rhyme
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.284 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.153 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.130 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.284.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.153.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.130.

#### rhythm
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.276 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.226 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.050 | 0.074 | 0.074 | no | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.276.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.226.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.050.

#### simile
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.011 | 0.564 | 0.564 | no | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.123 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.111 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; detection-rate difference = -0.011.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.123.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.111.

#### stanza
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.088 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.391 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.303 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.088.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.391.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.303.

#### symbolism
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.096 | 0.001 | 0.001 | yes | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.368 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.464 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; detection-rate difference = -0.096.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.368.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.464.

#### synecdoche
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.008 | 0.688 | 0.688 | no | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.008 | 0.500 | 0.688 | no | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.015 | 0.125 | 0.375 | no | adjusted | openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; detection-rate difference = -0.008.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.008.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.015.

#### understatement
| Pair | Status | N pairs | Rate diff (left-right) | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.034 | 0.004 | 0.012 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.019 | 0.267 | 0.267 | no | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.015 | 0.125 | 0.188 | no | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; detection-rate difference = +0.034.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; detection-rate difference = +0.019.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; detection-rate difference = -0.015.

## Device x Model Score Interactions By Metric
- Alpha: 0.05
- P-value adjustment: benjamini_hochberg

### Aggregate Score (`aggregate_score`)
| Device | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metaphor | ok | 261 | 0.036 | 0.089 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-2.198) -> weaker or negative association. |  |
| simile | ok | 261 | 0.016 | 0.067 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+1.237) -> stronger positive association. |  |
| personification | ok | 261 | 0.310 | 0.503 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+1.526) -> stronger positive association. |  |
| symbolism | ok | 261 | 0.325 | 0.503 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.830) -> weaker or negative association. |  |
| imagery | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| allusion | ok | 261 | 0.423 | 0.552 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-1.018) -> weaker or negative association. |  |
| apostrophe | ok | 261 | 0.045 | 0.105 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.419) -> weaker or negative association. |  |
| hyperbole | ok | 261 | 0.224 | 0.421 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.709) -> weaker or negative association. |  |
| understatement | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| irony | ok | 261 | 0.018 | 0.067 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-4.877) -> weaker or negative association. |  |
| paradox | ok | 261 | 0.335 | 0.503 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+1.175) -> stronger positive association. |  |
| oxymoron | ok | 261 | 0.035 | 0.089 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-5.278) -> weaker or negative association. |  |
| metonymy | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| synecdoche | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| allegory | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| alliteration | ok | 261 | 0.012 | 0.067 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.416) -> weaker or negative association. |  |
| assonance | ok | 261 | 0.091 | 0.181 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.684) -> weaker or negative association. |  |
| consonance | ok | 261 | 0.626 | 0.696 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.539) -> weaker or negative association. |  |
| rhyme | ok | 261 | <0.001 | 0.005 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-2.028) -> weaker or negative association. |  |
| internal rhyme | ok | 261 | 0.015 | 0.067 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-2.738) -> weaker or negative association. |  |
| onomatopoeia | ok | 261 | 0.027 | 0.080 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.996) -> weaker or negative association. |  |
| euphony | ok | 261 | 0.011 | 0.067 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-2.203) -> weaker or negative association. |  |
| cacophony | ok | 261 | 0.675 | 0.707 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-1.619) -> weaker or negative association. |  |
| repetition | ok | 261 | 0.073 | 0.156 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.256) -> weaker or negative association. |  |
| anaphora | ok | 261 | 0.022 | 0.073 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.583) -> weaker or negative association. |  |
| epistrophe | ok | 261 | 0.549 | 0.686 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+1.260) -> stronger positive association. |  |
| parallelism | ok | 261 | 0.818 | 0.818 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.446) -> weaker or negative association. |  |
| enjambment | ok | 261 | 0.683 | 0.707 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.527) -> weaker or negative association. |  |
| caesura | ok | 261 | 0.391 | 0.542 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+1.408) -> stronger positive association. |  |
| refrain | ok | 261 | 0.016 | 0.067 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.731) -> weaker or negative association. |  |
| meter | ok | 261 | 0.626 | 0.696 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.843) -> weaker or negative association. |  |
| rhythm | ok | 261 | 0.623 | 0.696 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.519) -> weaker or negative association. |  |
| stanza | ok | 261 | 0.397 | 0.542 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.816) -> weaker or negative association. |  |
| lineation | ok | 261 | 0.275 | 0.485 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.663) -> weaker or negative association. |  |
| juxtaposition | ok | 261 | 0.001 | 0.021 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+1.319) -> stronger positive association. |  |

Direction Narrative
- metaphor: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_metaphor` = -2.198 -> weaker or negative association
- metaphor: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_metaphor` = -1.915 -> weaker or negative association
- simile: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_simile` = +1.237 -> stronger positive association
- simile: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_simile` = -0.265 -> weaker or negative association
- personification: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_personification` = +1.526 -> stronger positive association
- personification: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_personification` = +0.304 -> stronger positive association
- symbolism: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_symbolism` = -0.830 -> weaker or negative association
- symbolism: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_symbolism` = -0.774 -> weaker or negative association
- allusion: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_allusion` = -1.018 -> weaker or negative association
- allusion: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_allusion` = -0.439 -> weaker or negative association
- apostrophe: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_apostrophe` = -1.419 -> weaker or negative association
- apostrophe: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_apostrophe` = -0.780 -> weaker or negative association
- hyperbole: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_hyperbole` = -1.709 -> weaker or negative association
- hyperbole: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_hyperbole` = -0.925 -> weaker or negative association
- irony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_irony` = -4.877 -> weaker or negative association
- irony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_irony` = +0.671 -> stronger positive association
- paradox: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_paradox` = +1.175 -> stronger positive association
- paradox: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_paradox` = -0.239 -> weaker or negative association
- oxymoron: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_oxymoron` = -5.278 -> weaker or negative association
- oxymoron: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_oxymoron` = -2.257 -> weaker or negative association
- alliteration: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_alliteration` = -1.416 -> weaker or negative association
- alliteration: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_alliteration` = +0.201 -> stronger positive association
- assonance: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_assonance` = -0.684 -> weaker or negative association
- assonance: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_assonance` = +0.493 -> stronger positive association
- consonance: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_consonance` = -0.539 -> weaker or negative association
- consonance: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_consonance` = -0.137 -> weaker or negative association
- rhyme: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_rhyme` = -2.028 -> weaker or negative association
- rhyme: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_rhyme` = -0.193 -> weaker or negative association
- internal rhyme: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_internal_rhyme` = -2.738 -> weaker or negative association
- internal rhyme: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_internal_rhyme` = -1.425 -> weaker or negative association
- onomatopoeia: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_onomatopoeia` = -1.996 -> weaker or negative association
- onomatopoeia: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_onomatopoeia` = +0.843 -> stronger positive association
- euphony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_euphony` = -2.203 -> weaker or negative association
- euphony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_euphony` = +0.176 -> stronger positive association
- cacophony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_cacophony` = -1.619 -> weaker or negative association
- cacophony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_cacophony` = -1.211 -> weaker or negative association
- repetition: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_repetition` = -1.256 -> weaker or negative association
- repetition: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_repetition` = -0.981 -> weaker or negative association
- anaphora: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_anaphora` = -1.583 -> weaker or negative association
- anaphora: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_anaphora` = -0.473 -> weaker or negative association
- epistrophe: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_epistrophe` = +1.260 -> stronger positive association
- epistrophe: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_epistrophe` = -0.552 -> weaker or negative association
- parallelism: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_parallelism` = -0.446 -> weaker or negative association
- parallelism: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_parallelism` = -0.090 -> weaker or negative association
- enjambment: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_enjambment` = -0.527 -> weaker or negative association
- enjambment: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_enjambment` = +0.461 -> stronger positive association
- caesura: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_caesura` = +1.408 -> stronger positive association
- caesura: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_caesura` = -0.418 -> weaker or negative association
- refrain: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_refrain` = -1.731 -> weaker or negative association
- refrain: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_refrain` = -0.425 -> weaker or negative association
- meter: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_meter` = -0.843 -> weaker or negative association
- meter: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_meter` = -0.252 -> weaker or negative association
- rhythm: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_rhythm` = -0.519 -> weaker or negative association
- rhythm: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_rhythm` = +0.287 -> stronger positive association
- stanza: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_stanza` = -0.816 -> weaker or negative association
- stanza: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_stanza` = -0.295 -> weaker or negative association
- lineation: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_lineation` = -0.663 -> weaker or negative association
- lineation: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_lineation` = +0.379 -> stronger positive association
- juxtaposition: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_juxtaposition` = +1.319 -> stronger positive association
- juxtaposition: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_juxtaposition` = -0.904 -> weaker or negative association

### Technical Craft Score (`technical_craft_score`)
| Device | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metaphor | ok | 261 | 0.076 | 0.189 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.446) -> weaker or negative association. |  |
| simile | ok | 261 | 0.208 | 0.346 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.151) -> stronger positive association. |  |
| personification | ok | 261 | 0.956 | 0.956 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.096) -> weaker or negative association. |  |
| symbolism | ok | 261 | 0.045 | 0.143 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.359) -> weaker or negative association. |  |
| imagery | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| allusion | ok | 261 | 0.013 | 0.143 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.453) -> weaker or negative association. |  |
| apostrophe | ok | 261 | 0.087 | 0.189 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.276) -> weaker or negative association. |  |
| hyperbole | ok | 261 | 0.303 | 0.396 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.347) -> weaker or negative association. |  |
| understatement | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| irony | ok | 261 | 0.061 | 0.165 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.058) -> weaker or negative association. |  |
| paradox | ok | 261 | 0.275 | 0.392 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.220) -> weaker or negative association. |  |
| oxymoron | ok | 261 | 0.035 | 0.143 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.827) -> weaker or negative association. |  |
| metonymy | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| synecdoche | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| allegory | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| alliteration | ok | 261 | 0.254 | 0.385 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.295) -> weaker or negative association. |  |
| assonance | ok | 261 | 0.539 | 0.622 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.137) -> weaker or negative association. |  |
| consonance | ok | 261 | 0.303 | 0.396 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.164) -> weaker or negative association. |  |
| rhyme | ok | 261 | 0.024 | 0.143 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.295) -> weaker or negative association. |  |
| internal rhyme | ok | 261 | 0.038 | 0.143 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.323) -> weaker or negative association. |  |
| onomatopoeia | ok | 261 | 0.094 | 0.189 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.408) -> weaker or negative association. |  |
| euphony | ok | 261 | 0.088 | 0.189 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.368) -> weaker or negative association. |  |
| cacophony | ok | 261 | 0.032 | 0.143 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.942) -> weaker or negative association. |  |
| repetition | ok | 261 | 0.187 | 0.329 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.220) -> weaker or negative association. |  |
| anaphora | ok | 261 | 0.121 | 0.227 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.260) -> weaker or negative association. |  |
| epistrophe | ok | 261 | 0.726 | 0.806 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.310) -> weaker or negative association. |  |
| parallelism | ok | 261 | 0.884 | 0.947 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.049) -> stronger positive association. |  |
| enjambment | ok | 261 | 0.937 | 0.956 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.058) -> stronger positive association. |  |
| caesura | ok | 261 | 0.015 | 0.143 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.513) -> stronger positive association. |  |
| refrain | ok | 261 | 0.048 | 0.143 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.308) -> weaker or negative association. |  |
| meter | ok | 261 | 0.368 | 0.460 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.181) -> weaker or negative association. |  |
| rhythm | ok | 261 | 0.257 | 0.385 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.165) -> stronger positive association. |  |
| stanza | ok | 261 | 0.538 | 0.622 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.106) -> weaker or negative association. |  |
| lineation | ok | 261 | 0.023 | 0.143 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.319) -> stronger positive association. |  |
| juxtaposition | ok | 261 | 0.003 | 0.078 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.371) -> weaker or negative association. |  |

Direction Narrative
- metaphor: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_metaphor` = -0.446 -> weaker or negative association
- metaphor: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_metaphor` = -0.322 -> weaker or negative association
- simile: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_simile` = +0.151 -> stronger positive association
- simile: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_simile` = -0.061 -> weaker or negative association
- personification: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_personification` = -0.096 -> weaker or negative association
- personification: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_personification` = -0.048 -> weaker or negative association
- symbolism: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_symbolism` = -0.359 -> weaker or negative association
- symbolism: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_symbolism` = -0.147 -> weaker or negative association
- allusion: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_allusion` = -0.453 -> weaker or negative association
- allusion: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_allusion` = -0.027 -> weaker or negative association
- apostrophe: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_apostrophe` = -0.276 -> weaker or negative association
- apostrophe: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_apostrophe` = -0.167 -> weaker or negative association
- hyperbole: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_hyperbole` = -0.347 -> weaker or negative association
- hyperbole: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_hyperbole` = -0.259 -> weaker or negative association
- irony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_irony` = -1.058 -> weaker or negative association
- irony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_irony` = -0.162 -> weaker or negative association
- paradox: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_paradox` = -0.220 -> weaker or negative association
- paradox: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_paradox` = +0.122 -> stronger positive association
- oxymoron: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_oxymoron` = -0.827 -> weaker or negative association
- oxymoron: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_oxymoron` = -0.740 -> weaker or negative association
- alliteration: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_alliteration` = -0.295 -> weaker or negative association
- alliteration: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_alliteration` = -0.124 -> weaker or negative association
- assonance: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_assonance` = -0.137 -> weaker or negative association
- assonance: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_assonance` = -0.012 -> weaker or negative association
- consonance: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_consonance` = -0.164 -> weaker or negative association
- consonance: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_consonance` = +0.024 -> stronger positive association
- rhyme: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_rhyme` = -0.295 -> weaker or negative association
- rhyme: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_rhyme` = -0.041 -> weaker or negative association
- internal rhyme: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_internal_rhyme` = -0.323 -> weaker or negative association
- internal rhyme: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_internal_rhyme` = -0.061 -> weaker or negative association
- onomatopoeia: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_onomatopoeia` = -0.408 -> weaker or negative association
- onomatopoeia: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_onomatopoeia` = +0.047 -> stronger positive association
- euphony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_euphony` = -0.368 -> weaker or negative association
- euphony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_euphony` = -0.154 -> weaker or negative association
- cacophony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_cacophony` = -0.942 -> weaker or negative association
- cacophony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_cacophony` = -0.293 -> weaker or negative association
- repetition: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_repetition` = -0.220 -> weaker or negative association
- repetition: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_repetition` = -0.166 -> weaker or negative association
- anaphora: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_anaphora` = -0.260 -> weaker or negative association
- anaphora: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_anaphora` = -0.108 -> weaker or negative association
- epistrophe: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_epistrophe` = -0.310 -> weaker or negative association
- epistrophe: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_epistrophe` = -0.016 -> weaker or negative association
- parallelism: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_parallelism` = +0.049 -> stronger positive association
- parallelism: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_parallelism` = -0.019 -> weaker or negative association
- enjambment: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_enjambment` = +0.058 -> stronger positive association
- enjambment: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_enjambment` = +0.055 -> stronger positive association
- caesura: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_caesura` = +0.513 -> stronger positive association
- caesura: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_caesura` = -0.248 -> weaker or negative association
- refrain: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_refrain` = -0.308 -> weaker or negative association
- refrain: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_refrain` = -0.222 -> weaker or negative association
- meter: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_meter` = -0.181 -> weaker or negative association
- meter: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_meter` = +0.093 -> stronger positive association
- rhythm: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_rhythm` = +0.165 -> stronger positive association
- rhythm: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_rhythm` = -0.121 -> weaker or negative association
- stanza: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_stanza` = -0.106 -> weaker or negative association
- stanza: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_stanza` = +0.016 -> stronger positive association
- lineation: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_lineation` = +0.319 -> stronger positive association
- lineation: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_lineation` = -0.137 -> weaker or negative association
- juxtaposition: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_juxtaposition` = -0.371 -> weaker or negative association
- juxtaposition: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_juxtaposition` = +0.095 -> stronger positive association

### Structure Score (`structure_score`)
| Device | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metaphor | ok | 261 | 0.036 | 0.343 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.468) -> weaker or negative association. |  |
| simile | ok | 261 | 0.602 | 0.737 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.073) -> stronger positive association. |  |
| personification | ok | 261 | 0.639 | 0.737 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.326) -> weaker or negative association. |  |
| symbolism | ok | 261 | 0.179 | 0.536 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.140) -> weaker or negative association. |  |
| imagery | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| allusion | ok | 261 | 0.522 | 0.737 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.194) -> weaker or negative association. |  |
| apostrophe | ok | 261 | 0.635 | 0.737 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.073) -> stronger positive association. |  |
| hyperbole | ok | 261 | 0.879 | 0.909 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.091) -> weaker or negative association. |  |
| understatement | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| irony | ok | 261 | 0.441 | 0.666 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.505) -> weaker or negative association. |  |
| paradox | ok | 261 | 0.444 | 0.666 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.209) -> weaker or negative association. |  |
| oxymoron | ok | 261 | 0.061 | 0.363 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.068) -> weaker or negative association. |  |
| metonymy | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| synecdoche | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| allegory | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| alliteration | ok | 261 | 0.199 | 0.544 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.460) -> stronger positive association. |  |
| assonance | ok | 261 | 0.176 | 0.536 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.475) -> stronger positive association. |  |
| consonance | ok | 261 | 0.401 | 0.666 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.157) -> stronger positive association. |  |
| rhyme | ok | 261 | 0.300 | 0.642 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.169) -> stronger positive association. |  |
| internal rhyme | ok | 261 | 0.565 | 0.737 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.280) -> weaker or negative association. |  |
| onomatopoeia | ok | 261 | 0.046 | 0.343 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.410) -> stronger positive association. |  |
| euphony | ok | 261 | 0.297 | 0.642 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.166) -> weaker or negative association. |  |
| cacophony | ok | 261 | 0.324 | 0.644 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.588) -> stronger positive association. |  |
| repetition | ok | 261 | 0.816 | 0.874 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.068) -> stronger positive association. |  |
| anaphora | ok | 261 | 0.726 | 0.806 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.092) -> stronger positive association. |  |
| epistrophe | ok | 261 | 0.344 | 0.644 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.384) -> stronger positive association. |  |
| parallelism | ok | 261 | 0.367 | 0.647 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.167) -> stronger positive association. |  |
| enjambment | ok | 261 | 0.919 | 0.919 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.064) -> stronger positive association. |  |
| caesura | ok | 261 | 0.627 | 0.737 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.267) -> stronger positive association. |  |
| refrain | ok | 261 | 0.250 | 0.624 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.182) -> stronger positive association. |  |
| meter | ok | 261 | 0.148 | 0.536 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.244) -> stronger positive association. |  |
| rhythm | ok | 261 | 0.042 | 0.343 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.329) -> stronger positive association. |  |
| stanza | ok | 261 | 0.102 | 0.510 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.254) -> stronger positive association. |  |
| lineation | ok | 261 | 0.038 | 0.343 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.414) -> stronger positive association. |  |
| juxtaposition | ok | 261 | 0.143 | 0.536 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.169) -> stronger positive association. |  |

Direction Narrative
- metaphor: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_metaphor` = -0.468 -> weaker or negative association
- metaphor: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_metaphor` = -0.138 -> weaker or negative association
- simile: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_simile` = +0.073 -> stronger positive association
- simile: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_simile` = -0.051 -> weaker or negative association
- personification: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_personification` = -0.326 -> weaker or negative association
- personification: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_personification` = -0.098 -> weaker or negative association
- symbolism: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_symbolism` = -0.140 -> weaker or negative association
- symbolism: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_symbolism` = +0.117 -> stronger positive association
- allusion: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_allusion` = -0.194 -> weaker or negative association
- allusion: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_allusion` = -0.095 -> weaker or negative association
- apostrophe: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_apostrophe` = +0.073 -> stronger positive association
- apostrophe: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_apostrophe` = -0.044 -> weaker or negative association
- hyperbole: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_hyperbole` = -0.091 -> weaker or negative association
- hyperbole: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_hyperbole` = -0.025 -> weaker or negative association
- irony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_irony` = -0.505 -> weaker or negative association
- irony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_irony` = +0.024 -> stronger positive association
- paradox: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_paradox` = -0.209 -> weaker or negative association
- paradox: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_paradox` = +0.023 -> stronger positive association
- oxymoron: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_oxymoron` = -1.068 -> weaker or negative association
- oxymoron: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_oxymoron` = -0.246 -> weaker or negative association
- alliteration: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_alliteration` = +0.460 -> stronger positive association
- alliteration: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_alliteration` = +0.355 -> stronger positive association
- assonance: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_assonance` = +0.475 -> stronger positive association
- assonance: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_assonance` = +0.455 -> stronger positive association
- consonance: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_consonance` = +0.157 -> stronger positive association
- consonance: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_consonance` = -0.036 -> weaker or negative association
- rhyme: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_rhyme` = +0.169 -> stronger positive association
- rhyme: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_rhyme` = +0.145 -> stronger positive association
- internal rhyme: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_internal_rhyme` = -0.280 -> weaker or negative association
- internal rhyme: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_internal_rhyme` = +0.035 -> stronger positive association
- onomatopoeia: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_onomatopoeia` = +0.410 -> stronger positive association
- onomatopoeia: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_onomatopoeia` = -0.184 -> weaker or negative association
- euphony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_euphony` = -0.166 -> weaker or negative association
- euphony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_euphony` = +0.165 -> stronger positive association
- cacophony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_cacophony` = +0.588 -> stronger positive association
- cacophony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_cacophony` = +0.438 -> stronger positive association
- repetition: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_repetition` = +0.068 -> stronger positive association
- repetition: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_repetition` = -0.015 -> weaker or negative association
- anaphora: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_anaphora` = +0.092 -> stronger positive association
- anaphora: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_anaphora` = +0.052 -> stronger positive association
- epistrophe: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_epistrophe` = +0.384 -> stronger positive association
- epistrophe: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_epistrophe` = -0.120 -> weaker or negative association
- parallelism: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_parallelism` = +0.167 -> stronger positive association
- parallelism: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_parallelism` = +0.023 -> stronger positive association
- enjambment: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_enjambment` = +0.064 -> stronger positive association
- enjambment: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_enjambment` = +0.011 -> stronger positive association
- caesura: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_caesura` = +0.267 -> stronger positive association
- caesura: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_caesura` = -0.016 -> weaker or negative association
- refrain: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_refrain` = +0.182 -> stronger positive association
- refrain: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_refrain` = -0.021 -> weaker or negative association
- meter: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_meter` = +0.244 -> stronger positive association
- meter: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_meter` = +0.006 -> stronger positive association
- rhythm: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_rhythm` = +0.329 -> stronger positive association
- rhythm: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_rhythm` = -0.021 -> weaker or negative association
- stanza: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_stanza` = +0.254 -> stronger positive association
- stanza: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_stanza` = +0.178 -> stronger positive association
- lineation: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_lineation` = +0.414 -> stronger positive association
- lineation: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_lineation` = +0.047 -> stronger positive association
- juxtaposition: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_juxtaposition` = +0.169 -> stronger positive association
- juxtaposition: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_juxtaposition` = -0.083 -> weaker or negative association

### Diction Score (`diction_score`)
| Device | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metaphor | ok | 261 | 0.475 | 0.509 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.281) -> weaker or negative association. |  |
| simile | ok | 261 | 0.178 | 0.243 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.250) -> stronger positive association. |  |
| personification | ok | 261 | 0.172 | 0.243 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.531) -> stronger positive association. |  |
| symbolism | ok | 261 | 0.255 | 0.294 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.262) -> weaker or negative association. |  |
| imagery | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| allusion | ok | 261 | 0.072 | 0.120 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.494) -> weaker or negative association. |  |
| apostrophe | ok | 261 | 0.002 | 0.007 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.539) -> weaker or negative association. |  |
| hyperbole | ok | 261 | 0.070 | 0.120 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.621) -> weaker or negative association. |  |
| understatement | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| irony | ok | 261 | 0.198 | 0.258 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.824) -> weaker or negative association. |  |
| paradox | ok | 261 | 0.054 | 0.108 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.558) -> stronger positive association. |  |
| oxymoron | ok | 261 | 0.309 | 0.343 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.884) -> weaker or negative association. |  |
| metonymy | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| synecdoche | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| allegory | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| alliteration | ok | 261 | 0.069 | 0.120 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.544) -> weaker or negative association. |  |
| assonance | ok | 261 | 0.161 | 0.243 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.357) -> weaker or negative association. |  |
| consonance | ok | 261 | 0.002 | 0.006 | yes | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.558) -> weaker or negative association. |  |
| rhyme | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.058) -> weaker or negative association. |  |
| internal rhyme | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.795) -> weaker or negative association. |  |
| onomatopoeia | ok | 261 | 0.210 | 0.262 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.421) -> weaker or negative association. |  |
| euphony | ok | 261 | 0.042 | 0.089 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.521) -> weaker or negative association. |  |
| cacophony | ok | 261 | 0.710 | 0.710 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.502) -> weaker or negative association. |  |
| repetition | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.881) -> weaker or negative association. |  |
| anaphora | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.693) -> weaker or negative association. |  |
| epistrophe | ok | 261 | 0.178 | 0.243 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.777) -> weaker or negative association. |  |
| parallelism | ok | 261 | 0.013 | 0.033 | yes | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.575) -> weaker or negative association. |  |
| enjambment | ok | 261 | 0.528 | 0.546 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.199) -> weaker or negative association. |  |
| caesura | ok | 261 | 0.016 | 0.037 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.399) -> stronger positive association. |  |
| refrain | ok | 261 | 0.003 | 0.008 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.570) -> weaker or negative association. |  |
| meter | ok | 261 | 0.009 | 0.026 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.513) -> weaker or negative association. |  |
| rhythm | ok | 261 | 0.251 | 0.294 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.321) -> weaker or negative association. |  |
| stanza | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.685) -> weaker or negative association. |  |
| lineation | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.600) -> weaker or negative association. |  |
| juxtaposition | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.533) -> stronger positive association. |  |

Direction Narrative
- metaphor: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_metaphor` = -0.281 -> weaker or negative association
- metaphor: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_metaphor` = -0.254 -> weaker or negative association
- simile: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_simile` = +0.250 -> stronger positive association
- simile: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_simile` = +0.001 -> stronger positive association
- personification: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_personification` = +0.531 -> stronger positive association
- personification: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_personification` = +0.377 -> stronger positive association
- symbolism: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_symbolism` = -0.262 -> weaker or negative association
- symbolism: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_symbolism` = -0.084 -> weaker or negative association
- allusion: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_allusion` = -0.494 -> weaker or negative association
- allusion: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_allusion` = -0.267 -> weaker or negative association
- apostrophe: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_apostrophe` = -0.539 -> weaker or negative association
- apostrophe: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_apostrophe` = -0.392 -> weaker or negative association
- hyperbole: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_hyperbole` = -0.621 -> weaker or negative association
- hyperbole: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_hyperbole` = -0.323 -> weaker or negative association
- irony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_irony` = -0.824 -> weaker or negative association
- irony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_irony` = +0.153 -> stronger positive association
- paradox: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_paradox` = +0.558 -> stronger positive association
- paradox: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_paradox` = +0.412 -> stronger positive association
- oxymoron: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_oxymoron` = -0.884 -> weaker or negative association
- oxymoron: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_oxymoron` = -0.313 -> weaker or negative association
- alliteration: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_alliteration` = -0.544 -> weaker or negative association
- alliteration: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_alliteration` = -0.259 -> weaker or negative association
- assonance: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_assonance` = -0.357 -> weaker or negative association
- assonance: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_assonance` = -0.097 -> weaker or negative association
- consonance: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_consonance` = -0.558 -> weaker or negative association
- consonance: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_consonance` = -0.214 -> weaker or negative association
- rhyme: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_rhyme` = -1.058 -> weaker or negative association
- rhyme: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_rhyme` = -0.416 -> weaker or negative association
- internal rhyme: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_internal_rhyme` = -0.795 -> weaker or negative association
- internal rhyme: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_internal_rhyme` = -0.638 -> weaker or negative association
- onomatopoeia: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_onomatopoeia` = -0.421 -> weaker or negative association
- onomatopoeia: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_onomatopoeia` = +0.047 -> stronger positive association
- euphony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_euphony` = -0.521 -> weaker or negative association
- euphony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_euphony` = -0.011 -> weaker or negative association
- cacophony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_cacophony` = -0.502 -> weaker or negative association
- cacophony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_cacophony` = -0.239 -> weaker or negative association
- repetition: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_repetition` = -0.881 -> weaker or negative association
- repetition: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_repetition` = -0.591 -> weaker or negative association
- anaphora: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_anaphora` = -0.693 -> weaker or negative association
- anaphora: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_anaphora` = -0.528 -> weaker or negative association
- epistrophe: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_epistrophe` = -0.777 -> weaker or negative association
- epistrophe: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_epistrophe` = +0.161 -> stronger positive association
- parallelism: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_parallelism` = -0.575 -> weaker or negative association
- parallelism: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_parallelism` = -0.259 -> weaker or negative association
- enjambment: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_enjambment` = -0.199 -> weaker or negative association
- enjambment: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_enjambment` = +0.123 -> stronger positive association
- caesura: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_caesura` = +0.399 -> stronger positive association
- caesura: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_caesura` = -0.389 -> weaker or negative association
- refrain: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_refrain` = -0.570 -> weaker or negative association
- refrain: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_refrain` = -0.342 -> weaker or negative association
- meter: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_meter` = -0.513 -> weaker or negative association
- meter: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_meter` = -0.251 -> weaker or negative association
- rhythm: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_rhythm` = -0.321 -> weaker or negative association
- rhythm: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_rhythm` = -0.197 -> weaker or negative association
- stanza: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_stanza` = -0.685 -> weaker or negative association
- stanza: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_stanza` = -0.525 -> weaker or negative association
- lineation: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_lineation` = -0.600 -> weaker or negative association
- lineation: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_lineation` = -0.409 -> weaker or negative association
- juxtaposition: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_juxtaposition` = +0.533 -> stronger positive association
- juxtaposition: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_juxtaposition` = -0.110 -> weaker or negative association

### Originality Score (`originality_score`)
| Device | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metaphor | ok | 261 | 0.075 | 0.162 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.516) -> weaker or negative association. |  |
| simile | ok | 261 | <0.001 | 0.008 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.416) -> stronger positive association. |  |
| personification | ok | 261 | 0.037 | 0.122 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.689) -> stronger positive association. |  |
| symbolism | ok | 261 | 0.261 | 0.373 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.259) -> weaker or negative association. |  |
| imagery | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| allusion | ok | 261 | 0.658 | 0.705 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.175) -> stronger positive association. |  |
| apostrophe | ok | 261 | 0.016 | 0.067 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.444) -> weaker or negative association. |  |
| hyperbole | ok | 261 | 0.129 | 0.227 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.506) -> weaker or negative association. |  |
| understatement | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| irony | ok | 261 | <0.001 | 0.008 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.831) -> weaker or negative association. |  |
| paradox | ok | 261 | 0.371 | 0.484 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.295) -> stronger positive association. |  |
| oxymoron | ok | 261 | 0.067 | 0.162 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.376) -> weaker or negative association. |  |
| metonymy | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| synecdoche | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| allegory | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| alliteration | ok | 261 | 0.001 | 0.008 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.493) -> weaker or negative association. |  |
| assonance | ok | 261 | 0.079 | 0.162 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.340) -> weaker or negative association. |  |
| consonance | ok | 261 | 0.553 | 0.664 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.177) -> weaker or negative association. |  |
| rhyme | ok | 261 | <0.001 | 0.007 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.536) -> weaker or negative association. |  |
| internal rhyme | ok | 261 | 0.005 | 0.033 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.196) -> weaker or negative association. |  |
| onomatopoeia | ok | 261 | 0.036 | 0.122 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.590) -> weaker or negative association. |  |
| euphony | ok | 261 | 0.051 | 0.152 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.507) -> weaker or negative association. |  |
| cacophony | ok | 261 | 0.307 | 0.419 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.780) -> weaker or negative association. |  |
| repetition | ok | 261 | 0.095 | 0.178 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.242) -> weaker or negative association. |  |
| anaphora | ok | 261 | 0.011 | 0.056 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.438) -> weaker or negative association. |  |
| epistrophe | ok | 261 | 0.529 | 0.661 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.571) -> stronger positive association. |  |
| parallelism | ok | 261 | 0.581 | 0.670 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.104) -> stronger positive association. |  |
| enjambment | ok | 261 | 0.189 | 0.298 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.366) -> weaker or negative association. |  |
| caesura | ok | 261 | 0.869 | 0.869 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.132) -> weaker or negative association. |  |
| refrain | ok | 261 | 0.081 | 0.162 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.324) -> weaker or negative association. |  |
| meter | ok | 261 | 0.211 | 0.316 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.423) -> weaker or negative association. |  |
| rhythm | ok | 261 | 0.692 | 0.716 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.172) -> weaker or negative association. |  |
| stanza | ok | 261 | 0.170 | 0.283 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.285) -> weaker or negative association. |  |
| lineation | ok | 261 | 0.653 | 0.705 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.179) -> weaker or negative association. |  |
| juxtaposition | ok | 261 | 0.059 | 0.160 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.308) -> stronger positive association. |  |

Direction Narrative
- metaphor: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_metaphor` = -0.516 -> weaker or negative association
- metaphor: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_metaphor` = -0.409 -> weaker or negative association
- simile: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_simile` = +0.416 -> stronger positive association
- simile: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_simile` = -0.138 -> weaker or negative association
- personification: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_personification` = +0.689 -> stronger positive association
- personification: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_personification` = +0.060 -> stronger positive association
- symbolism: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_symbolism` = -0.259 -> weaker or negative association
- symbolism: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_symbolism` = -0.189 -> weaker or negative association
- allusion: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_allusion` = +0.175 -> stronger positive association
- allusion: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_allusion` = -0.000 -> weaker or negative association
- apostrophe: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_apostrophe` = -0.444 -> weaker or negative association
- apostrophe: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_apostrophe` = -0.162 -> weaker or negative association
- hyperbole: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_hyperbole` = -0.506 -> weaker or negative association
- hyperbole: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_hyperbole` = -0.201 -> weaker or negative association
- irony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_irony` = -1.831 -> weaker or negative association
- irony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_irony` = +0.153 -> stronger positive association
- paradox: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_paradox` = +0.295 -> stronger positive association
- paradox: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_paradox` = -0.085 -> weaker or negative association
- oxymoron: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_oxymoron` = -1.376 -> weaker or negative association
- oxymoron: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_oxymoron` = -0.378 -> weaker or negative association
- alliteration: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_alliteration` = -0.493 -> weaker or negative association
- alliteration: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_alliteration` = +0.063 -> stronger positive association
- assonance: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_assonance` = -0.340 -> weaker or negative association
- assonance: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_assonance` = -0.018 -> weaker or negative association
- consonance: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_consonance` = -0.177 -> weaker or negative association
- consonance: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_consonance` = +0.017 -> stronger positive association
- rhyme: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_rhyme` = -0.536 -> weaker or negative association
- rhyme: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_rhyme` = -0.025 -> weaker or negative association
- internal rhyme: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_internal_rhyme` = -1.196 -> weaker or negative association
- internal rhyme: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_internal_rhyme` = -0.213 -> weaker or negative association
- onomatopoeia: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_onomatopoeia` = -0.590 -> weaker or negative association
- onomatopoeia: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_onomatopoeia` = +0.111 -> stronger positive association
- euphony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_euphony` = -0.507 -> weaker or negative association
- euphony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_euphony` = -0.015 -> weaker or negative association
- cacophony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_cacophony` = -0.780 -> weaker or negative association
- cacophony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_cacophony` = -0.734 -> weaker or negative association
- repetition: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_repetition` = -0.242 -> weaker or negative association
- repetition: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_repetition` = +0.198 -> stronger positive association
- anaphora: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_anaphora` = -0.438 -> weaker or negative association
- anaphora: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_anaphora` = -0.032 -> weaker or negative association
- epistrophe: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_epistrophe` = +0.571 -> stronger positive association
- epistrophe: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_epistrophe` = +0.321 -> stronger positive association
- parallelism: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_parallelism` = +0.104 -> stronger positive association
- parallelism: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_parallelism` = -0.095 -> weaker or negative association
- enjambment: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_enjambment` = -0.366 -> weaker or negative association
- enjambment: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_enjambment` = -0.054 -> weaker or negative association
- caesura: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_caesura` = -0.132 -> weaker or negative association
- caesura: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_caesura` = +0.054 -> stronger positive association
- refrain: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_refrain` = -0.324 -> weaker or negative association
- refrain: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_refrain` = +0.034 -> stronger positive association
- meter: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_meter` = -0.423 -> weaker or negative association
- meter: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_meter` = -0.125 -> weaker or negative association
- rhythm: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_rhythm` = -0.172 -> weaker or negative association
- rhythm: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_rhythm` = -0.090 -> weaker or negative association
- stanza: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_stanza` = -0.285 -> weaker or negative association
- stanza: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_stanza` = -0.018 -> weaker or negative association
- lineation: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_lineation` = -0.179 -> weaker or negative association
- lineation: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_lineation` = -0.103 -> weaker or negative association
- juxtaposition: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_juxtaposition` = +0.308 -> stronger positive association
- juxtaposition: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_juxtaposition` = -0.052 -> weaker or negative association

### Impact Score (`impact_score`)
| Device | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metaphor | ok | 261 | 0.005 | 0.026 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.680) -> weaker or negative association. |  |
| simile | ok | 261 | 0.037 | 0.125 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.303) -> stronger positive association. |  |
| personification | ok | 261 | 0.147 | 0.276 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.519) -> stronger positive association. |  |
| symbolism | ok | 261 | 0.060 | 0.147 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.356) -> weaker or negative association. |  |
| imagery | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| allusion | ok | 261 | 0.885 | 0.916 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.109) -> weaker or negative association. |  |
| apostrophe | ok | 261 | 0.009 | 0.033 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.357) -> weaker or negative association. |  |
| hyperbole | ok | 261 | 0.249 | 0.407 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.343) -> weaker or negative association. |  |
| understatement | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| irony | ok | 261 | 0.043 | 0.128 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.862) -> weaker or negative association. |  |
| paradox | ok | 261 | 0.556 | 0.667 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.182) -> weaker or negative association. |  |
| oxymoron | ok | 261 | 0.055 | 0.147 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.256) -> weaker or negative association. |  |
| metonymy | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| synecdoche | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| allegory | error | 261 | N/A | N/A | no | none |  | Singular matrix |
| alliteration | ok | 261 | <0.001 | 0.007 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.542) -> weaker or negative association. |  |
| assonance | ok | 261 | 0.001 | 0.010 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.382) -> weaker or negative association. |  |
| consonance | ok | 261 | 0.321 | 0.471 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.217) -> stronger positive association. |  |
| rhyme | ok | 261 | 0.002 | 0.013 | yes | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.278) -> stronger positive association. |  |
| internal rhyme | ok | 261 | 0.258 | 0.407 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.586) -> weaker or negative association. |  |
| onomatopoeia | ok | 261 | 0.093 | 0.187 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.407) -> weaker or negative association. |  |
| euphony | ok | 261 | <0.001 | 0.007 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.730) -> weaker or negative association. |  |
| cacophony | ok | 261 | 0.730 | 0.782 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.367) -> weaker or negative association. |  |
| repetition | ok | 261 | 0.173 | 0.306 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.268) -> weaker or negative association. |  |
| anaphora | ok | 261 | 0.064 | 0.147 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.235) -> weaker or negative association. |  |
| epistrophe | ok | 261 | 0.466 | 0.595 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.453) -> stronger positive association. |  |
| parallelism | ok | 261 | 0.476 | 0.595 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.184) -> stronger positive association. |  |
| enjambment | ok | 261 | 0.335 | 0.471 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.262) -> weaker or negative association. |  |
| caesura | ok | 261 | 0.625 | 0.721 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.203) -> stronger positive association. |  |
| refrain | ok | 261 | 0.008 | 0.032 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.468) -> weaker or negative association. |  |
| meter | ok | 261 | 0.925 | 0.925 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.085) -> stronger positive association. |  |
| rhythm | ok | 261 | 0.723 | 0.782 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.155) -> stronger positive association. |  |
| stanza | ok | 261 | 0.087 | 0.186 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.254) -> stronger positive association. |  |
| lineation | ok | 261 | 0.345 | 0.471 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.247) -> stronger positive association. |  |
| juxtaposition | ok | 261 | 0.002 | 0.011 | yes | adjusted | Largest interaction term: openai/gpt-oss-120b (-0.443) -> weaker or negative association. |  |

Direction Narrative
- metaphor: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_metaphor` = -0.680 -> weaker or negative association
- metaphor: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_metaphor` = -0.559 -> weaker or negative association
- simile: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_simile` = +0.303 -> stronger positive association
- simile: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_simile` = -0.033 -> weaker or negative association
- personification: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_personification` = +0.519 -> stronger positive association
- personification: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_personification` = +0.259 -> stronger positive association
- symbolism: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_symbolism` = -0.356 -> weaker or negative association
- symbolism: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_symbolism` = -0.134 -> weaker or negative association
- allusion: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_allusion` = -0.109 -> weaker or negative association
- allusion: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_allusion` = -0.079 -> weaker or negative association
- apostrophe: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_apostrophe` = -0.357 -> weaker or negative association
- apostrophe: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_apostrophe` = +0.057 -> stronger positive association
- hyperbole: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_hyperbole` = -0.343 -> weaker or negative association
- hyperbole: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_hyperbole` = -0.076 -> weaker or negative association
- irony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_irony` = -0.862 -> weaker or negative association
- irony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_irony` = +0.400 -> stronger positive association
- paradox: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_paradox` = -0.182 -> weaker or negative association
- paradox: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_paradox` = +0.090 -> stronger positive association
- oxymoron: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_oxymoron` = -1.256 -> weaker or negative association
- oxymoron: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_oxymoron` = -0.550 -> weaker or negative association
- alliteration: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_alliteration` = -0.542 -> weaker or negative association
- alliteration: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_alliteration` = -0.000 -> weaker or negative association
- assonance: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_assonance` = -0.382 -> weaker or negative association
- assonance: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_assonance` = +0.126 -> stronger positive association
- consonance: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_consonance` = +0.217 -> stronger positive association
- consonance: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_consonance` = +0.161 -> stronger positive association
- rhyme: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_rhyme` = +0.278 -> stronger positive association
- rhyme: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_rhyme` = -0.215 -> weaker or negative association
- internal rhyme: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_internal_rhyme` = -0.586 -> weaker or negative association
- internal rhyme: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_internal_rhyme` = -0.069 -> weaker or negative association
- onomatopoeia: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_onomatopoeia` = -0.407 -> weaker or negative association
- onomatopoeia: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_onomatopoeia` = +0.188 -> stronger positive association
- euphony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_euphony` = -0.730 -> weaker or negative association
- euphony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_euphony` = +0.153 -> stronger positive association
- cacophony: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_cacophony` = -0.367 -> weaker or negative association
- cacophony: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_cacophony` = -0.214 -> weaker or negative association
- repetition: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_repetition` = -0.268 -> weaker or negative association
- repetition: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_repetition` = -0.099 -> weaker or negative association
- anaphora: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_anaphora` = -0.235 -> weaker or negative association
- anaphora: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_anaphora` = +0.113 -> stronger positive association
- epistrophe: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_epistrophe` = +0.453 -> stronger positive association
- epistrophe: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_epistrophe` = +0.058 -> stronger positive association
- parallelism: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_parallelism` = +0.184 -> stronger positive association
- parallelism: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_parallelism` = +0.143 -> stronger positive association
- enjambment: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_enjambment` = -0.262 -> weaker or negative association
- enjambment: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_enjambment` = +0.063 -> stronger positive association
- caesura: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_caesura` = +0.203 -> stronger positive association
- caesura: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_caesura` = +0.129 -> stronger positive association
- refrain: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_refrain` = -0.468 -> weaker or negative association
- refrain: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_refrain` = -0.059 -> weaker or negative association
- meter: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_meter` = +0.085 -> stronger positive association
- meter: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_meter` = +0.036 -> stronger positive association
- rhythm: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_rhythm` = +0.155 -> stronger positive association
- rhythm: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_rhythm` = +0.063 -> stronger positive association
- stanza: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_stanza` = +0.254 -> stronger positive association
- stanza: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_stanza` = -0.027 -> weaker or negative association
- lineation: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_lineation` = +0.247 -> stronger positive association
- lineation: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_lineation` = +0.167 -> stronger positive association
- juxtaposition: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:device_juxtaposition` = -0.443 -> weaker or negative association
- juxtaposition: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:device_juxtaposition` = +0.132 -> stronger positive association

## Diction Feature x Model Score Interactions By Metric
- Alpha: 0.05
- P-value adjustment: benjamini_hochberg

### Aggregate Score (`aggregate_score`)
| Feature | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| avg_word_length | ok | 261 | 0.087 | 0.087 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+1.809) -> stronger positive association. |  |
| latinate_ratio | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-4.829) -> weaker or negative association. |  |
| type_token_ratio | ok | 261 | 0.065 | 0.087 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+5.220) -> stronger positive association. |  |

Direction Narrative
- avg_word_length: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:avg_word_length` = +1.809 -> stronger positive association
- avg_word_length: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:avg_word_length` = +0.401 -> stronger positive association
- latinate_ratio: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:latinate_ratio` = -4.829 -> weaker or negative association
- latinate_ratio: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:latinate_ratio` = +0.303 -> stronger positive association
- type_token_ratio: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:type_token_ratio` = +5.220 -> stronger positive association
- type_token_ratio: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:type_token_ratio` = +2.862 -> stronger positive association

### Technical Craft Score (`technical_craft_score`)
| Feature | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| avg_word_length | ok | 261 | 0.265 | 0.265 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.308) -> stronger positive association. |  |
| latinate_ratio | ok | 261 | 0.017 | 0.051 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.641) -> weaker or negative association. |  |
| type_token_ratio | ok | 261 | 0.133 | 0.200 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.908) -> stronger positive association. |  |

Direction Narrative
- avg_word_length: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:avg_word_length` = +0.308 -> stronger positive association
- avg_word_length: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:avg_word_length` = +0.164 -> stronger positive association
- latinate_ratio: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:latinate_ratio` = -0.641 -> weaker or negative association
- latinate_ratio: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:latinate_ratio` = +0.125 -> stronger positive association
- type_token_ratio: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:type_token_ratio` = +0.908 -> stronger positive association
- type_token_ratio: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:type_token_ratio` = +0.784 -> stronger positive association

### Structure Score (`structure_score`)
| Feature | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| avg_word_length | ok | 261 | 0.193 | 0.193 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.333) -> weaker or negative association. |  |
| latinate_ratio | ok | 261 | 0.013 | 0.040 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.510) -> weaker or negative association. |  |
| type_token_ratio | ok | 261 | 0.085 | 0.127 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.961) -> weaker or negative association. |  |

Direction Narrative
- avg_word_length: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:avg_word_length` = -0.333 -> weaker or negative association
- avg_word_length: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:avg_word_length` = -0.077 -> weaker or negative association
- latinate_ratio: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:latinate_ratio` = -0.510 -> weaker or negative association
- latinate_ratio: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:latinate_ratio` = +0.347 -> stronger positive association
- type_token_ratio: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:type_token_ratio` = -0.961 -> weaker or negative association
- type_token_ratio: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:type_token_ratio` = -0.001 -> weaker or negative association

### Diction Score (`diction_score`)
| Feature | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| avg_word_length | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.991) -> stronger positive association. |  |
| latinate_ratio | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.345) -> weaker or negative association. |  |
| type_token_ratio | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+2.656) -> stronger positive association. |  |

Direction Narrative
- avg_word_length: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:avg_word_length` = +0.991 -> stronger positive association
- avg_word_length: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:avg_word_length` = +0.338 -> stronger positive association
- latinate_ratio: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:latinate_ratio` = -1.345 -> weaker or negative association
- latinate_ratio: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:latinate_ratio` = -0.444 -> weaker or negative association
- type_token_ratio: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:type_token_ratio` = +2.656 -> stronger positive association
- type_token_ratio: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:type_token_ratio` = +1.884 -> stronger positive association

### Originality Score (`originality_score`)
| Feature | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| avg_word_length | ok | 261 | 0.032 | 0.038 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.576) -> stronger positive association. |  |
| latinate_ratio | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.377) -> weaker or negative association. |  |
| type_token_ratio | ok | 261 | 0.038 | 0.038 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+1.427) -> stronger positive association. |  |

Direction Narrative
- avg_word_length: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:avg_word_length` = +0.576 -> stronger positive association
- avg_word_length: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:avg_word_length` = +0.091 -> stronger positive association
- latinate_ratio: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:latinate_ratio` = -1.377 -> weaker or negative association
- latinate_ratio: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:latinate_ratio` = -0.049 -> weaker or negative association
- type_token_ratio: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:type_token_ratio` = +1.427 -> stronger positive association
- type_token_ratio: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:type_token_ratio` = +0.153 -> stronger positive association

### Impact Score (`impact_score`)
| Feature | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| avg_word_length | ok | 261 | 0.211 | 0.211 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+0.268) -> stronger positive association. |  |
| latinate_ratio | ok | 261 | <0.001 | 0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.956) -> weaker or negative association. |  |
| type_token_ratio | ok | 261 | 0.065 | 0.097 | no | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (+1.190) -> stronger positive association. |  |

Direction Narrative
- avg_word_length: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:avg_word_length` = +0.268 -> stronger positive association
- avg_word_length: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:avg_word_length` = -0.115 -> weaker or negative association
- latinate_ratio: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:latinate_ratio` = -0.956 -> weaker or negative association
- latinate_ratio: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:latinate_ratio` = +0.325 -> stronger positive association
- type_token_ratio: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:type_token_ratio` = +1.190 -> stronger positive association
- type_token_ratio: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:type_token_ratio` = +0.041 -> stronger positive association

## Author Variable x Model Score Interactions By Metric
- Alpha: 0.05
- P-value adjustment: benjamini_hochberg

### Aggregate Score (`aggregate_score`)
| Feature | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| author_gender | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-3.545) -> weaker or negative association. |  |
| author_ethnicity | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-3.545) -> weaker or negative association. |  |
| author_nationality | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-3.545) -> weaker or negative association. |  |

Direction Narrative
- author_gender: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_gender)[T.anonymous]` = -3.545 -> weaker or negative association
- author_gender: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_gender)[T.anonymous]` = -0.407 -> weaker or negative association
- author_ethnicity: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_ethnicity)[T.anonymous]` = -3.545 -> weaker or negative association
- author_ethnicity: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_ethnicity)[T.anonymous]` = -0.407 -> weaker or negative association
- author_nationality: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_nationality)[T.anonymous]` = -3.545 -> weaker or negative association
- author_nationality: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_nationality)[T.anonymous]` = -0.407 -> weaker or negative association

### Technical Craft Score (`technical_craft_score`)
| Feature | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| author_gender | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.528) -> weaker or negative association. |  |
| author_ethnicity | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.528) -> weaker or negative association. |  |
| author_nationality | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.528) -> weaker or negative association. |  |

Direction Narrative
- author_gender: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_gender)[T.anonymous]` = -0.528 -> weaker or negative association
- author_gender: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_gender)[T.anonymous]` = -0.258 -> weaker or negative association
- author_ethnicity: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_ethnicity)[T.anonymous]` = -0.528 -> weaker or negative association
- author_ethnicity: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_ethnicity)[T.anonymous]` = -0.258 -> weaker or negative association
- author_nationality: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_nationality)[T.anonymous]` = -0.528 -> weaker or negative association
- author_nationality: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_nationality)[T.anonymous]` = -0.258 -> weaker or negative association

### Structure Score (`structure_score`)
| Feature | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| author_gender | ok | 261 | 0.177 | 0.177 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.210) -> stronger positive association. |  |
| author_ethnicity | ok | 261 | 0.177 | 0.177 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.210) -> stronger positive association. |  |
| author_nationality | ok | 261 | 0.177 | 0.177 | no | adjusted | Largest interaction term: openai/gpt-oss-120b (+0.210) -> stronger positive association. |  |

Direction Narrative
- author_gender: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_gender)[T.anonymous]` = +0.210 -> stronger positive association
- author_gender: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_gender)[T.anonymous]` = +0.055 -> stronger positive association
- author_ethnicity: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_ethnicity)[T.anonymous]` = +0.210 -> stronger positive association
- author_ethnicity: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_ethnicity)[T.anonymous]` = +0.055 -> stronger positive association
- author_nationality: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_nationality)[T.anonymous]` = +0.210 -> stronger positive association
- author_nationality: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_nationality)[T.anonymous]` = +0.055 -> stronger positive association

### Diction Score (`diction_score`)
| Feature | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| author_gender | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.496) -> weaker or negative association. |  |
| author_ethnicity | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.496) -> weaker or negative association. |  |
| author_nationality | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-1.496) -> weaker or negative association. |  |

Direction Narrative
- author_gender: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_gender)[T.anonymous]` = -1.496 -> weaker or negative association
- author_gender: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_gender)[T.anonymous]` = -0.497 -> weaker or negative association
- author_ethnicity: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_ethnicity)[T.anonymous]` = -1.496 -> weaker or negative association
- author_ethnicity: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_ethnicity)[T.anonymous]` = -0.497 -> weaker or negative association
- author_nationality: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_nationality)[T.anonymous]` = -1.496 -> weaker or negative association
- author_nationality: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_nationality)[T.anonymous]` = -0.497 -> weaker or negative association

### Originality Score (`originality_score`)
| Feature | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| author_gender | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.919) -> weaker or negative association. |  |
| author_ethnicity | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.919) -> weaker or negative association. |  |
| author_nationality | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.919) -> weaker or negative association. |  |

Direction Narrative
- author_gender: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_gender)[T.anonymous]` = -0.919 -> weaker or negative association
- author_gender: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_gender)[T.anonymous]` = -0.098 -> weaker or negative association
- author_ethnicity: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_ethnicity)[T.anonymous]` = -0.919 -> weaker or negative association
- author_ethnicity: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_ethnicity)[T.anonymous]` = -0.098 -> weaker or negative association
- author_nationality: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_nationality)[T.anonymous]` = -0.919 -> weaker or negative association
- author_nationality: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_nationality)[T.anonymous]` = -0.098 -> weaker or negative association

### Impact Score (`impact_score`)
| Feature | Status | N poems | P | Adj P | Significant | Basis | Direction summary | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| author_gender | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.658) -> weaker or negative association. |  |
| author_ethnicity | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.658) -> weaker or negative association. |  |
| author_nationality | ok | 261 | <0.001 | <0.001 | yes | adjusted | Largest interaction term: qwen/qwen3.5-397b-a17b (-0.658) -> weaker or negative association. |  |

Direction Narrative
- author_gender: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_gender)[T.anonymous]` = -0.658 -> weaker or negative association
- author_gender: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_gender)[T.anonymous]` = +0.237 -> stronger positive association
- author_ethnicity: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_ethnicity)[T.anonymous]` = -0.658 -> weaker or negative association
- author_ethnicity: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_ethnicity)[T.anonymous]` = +0.237 -> stronger positive association
- author_nationality: qwen/qwen3.5-397b-a17b term `C(model)[T.qwen/qwen3.5-397b-a17b]:C(author_nationality)[T.anonymous]` = -0.658 -> weaker or negative association
- author_nationality: openai/gpt-oss-120b term `C(model)[T.openai/gpt-oss-120b]:C(author_nationality)[T.anonymous]` = +0.237 -> stronger positive association

## AI-vs-Non-AI Preference Interactions By Metric
- Alpha: 0.05
- Pairwise p-value adjustment: benjamini_hochberg
- Inferential claims here are based on cross-model interaction tests (omnibus and pairwise gap-difference tests) only.
- Per-model AI-minus-Non-AI values below are descriptive effect summaries, not standalone significance tests.

### Aggregate Score (`aggregate_score`)
- Method: `mixedlm`
- Omnibus p-value: <0.001
- Omnibus significance: significant at alpha=0.05 (raw_unadjusted)

#### Descriptive AI-minus-Non-AI Gap By Model (Not a Standalone Test)
| Model | AI mean | Non-AI mean | AI - Non-AI | N AI | N Non-AI |
| --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b | 40.663 | 36.017 | +4.646 | 80 | 181 |
| openai/gpt-oss-120b | 30.025 | 24.972 | +5.053 | 80 | 181 |
| qwen/qwen3.5-397b-a17b | 39.837 | 31.646 | +8.191 | 80 | 181 |

#### Pairwise Gap-Difference Interaction Tests
| Pair | Status | N poems | Gap diff | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.407 | 0.343 | 0.343 | no | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | -3.545 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -3.138 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; gap-difference (AI-minus-Non-AI) = -0.407.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; gap-difference (AI-minus-Non-AI) = -3.545.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; gap-difference (AI-minus-Non-AI) = -3.138.

### Technical Craft Score (`technical_craft_score`)
- Method: `mixedlm`
- Omnibus p-value: <0.001
- Omnibus significance: significant at alpha=0.05 (raw_unadjusted)

#### Descriptive AI-minus-Non-AI Gap By Model (Not a Standalone Test)
| Model | AI mean | Non-AI mean | AI - Non-AI | N AI | N Non-AI |
| --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b | 7.950 | 7.155 | +0.795 | 80 | 181 |
| openai/gpt-oss-120b | 6.075 | 5.022 | +1.053 | 80 | 181 |
| qwen/qwen3.5-397b-a17b | 8.213 | 6.890 | +1.323 | 80 | 181 |

#### Pairwise Gap-Difference Interaction Tests
| Pair | Status | N poems | Gap diff | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.258 | 0.015 | 0.022 | yes | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.528 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.270 | 0.043 | 0.043 | yes | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; gap-difference (AI-minus-Non-AI) = -0.258.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; gap-difference (AI-minus-Non-AI) = -0.528.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; gap-difference (AI-minus-Non-AI) = -0.270.

### Structure Score (`structure_score`)
- Method: `mixedlm`
- Omnibus p-value: 0.177
- Omnibus significance: not significant at alpha=0.05 (raw_unadjusted)

#### Descriptive AI-minus-Non-AI Gap By Model (Not a Standalone Test)
| Model | AI mean | Non-AI mean | AI - Non-AI | N AI | N Non-AI |
| --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b | 6.950 | 6.807 | +0.143 | 80 | 181 |
| openai/gpt-oss-120b | 5.237 | 5.304 | -0.066 | 80 | 181 |
| qwen/qwen3.5-397b-a17b | 7.237 | 7.149 | +0.088 | 80 | 181 |

#### Pairwise Gap-Difference Interaction Tests
| Pair | Status | N poems | Gap diff | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.210 | 0.066 | 0.199 | no | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | +0.055 | 0.597 | 0.597 | no | adjusted | nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.155 | 0.236 | 0.353 | no | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; gap-difference (AI-minus-Non-AI) = +0.210.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b higher than qwen/qwen3.5-397b-a17b; gap-difference (AI-minus-Non-AI) = +0.055.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; gap-difference (AI-minus-Non-AI) = -0.155.

### Diction Score (`diction_score`)
- Method: `mixedlm`
- Omnibus p-value: <0.001
- Omnibus significance: significant at alpha=0.05 (raw_unadjusted)

#### Descriptive AI-minus-Non-AI Gap By Model (Not a Standalone Test)
| Model | AI mean | Non-AI mean | AI - Non-AI | N AI | N Non-AI |
| --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b | 8.950 | 8.033 | +0.917 | 80 | 181 |
| openai/gpt-oss-120b | 6.475 | 5.061 | +1.414 | 80 | 181 |
| qwen/qwen3.5-397b-a17b | 8.650 | 6.238 | +2.412 | 80 | 181 |

#### Pairwise Gap-Difference Interaction Tests
| Pair | Status | N poems | Gap diff | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.497 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | -1.496 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.998 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; gap-difference (AI-minus-Non-AI) = -0.497.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; gap-difference (AI-minus-Non-AI) = -1.496.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; gap-difference (AI-minus-Non-AI) = -0.998.

### Originality Score (`originality_score`)
- Method: `mixedlm`
- Omnibus p-value: <0.001
- Omnibus significance: significant at alpha=0.05 (raw_unadjusted)

#### Descriptive AI-minus-Non-AI Gap By Model (Not a Standalone Test)
| Model | AI mean | Non-AI mean | AI - Non-AI | N AI | N Non-AI |
| --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b | 7.975 | 6.425 | +1.550 | 80 | 181 |
| openai/gpt-oss-120b | 6.537 | 4.890 | +1.648 | 80 | 181 |
| qwen/qwen3.5-397b-a17b | 7.513 | 5.044 | +2.468 | 80 | 181 |

#### Pairwise Gap-Difference Interaction Tests
| Pair | Status | N poems | Gap diff | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | -0.098 | 0.455 | 0.455 | no | adjusted | nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.919 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.820 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b lower than openai/gpt-oss-120b; gap-difference (AI-minus-Non-AI) = -0.098.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; gap-difference (AI-minus-Non-AI) = -0.919.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; gap-difference (AI-minus-Non-AI) = -0.820.

### Impact Score (`impact_score`)
- Method: `mixedlm`
- Omnibus p-value: <0.001
- Omnibus significance: significant at alpha=0.05 (raw_unadjusted)

#### Descriptive AI-minus-Non-AI Gap By Model (Not a Standalone Test)
| Model | AI mean | Non-AI mean | AI - Non-AI | N AI | N Non-AI |
| --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b | 8.838 | 7.597 | +1.241 | 80 | 181 |
| openai/gpt-oss-120b | 5.700 | 4.696 | +1.004 | 80 | 181 |
| qwen/qwen3.5-397b-a17b | 8.225 | 6.326 | +1.899 | 80 | 181 |

#### Pairwise Gap-Difference Interaction Tests
| Pair | Status | N poems | Gap diff | P | Adj P | Significant | Basis | Direction | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron-3-super-120b-a12b vs openai/gpt-oss-120b | ok | 261 | +0.237 | 0.038 | 0.038 | yes | adjusted | nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b |  |
| nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.658 | <0.001 | <0.001 | yes | adjusted | nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b |  |
| openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b | ok | 261 | -0.895 | <0.001 | <0.001 | yes | adjusted | openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b |  |

Direction Narrative
- nemotron-3-super-120b-a12b vs openai/gpt-oss-120b: nemotron-3-super-120b-a12b higher than openai/gpt-oss-120b; gap-difference (AI-minus-Non-AI) = +0.237.
- nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b: nemotron-3-super-120b-a12b lower than qwen/qwen3.5-397b-a17b; gap-difference (AI-minus-Non-AI) = -0.658.
- openai/gpt-oss-120b vs qwen/qwen3.5-397b-a17b: openai/gpt-oss-120b lower than qwen/qwen3.5-397b-a17b; gap-difference (AI-minus-Non-AI) = -0.895.

## Skipped And Error Rows
- `device_score_interactions` / `imagery`: status=error; reason=Singular matrix
- `device_score_interactions` / `understatement`: status=error; reason=Singular matrix
- `device_score_interactions` / `metonymy`: status=error; reason=Singular matrix
- `device_score_interactions` / `synecdoche`: status=error; reason=Singular matrix
- `device_score_interactions` / `allegory`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `aggregate_score` / `imagery`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `aggregate_score` / `understatement`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `aggregate_score` / `metonymy`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `aggregate_score` / `synecdoche`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `aggregate_score` / `allegory`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `technical_craft_score` / `imagery`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `technical_craft_score` / `understatement`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `technical_craft_score` / `metonymy`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `technical_craft_score` / `synecdoche`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `technical_craft_score` / `allegory`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `structure_score` / `imagery`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `structure_score` / `understatement`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `structure_score` / `metonymy`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `structure_score` / `synecdoche`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `structure_score` / `allegory`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `diction_score` / `imagery`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `diction_score` / `understatement`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `diction_score` / `metonymy`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `diction_score` / `synecdoche`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `diction_score` / `allegory`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `originality_score` / `imagery`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `originality_score` / `understatement`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `originality_score` / `metonymy`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `originality_score` / `synecdoche`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `originality_score` / `allegory`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `impact_score` / `imagery`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `impact_score` / `understatement`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `impact_score` / `metonymy`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `impact_score` / `synecdoche`: status=error; reason=Singular matrix
- `device_score_interactions_by_metric` / `impact_score` / `allegory`: status=error; reason=Singular matrix
- `device_detection.posthoc` / `imagery` / `nemotron-3-super-120b-a12b vs qwen/qwen3.5-397b-a17b`: status=skipped; reason=no_discordant_pairs

## Caveats
- P-values indicate evidence against the null; they do not measure practical effect size on their own.
- Mixed-effects and non-parametric fallbacks are inferential models and do not prove causation.
