I now had a meeting with my professor to discuss any doubts about my thesis experiment. We aggreed on the following:
- The overall goal is to determine in what context LLMs generate vulnerable code in Rust. Since Rust is not included in the studies.
- I should select one well cited paper which performs some sort of code generation for example in C or C++ from tasks targeted at specific CWEs.
- He shared my concerns about how vibe coding is understood today and that these small controlled tasks do not represent that. However, for the seminar thesis it is still enough.
- I should select min. 4 CWEs (I can do more if I want) and create multiple tasks / scenarios for each specifically for Rust.
- There should be 2 types of CWEs
  - CWEs that are generally prevented by the design of Rust
    -> Here it is specifically interesting if the code even compails.
    -> Do LLMs have problems with the borrow checker?
    -> Do LLMs use unsafe options like "unsafe" or "Box" types which then again lead to memory bugs.
  - CWEs that are not prevented by Rust
    -> like Integer overflow
    -> OS injection / missing input validation like
- I should use two LLMs (e.g. GhatGPT, Claude, Gemini) to which I have access.

Based on this, my plan is to first create the overall structure for the context presentation and then select one of the SLR papers for this (I already have one in mind but more on that later).

For the context presentation I have these slides in mind:

[1]: Motivation why this topic is relevant. Maybe show some LLM generated code for a simple scenarion to prove that LLMs produce vulnerable code.
[2]: Present the SLR as the main reference paper for this thesis. A slide briefly mentioning what the SLR did and an image of it (for nicer representation that I am now talking about a paper).
[3-5]: Starting with some basic results of the SLR. Vulnerability categories and the difference in experiment setups of the cited papers.
[6]: Overview of how I group the experiments the papers did: User study, StackOverflow vs LLM, Controlled Code Generation, Real World Code Analysis, Mitigation / Fine tuning
[7]: Results & Limitations of papers which did a user study (2 papers)
[8]: Results & Limitations of papers which did StackOverflow vs LLM (2 papers)
[9-10]: Results & Limitations of papers which did Controlled Code Generation (most papers) -> 2 types: self defined tasks vs existing datasets / dataset curation from git commits with vulnerabilities
[11]: Results & Limitations of papers which did Real World Code Analysis (2 papers)
[12]: Results & Limitations of papers which did Mitigation / Fine tuning (2 papers)
[13]: Overall gaps and limitations -> No Rust (show language distribution plot)
[14]: Summary other limitations
[15]: Thesis Experiment Summary
[16-18]: Selected CWEs and scenarios
[19]: Research questions:
  - In which context do LLMs generate vulnerabilities for Rust?
  - Do LLMs face problems with the borrow checker?
  - Are LLMs prone to use unsafe Rust features like unsafe or Box?

The specific number of a slide is just a guess and not a hard fix. But it should not be much more than 20 since I only have 20 minutes.

What do you think about that in general?
