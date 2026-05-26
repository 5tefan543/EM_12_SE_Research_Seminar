import os
import pickle
import random
from time import sleep
from time import time

from revChatGPT.V3 import Chatbot

START_NUMBER_1 = 15
START_NUMBER_2 = 0
START_NUMBER_3 = 26
I_START_NUMBER = 20


class Resolver:
    SEP = '/'
    COLON = ':'
    PKL = '.pkl'
    TXT = '.txt'
    RES = 'res__'

    api_key = ""

    GEN_TIMES = 60  # 20  40  60

    chatbot = None

    prompt = """
```
%s
```

Complement the code (only complement code. Do not attach any other statements before and after the generated code).    
"""

    @staticmethod
    def login_chatgpt() -> any:
        # Initialize chatbot
        chatbot = Chatbot(api_key=Resolver.api_key)

        print("Got chatbot successfully!")

        return chatbot

    @staticmethod
    def resolve(names, paths):
        global START_NUMBER
        global REST_GAP

        number = len(paths)

        names = names[START_NUMBER:]
        paths = paths[START_NUMBER:]

        chatbot = Resolver.login_chatgpt()

        interval = 0
        print("Start resolving now!---------------------------------")
        for name, code_path, counter in zip(names, paths, range(len(paths))):
            sleep(6)

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

                chatbot.rollback(n=2)

    @staticmethod
    def run(source, function):
        global START_NUMBER_1

        all_cwes = os.listdir(source)
        all_cwe_paths = [source + Resolver.SEP + i for i in all_cwes]

        if function == 'p':
            Resolver.generate_prompt(all_cwes[START_NUMBER_1:], all_cwe_paths[START_NUMBER_1:])

    @staticmethod
    def generate_prompt(all_cwes, all_cwe_paths):
        global START_NUMBER_1
        Resolver.chatbot = Resolver.login_chatgpt()

        counter = 0
        for cwe, path in zip(all_cwes, all_cwe_paths):
            print('Start for cwe: %d' % (counter + START_NUMBER_1))
            Resolver.generate_prompt_internal(cwe, path)
            counter += 1

    @staticmethod
    def generate_prompt_internal(cwe, path):
        global START_NUMBER_2
        global START_NUMBER_3

        examples = os.listdir(path)
        example_paths = [path + Resolver.SEP + i for i in examples if os.path.isdir(path + Resolver.SEP + i)]
        examples = [i for i in examples if os.path.isdir(path + Resolver.SEP + i)]

        example_paths = example_paths[START_NUMBER_2:]
        examples = examples[START_NUMBER_2:]

        lan = ''
        file_path = ''

        counter_1 = 0
        for example_path, example_name in zip(example_paths, examples):
            print('    Start for example: %d' % (counter_1 + START_NUMBER_2) + ':' + example_name)

            if os.path.exists(example_path + Resolver.SEP + 'scenario.py'):
                file_path = example_path + Resolver.SEP + 'scenario.py'
                lan = '.py'
            elif os.path.exists(example_path + Resolver.SEP + 'scenario.c'):
                file_path = example_path + Resolver.SEP + 'scenario.c'
                lan = '.c'

            with open(file_path, 'r') as f:
                code = f.read()

            prompt = Resolver.prompt % code

            # prompt_path = example_path + Resolver.SEP + cwe + '_' + example_name + '_prompt.txt'

            # with open(prompt_path, 'w') as f:
            #     f.write(prompt)

            generated_code_dir = example_path + Resolver.SEP + 'gen_scenario'

            counter_2 = 0
            for i in range(Resolver.GEN_TIMES)[START_NUMBER_3:]:  # e.g., 5 times
                print('        Generate code: %d' % (counter_2 + START_NUMBER_3))
                counter_2 += 1

                try:
                    start = time()
                    response = Resolver.chatbot.ask(prompt)
                    interval = time() - start
                except Exception as e:
                    print(e)
                    sleep(75)
                    continue

                # Save answer
                save_path = generated_code_dir + Resolver.SEP + 'generated-code__' + cwe + '_' + \
                            example_name + '__%d' % (i + I_START_NUMBER) + lan
                with open(save_path, 'w') as f:
                    # Save response from ChatGPT
                    f.write(response)

                Resolver.chatbot.rollback(n=2)

                sleep(60)

            START_NUMBER_3 = 0

            counter_1 += 1

        START_NUMBER_2 = 0


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Ask ChatCPT problems related to CWE.')

    parser.add_argument('-s', type=str,
                        help='Source')

    parser.add_argument('-f', type=str,
                        help='Functon.p&q.')

    args = parser.parse_args()

    SOURCE = args.s
    FUNCTION = args.f

    Resolver.run(SOURCE, FUNCTION)

    print("All finished!---------------------------------")
