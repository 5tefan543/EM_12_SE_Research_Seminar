import os
import pickle
import random
from time import sleep
from time import time

from revChatGPT.V3 import Chatbot

START_NUMBER = 0
REST_GAP     = 250

SLEEP_TIME_1 = 3600   # morning: 3600    night: 4000   1800
SLEEP_TIME_MIN = 10   # morning: 5    night: 10      10
SLEEP_TIME_MAX = 15   # morning: 11   night: 20       15

class Resolver:
    supplementary_prefix = '/mnt/disk4/ChatGPT-SCG-Supplementary'
    GPT_PROMPT = 'gpt_prompt'
    AF = 'Af'
    BE = 'Be'

    ALG = 'alg'
    DB = 'db'
    CON = 'con'

    ALG_RES = 'alg_res'
    DB_RES = 'db_res'
    CON_RES = 'con_res'

    TOPIC_DICT = {
        'a': ALG,
        'd': DB,
        'c': CON
    }

    RES_DICT = {
        'a': ALG_RES,
        'd': DB_RES,
        'c': CON_RES
    }

    CPP = 'cpp'
    JAVA = 'java'
    PYTHON3 = 'python3'
    C = 'c'
    JAVASCRIPT = 'javascript'
    MYSQL = 'mysql'

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
    RES = 'res__'

    api_key = ""

    RM_CONV_GAP = 20

    GEN_TIMES = 5

    @staticmethod
    def login_chatgpt() -> any:
        # Initialize chatbot
        chatbot = Chatbot(api_key=Resolver.api_key)

        print("Got chatbot successfully!")

        return chatbot

    @staticmethod
    def resolve(names, paths, save_dir, time_saver_path):
        global START_NUMBER
        global REST_GAP

        number = len(paths)

        names = names[START_NUMBER:]
        paths = paths[START_NUMBER:]

        chatbot = Resolver.login_chatgpt()


        interval = 0
        print("Start resolving now!---------------------------------")
        for name, code_path, counter in zip(names, paths, range(len(paths))):
            sleep(5)

            counter += START_NUMBER

            print('    Resolving: %s %d' % (name, counter))
            print('    ----Estimated time: %.2fh' % float(interval * (number - counter) * 5 / 3600))

            with open(code_path, 'r') as f:
                # Prompt for ChatGPT
                prompt = f.read()

            for i in range(Resolver.GEN_TIMES):  # e.g., 5 times
                try:
                    start = time()
                    response = chatbot.ask(prompt)
                    interval = time() - start
                except Exception as e:
                    print(e)
                    continue

                # Save answer
                save_path = save_dir + Resolver.SEP + \
                            Resolver.RES + name[:-len(Resolver.TXT)] + '__%d' % (i + 1) + Resolver.TXT
                with open(save_path, 'w') as f:
                    # Save response from ChatGPT
                    f.write(response)

                chatbot.rollback(n=2)

    @staticmethod
    def run(choice, topic):
        res_dir = Resolver.RES_DICT[topic]
        topic   = Resolver.TOPIC_DICT[topic]

        if choice == 'af':
            save_dir = Resolver.supplementary_prefix + Resolver.SEP + \
                       Resolver.GPT_PROMPT + Resolver.SEP + Resolver.AF + Resolver.SEP + res_dir
            read_dir = Resolver.supplementary_prefix + Resolver.SEP + \
                       Resolver.GPT_PROMPT + Resolver.SEP + Resolver.AF + Resolver.SEP + topic
        elif choice == 'be':
            save_dir = Resolver.supplementary_prefix + Resolver.SEP + \
                       Resolver.GPT_PROMPT + Resolver.SEP + Resolver.BE + Resolver.SEP + res_dir
            read_dir = Resolver.supplementary_prefix + Resolver.SEP + \
                       Resolver.GPT_PROMPT + Resolver.SEP + Resolver.BE + Resolver.SEP + topic
        else:
            return

        all_prompt_names = os.listdir(read_dir)
        all_prompt_paths = [read_dir + Resolver.SEP + i for i in all_prompt_names]

        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        time_saver_path = 'time_saver_' + choice + '_' + topic + Resolver.PKL
        Resolver.resolve(all_prompt_names, all_prompt_paths, save_dir, time_saver_path)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Ask ChatCPT LeetCode problems')

    parser.add_argument('-c', type=str, default='af',
                        help='Choice. af: problems after 2021; '
                             'be: problems before 2021.')
    parser.add_argument('-t', type=str, default='a',
                        help='Topic. a: algorithm; '
                             'd: database; c: concurrency.')

    args = parser.parse_args()

    CHOICE = args.c
    TOPIC = args.t

    Resolver.run(CHOICE, TOPIC)

    print("All finished!---------------------------------")
