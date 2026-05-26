import os
import subprocess
import re
import config
import json
import copy


def get_mark_setups_for_dir(source_dir):
    # find all chatgpt generated files
    mark_setups = []

    for root, dirs, files in os.walk(source_dir):
        if 'mark_setup.json' in files:
            file = 'mark_setup.json'

            with open(os.path.join(root, file), 'r') as mark_setup_file_handle:
                mark_setup_json = mark_setup_file_handle.read()
                mark_setup_dict = json.loads(mark_setup_json)

            if config.CODE_DIR in dirs:
                d = config.CODE_DIR
                scenario_name = "scenario"

                mark_dict = copy.deepcopy(mark_setup_dict)

                # add the fields from the original mark_setup_file
                mark_dict['mark_setup_dir'] = root
                mark_dict['mark_setup_file_name'] = file
                mark_dict['gen_dir'] = d
                mark_dict['scenario_name'] = scenario_name
                mark_dict['deep_scenario_name'] = os.path.basename(root)

                # append to mark_setups
                mark_setups.append(mark_dict)
    return mark_setups


def main(lan):
    counter_1 = 0
    counter_2 = 0


    mark_setups = get_mark_setups_for_dir("/mnt/disk4/ChatGPT-SCG-Supplementary/CWE")

    # print(mark_setups)

    # for each mark_setup, run the codeQL analysis if requested
    for mark_setup in mark_setups:
        if 'check_ql' not in mark_setup:
            print(mark_setup['mark_setup_dir'])
            counter_1 += 1
            continue

        counter_2 += 1

        db_name = "codeql-db"
        results_csv_name = config.INTERMEDIATE_RESULT_FILE
        if mark_setup['scenario_name'] != "":
            db_name = mark_setup['scenario_name'] + "_" + db_name
            results_csv_name = mark_setup['deep_scenario_name'] + "__" + \
                               mark_setup['scenario_name'] + "_" + results_csv_name

        # check if the results csv file exists
        # if os.path.isfile(os.path.join(mark_setup['mark_setup_dir'], results_csv_name)):
        #     print("Results file already exists, skipping: " + os.path.join(mark_setup['mark_setup_dir'],
        #                                                                    results_csv_name))
        #     continue

        cmd = ""

        # if mark_setup['language'] == 'python' and (lan == 'py' or True):
        #     cmd = "codeql database create {} --language=python --overwrite --source-root {} && codeql database analyze --threads=4 {} {} --format=csv --output={}"
        #     cmd = cmd.format(os.path.join(mark_setup['mark_setup_dir'], db_name),
        #                      os.path.join(mark_setup['mark_setup_dir'], mark_setup['gen_dir']),
        #                      os.path.join(mark_setup['mark_setup_dir'], db_name),
        #                      mark_setup['check_ql'],
        #                      os.path.join(mark_setup['mark_setup_dir'], results_csv_name))
        #
        # elif mark_setup['language'] == 'c' and (lan == 'c' or True):
        #     cmd = "codeql database create {} --language=cpp --overwrite --command=\"make -B\" --source-root {} && codeql database analyze --threads=4 {} {} --format=csv --output={}"
        #     cmd = cmd.format(os.path.join(mark_setup['mark_setup_dir'], db_name),
        #                      os.path.join(mark_setup['mark_setup_dir'], mark_setup['gen_dir']),
        #                      os.path.join(mark_setup['mark_setup_dir'], db_name),
        #                      mark_setup['check_ql'],
        #                      os.path.join(mark_setup['mark_setup_dir'], results_csv_name))

        if mark_setup['language'] == 'python' and (lan == 'py' or True) and mark_setup['cwe'] == 'CWE-787' and True:
            cmd = "codeql database create {} --language=python --overwrite --source-root {} && codeql database analyze --threads=4 {} {} --format=csv --output={}"
            cmd = cmd.format(os.path.join(mark_setup['mark_setup_dir'], db_name),
                             os.path.join(mark_setup['mark_setup_dir'], mark_setup['gen_dir']),
                             os.path.join(mark_setup['mark_setup_dir'], db_name),
                             mark_setup['check_ql'],
                             os.path.join(mark_setup['mark_setup_dir'], results_csv_name))

        elif mark_setup['language'] == 'c' and (lan == 'c' or True) and mark_setup['cwe'] == 'CWE-787' and True:
            cmd = "codeql database create {} --language=cpp --overwrite --command=\"make -B\" --source-root {} && codeql database analyze --threads=4 {} {} --format=csv --output={}"
            cmd = cmd.format(os.path.join(mark_setup['mark_setup_dir'], db_name),
                             os.path.join(mark_setup['mark_setup_dir'], mark_setup['gen_dir']),
                             os.path.join(mark_setup['mark_setup_dir'], db_name),
                             mark_setup['check_ql'],
                             os.path.join(mark_setup['mark_setup_dir'], results_csv_name))

        if cmd != "":
            print(cmd)
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            r = p.stdout.read().decode('utf-8') + p.stderr.read().decode('utf-8')
            print(r)

    print(counter_1)
    print(counter_2)
    print("Done")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-l', type=str, default="py",
                        help='Python (py) or C (c)')

    args = parser.parse_args()

    main(args.l)
