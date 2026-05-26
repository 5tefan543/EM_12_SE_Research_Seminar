from __future__ import annotations

import logging
import os
import json
from time import sleep
import pickle
import shelve
import json

import leetcode
import leetcode.auth

START_NUMBER = 0
REST_GAP     = 400
HUMAN = False

MAX_COUNTER = 373
LAN_GEN = None

class Judgement:
    leetcode_session = ''

    CPP = 'cpp'
    JAVA = 'java'
    PYTHON3 = 'python3'
    C = 'c'
    JAVASCRIPT = 'javascript'
    MYSQL = 'mysql'

    problem_all_complex_path = 'problem_all_complex.json'

    EXTENSION = {
        CPP: '.cpp',
        JAVA: '.java',
        PYTHON3: '.py',
        C: '.c',
        JAVASCRIPT: '.js',
        MYSQL: '.sql'
    }

    LANGUAGE = {
        CPP: 'C++',
        JAVA: 'Java',
        PYTHON3: 'Python3',
        C: 'C',
        JAVASCRIPT: 'JavaScript',
        MYSQL: 'SQL'
    }

    __CPP__ = '__cpp__'
    __JAVA__ = '__java__'
    __PYTHON3__ = '__python3__'
    __C__ = '__c__'
    __JAVASCRIPT__ = '__javascript__'
    __MYSQL__ = '__mysql__'

    PROMPT = """The original code in %s:
```
%s
```

Template:
```
%s
```

Translate the code into %s form (only translate code. Do not attach any other statements before and after the translated code).
        """

    @staticmethod
    def strip(source_read, target_save):
        v1 = [i for i in os.listdir(source_read)]
        v2 = [source_read + '/' + i for i in os.listdir(source_read)]

        v3 = []
        for i in v1:
            if Judgement.__CPP__ in i:
                v3.append(Judgement.CPP)
            elif Judgement.__JAVA__ in i:
                v3.append(Judgement.JAVA)
            elif Judgement.__PYTHON3__ in i:
                v3.append(Judgement.PYTHON3)
            elif Judgement.__C__ in i:
                v3.append(Judgement.C)
            elif Judgement.__JAVASCRIPT__ in i:
                v3.append(Judgement.JAVASCRIPT)
            elif Judgement.__MYSQL__ in i:
                v3.append(Judgement.MYSQL)

        for name, path, lan in zip(v1, v2, v3):
            target_path = target_save + '/' + name[:-4] + Judgement.EXTENSION[lan]

            with open(path, 'r') as f:
                content = f.read()

            first_index = content.find('```')
            end_index = content.find('```', first_index + 3)
            first_index = content.find('\n', first_index) + 1

            if first_index < 0 or end_index < 0:
                code = ''
            else:
                code = content[first_index:end_index]

            with open(target_path, 'w') as f:
                f.write(code)

    @staticmethod
    def translate(source_read, target_save, language):
        relay_dir = '/mnt/disk4/ChatGPT-SCG-Supplementary/OriRes-LeetCode/all'
        ALG_LANGUAGE = {Judgement.CPP: 'C++',
                        Judgement.JAVA: 'Java',
                        Judgement.PYTHON3: 'Python3',
                        Judgement.C: 'C',
                        Judgement.JAVASCRIPT: 'JavaScript'}

        source_code = language[:language.find(':')]
        target_code = language[language.find(':') + 1:]

        v1 = [i for i in os.listdir(source_read) if '__' + source_code + '__' in i]
        v2 = [source_read + '/' + i for i in v1]

        for name, path in zip(v1, v2):
            target_path = target_save + '/' + name[:name.rfind('.')].replace('__' + source_code + '__',
                                                                             '__' + target_code + '__') + '.txt'

            with open(path, 'r') as f:
                code = f.read()

            t1 = name.find(':')
            t2 = name.rfind('__', 0, t1) + 2
            t3 = name.find('__', t1)

            relay_name = name[t2:t3]
            relay_path = relay_dir + '/' + relay_name + '.pkl'
            with open(relay_path, 'rb') as f:
                res = pickle.load(f)

            question = res.data.question

            code_template = ''
            for code_snippet in question.code_snippets:
                if code_snippet.lang == ALG_LANGUAGE[target_code]:
                    code_template = code_snippet.code
                    break


            prompt = Judgement.PROMPT % (Judgement.LANGUAGE[source_code],
                                         code, code_template, Judgement.LANGUAGE[target_code]
                                         )

            # Save
            with open(target_path, 'w') as f:
                f.write(prompt)

    @staticmethod
    def translate_human(source_read, target_save, language):
        relay_dir = '/mnt/disk4/ChatGPT-SCG-Supplementary/OriRes-LeetCode/all'
        ALG_LANGUAGE = {Judgement.CPP: 'C++',
                        Judgement.JAVA: 'Java',
                        Judgement.PYTHON3: 'Python3',
                        Judgement.C: 'C',
                        Judgement.JAVASCRIPT: 'JavaScript'}

        v0 = [i for i in os.listdir(relay_dir)]
        mapping = dict()
        for i in v0:
            i = i[:-4]
            f_id = i[:i.find(':')]
            name = i[i.find(':') + 1:]
            mapping[name] = f_id


        source_code = language[:language.find(':')]
        target_code = language[language.find(':') + 1:]

        v1 = [i for i in os.listdir(source_read)]
        v2 = [source_read + '/' + i for i in v1]

        for name, path in zip(v1, v2):
            target_path = target_save + '/' + name[:name.rfind('.')] + '__' + target_code + '__' + '.txt'

            with open(path, 'r') as f:
                code = f.read()

            pure_name = name[:name.rfind('.')]
            if pure_name not in list(mapping.keys()):
                continue

            relay_name = mapping[pure_name] + ':' + pure_name
            relay_path = relay_dir + '/' + relay_name + '.pkl'
            with open(relay_path, 'rb') as f:
                res = pickle.load(f)

            question = res.data.question

            code_template = ''
            for code_snippet in question.code_snippets:
                if code_snippet.lang == ALG_LANGUAGE[target_code]:
                    code_template = code_snippet.code
                    break

            prompt = Judgement.PROMPT % (Judgement.LANGUAGE[source_code],
                                         code, code_template, Judgement.LANGUAGE[target_code]
                                         )

            # Save
            with open(target_path, 'w') as f:
                f.write(prompt)

    @staticmethod
    def send(source_read, target_save):
        global START_NUMBER
        global MAX_COUNTER
        global LAN_GEN

        with open('v7.pkl', 'rb') as f:
            v7 = pickle.load(f)

        v6 = []
        for i in v7.keys():
            v6.append(v7[i])

        # Read all problem title slugs
        with open(Judgement.problem_all_complex_path, 'r') as f:
            problem_all_complex = json.load(f)

        stat_status_pairs = problem_all_complex['stat_status_pairs']
        problems_no_paid = [i for i in stat_status_pairs if i['paid_only'] is False]

        mapping = dict()

        for i in problems_no_paid:
            mapping[str(i['stat']['frontend_question_id'])] = str(i['stat']['question_id'])

        # Initialize client
        configuration = leetcode.Configuration()

        csrf_token: str = leetcode.auth.get_csrf_cookie(Judgement.leetcode_session)

        configuration.api_key["x-csrftoken"] = csrf_token
        configuration.api_key["csrftoken"] = csrf_token
        configuration.api_key["LEETCODE_SESSION"] = Judgement.leetcode_session
        configuration.api_key["Referer"] = "https://leetcode.com"
        configuration.debug = False

        api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

        v1 = [i for i in os.listdir(source_read)]
        v2 = [source_read + '/' + i for i in os.listdir(source_read)]

        v3 = []
        for i in v1:
            if Judgement.__CPP__ in i:
                v3.append(Judgement.CPP)
            elif Judgement.__JAVA__ in i:
                v3.append(Judgement.JAVA)
            elif Judgement.__PYTHON3__ in i:
                v3.append(Judgement.PYTHON3)
            elif Judgement.__C__ in i:
                v3.append(Judgement.C)
            elif Judgement.__JAVASCRIPT__ in i:
                v3.append(Judgement.JAVASCRIPT)
            elif Judgement.__MYSQL__ in i:
                v3.append(Judgement.MYSQL)

        v1 = v1[START_NUMBER:]
        v2 = v2[START_NUMBER:]
        v3 = v3[START_NUMBER:]

        counter = 0
        number = 0
        for name, path, lan in zip(v1, v2, v3):
            # res__1-bit-and-2-bit-characters__cpp__1.cpp
            first_idx = 5
            end_idx = name.find('__', first_idx)
            problem_name = name[first_idx:end_idx]
            if problem_name in list(v7.keys()):
                problem_id = v7[problem_name]
            else:
                problem_id = -1

            if lan != LAN_GEN or problem_id not in v6:
                counter += 1
                continue

            if number == MAX_COUNTER:
                break

            number += 1

            if (counter + 1) % REST_GAP == 0:
                api_instance = None
                sleep(180)
                # Initialize client
                configuration = leetcode.Configuration()

                csrf_token: str = leetcode.auth.get_csrf_cookie(Judgement.leetcode_session)

                configuration.api_key["x-csrftoken"] = csrf_token
                configuration.api_key["csrftoken"] = csrf_token
                configuration.api_key["LEETCODE_SESSION"] = Judgement.leetcode_session
                configuration.api_key["Referer"] = "https://leetcode.com"
                configuration.debug = False

                api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

            print(str(counter + START_NUMBER) + ':' + name)
            counter += 1

            target_path = target_save + '/' + name[:name.rfind('.')] + '.json'

            with open(path, 'r') as f:
                code = f.read()

            submission = leetcode.Submission(
                judge_type="large", typed_code=code, question_id=mapping[problem_id], test_mode=False, lang=lan
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

            with open(target_path, 'w') as f:
                json.dump(submission_result, f)

            sleep(70)

    @staticmethod
    def run(source, target, function, language):
        global START_NUMBER
        global HUMAN
        global LAN_GEN
        if not os.path.exists(source):
            print("Source path not exists...")
            exit(-1)

        if not os.path.exists(target):
            os.makedirs(target)

        source_read = source[:]
        target_save = target[:]

        if function == "STRIP":
            Judgement.strip(source_read, target_save)
        elif function == "JUDGE":
            for LAN_GEN in [# Judgement.JAVA,
                            # Judgement.PYTHON3,
                            # Judgement.CPP,
                            # Judgement.JAVASCRIPT,
                            Judgement.C]:
                Judgement.send(source_read, target_save)
                START_NUMBER = 0
        elif function == "TRANSLATE":
            if HUMAN:
                Judgement.translate_human(source_read, target_save, language)
            else:
                Judgement.translate(source_read, target_save, language)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process feedbacks from ChatGPT.')

    parser.add_argument('-s', type=str,
                        help='Source.')
    parser.add_argument('-t', type=str,
                        help='Target.')
    parser.add_argument('-f', type=str,
                        help='Function. STRIP '
                             'or JUDGE '
                             'or TRANSLATE.')
    parser.add_argument('-l', type=str, default='cpp:python3',
                        help='Language. cpp, c, python3, java, javascript. (e.g., cpp:python3)')

    args = parser.parse_args()

    SOURCE = args.s
    TARGET = args.t
    FUNCTION = args.f
    LANGUAGE = args.l

    Judgement.run(SOURCE, TARGET, FUNCTION, LANGUAGE)

    print("All finished!---------------------------------")
