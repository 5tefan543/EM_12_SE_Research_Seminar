from __future__ import annotations
import os
import pickle
import random
from time import sleep
from time import time
import logging
import os
import json
from time import sleep
import pickle
import shelve
import json
import csv
import tiktoken

import leetcode
import leetcode.auth

from revChatGPT.V3 import Chatbot


class Analysis:
    header = ['problem_name', 'language', 'round1', 'round2', 'round3', 'round4', 'round5', 'final_status']

    prompt_template_1 = '''
    %s
    
    The code in %s below cannot pass all test cases:
    ```
    %s
    ```
    
    Error Message:
    %s
    
    Fix the code and generate the fixed code.
    '''

    prompt_template_2 = '''
    The fixed code still has error.
    ```
    %s
    ```
    
    The tested result of the code (error messages):
    %s
    
    Fix the code and generate the fixed code.
    '''

    leetcode_session = ''

    api_key = ""

    wa_workflow_csv = 'wa_workflow.csv'

    __CPP__ = '__cpp__'
    __JAVA__ = '__java__'
    __PYTHON3__ = '__python3__'
    __C__ = '__c__'
    __JAVASCRIPT__ = '__javascript__'

    LANGUAGE = {
        __CPP__: 'C++',
        __JAVA__: 'Java',
        __PYTHON3__: 'Python3',
        __C__: 'C',
        __JAVASCRIPT__: 'JavaScript',
    }

    EXTENSION = {
        __CPP__: '.cpp',
        __JAVA__: '.java',
        __PYTHON3__: '.py',
        __C__: '.c',
        __JAVASCRIPT__: '.js',
    }

    LANGUAGE_LOWERCASE = {
        __CPP__: 'cpp',
        __JAVA__: 'java',
        __PYTHON3__: 'python3',
        __C__: 'c',
        __JAVASCRIPT__: 'javascript',
    }

    @staticmethod
    def login_chatgpt() -> any:
        # Initialize chatbot
        chatbot = Chatbot(api_key=Analysis.api_key)

        print("Got chatbot successfully!")

        return chatbot


    @staticmethod
    def run(input_dir, output_dir):
        csv_path = 'wrong_answer_fix.csv'
        if not os.path.exists(csv_path):
            with open(csv_path, 'a', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(Analysis.header)


        with open('all_dict.pkl', 'rb') as f:
            all_dict = pickle.load(f)

        with open(Analysis.wa_workflow_csv, 'r') as csv_file:
            csv_reader = list(csv.reader(csv_file, delimiter=','))

        v1 = [i[0] for i in csv_reader[1:]]

        chatbot = Analysis.login_chatgpt()

        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0301")

        # Initialize client
        configuration = leetcode.Configuration()

        csrf_token: str = leetcode.auth.get_csrf_cookie(Analysis.leetcode_session)

        configuration.api_key["x-csrftoken"] = csrf_token
        configuration.api_key["csrftoken"] = csrf_token
        configuration.api_key["LEETCODE_SESSION"] = Analysis.leetcode_session
        configuration.api_key["Referer"] = "https://leetcode.com"
        configuration.debug = False

        api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

        with open('problem_all_complex.json', 'r') as f:
            problem_all_complex = json.load(f)

        stat_status_pairs = problem_all_complex['stat_status_pairs']
        problems_no_paid = [i for i in stat_status_pairs if i['paid_only'] is False]

        mapping = dict()

        for i in problems_no_paid:
            mapping[str(i['stat']['frontend_question_id'])] = str(i['stat']['question_id'])

        __counter__ = 0
        for i in v1:
            print(str(__counter__) + ' : ' + i)
            __counter__ += 1

            # if random.random() < 0.5:
            #     continue

            problem_name = i
            save_dir = output_dir + '/' + i
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)

            target_dir = input_dir + '/' + i
            v2 = list(os.listdir(target_dir))

            txt = [target_dir + '/' + i for i in v2 if i[-4:] == '.txt'][0]
            codes = [target_dir + '/' + i for i in v2 if not (i.startswith('AAAAA') or i.startswith('___'))]

            with open(txt, 'r') as f:
                content = f.read()

            for code_path in codes:
                # new session for ChatGPT
                chatbot.reset()

                if Analysis.__CPP__ in code_path:
                    lan = Analysis.LANGUAGE_LOWERCASE[Analysis.__CPP__]
                if Analysis.__C__ in code_path:
                    lan = Analysis.LANGUAGE_LOWERCASE[Analysis.__C__]
                if Analysis.__JAVA__ in code_path:
                    lan = Analysis.LANGUAGE_LOWERCASE[Analysis.__JAVA__]
                if Analysis.__PYTHON3__ in code_path:
                    lan = Analysis.LANGUAGE_LOWERCASE[Analysis.__PYTHON3__]
                if Analysis.__JAVASCRIPT__ in code_path:
                    lan = Analysis.LANGUAGE_LOWERCASE[Analysis.__JAVASCRIPT__]

                language = lan

                print('    ' + language)

                status = all_dict[problem_name][language]
                frontend_id = 0
                if status['status_msg'] == 'Wrong Answer':
                    last_testcase = 'Last test case: ' + status['last_testcase'] + '\n'
                    code_output = 'Code output: ' + status['code_output'] + '\n'
                    expected_output = 'Expected output: ' + status['expected_output']
                    error_messages = last_testcase + code_output + expected_output
                    question_id = status['question_id']
                else:
                    continue

                with open(code_path, 'r') as f:
                    code = f.read()

                # round0
                prompt_0 = Analysis.prompt_template_1 % (content, language, code, error_messages)
                with open(save_dir + '/' + 'prompt_0_%s.txt' % language, 'w') as f:
                    f.write(prompt_0)

                response = ''
                while True:
                    try:
                        response = chatbot.ask(prompt_0)
                    except Exception as e:
                        print(e)
                        sleep(60)
                        chatbot.rollback(n=1)
                        continue

                    with open(save_dir + '/' + 'response_0.txt', 'w') as f:
                        f.write(response)

                    first_index = response.find('```')
                    end_index = response.find('```', first_index + 3)
                    first_index = response.find('\n', first_index) + 1

                    if first_index < 0 or end_index < 0:
                        code = ''
                        sleep(60)
                        chatbot.rollback(n=2)
                        continue
                    else:
                        code = response[first_index:end_index]
                        with open(save_dir + '/' + 'code_1.txt', 'w') as f:
                            f.write(code)

                    break

                sleep(60)

                a_flag = 0
                status_list = []
                continue_flag = 1
                for count in range(5):
                    if continue_flag == 0:
                        break

                    # leetcode
                    submission = leetcode.Submission(
                        judge_type="large", typed_code=code, question_id=question_id, test_mode=False, lang=language
                    )

                    submission_id = api_instance.problems_problem_submit_post(
                        problem=problem_name, body=submission
                    )

                    sleep(6)

                    while True:
                        submission_result = api_instance.submissions_detail_id_check_get(
                            id=submission_id.submission_id
                        )

                        if len(submission_result) < 5:
                            sleep(3)
                        else:
                            break

                    with open(save_dir + '/' + 'json_%s.json' % (count + 1), 'w') as f:
                        json.dump(submission_result, f)

                    status = submission_result
                    if status['status_msg'] == 'Accepted':
                        status_list.append('Accepted')
                        a_flag = 1
                        break
                    elif status['status_msg'] == 'Wrong Answer':
                        status_list.append('Wrong Answer')
                        last_testcase = 'Last test case: ' + status['last_testcase'] + '\n'
                        code_output = 'Code output: ' + status['code_output'] + '\n'
                        expected_output = 'Expected output: ' + status['expected_output']
                        error_messages = last_testcase + code_output + expected_output
                    elif status['status_msg'] == 'Compile Error':
                        status_list.append('Compile Error')
                        if 'full_compile_error' in status.keys():
                            error_messages = status['full_compile_error']
                        else:
                            error_messages = status['compile_error']
                    elif status['status_msg'] == 'Time Limit Exceeded':
                        status_list.append('Time Limit Exceeded')
                        error_messages = 'Time Limit Exceeded.'
                    elif status['status_msg'] == 'Runtime Error':
                        status_list.append('Runtime Error')
                        if 'full_runtime_error' in status.keys():
                            error_messages = status['full_runtime_error']
                        else:
                            error_messages = status['runtime_error']
                    else:
                        status_list.append('Out of memory')
                        error_messages = 'Out of memory.'

                    encoded_list = encoding.encode(error_messages)
                    if len(encoded_list) > 200:
                        error_messages = encoding.decode(encoded_list[:200])

                    prompt_ = Analysis.prompt_template_2 % (code, error_messages)
                    with open(save_dir + '/' + 'prompt_%s.txt' % (count + 1), 'w') as f:
                        f.write(prompt_)

                    response = ''
                    counter = 0
                    continue_flag = 1
                    while True:
                        if counter == 5:
                            continue_flag = 0
                            break

                        try:
                            chatbot.add_to_conversation(prompt_, "user", convo_id='default')
                            if 4096 - chatbot.get_token_count() < 1000:
                                chatbot.rollback(n=1)
                                prompt_ = Analysis.prompt_template_1 % (content, language, code, error_messages)
                                chatbot.add_to_conversation(prompt_, "user", convo_id='default')
                                while 4096 - chatbot.get_token_count() < 1000:
                                    chatbot.conversation['default'].pop(1)
                            chatbot.rollback(n=1)
                            response = chatbot.ask(prompt_)
                        except Exception as e:
                            print(e)
                            sleep(60)
                            chatbot.rollback(n=1)
                            continue

                        with open(save_dir + '/' + 'response_%s.txt' % (count + 1), 'w') as f:
                            f.write(response)

                        first_index = response.find('```')
                        end_index = response.find('```', first_index + 3)
                        first_index = response.find('\n', first_index) + 1

                        if first_index < 0 or end_index < 0:
                            code = ''
                            sleep(60)
                            chatbot.rollback(n=2)
                            counter += 1
                            continue
                        else:
                            code = response[first_index:end_index]
                            with open(save_dir + '/' + 'code_%s.txt' % (count + 2), 'w') as f:
                                f.write(code)

                        break

                    sleep(60)

                r = 5 - len(status_list)
                for o in range(r):
                    status_list.append('_')

                if a_flag == 1:
                    status_list.append('A.')
                else:
                    status_list.append('U.')
                data = [problem_name, language] + status_list

                with open(csv_path, 'a', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(data)


if __name__ == '__main__':

    Analysis.run('rq1-sample-analysis', 'wa_workflow')  # Update the first parameter to the path containing error code snippets.

    print("All finished!---------------------------------")