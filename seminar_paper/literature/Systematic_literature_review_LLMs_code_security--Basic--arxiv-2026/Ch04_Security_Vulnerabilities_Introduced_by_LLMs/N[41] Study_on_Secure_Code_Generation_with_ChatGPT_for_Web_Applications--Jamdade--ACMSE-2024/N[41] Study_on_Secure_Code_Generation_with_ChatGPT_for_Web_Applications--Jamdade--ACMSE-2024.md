## Paper Metadata

- Title: A Pilot Study on Secure Code Generation with ChatGPT for Web Applications
- Year: 2024
- Authors: Mahesh Jamdade, Yi Liu
- Preprint: No, published by ACM
- Link: https://dl.acm.org/doi/10.1145/3603287.3651194

### One sentence takeaway
  - This paper presents a pilot study that uses ChatGPT for generating web application code with a specific emphasis on mitigating four prevalent web application vulnerability types.

### Most intersting find
  - We also observed that if we requested ChatGPT to mitigate the code to address a specific vulnerability type, ChatGPT would address it in the subsequent similar coding requests, even without explicitly mentioning that vulnerability type in the prompt.


## Methodology
  - Research questions:
    - R1: Does ChatGPT generate code containing common web application vulnerabilities?
    - R2: Are there any prompt patterns that can assist in generating secure code to mitigate the common web application vulnerabilities?
  - The case study used in this paper is a full-stack web application (library system), entirely developed by using prompts fed to ChatGPT, from the requirements analysis and design to the implementation.
  - While certain vulnerabilities can be mitigated in the front-end using input validation, our focus in this paper is on the back-end solutions.
  - The authors started with initial prompts to generate the backend classes. If the generated code contained vulnerabilities, they asked the LLM to fix the vulnerabilities with specific security prompts.

#### Analysis:
  - manual by authors

#### CWE classification:
  - Yes


## Experimental Setup

#### LLM model(s) used:
  - ChatGPT

#### Programming languages used:
  - Node.js, TypeScript, PostgreSQL

#### Prompting strategy:
  - Examples:
    - Initial prompt: Implement separate methods to find user by user name and id in User Service.
    - Security Prompt: Update the methods to secure them from SQL injection.

#### Dataset / tasks:
  - Creation of a simple webapp with 7 microservices that is designed for a university library that provides online access to students, staff, and library personnel. 

#### Evaluation metric
  - Code is considered insecure if it contains the desired vulnerability.


## Results
  - We found that the generated code contained all four types of vulnerabilities focused in this paper.
  - ChatGPT does not inherently address vulnerabilities in code unless prompted to do so.
  - We noticed that the vulnerability type needs to be explicitly specified in the prompts; otherwise, ChatGPT may not identify which vulnerability type to address if a similar case has not been handled before.

### Types of vulnerabilities identified
  - SQL Injection (SQLi) (CWE-89)
  - Cross Site Scripting (XSS) (CWE-79)
  - Carriage Return Line Feed (CRLF) Injection (CWE-93)
  - Exposure of Sensitive Information (CWE-200)