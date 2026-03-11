# LLM Cost Estimate for Literary Analysis Project

## Per-Poem Token Estimates

### Input: Average Poem
- **Average word count:** 172 words
- **Average characters per word:** 5
- **Total characters:** 172 × 6 = 1,032 characters
- **Tokens (1 token ≈ 4 chars):** ~258 tokens

### Prompt 1: Literary Devices Inference
- Instruction text: ~50 tokens
- Literary devices list (35 devices): ~150 tokens  
- Poem text: ~258 tokens
- **Total input:** ~458 tokens per poem

### Prompt 2: Score Inference
- Instruction & rubric (5 categories with descriptions): ~150 tokens
- Poem text: ~258 tokens
- **Total input:** ~408 tokens per poem

### Expected Outputs (per inference)
- **Literary Devices:** Rationale (~200 tokens) + device list (~20 tokens) = ~220 tokens
- **Score:** Rationale (~300 tokens) + 5 numerical scores (~10 tokens) = ~310 tokens

---

## Cost Breakdown per Poem (2 inferences × 3 models = 6 API calls)

### Input Tokens (all models)
- Literary Devices: 458 tokens × 3 models = 1,374 tokens
- Scoring: 408 tokens × 3 models = 1,224 tokens
- **Total input: 2,598 tokens per poem**

### Output Tokens (estimates)
- Literary Devices: 220 tokens × 3 models = 660 tokens
- Scoring: 310 tokens × 3 models = 930 tokens
- **Total output: 1,590 tokens per poem**

---

## Pricing (estimated 2026 rates)

### Model Pricing (per 1M tokens)
- **GPT-5.4:** Input $2.50, Output $15.00
- **Claude 4.6 Opus:** Input $5.00, Output $25.00
- **Gemini 3.1 Pro:** Input $2.00, Output $12.00

### Cost per Poem (per model)
| Model | Input Cost ($ per token) | Output Cost ($ per token) | Total Cost |
|-------|-----------|-----------|-----------|
| GPT-5.4 | $0.0000025 | $0.000015 | **$0.030345** |
| Claude Opus | $0.000005 | $0.000025 | **$0.05274** |
| Gemini Pro | $0.000002 | $0.000012 | **$0.024276** |

### **Cost per Poem (all 3 models):** ~$0.107361

---

## Scaling to Full Dataset

| Poem Count | Total Cost | GPT-5.4 | Claude | Gemini | Notes |
|-----------|-----------|---------|--------|--------|-------|
| 10 | $1.07361 | $0.30345 | $0.52740 | $0.24276 | Test batch |
| 50 | $5.36805 | $1.51725 | $2.63700 | $1.21380 | |
| 100 | $10.73610 | $3.03450 | $5.27400 | $2.42760 | |
| 500 | $53.68050 | $15.17250 | $26.37000 | $12.13800 | |
| 1,000 | $107.36100 | $30.34500 | $52.74000 | $24.27600 | Full-scale run |

---

## Full-Scale Allocation With Leeway (1,000 Poems)

Baseline full-scale API cost is **$107.36**.

### Budget by Leeway Level

| Leeway | Formula | Total Budget |
|-------|---------|--------------|
| 0% | $107.36 × 1.00 | **$107.36** |
| 15% | $107.36 × 1.15 | **$123.47** |
| 25% | $107.36 × 1.25 | **$134.20** |
| 40% | $107.36 × 1.40 | **$150.31** |

### Specific Allocation (Recommended: 25% Leeway)

Using a **$134.20** budget cap:

- **Core planned inference (all poems, all models):** $107.36
- **Retry / transient API failures reserve (10%):** $13.42
- **Longer-than-expected outputs reserve (7.5%):** $8.05
- **Prompt iteration / QA spot-check reserve (5%):** $5.37

Total allocated: **$134.20**

### Model-Level Allocation at 25% Leeway

| Model | Baseline | With 25% Leeway |
|------|----------|------------------|
| GPT-5.4 | $30.35 | $37.93 |
| Claude 4.6 Opus | $52.74 | $65.93 |
| Gemini 3.1 Pro | $24.28 | $30.35 |
| **Total** | **$107.36** | **$134.20** |

Note: Current `data/poems.csv` has 1 poem row, so this is a projection for the full target dataset.