## Paper Metadata

- Title: Do Users Write More Insecure Code with AI Assistants?
- Year: 2023
- Authors: Neil Perry, Megha Srivastava, Deepak Kumar, Dan Boneh
- Preprint: No, published by ACM
- Link: https://dl.acm.org/doi/10.1145/3576915.3623157

### One sentence takeaway
  - In this paper, we conduct a user study to examine how developers choose to interact with AI code assistants and how those interactions can cause security mistakes.

### Most intersting find
  - Participants with access to an AI assistant were also more likely to believe they wrote secure code, suggesting that such tools may lead users to be overconfident about security flaws in their code.


## Methodology
  - We designed and conducted a comprehensive user study where 47 participants conducted five security-related programming tasks spanning three different programming languages.
  - Three research questions:
    - Do users write more insecure code when given access to an AI programming assistant?
    - Do users trust AI assistants to write secure code?
    - How do users’ language and behavior when interacting with an AI assistant affect the degree of security vulnerabilities in their code?
  - We chose questions that were self contained, could be solved in a short amount of time, and covered a wide breadth of potential security mistakes that are commonly taught in introductory computer security courses.
  - Participants were split into two groups: control group (without AI use) & experiment group (with AI use)
  - The questions were presented in a randomized order to all participants who were free to attempt the questions in any order, change and return to questions, install any libraries, access any resource on the Internet, and use the AI assistant if they were in the experiment group.

#### Analysis:
  - manual

#### CWE classification:
  - not used


## Experimental Setup

#### LLM model(s) used:
  - codex-davinci-002 -> Participants could adjust parameters like temperature and response length

#### Programming languages used:
  - Python, Javascipt, C

#### Prompting strategy:
  - Prompts were designed by the particpants of the user study.
  - Participants iteratively refined prompts (query repair, parameter tuning, reuse of outputs, etc.)

#### Dataset / tasks:
  - All participants were asked to solve six questions (one question was later excluded from analysis), covering the following areas:
    - use of cryptographic libraries (encryption/decryption, signing messages)
    - handling and using user controlled data (paths provided by a user in a sandboxed directory, script injection)
    - common web vulnerabilities (SQL injection, script injection)
    - lower level problems such as memory management (buffer overflows, integer overflows, etc.)

#### Evaluation metric
  - For each question, we designed a classification system for correctness and security which we use to determine the rates of correctness and security mistakes, the types of security mistakes made, and their source (i.e., from the AI or from the user).
  - We then use this data to construct a logistic regression to examine the effect of having access to the AI assistant on the security of the solution.


## Results
  - Overall, we find that participants who had access to an AI assistant wrote significantly less secure code than those without access to an assistant.
  - We found that those who specified task instructions, provided function declarations to use, and had the AI Assistant focus on writing helper functions generated more secure code.

### Types of vulnerabilities identified
  - Cryptography: missing authentication, incorrect padding, use of trivial or insecure ciphers, use of insecure modes or libraries, use of unsafe randomness, use of bad / insecure curves
  - Sandboxed File Access: symlink attacks, lack of path canonicalization
  - SQL Injections
  - Memory Management: buffer overflows, integer overflows, missing return code checks