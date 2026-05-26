## Paper Metadata

- Title: Instruction Tuning for Secure Code Generation
- Year: 2024
- Authors: Jingxuan He, Mark Vero, Gabriela Krasnopolska, Martin Vechev
- Preprint: No, published by PMLR
- Link: https://dl.acm.org/doi/10.5555/3692070.3692793

### One sentence takeaway
  - We introduce SafeCoder, a novel approach that addresses the security limitation of LMs during the instruction tuning phase.

### Most intersting find
  - Adding explicit security instructions to prompts (even CWE-specific ones) does not significantly improve the security of generated code.


## Methodology
  - SafeCoder performs security-specific tuning using a dataset of secure and insecure programs.
  - To address the challenge of being functional correct and secure at the same time, SafeCoder mixes the security dataset with a standard instruction tuning dataset.
  - In each training iteration, specific loss functions are employed depending on the origin of the training sample, forming a joint optimization for the objectives specified by the two datasets.

#### Analysis:
  - automated -> CodeQL

#### CWE classification:
  - Yes


## Experimental Setup

#### LLM model(s) used:
  - StarCoder-1B, StarCoder-3B, CodeLlama-7B, Phi-2-2.7B, Llama2-7B, Mistral-7B

#### Programming languages used:
  - C, C++, Go, Java, JavaScript, Python, Ruby

#### Prompting strategy:
  - Instruction-tuning prompt templates

#### Dataset / tasks:
  - We propose an automated, two-step pipeline for extracting high-quality security datasets from GitHub.
  - Then, the program before (resp., after) each commit is treated as unsafe (resp., secure).
  - Our data collection yields 465 samples spanning 23 CWEs and 6 mainstream languages.
  - The final dataset consists of 1268 samples that cover 25 CWEs across 6 languages.

#### Evaluation metric
  - We assess utility in two critical dimensions, coding ability and natural language understanding.
  - Functional correctness: pass@1 and pass@10 metrics
  - Natural language understanding: We use 5-shot prompting and greedy decoding for both MMLU and TruthfulQA. 
  - Security: percentage of generated programs classified as secure by CodeQL


## Results
  - SafeCoder is able to drastically improve security (by about 30%), while preserving utility.
  - In practice, we observe a well-balanced interplay between the two objectives, resulting in a remarkable security-for-free benefit. That is, the resulting LM achieves significantly improved security with negligible sacrifice on utility, when compared to an LM trained solely with standard instruction tuning.
  - Across a diverse set of 60 testing scenarios, using SafeCoder during instruction tuning yields LMs that reach a secure code generation rate of ∼90%, surpassing their pretrained versions and their instruction-tuned counterparts without SafeCoder by ∼30%.

### Types of vulnerabilities identified
  - 25 CWEs