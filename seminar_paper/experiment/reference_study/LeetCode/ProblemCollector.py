"""
This file is used to get leetcode problems from https://leetcode.com/problemset/all/ by using python-leetcode.
"""

from __future__ import annotations

import logging
import os
import json
from time import sleep
import pickle

import leetcode
import leetcode.auth


class ProblemCollector:
    supplementary_prefix = '/mnt/disk4/ChatGPT-SCG-Supplementary'
    ORI_RES = 'OriRes-LeetCode'  # OriginalResponse-LeetCode
    GPT_PROMPT = 'gpt_prompt'
    AF = 'Af'
    BE = 'Be'

    ALG = 'alg'
    DB  = 'db'
    CON = 'con'

    CPP        = 'cpp'
    JAVA       = 'java'
    PYTHON3    = 'python3'
    C          = 'c'
    JAVASCRIPT = 'javascript'
    MYSQL      = 'mysql'

    LANGUAGE_SUFFIX_DICT = {
        'C++': CPP,
        'Java': JAVA,
        'Python3': PYTHON3,
        'C': C,
        'JavaScript': JAVASCRIPT,
        'MySQL': MYSQL
    }

    SEP = '/'
    COLON = ':'
    PKL = '.pkl'
    TXT = '.txt'

    leetcode_session = ''

    problem_all_complex_path = 'problem_all_complex.json'
    TIME_SEP = 2124
    QUERY = """
        query getQuestionDetail($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            boundTopicId
            title
            content
            translatedTitle
            isPaidOnly
            difficulty
            likes
            dislikes
            isLiked
            similarQuestions
            contributors {
              username
              profileUrl
              avatarUrl
              __typename
            }
            langToValidPlayground
            topicTags {
              name
              slug
              translatedName
              __typename
            }
            companyTagStats
            codeSnippets {
              lang
              langSlug
              code
              __typename
            }
            stats
            codeDefinition
            hints
            solution {
              id
              canSeeDetail
              __typename
            }
            status
            sampleTestCase
            enableRunCode
            metaData
            translatedContent
            judgerAvailable
            judgeType
            mysqlSchemas
            enableTestMode
            envInfo
            __typename
          }
        }
    """

    ALG_LANGUAGE = ['C++', 'Java', 'Python3', 'C', 'JavaScript']
    DB_LANGUAGE  = ['MySQL']
    CON_LANGUAGE = ['C++', 'Java', 'Python3', 'C']
    LANGUAGE_DICT = {
        ALG: ALG_LANGUAGE,
        DB: DB_LANGUAGE,
        CON: CON_LANGUAGE
    }

    ALG_TYPE = 19  # equal to the number of code snippets
    DB_TYPE  = 3   # equal
    CON_TYPE = 6   # equal

    """
    Prompt Template:
    
    <Question>   # one LeetCode porblem
    
    [<Example>,]
    
    Template:
    ```
    <Code Snippet>
    ```
    
    Generate the code in <LANGUAGE> form (only generate code. Do not attach any other statements before and after 
    the generated code).
    """

    PROMPT = """
%s

Template:
```
%s
```

Generate the code in %s form (only generate code. Do not attach any other statements before and after the generated code).
    """

    @staticmethod
    def login_leetcode() -> any:
        '''
        Use your session (Chrome) to login leetcode.

        :return: connection instance used for subsequent processes.
        '''
        # Initialize client
        configuration = leetcode.Configuration()

        leetcode_session: str = ProblemCollector.leetcode_session
        csrf_token: str = leetcode.auth.get_csrf_cookie(leetcode_session)

        configuration.api_key["x-csrftoken"] = csrf_token
        configuration.api_key["csrftoken"] = csrf_token
        configuration.api_key["LEETCODE_SESSION"] = leetcode_session
        configuration.api_key["Referer"] = "https://leetcode.com"
        configuration.debug = False

        api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

        return api_instance

    @staticmethod
    def collect():
        # Build directories
        ori_res_dir = ProblemCollector.supplementary_prefix + ProblemCollector.SEP + ProblemCollector.ORI_RES
        if not os.path.exists(ori_res_dir):
            os.mkdir(ori_res_dir)

        af_dir = ori_res_dir + ProblemCollector.SEP + ProblemCollector.AF
        if not os.path.exists(af_dir):
            os.mkdir(af_dir)

        be_dir = ori_res_dir + ProblemCollector.SEP + ProblemCollector.BE
        if not os.path.exists(be_dir):
            os.mkdir(be_dir)

        # Login LeetCode
        api_instance = ProblemCollector.login_leetcode()

        # Read all problem title slugs
        with open(ProblemCollector.problem_all_complex_path, 'r') as f:
            problem_all_complex = json.load(f)

        stat_status_pairs = problem_all_complex['stat_status_pairs']

        # Retain problems frontend_question_id > 2124, which are the ones after 2021 (start from 2022 Jan 01).
        problems_no_paid = [i for i in stat_status_pairs if i['paid_only'] is False]
        problems_need_paid = [i for i in stat_status_pairs if i['paid_only'] is True]

        # Get all question title slugs
        title_slugs_af_2021 = [i['stat']['question__title_slug'] for i in problems_no_paid if
                               i['stat']['frontend_question_id'] >= ProblemCollector.TIME_SEP]
        title_slugs_be_2021 = [i['stat']['question__title_slug'] for i in problems_no_paid if
                               i['stat']['frontend_question_id'] < ProblemCollector.TIME_SEP]

        # Query! After 2021 first
        print("Collecting problems after 2021. --------------------")
        counter = 1
        for title_slug in title_slugs_af_2021:
            graphql_request = leetcode.GraphqlQuery(
                query=ProblemCollector.QUERY,
                variables=leetcode.GraphqlQueryGetQuestionDetailVariables(title_slug=title_slug),
                operation_name="getQuestionDetail",
            )

            try:
                response = api_instance.graphql_post(body=graphql_request)
            except Exception as e:
                print(e)
                sleep(5)
                continue


            file_name = response.data.question.question_frontend_id + ProblemCollector.COLON + title_slug + \
                        ProblemCollector.PKL
            save_path = af_dir + ProblemCollector.SEP + file_name

            with open(save_path, 'wb') as f:
                pickle.dump(response, f)

            print("    num: " + str(counter) + ' ' + file_name)
            counter += 1

            sleep(1)

        # Query! Before 2021 first
        print("Collecting problems before 2021. ----------")
        counter = 1
        for title_slug in title_slugs_be_2021:
            graphql_request = leetcode.GraphqlQuery(
                query=ProblemCollector.QUERY,
                variables=leetcode.GraphqlQueryGetQuestionDetailVariables(title_slug=title_slug),
                operation_name="getQuestionDetail",
            )

            try:
                response = api_instance.graphql_post(body=graphql_request)
            except Exception as e:
                print(e)
                sleep(5)
                continue

            file_name = response.data.question.question_frontend_id + ProblemCollector.COLON + title_slug + \
                        ProblemCollector.PKL
            save_path = be_dir + ProblemCollector.SEP + file_name

            with open(save_path, 'wb') as f:
                pickle.dump(response, f)

            print("    num: " + str(counter) + ' ' + file_name)
            counter += 1

            sleep(1)

    @staticmethod
    def process():
        # Check whether phase 1 is run
        ori_res_dir = ProblemCollector.supplementary_prefix + ProblemCollector.SEP + ProblemCollector.ORI_RES

        ori_af_dir = ori_res_dir + ProblemCollector.SEP + ProblemCollector.AF
        if not os.path.exists(ori_af_dir):
            exit(1)

        ori_be_dir = ori_res_dir + ProblemCollector.SEP + ProblemCollector.BE
        if not os.path.exists(ori_be_dir):
            exit(1)

        # Build directories
        gpt_prom_dir = ProblemCollector.supplementary_prefix + ProblemCollector.SEP + ProblemCollector.GPT_PROMPT
        if not os.path.exists(gpt_prom_dir):
            os.mkdir(gpt_prom_dir)

        af_dir = gpt_prom_dir + ProblemCollector.SEP + ProblemCollector.AF
        if not os.path.exists(af_dir):
            os.mkdir(af_dir)

        be_dir = gpt_prom_dir + ProblemCollector.SEP + ProblemCollector.BE
        if not os.path.exists(be_dir):
            os.mkdir(be_dir)

        af__dir_dict = {}
        be__dir_dict = {}
        for i in [ProblemCollector.ALG, ProblemCollector.DB, ProblemCollector.CON]:
            t1 = af_dir + ProblemCollector.SEP + i
            if not os.path.exists(t1):
                os.mkdir(t1)
            af__dir_dict[i] = t1

            t2 = be_dir + ProblemCollector.SEP + i
            if not os.path.exists(t2):
                os.mkdir(t2)
            be__dir_dict[i] = t2

        # Process after 2021
        v1 = os.listdir(ori_af_dir)
        v2 = [ori_af_dir + ProblemCollector.SEP + i for i in v1]

        for file_name, file_path in zip(v1, v2):
            with open(file_path, 'rb') as f:
                res = pickle.load(f)

            # Judge the problem's topic
            question = res.data.question
            ty = len(question.code_snippets)

            if ty == ProblemCollector.ALG_TYPE:
                # Algorithm topic
                to  = ProblemCollector.ALG
                lan = ProblemCollector.ALG_LANGUAGE
            elif ty == ProblemCollector.DB_TYPE:
                # Database topic
                to  = ProblemCollector.DB
                lan = ProblemCollector.DB_LANGUAGE
            elif ty == ProblemCollector.CON_TYPE:
                # Concurrency topic
                to  = ProblemCollector.CON
                lan = ProblemCollector.CON_LANGUAGE
            else:
                to  = ProblemCollector.ALG
                lan = ProblemCollector.ALG_LANGUAGE

            save_dir            = af__dir_dict[to]
            question_content    = question.content
            question_difficulty = question.difficulty
            for code_snippet in question.code_snippets:
                if code_snippet.lang in lan:
                    code_snippet_lan = code_snippet.lang
                    code_suffix      = '__' + ProblemCollector.LANGUAGE_SUFFIX_DICT[code_snippet_lan]
                    code_name        = question_difficulty + '__' + file_name[:-len(ProblemCollector.PKL)] + \
                                       code_suffix + ProblemCollector.TXT

                    question_template = code_snippet.code

                    """
                    Content: question_content
                    
                    Template: question_template
                    
                    Language: code_snippet_lan
                    """

                    code_prompt = ProblemCollector.PROMPT % (question_content,
                                                             question_template,
                                                             code_snippet_lan)

                    # Save
                    save_path = save_dir + ProblemCollector.SEP + code_name
                    with open(save_path, 'w') as f:
                        f.writelines(code_prompt)

        # Process before 2021
        v1 = os.listdir(ori_be_dir)
        v2 = [ori_be_dir + ProblemCollector.SEP + i for i in v1]

        for file_name, file_path in zip(v1, v2):
            with open(file_path, 'rb') as f:
                res = pickle.load(f)

            # Judge the problem's topic
            question = res.data.question
            ty = len(question.code_snippets)

            if ty == ProblemCollector.ALG_TYPE:
                # Algorithm topic
                to = ProblemCollector.ALG
                lan = ProblemCollector.ALG_LANGUAGE
            elif ty == ProblemCollector.DB_TYPE:
                # Database topic
                to = ProblemCollector.DB
                lan = ProblemCollector.DB_LANGUAGE
            elif ty == ProblemCollector.CON_TYPE:
                # Concurrency topic
                to = ProblemCollector.CON
                lan = ProblemCollector.CON_LANGUAGE
            else:
                to = ProblemCollector.ALG
                lan = ProblemCollector.ALG_LANGUAGE

            save_dir = be__dir_dict[to]
            question_content = question.content
            question_difficulty = question.difficulty
            for code_snippet in question.code_snippets:
                if code_snippet.lang in lan:
                    code_snippet_lan = code_snippet.lang
                    code_suffix = '__' + ProblemCollector.LANGUAGE_SUFFIX_DICT[code_snippet_lan]
                    code_name = question_difficulty + '__' + file_name[:-len(ProblemCollector.PKL)] + \
                                code_suffix + ProblemCollector.TXT

                    question_template = code_snippet.code

                    """
                    Content: question_content

                    Template: question_template

                    Language: code_snippet_lan
                    """

                    code_prompt = ProblemCollector.PROMPT % (question_content,
                                                             question_template,
                                                             code_snippet_lan)

                    # Save
                    save_path = save_dir + ProblemCollector.SEP + code_name
                    with open(save_path, 'w') as f:
                        f.writelines(code_prompt)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Collect problems in LeetCode.')

    parser.add_argument('-p', type=str,
                        help='Collecting phases. 1: directly collecting problems; '
                             '2: get prompts of problems in different languages.')

    args = parser.parse_args()

    if not args.p:
        logging.error("Wrong args!")
        exit(1)

    PHASE = args.p

    if PHASE == '1':
        # Directly collecting problems without any fining process
        ProblemCollector.collect()
    elif PHASE == '2':
        # Get prompts of LeetCode problems
        ProblemCollector.process()
