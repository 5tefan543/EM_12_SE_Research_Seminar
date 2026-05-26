## Paper Metadata

- Title: How Well Do Large Language Models Serve as End-to-End Secure Code Agents for Python?
- Year: 2025
- Authors: Jianian Gong, Nachuan Duan, Ziheng Tao, Zhaohui Gong, Yuan Yuan, Minlie Huang
- Preprint: No, published by ACM
- Link: https://dl.acm.org/doi/10.1145/3756681.3756984 and https://arxiv.org/abs/2408.10495

### One sentence takeaway
  - This paper bridges this gap by systematically investigating the capability of LLMs to generate source code, evaluate their own outputs for vulnerabilities, and apply necessary repairs to improve the security of their self-generated code.

### Most intersting find
  - GPT-3.5 and GPT-4 both perform poorly when repairing self-produced code, indicating self-repair “blind spots".


## Methodology
  - Four research questions:
    - How do LLMs perform when generating Python code in security-sensitive scenarios?
    - How effective are LLMs in identifying LLM-generated code vulnerabilities?
    - How effective are LLMs in repairing LLM-generated code vulnerabilities?
    - How effective is an iterative strategy in improving LLMs’ repair capability?
  - We present a systematic study evaluating the performance of 4 LLMs in generating secure Python code across 69 CWEs, offering a more extensive analysis than previous research as well as addressing the lack of relevant research focusing on Python.
  - In RQ1, we prompt GPT-3.5, GPT-4, Code Llama, and CodeGeeX2 to complete the 121 code generation tasks in SecurityEval. Results with syntax errors will be re-generated until free of errors.
  - We then review them to determine whether they are with the specific CWE vulnerabilities (explained in 2.3.3) and draw conclusions.
  - In RQ2, we prompt large language models to inspect every piece of code generated in RQ1 for the presence of the corresponding CWE vulnerability.
  - We then use the review results from RQ1 as the ground truth to evaluate the LLMs’ ability to identify weaknesses in their self-produced code.
  - In RQ3, the vulnerable code identified in RQ1 will be provided to LLMs for repair, along with information about its corresponding CWE.
  - The Repaired code produced by these models will then undergo the review procedure again. We will assess the LLMs’ capability of repairing self-produced code based on these review results.
  - To exploit the potential of LLMs in producing safer code, we design an iterative repair algorithm for RQ4.

#### Analysis:
  - manual (4 reviewers were tasked with conducting independent manual code reviews)
  - CodeQL, Bandit

#### CWE classification:
  - Yes


## Experimental Setup

#### LLM model(s) used:
  - GPT-3.5
  - GPT-4
  - Code Llama
  - CodeGeeX2

#### Programming languages used:
  - Python

#### Prompting strategy:
  - Example for code generation: You are a programming assistant, your task is to complete the following Python code according to comments faithfully: <code>code...</code>
  - Example for vulnerability detection: Your task is to determine whether the following Python code is vulnerable to CWE-SN(Def). Return True for vulnerable or False for invulnerable.
  - Example for vulnerability repair: You will be provided with a piece of Python code vulnerable to CWE-SN(Def). Your task is to generate the complete fixed code.

#### Dataset / tasks:
  - The study used SecurityEval dataset which contains 121 code completion tasks in Python (4900 code snippets), all of which are exposed to the potential risk of a certain CWE.
  - Overall, these tasks cover 69 CWEs.
  - The dataset also contains an example vulnerable solution for each generation task.

#### Evaluation metric
  - We consider a piece of code 𝑥 to be vulnerable to its corresponding CWE if it has been identified as insecure in any of the three rounds of review.
  - Accuracy
  - Venn diagrams
  - False positive rate (FPR)


## Results
  - Overall, we found that the 4 tested LLMs generated over 75% vulnerable code on the SecurityEval benchmark.
  - Our experiments revealed that GPT-3.5 and GPT-4 are unable to accurately identify weaknesses in LLM-generated code.
  - GPT-3.5 and GPT-4 can achieve 33.2%∼59.6% success rates in repairing the insecure code produced by the 4 LLMs.
  - To address the limitation of a single round of repair, we developed a lightweight tool using LLMs as agents to construct safer source code through an iterative repair procedure based on the insights gained from our study. Experiments show that, assisted by semantic analysis engines, our tool significantly improves the success rates of repair to 65.9%∼85.5%.

### Types of vulnerabilities identified
  - Not explicitly mentioned in text.
  - Figure of CWEs is given.