## Paper Metadata

- Title: Time to separate from StackOverflow and match with ChatGPT for encryption
- Year: 2024
- Authors: Ehsan Firouzi, Mohammad Ghafari
- Preprint: No, published by Elsevier
- Link: https://www.sciencedirect.com/science/article/pii/S0164121224001808

### One sentence takeaway
  - We studied StackOverflow posts to identify the problems that developers encounter when using Java Cryptography Architecture (JCA) for symmetric encryption.

### Most intersting find
  - The number of security violations in the symmetric encryption posts on the StackOverflow website is significant, making it a misleading and dangerous information source, especially for novices.


## Methodology
  - Research questions:
    - RQ1 : What are common developer challenges in symmetric encryption?
    - RQ2 : What are the security risks present in the shared JCA code on StackOverflow?
    - RQ3 : How effective is ChatGPT for addressing developer issues in symmetric encryption?
  - We manually inspected 400 StackOverflow posts that are about JCA symmetric encryption.
  - We provided 100 StackOverflow questions to ChatGPT and recorded the answers.
    - Firstly, we presented each ‘‘exact’’ question from the posts to ChatGPT
    - Secondly, we explicitly instructed ChatGPT to generate a ‘‘secure’’ code example. and checked the answers from a security perspective.
    - Lastly, for posts where ChatGPT’s response remained insecure, we searched how we can optimize the prompt to get a more secure answer.

#### Analysis:
  - manual by authors

#### CWE classification:
  - Yes


## Experimental Setup

#### LLM model(s) used:
  - GPT-3.5

#### Programming languages used:
  - Java

#### Prompting strategy:
  - Simple code generation instructions and more improved prompts with secure instructions.
  - Example of simple prompt: "Answer this StackOverflow question and provide a code example"

#### Dataset / tasks:
  - We relied on the Stack Exchange Data Dump released on March 8, 2023
  - We extracted the StackOverflow posts that are related to symmetric encryption and randomly selected a representative subset of these posts for manual inspection.
  - In summary, we gathered a total of 3426 posts for our ‘‘full dataset’’ and chose 400 posts to form our ‘‘sample dataset’’.

#### Evaluation metric
  - agreement metric (Cohen's) for manual security analysis between developers
  - Security violation detection (based on 13 rules)
  - Manual + regex-based large-scale analysis


## Results
  - We found that the majority of reported problems (i.e., 214 posts) are at the ‘‘cipher object initialization’’ stage. The primary challenges were in key and initialization vector (IV) management.
  - The examination of 13 security rules in 400 posts revealed a striking number of 327 posts (i.e. 82%) with security violations.
  - Overall, the findings revealed 5305 violations in 3174 posts, averaging 1.7 violations in 92% of StackOverflow posts.
  - When we provided the exact StackOverflow questions to ChatGPT, it transferred almost every violation from the question to its answer. When we explicitly prompted to provide a ‘‘secure solution’’, it cleared violations in 42 questions.

### Types of vulnerabilities identified
  - Using weak Algorithm
  - Using ECB encryption mode
  - Using CBC encryption mode
  - Using static or constant key
  - Using static salt for key derivation
  - and so on