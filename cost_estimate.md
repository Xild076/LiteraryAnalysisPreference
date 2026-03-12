# LLM Cost Estimate for Literary Analysis Project

## Per-Poem Token Estimates

### Input: Average Poem
- **Average word count:** 200 words (liberal estimate)
- **Average characters per word:** 5
- **Total characters:** 200 × 6 = 1,200 characters
- **Tokens (measured):** ~201 tokens

### Prompt 0: Prior Knowledge Check
- Instruction text: ~39 tokens
- Schema (`CheckPriorKnowledgeInference`): ~77 tokens
- Poem text: ~201 tokens
- **Total input:** ~317 tokens per poem

### Prompt 1: Literary Devices Inference
- Instruction text + devices list (35 devices): ~149 tokens
- Schema (`LiteraryDevicesInference`): ~139 tokens
- Poem text: ~201 tokens
- **Total input:** ~489 tokens per poem

### Prompt 2: Score Inference
- Instruction & rubric: ~78 tokens
- Schema (`ScoreInference`): ~293 tokens
- Poem text: ~201 tokens
- **Total input:** ~572 tokens per poem

### Expected Outputs (per inference)
- **Prior Knowledge Check:** ~10 tokens
- **Literary Devices:** Rationale (~200 tokens) + device list (~20 tokens) = ~220 tokens
- **Score:** Rationale (~300 tokens) + 5 numerical scores (~10 tokens) = ~310 tokens

---

## Cost Breakdown per Poem (2 inferences × 3 models = 6 API calls)

### Input Tokens (all models)
- Prior Knowledge Check: 317 tokens × 3 models = 951 tokens
- Literary Devices: 489 tokens × 3 models = 1,467 tokens
- Scoring: 572 tokens × 3 models = 1,716 tokens
- **Total input: 4,134 tokens per poem**

### Output Tokens (estimates)
- Prior Knowledge Check: 10 tokens × 3 models = 30 tokens
- Literary Devices: 220 tokens × 3 models = 660 tokens
- Scoring: 310 tokens × 3 models = 930 tokens
- **Total output: 1,620 tokens per poem**

---

## Pricing (estimated 2026 rates)

### Model Pricing (per 1M tokens)
- **GPT-5.4:** Input $2.50, Output $15.00
- **Claude 4.6 Opus:** Input $5.00, Output $25.00
- **Gemini 3.1 Pro:** Input $2.00, Output $12.00

### Cost per Poem (per model)

Per-model input: 1,378 tokens. Per-model output: 540 tokens.

| Model | Rate (Input / Output per 1M) | Input Cost | Output Cost | Total Cost |
|-------|------------------------------|-----------|------------|------------|
| GPT-5.4 | $2.50 / $15.00 | $0.003445 | $0.008100 | **$0.011545** |
| Claude Opus | $5.00 / $25.00 | $0.006890 | $0.013500 | **$0.020390** |
| Gemini Pro | $2.00 / $12.00 | $0.002756 | $0.006480 | **$0.009236** |

### **Cost per Poem (all 3 models):** ~$0.041171

---

## Scaling to Full Dataset

| Poem Count | Total Cost | GPT-5.4 | Claude | Gemini | Notes |
|-----------|-----------|---------|--------|--------|-------|
| 10 | $0.41 | $0.12 | $0.20 | $0.09 | Test batch |
| 50 | $2.06 | $0.58 | $1.02 | $0.46 | |
| 100 | $4.12 | $1.15 | $2.04 | $0.92 | |
| 500 | $20.59 | $5.77 | $10.20 | $4.62 | |
| 1,000 | $41.17 | $11.55 | $20.39 | $9.24 | Full-scale run |

---

## Full-Scale Allocation With Leeway (1,000 Poems)

Baseline full-scale API cost is **$41.17**.

### Budget by Leeway Level

| Leeway | Formula | Total Budget |
|-------|---------|--------------|
| 0% | $41.17 × 1.00 | **$41.17** |
| 15% | $41.17 × 1.15 | **$47.35** |
| 25% | $41.17 × 1.25 | **$51.46** |
| 40% | $41.17 × 1.40 | **$57.64** |

### Specific Allocation (Recommended: 25% Leeway)

Using a **$51.46** budget cap:

- **Core planned inference (all poems, all models):** $41.17
- **Retry / transient API failures reserve (10%):** $4.12
- **Longer-than-expected outputs reserve (7.5%):** $3.09
- **Prompt iteration / QA spot-check reserve (7.5%):** $3.09

Total allocated: **$51.47**

### Model-Level Allocation at 25% Leeway

| Model | Baseline (1,000 poems) | With 25% Leeway |
|------|----------|------------------|
| GPT-5.4 | $11.55 | $14.43 |
| Claude 4.6 Opus | $20.39 | $25.49 |
| Gemini 3.1 Pro | $9.24 | $11.55 |
| **Total** | **$41.17** | **$51.46** |

Note: Current `data/poems.csv` has 1 poem row, so this is a projection for the full target dataset.