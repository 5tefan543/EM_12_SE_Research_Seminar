## Paper Metadata

- Title: Codexity: Secure AI-assisted Code Generation
- Year: 2024
- Authors: Sung Yong Kim, Zhiyu Fan, Yannic Noller, Abhik Roychoudhury
- Preprint: Yes
- Link: https://arxiv.org/abs/2405.03927

### One sentence takeaway
  - In this work, we present Codexity, a security-focused code generation framework integrated with three LLMs.

### Most intersting find
  - 


## Methodology
  - Codexity leverages the feedback of static analysis tools such as Infer and CppCheck to mitigate security vulnerabilities and act as the first guard to prevent potential vulnerabilities introduced by AI programming assistants.
  - In Codexity’s workflow, the user first needs to select a repair strategy in the configuration setting to activate the system.
    - Iteration Repair: LLM generates code -> analyzed by static tools -> iteratively try to fix until no vulnerability is detected -> code presented to user
    - Preshot Repair: Local LLM generates code -> analyzed by static tools -> information + prompt given to stronger (cloud-based) model -> code presented to user

#### Analysis:
  - automated -> Infer, CppCheck

#### CWE classification:
  - Yes


## Experimental Setup

#### LLM model(s) used:
  - Local LLM: StarCoder-15.5B, SantaCoder-1.1B
  - Cloud model: gpt-3.5-turbo
  - Baseline models: ChatGPT, FootPatch, Copilot

#### Programming languages used:
  - C

#### Prompting strategy:
  - Partial code snipptes for code completion.

#### Dataset / tasks:
  - We curated a benchmark of developer prompts that are prone to generate vulnerable programs from ShareGPT and StackOverflow.
  - We first collected 403 user posts relevant to C programming queries by filtering all the posts in the ShareGPT dataset and the first 700 posts in StackOverflow using ‘c’ and ‘int main’ as keywords.
  - We employ a two-round vulnerable prompts detection strategy.
    - In the first round, we extracted the code snippet from the LLM response and ran the static analyzers in Codexity on the extracted code snippet of the 403 programming posts. As a result, we identified 124 posts containing vulnerabilities in their response.
    - In the second round, we extracted the non-vulnerable part of the code snippet from the 124 posts and asked ChatGPT to complete the programming questions to confirm further whether they are prone to generate vulnerable programs.
  - Finally, we ended up with 90 vulnerable prompts and generated 751 vulnerable code completions with 1645 vulnerabilities. 

#### Evaluation metric
  - We specified a prompt as vulnerable if (1) ChatGPT produces a vulnerable program when the temperature is set to 0, or (2) ChatGPT produces at least one vulnerable program in one of the ten runs when the temperature is set to 0.8.


## Results
  - In our experiments with 990 real-world code completion attempts, we demonstrate that, compared to ChatGPT, Codexity prevents the generation of 60% of the vulnerabilities.

### Types of vulnerabilities identified
  - Null & Nullptr Dereference
  - Resource Leak
  - Buffer Overrun
  - Memory Leak
  - Use After Lifetime
  - Integer Overflow
  - etc.