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
    5. Impact: The impact of the poem infered.

Finally, we perform statistical analysis based on this information. Basically, we need to determine if the score is associated with the presence of a certain literary device, author demographic, or diction pattern.

Since we plan to pair these poems with themselves to observe the drift, we don't need to control for anything on the poem side. Rather, we need to control for the LLM output side. We do this by minimzing temperature.