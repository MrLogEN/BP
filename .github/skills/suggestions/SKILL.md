---
name: suggestions
description: Guide for providing suggestions for improving text style and clarity in a bachelor's thesis. Use when asked for feedback or suggestions on text.
---

> **Tento skill kontroluje styl, srozumitelnost a akademičnost textu.** Pro pravopis a překlepy použij skill `spellcheck`.

## Workflow
The steps to provide good suggestions for text style or clarity.
1. Read the text (files, file, parts of a file) that a suggestion is requested for
2. Identify issues related to:
   - grammar and spelling
   - stylistic appropriateness for academic writing
   - clarity and readability
   - redundancy or awkward phrasing
3. Compile suggestions using the template below:

```md
1. `filename`, ř. line-number, poz. position-range-on-the-line
    **Úsek:** `konkrétní část textu, která je stylisticky nevhodná nebo nejasná`
    **Doporučení:** `konkrétní oprava nebo přeformulování`
    **Důvod:** `stručné zdůvodnění zlepšení (např. gramatika, styl, srozumitelnost)`

```
Example output:
```md
1. `vymezeni.tex`, ř. 86, poz. 101–127
    **Úsek:** `dochází většímu ochlazování`
    **Doporučení:** `dochází k většímu ochlazování`
    **Důvod:** chybí předložka.

2. `vymezeni.tex`, ř. 90, poz. 241–285
    **Úsek:** `Při provedené studii mezi žáky bylo zjištěno,`
    **Doporučení:** `Ve studii mezi žáky bylo zjištěno,`
    **Důvod:** přirozenější odborný styl.
```


## Rules
There are the following rules for providing suggestions:
- All suggestions, explanations, and comments must be written in Czech, regardless of the input language
- Always follow the format template exactly
- Do not modify the structure, labels, or formatting of the template
- Never omit any field (Úsek, Doporučení, Důvod)
- Always use backticks (`) around Úsek and Doporučení content
- Suggestions must be concrete and actionable (provide an exact replacement when possible)
- Do not provide vague suggestions (e.g., "improve wording"); always specify an exact change
- Do not invent filenames, line numbers, or positions if they are not provided
- If line number or position is not available, omit that part instead of guessing
- Start numbering from 1 and increment sequentially
- Do not repeat the same suggestion multiple times
- Prioritize critical issues (grammar, meaning) over minor stylistic suggestions
- Only suggest changes where improvement is clearly beneficial; do not rewrite correct text unnecessarily
- Focus on the most important issues; avoid excessive or trivial suggestions
- Keep explanations concise (ideally one short sentence)
