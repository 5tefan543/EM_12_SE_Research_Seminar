# No Need to Lift a Finger Anymore? Assessing the Quality of Code Generation by ChatGPT
This project contains the scripts used for assessing ChatGPT-based code generation.

## Environment
Type the following command to create python environment:
```
conda env create -f environment.yaml
```

## Get All LeetCode Problems
You first need to configure LeetCode parameters following https://github.com/fspv/python-leetcode and changing the corresponding variable of ```leetcode_session``` in [LeetCode/ProblemCollector.py](LeetCode/ProblemCollector.py).

Then, you need to set an empty directory for subsequent collection. The directory should be set to the variable ```supplementary_prefix``` in [LeetCode/ProblemCollector.py](LeetCode/ProblemCollector.py).

You can type ```python LeetCode/ProblemCollector.py -p 1``` to collect problems and type ```python LeetCode/ProblemCollector.py -p 2``` to get prompts of these problems in five different languages.

## Code Geneartion for LeetCode Problems
First, you need to set the variable ```supplementary_prefix``` in [ChatGPT/Resolver-v3.py](ChatGPT/Resolver-v3.py) with your previous setting. You also need to encode your OpenAI API into [ChatGPT/Resolver-v3.py](ChatGPT/Resolver-v3.py).

Then, you can type ```Python ChatGPT/Resolver-v3.py -c af``` and ```Python ChatGPT/Resolver-v3.py -c be``` to perform code generation for both Aft. problems and Bef. problems.

## Evaluate Functional Correctness for Generated Code Snippets
After generating code for LeetCode problems, you can type the following commands for evaluation.
```
python LeetCode/Judgment-3.py -s <directory to ChatGPT responses> -t <directory for saving stripped code> -f STRIP

python LeetCode/Judgment-3.py -s <directory to stripped code> -t <directory for saving judged results> -f JUDGE
```

## Perform Multi-round Fixing Process for Functional Correctness

You need to encode your OpenAI API.

For performing multi-round fixing process for generated code of LeetCode, you can type:
```
python WorkFlow/WrongAnswer-WorkFLow.py
```
This script only fixes W.A. code snippets. For code snippets with other errors, we use jupyter to fix them one by one due to OpenAI api latency problem. For fixing code snippets with other errors, you can change the encoded parameters in WorkFlow/WrongAnswer-WorkFLow.py to perform fixing.

For convience, we provide all fixed results in the repository.


## Code Complexity
For evaluating the code comlexity, you need to install SonarQube and then follow SonarQube's turorial to scan generated code snippets.

You can type the following URL to retirve scanned results for code complexity:
```
http://localhost:9000/api/measures/component_tree?component=<project name>&metricKeys=complexity,cognitive_complexity&qualifiers=FIL&ps=500&p=<page number>
```

## Security Code

Before performing security code generation, you need to first install CodeQL.

Then add global variables:
```
export CODEQL_HOME=$HOME/codeql-home
export PATH=$PATH:$CODEQL_HOME/codeql
```

For detecting generated code snippets of LeetCode problems, you can use the following CodeQL queries:
```
CWE_CODEQL = dict()
CWE_CODEQL['cwe-787'] = [
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Likely Bugs/Memory Management/PotentialBufferOverflow.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Security/CWE/CWE-120/BadlyBoundedWrite.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Security/CWE/CWE-120/UnboundedWrite.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/experimental/Security/CWE/CWE-193/InvalidPointerDeref.ql",
]

CWE_CODEQL['cwe-416'] = [
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Critical/UseAfterFree.ql"
]
CWE_CODEQL['cwe-476'] = [
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Critical/MissingNullTest.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Critical/InconsistentNullnessTesting.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Likely Bugs/RedundantNullCheckSimple.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/experimental/Likely Bugs/RedundantNullCheckParam.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/experimental/Security/CWE/CWE-476/DangerousUseOfExceptionBlocks.ql",
]
CWE_CODEQL['cwe-190'] = [
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Security/CWE/CWE-190/ArithmeticTainted.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Security/CWE/CWE-190/ArithmeticUncontrolled.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Likely Bugs/AmbiguouslySignedBitField.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Likely Bugs/Arithmetic/BadAdditionOverflowCheck.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Likely Bugs/Arithmetic/SignedOverflowCheck.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Security/CWE/CWE-190/ArithmeticWithExtremeValues.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Security/CWE/CWE-190/ComparisonWithWiderType.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Security/CWE/CWE-190/IntegerOverflowTainted.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/experimental/Security/CWE/CWE-190/DangerousUseOfTransformationAfterOperation.ql",
]
CWE_CODEQL['cwe-119'] = [
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Security/CWE/CWE-119/OverflowBuffer.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Best Practices/Likely Errors/OffsetUseBeforeRangeCheck.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/experimental/Security/CWE/CWE-415/DoubleFree.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Critical/LateNegativeTest.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Critical/MissingNegativityTest.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Critical/OverflowCalculated.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Critical/OverflowDestination.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Likely Bugs/Memory Management/ReturnStackAllocatedMemory.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/Likely Bugs/Memory Management/UsingExpiredStackAddress.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/experimental/Security/CWE/CWE-120/MemoryUnsafeFunctionScan.ql",
"$CODEQL_HOME/codeql-repo/cpp/ql/src/experimental/Security/CWE/CWE-805/BufferAccessWithIncorrectLengthValue.ql",
]

JAVA_CWE_190 = [
    "$CODEQL_HOME/codeql-repo/java/ql/src/Security/CWE/CWE-190/ArithmeticTainted.ql",
    "$CODEQL_HOME/codeql-repo/java/ql/src/Security/CWE/CWE-190/ArithmeticTaintedLocal.ql",
    "$CODEQL_HOME/codeql-repo/java/ql/src/Security/CWE/CWE-190/ArithmeticUncontrolled.ql",
    "$CODEQL_HOME/codeql-repo/java/ql/src/Security/CWE/CWE-190/ArithmeticWithExtremeValues.ql",
    "$CODEQL_HOME/codeql-repo/java/ql/src/Security/CWE/CWE-190/ComparisonWithWiderType.ql",
]
```

To perform detection, you need to first create database for code snippets in a directory by typing:
```
codeql database create <path to database> --language=<language> --source-root=<directory to code snippest in language> --command=<build>
```

Then, you can type the following command for detection to specific CWE:
```
codeql database analyze --threads=10 <path to database> <CWE-Query> --format=csv --output=<output path>
```

For performing evaluation on 54 CWE code scenarios (You need to encode your OpenAI API), you can type the following commands:
```
python ChatGPT/CWE_Resolver.py -s Data/CWE -f p  # Regenerate code snippets. You can jump this step.

python CWE/CWEPREPROCESS.py

python CWE/CWEMARK.py -l py

python CWE/CWEMARK.py -l c
```

## Multi-round Fixing Process for Security Code Generation

We utilize jupyter to perform multi-round fixing process. We do not make it automatic since fixed results also need human chekcing for avoiding omitted vulnerabilities.

For convience, we provide all fixed results with manually checking in the repository.


## Data

All data including code snippets, prompts, fixed results and so on are stored in the Data folder.
