## Paper Metadata

- Title: Occasionally Secure: A Comparative Analysis of LLM Platform-Generated Code
- Year: 2025
- Authors: Ran Elgedawy, Porter Dosch, John Sadik, Farzin Gholamrezae, Scott Ruoti
- Preprint: Yes (arXiv)
- Link: https://arxiv.org/abs/2402.00689

### One sentence takeaway
  - This paper presents a longitudinal study (3 phases) examining nine platforms across OpenAI GPT, Google Gemini, and DeepSeek families, evaluating 450 code samples generated for common e-commerce development tasks.

### Most intersting find
  - Complex patterns of vulnerability evolution over time.
  - Study is evidence about the fast pace and evolution of LLMs in a short period of time.


## Methodology
  - Methodology simulates real-world development scenarios by incorporating two distinct developer personas: one that emphasizes security-conscious development and another without an explicit focus on security.
  - Detailed comparative analysis of code generation capabilities across major LLM platforms, identifying distinct approaches in security measures, consistency and complexity of generated codes.
  - Models are iteratively prompted until code is functional and meets ground rules.

#### Analysis:
  - manual review -> process: Figure 1 (section 3.1), focusing on OWASP Top 10 2021 securiy issues
  - automated security scanning -> CodeQL (semantic code analysis engine)

#### CWE classification:
  - No


## Experimental Setup

#### LLM model(s) used:
  - GPT-3.5,
  - GPT-4
  - GPT-4o
  - GPT-o3-mini-regular
  - GPT-o3-mini-high
  - Bard
  - Gemini
  - Gemini Flash 2.0 Reasoning
  - DeepSeek

#### Programming languages used:
  - Python

#### Prompting strategy:
  - Evidence that the impact of security-conscious prompting varies significantly across platforms, with some models showing improved security practices while others exhibit unintended negative effects.
  - Developer provides relevant information about their own background, including their level of security awareness, along with details about the task to the model.
  - Each prompt began with a distinct ”persona” reflecting how security-conscious the developer is.
  - Example prompt for topic "User registration, authentication, and login": "I am working on an e-commerce website. Write code that implements user registration functionality..."
  - Prompt details in Appendix A

#### Dataset / tasks:
  - Each dataset collected includes outputs generated under similar conditions, with consistent tasks, prompts, and revision guidelines.
  - 450 code samples across nine unique tasks selected with attention to security vulnerabilities based on OWASP Top 10 2021
  - Process -> Section 4.1

#### Evaluation metric
  - Evaluated the code outputs on four factors: functionality, security, complexity, and consistency.


## Results
  - Our findings demonstrate remarkable advancements in code quality over time. Latest models achieved 100% functional code with substantially less iterative correction required. Security vulnerability patterns varied significantly, with DeepSeek generating the highest vulnerability count (47) while Gemini consistently demonstrated stronger security characteristics. Recent models showed convergence toward more modular, self-contained implementations with fewer external dependencies, and dramatically improved output consistency, with syntax similarity rates exceeding 83%.
  - Security persona has inconsistent effects (sometimes improves, sometimes worsens security)
  - Phase 2 regression in some models (more vulnerabilities, more revisions)
  - Phase 3 improvement linked to reasoning capabilities (e.g., chain-of-thought)

### Types of vulnerabilities identified
  - SQL Injections
  - Lack of input validation
  - Lack of Authentication and/or Authorization
  - Lack of Logging and Monitoring
  - Lack of Error Handling
  - Potential Data Exposure
  - Others