## Paper Metadata

- Title: Lost at C: A User Study on the Security Implications of Large Language Model Code Assistants
- Year: 2023
- Authors: Gustavo Sandoval, Hammond Pearce, Teo Nys, Ramesh Karri, Siddharth Garg, Brendan Dolan-Gavitt
- Preprint: No, published by USENIX
- Link: https://www.usenix.org/system/files/sec23fall-prepub-353-sandoval.pdf

### One sentence takeaway
  - We perform the first security-motivated randomized trial comparing programmers with and without access to a Codex-based code completion assistant.

### Most intersting find
  - 


## Methodology
  - We conduct a security-driven user study (N=58) to assess code written by student programmers when assisted by LLMs.
  - Do developers with access to an LLM-based code completion assistants produce less secure code than the code produced by programmers without this access?
  - Our user study had 58 computer science undergraduate and graduate students with programming backgrounds split randomly into ‘control’ (no Codex LLM access) and ‘assisted’ (with Codex LLM access) groups.
  - In addition to the two user groups, we created 30 solutions that were generated entirely by the Codex LLM as an ‘autopilot’ group.

#### Analysis:
  - quantitatively
  - qualitatively
  - manual: audit by 3 authors (~66 person-hours)

#### CWE classification:
  - yes


## Experimental Setup

#### LLM model(s) used:
  - code-cushman-001
  - code-davinci-001
  - code-davinci-002

#### Programming languages used:
  - C

#### Prompting strategy:
  - The complete assignment was provided all-at-once with all 11 functisons simultaneouly.
  - Therefore the prompt is all text before the cursor similar to how Copilot works.

#### Dataset / tasks:
  - Participants were (t)asked to complete a set of 11 functions that perform basic operations on a linked list representing a “shopping list”

#### Evaluation metric
  - We examined completed code for functionality and security.
  - CWEs/LoC
  - Per function CWE rates


## Results
  - Our results indicate that the security impact in this setting (low-level C with pointer and array manipulations) is small.
  - We confirm existing findings on the productivity benefits of AI-assistance (RQ1), while finding that the AI-assisted group produced security-critical bugs at a rate no greater than 10 % higher than the control group (non-assisted) (RQ2).
  - When investigating the origin of bugs within the assisted users (RQ3), 63 % of the bugs originate in code written by humans and 36 % of the bugs were present in taken suggestions.

### Types of vulnerabilities identified
  - CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer
  - CWE-400: Uncontrolled Resource Consumption
  - CWE-401: Missing Release of Memory
  - CWE-416: Use After Free
  - CWE-476: NULL Pointer Dereference
  - CWE-787: Out-of-bounds Write
  - CWE-758: Reliance on Undefined Behavior
  - CWE-252: Unchecked Return Value
  - CWE-843: Access using Incompatible Type
  - CWE-457: Use of Uninitialized Variable
  - CWE-835: Infinite Loop