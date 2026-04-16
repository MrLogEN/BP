---
name: spellcheck
description: Guide for identifying and correcting spelling and basic grammatical errors in text. Use when asked to proofread text for correctness.
---

> **Tento skill kontroluje pravopis a překlepy.** Pro stylistické a akademické návrhy použij skill `suggestions`.

## Workflow
1. Read the provided text (file, files, or excerpts)
2. Identify issues related to:
   - spelling errors
   - typos
   - basic grammatical mistakes
3. Provide corrections using the template below

## Output format
```md
1. `filename`, ř. line-number, poz. position-range-on-the-line
    **Úsek:** `původní chybný text`
    **Oprava:** `opravený text`
    **Důvod:** `stručné vysvětlení chyby (např. překlep, pravopis)`
```

## Rules
- All corrections and explanations must be in Czech
- Focus only on spelling and typos — do NOT suggest style improvements (that is the `suggestions` skill)
- Do not modify meaning or structure of text
- If no errors are found, state that clearly
