# About the project
The goal of this thesis is to describe Indoor Environment Quality (IEQ), analyze existing open source applications collecting open data on IEQ, find requirements for the app and finaly to propose a solution and implement it.

# Available Skills & Orchestration

You have access to specialized skills located in the `@skills/` directory. You should act as an orchestrator and use these skills to fulfill user requests instead of running manual scripts or commands yourself.

## Text Improvement & Review
When asked to review, correct, or improve text:
- **`spellcheck`:** Use this skill first to identify and correct basic spelling and typographical errors.
- **`suggestions`:** Use this skill for deeper grammatical, stylistic, and clarity improvements to maintain an academic tone.

## Academic Research & Sourcing
When asked to find information, facts, or sources for the thesis:
- **`research_router`:** Use this skill exclusively. It acts as an orchestrator that will automatically query the local Zotero library (`search_zotero`) and, if necessary and permitted by the user, expand the search to Google Scholar (`search_scholar`).

# General Rules
- Always communicate your reasoning and findings in Czech unless explicitly asked otherwise.
- Strictly adhere to the output formats defined by the individual skills you invoke.
- Do not invent sources or facts.
