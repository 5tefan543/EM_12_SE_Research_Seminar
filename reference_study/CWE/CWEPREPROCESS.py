from __future__ import annotations

import logging
import os
import json
import shutil
from time import sleep
import pickle
import shelve
import json
import subprocess

import leetcode
import leetcode.auth

START_NUMBER = 0  # 455
REST_GAP     = 400
HUMAN = True


class CWEPREPROCESS:
    @staticmethod
    def strip(source_read):
        for root, dirs, files in os.walk(source_read):
            if "gen_scenario" in dirs:
                gen_path = root + '/' + "gen_scenario_2"
                code_path = root + '/' + "code_scenario_2"

                if not os.path.exists(code_path):
                    os.mkdir(code_path)

                v1 = os.listdir(gen_path)
                v2 = [gen_path + '/' + i for i in v1]
                v3 = [code_path + '/' + i for i in v1]

                for name, gen, code__ in zip(v1, v2, v3):
                    with open(gen, 'r') as f:
                        content = f.read()

                    first_index = content.find('```')
                    end_index = content.find('```', first_index + 3)
                    first_index = content.find('\n', first_index) + 1

                    if first_index < 0 or end_index < 0:
                        continue
                    else:
                        code = content[first_index:end_index]

                    with open(code__, 'w') as f:
                        f.write(code)

    @staticmethod
    def copy_makefile(source_read):
        for root, dirs, files in os.walk(source_read):
            if "gen_scenario" in dirs:
                gen_path = root + '/' + "gen_scenario/Makefile"
                code_path = root + '/' + "code_scenario_2/Makefile"

                if os.path.exists(gen_path):
                    shutil.copy(gen_path, code_path)



if __name__ == '__main__':

    cwe_dir = "/mnt/disk4/ChatGPT-SCG-Supplementary/CWE"

    import csv

    for root, dirs, files in os.walk(cwe_dir):
        if "gen_scenario" in dirs:
            cwe_number = root.split('/')[-2]
            cwe_name = root.split('/')[-1]

            v1 = os.listdir(root)

            lan = ''
            for i in v1:
                if '.c' == i[-2:]:
                    lan = 'c'
                    break
                if '.py' == i[-3:]:
                    lan = 'python3'
                    break

            code_path = root + '/' + cwe_name + '__scenario_codeql_results.csv'

            file_name = set()
            try:
                with open(code_path, 'r') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for row in reader:
                        file_name.add(row[-5])
            except Exception as e:
                continue
            print(cwe_number)
            print(cwe_name)
            print(lan)
            print(len(file_name))
            print(file_name)
            print('-----------------------------------')
    pass
