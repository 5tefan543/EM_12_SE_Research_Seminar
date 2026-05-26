## Paper Metadata

- Title: Just another copy and paste? Comparing the security vulnerabilities of ChatGPT generated code and StackOverflow answers
- Year: 2024
- Authors: Sivana Hamer, Marcelo d’Amorim, Laurie Williams
- Preprint: No, published by IEEE
- Link: https://ieeexplore.ieee.org/document/10579524

### One sentence takeaway
  - In this work, our goal is to raise software developers’ awareness of the security implications when selecting code snippets by empirically comparing the vulnerabilities of ChatGPT and StackOverflow (SO).

### Most intersting find
  - Any code copied and pasted, created by AI or humans, cannot be trusted blindly, requiring good software engineering practices to reduce risk.


## Methodology
  - Research questions:
    - RQ1: What vulnerabilities differences are there between ChatGPT and SO code snippets?
    - RQ2: What types of vulnerabilities in terms of Common Weakness Enumeration (CWE) types are present for ChatGPT-generated code versus SO-answered?
  - We conducted an experimental study to compare both information sources in five steps.
    - We selected the platforms under study, ChatGPT and SO.
    - We then selected security-related questions and answers from SO.
    - Collected the code snippets from the answers.
    - We prompted ChatGPT with the SO questions to generate code.
    - We then compare the gathered vulnerabilities of SO and ChatGPT using CodeQL.
  - Only compilable Java snippets with 1 class were retained.

#### Analysis:
  - automated -> CodeQL

#### CWE classification:
  - Yes


## Experimental Setup

#### LLM model(s) used:
  - gpt-3.5-turbo-0613

#### Programming languages used:
  - Java

#### Prompting strategy:
  - We queried ChatGPT, reusing the SO question as our prompt.

#### Dataset / tasks:
  - Existing Java dataset from StackOverflow with security-related questions and 1,429 answers.
  - Final dataset includes 87 questions and 90 answers.

#### Evaluation metric
  - We performed a Chi-squared test to determine if the differences in the number of vulnerabilities of the code snippets by platform were statistically significant.
  - To compare the number of vulnerabilities in each code snippet produced in SO versus ChatGPT, we utilized a paired t-test.


## Results
  - ChatGPT-generated code contained 248 vulnerabilities compared to the 302 vulnerabilities found in SO snippets, producing 20% fewer vulnerabilities with a statistically significant difference.
  - Additionally, ChatGPT generated 19 types of CWE, fewer than the 22 found in SO.
  - Our findings suggest developers are undereducated on insecure code propagation from both platforms, as we found 274 unique vulnerabilities and 25 types of CWE.
  - Additionally, the vulnerabilities found in the ChatGPT-generated code and SO overlapped only in 25% of the vulnerabilities.

### Types of vulnerabilities identified
  - 25 CWEs