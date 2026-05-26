## Paper Metadata

- Title: Large Language Models for Code: Security Hardening and Adversarial Testing
- Year: 2023
- Authors: Jingxuan He, Martin Vechev
- Preprint: No, published by ACM
- Link: https://dl.acm.org/doi/10.1145/3576915.3623175

### One sentence takeaway
  - This work studies the security of LMs along two important axes: (i) security hardening, which aims to enhance LMs’ reliability in generating secure code, and (ii) adversarial testing, which seeks to evaluate LMs’ security at an adversarial standpoint.

### Most intersting find
  - Our training set is superior in both security control and functional correctness, when compared to a baseline dataset constructed by indiscriminately including ∼19x more samples from our base datasets [33, 57, 75] at the cost of lower data quality.


## Methodology
  - In this work, we investigate the security of LMs for code in two complementary directions.
    - First, we introduce security hardening in order to enhance LMs’ ability to generate secure code.
    - Second, we explore the potential of degrading LMs’ security level from an adversarial perspective.
  - We address both of these by formulating a new security task called controlled code generation.
  - This task involves providing LMs with an additional binary property, alongside the prompt, that specifies whether it should generate secure (for security hardening) or unsafe code (for adversarial testing).
  - We propose a novel learning-based approach called SVEN to solve this task. SVEN leverages property-specific continuous vectors to guide program generation towards the given property, without modifying the LM’s weights.
  - Our training procedure optimizes these continuous vectors by enforcing specialized loss terms on different regions of code, using a high-quality dataset carefully curated by us.
  - We desire to train a separate module that can be plugged into LMs to achieve security control without overwriting their weights.

#### Analysis:
  - automated -> CodeQL

#### CWE classification:
  - Yes


## Experimental Setup

#### LLM model(s) used:
  - CodeGen-350M, CodeGen-2.7B, CodeGen-6.1B

#### Programming languages used:
  - C, C++, Python

#### Prompting strategy:
  - Standard prompting: natural language + partial code

#### Dataset / tasks:
  - Our training dataset consists of security fixes extracted from GitHub commits, where each fix includes a program pair: the program before (resp., after) the fix is insecure (resp., secure).
  - To obtain a high-quality dataset for SVEN, we perform manual curation on [33, 57, 75], which results in ∼1.6k programs.
  - It consists of 1606 programs (803 pairs).

#### Evaluation metric
  - Each evaluation scenario targets one CWE and contains a prompt expressing the desired code functionality, based on which the model can suggest secure or unsafe code completions. For each scenario and each model, we sample 25 completions and filter out duplicates or programs that cannot be compiled or parsed.
  - functional correctness with pass@𝑘
  - security rate (percentage of secure programs among valid ones)


## Results
  - Our extensive evaluation shows that SVEN is highly effective in achieving strong security control.
  - For example, SVEN improves secure code generation for CodeGen-2.7B from 59.1% to 92.3% (or degrades to 36.8% for adversarial testing) while closely matching the original functional correctness of the code when generated without SVEN.

### Types of vulnerabilities identified
  - \>9 CWEs