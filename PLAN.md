# LLM's Literary Analysis Systematic Preferences

What we want to look at:
1. Difference in scoring when compared to hidden authorial variables
2. Relative preferences in:
    - Diction
    - Literary devices

**Essentially:** Does an LLM's relative evaluation of a piece of literature indicate a preference for a certain diction, literary device, or authorial demographic when compared to other LLMs?

*or*

Whether variation in LLM literary evaluation is associated with hidden authorial variables and textual features such as diction and literary devices?

**Our hypothesis:** LLMs will differ systematically in literary evaluation.

## Experimental Set-Up

First, we curate a collection of poetry and locate metadata.

We run 2 inferences with each model, prompting with the poem text, instructions, and output schema:
1. **Literary Devices:** Creates a list of literary devices identifies within the poem
2. **Score:** Generates a score based on a preset rubric:
    1. Technique: The quality of technique used
    2. Structure: The quality of structure used
    3. Prose: The quality of prose observed
    4. Originality: The quality of originality observed
    5. Impact: The impact of the poem inferred.

Finally, we perform statistical analysis to determine whether score differences are associated with literary devices, diction patterns, and hidden authorial variables.

Because each poem is evaluated by every LLM, poem-level pairing must be preserved in the analysis. Lower temperature helps reduce randomness, but it is not a substitute for statistical control. We still control for poem-level repeated measures in the tests below.

## What We Compare And Which Test To Use

### A) Comparisons within each LLM (one model at a time)

1. Does this LLM detect some literary devices more often than others?
    - Data: device counts per poem for a fixed device taxonomy.
    - Test: Chi-square goodness-of-fit test.

2. Within this LLM, are some devices associated with higher rubric scores?
    - Data: poem score vs presence/absence (or count) of each device.
    - Test: Linear regression (or ordinal logistic regression if score is treated as ordinal).

3. Within this LLM, are diction features associated with higher scores?
    - Data: score vs diction features (for example lexical diversity, concreteness, sentiment, rare-word rate).
    - Test: Multiple linear regression with feature coefficients.

4. Within this LLM, are hidden authorial variables associated with higher scores?
    - Data: score vs author metadata (gender, ethnicity, nationality, age, etc.).
    - Test: ANOVA or linear regression with categorical predictors.

### B) Comparisons between LLMs (relative model differences)

1. Do LLMs differ in overall scoring on the same poems?
    - Data: repeated scores for each poem across models.
    - Primary test: Linear mixed-effects model with `score ~ model + (1 | poem_id)`.
    - Simpler fallback: Friedman test (non-parametric repeated measures).

2. Do LLMs differ in device detection rates?
    - Data: device presence/absence by model on the same poems.
    - Test: Cochran's Q test for each device across models.
    - Post-hoc: McNemar pairwise tests with multiple-comparison correction.

3. Do LLMs differ in how strongly devices relate to score?
    - Data: interaction between model and device features.
    - Test: Mixed-effects model with interaction terms, for example `score ~ model * device + (1 | poem_id)`.

4. Do LLMs differ in how strongly diction features relate to score?
    - Data: model-by-diction interactions.
    - Test: Mixed-effects model with interactions, for example `score ~ model * diction_feature + (1 | poem_id)`.

5. Do LLMs differ in how authorial variables relate to score?
    - Data: model-by-author-variable interactions.
    - Test: Mixed-effects model with interactions, for example `score ~ model * author_variable + (1 | poem_id)`.

### C) Multiple testing and reporting

1. Apply multiple-testing correction for all post-hoc tests (Holm or Benjamini-Hochberg).
2. Report effect sizes and confidence intervals, not only p-values.
3. If possible, run repeated inferences per poem-model pair and report within-model variance.