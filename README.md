# Vibe Coding and Software Vulnerabilities

This repository contains the seminar material for the topic **Vibe Coding and Software Vulnerabilities** in the course *Security, Privacy, and Forensics* / *SE 703364: Secure and Distributed Computing*.

The project investigates how large language models (LLMs) affect software security when they are used for code generation and code assistance. The central question is whether AI-assisted programming introduces new vulnerabilities, reduces existing ones, or simply changes the kinds of weaknesses developers have to reason about. A particular focus is placed on whether existing results from C/C++-oriented studies also apply to **Rust**, a language designed to prevent many memory-safety errors by default.

## Repository scope

This repository is not only the implementation of the experiment. It collects all relevant seminar artifacts, including:

- literature notes and summaries,
- material for the context presentation,
- figures and visualizations used in the seminar,
- experiment design documents,
- code and prompts for the Rust code-generation experiment,
- generated outputs and analysis scripts,
- material for the result presentation,
- drafts and sources for the final seminar thesis.

## Background

The seminar topic starts from the observation that LLMs are now widely used to automate programming tasks. Prior research has studied whether generated or assisted code contains more or fewer security vulnerabilities, but the results depend on the model, prompt design, task type, programming language, and evaluation method.

The project builds on two starting references:

- Sandoval et al. (2023), *Lost at C: A User Study on the Security Implications of Large Language Model Code Assistants*.
- Basic and Giaretta (2025/2026), *From Vulnerabilities to Remediation: A Systematic Literature Review of LLMs in Code Security*.

The broader literature shows that LLM-generated code can contain vulnerabilities such as injection flaws, memory-management bugs, insecure file handling, weak cryptography, resource-management issues, and poor error handling. However, the evidence is mixed: some studies report increased risk, while others find that AI-assisted developers do not necessarily produce more severe security bugs than unassisted developers.

## Research direction

The project focuses on the following research direction:

> Do findings about LLM-generated vulnerabilities transfer to Rust, or does Rust's type system, ownership model, and borrow checker change the security implications of AI-assisted programming?

The planned experiment uses controlled code-generation tasks instead of a full user study. A small set of CWE-inspired scenarios is defined, prompts are executed against an LLM, and the resulting Rust code is analyzed for correctness, compile behavior, and security-relevant weaknesses.

The experiment is especially interested in multi-round generation: if the model produces code that does not compile, compiler or borrow-checker errors may be fed back into the model. This makes it possible to study whether iterative repair improves the code, introduces new vulnerabilities, or shifts problems from low-level memory safety toward higher-level issues such as denial of service, missing validation, or logic errors.

## Repository structure

The repository is organized around the main seminar artifacts and the experiment:

```text
.
├── Notes.pdf                               # General notes collected during the seminar
├── README.md                               # Project overview
├── slides/                                 # Seminar topic and course information
└── seminar_paper/                          # Literature, presentations, experiment, and paper-related material
    ├── literature/                         # Starting literature, summaries, and related papers
    ├── presentations/                      # Context and result presentation material
    └── experiment/                         # Main controlled Rust code-generation experiment
```

## Seminar deliverables

The repository supports the three required seminar steps:

1. **Context presentation**  
   Summarizes related work, identifies research gaps, and motivates the planned Rust-focused experiment.

2. **Result presentation**  
   Presents the experiment design, selected evidence, preliminary findings, and interpretation.

3. **Seminar thesis**  
   Documents the full process with an individual focus, including background, method, results, discussion, and limitations.

## Experiment overview

The Rust experiment is intended to be small, controlled, and reproducible. Instead of measuring general coding productivity, it focuses on security-relevant code-generation behavior.

Planned elements include:

- selection of a small number of CWE categories,
- multiple scenarios per CWE,
- prompt templates for controlled generation,
- optional multi-round repair using compiler or borrow-checker feedback,
- collection of generated Rust code,
- manual and/or tool-assisted security analysis,
- comparison between first-round and repaired outputs.

The experiment does not aim to reproduce the full methodology of prior user studies. Instead, it adapts their security-oriented perspective to a Rust setting.

## AI usage disclaimer

This repository was created as part of a university seminar on AI-assisted programming and software vulnerabilities. AI tools, including large language models, may have been used during the project for tasks such as literature organization, wording suggestions, code generation, prompt execution, experiment support, and drafting or revising documentation.

All AI-assisted material is treated as a working aid rather than as an authoritative source. The final responsibility for the repository content, experiment design, interpretation of results, citations, and submitted seminar material remains with the author. Generated code and text should be reviewed critically, especially because the project itself investigates how AI-assisted programming can introduce or obscure security-relevant weaknesses.

## Notes

This repository is part of a university seminar project. The material is work in progress and may change as the context presentation, experiment, result presentation, and final thesis are developed.
