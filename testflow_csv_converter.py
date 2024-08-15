#!/usr/local/bin/python3

import itertools as it
import csv

row_counter = 1 # count total rows written, for science
tct_counter = it.count(1) # start a global counter that will increment by 1 to use for testflo "issueIndex" field (test case template ID field)
with open('/Users/nixl/test_files/just_regression_tr_fixed.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    """ with open('/Users/nixl/test_files/test_flow_tr_import.csv', 'w', newline='') as outcsv:
        fieldnames=['issueIndex', 'summary', 'description', 'stepGroup', 'tctStepId', 'Action', 'Input', 'Expected result', 'components', 'assigneeId', 'textCfValue', 'requirements']
        writer = csv.DictWriter(outcsv, fieldnames=fieldnames)
        writer.writeheader() """

# 'issueIndex', 'summary', 'description', 'stepGroup', 'tctStepId', 'Action', 'Input', 'Expected result', 'components', 'assigneeId', 'textCfValue', 'requirements'
# 'ID', 'summary', 'description', 'components', 'results', 'steps'
    l = []
    for row in reader:
        l.append(''.join([x[0].upper()+x[1::] for x in row['components'].split()]))
for x in set(l):
    print(x)

""" tf_idx = next(tct_counter)
            tf_row = {}
            tf_row["issueIndex"] = tf_idx
            tf_row["summary"] = row["summary"]
            if row['description']:
                tf_row["description"] = ''.join(["Imported Preconditions:\n", row["description"]])
            else:
                tf_row["description"] = ''
            tf_row['components'] = ''.join([x[0].upper()+x[1::] for x in row['components'].split()])
            for key in ['assigneeId', 'textCfValue', 'requirements']:
                tf_row[key] = ''
            # if row has no steps
            if not row["steps"]:
                for key in ['stepGroup', 'tctStepId', 'Action', 'Input', 'Expected result']:
                    tf_row[key] = ''
                ##### probably want to debug print stuff here if you have issues
                writer.writerow(tf_row)
                row_counter += 1
                #print(tf_row)
            # if row has steps
            else:
                step_counter = it.count(1)
                steps = row["steps"].splitlines()
                first_step = steps[0][3::] # remove the "1." from the step since we are using a counter for the index
                tf_row['stepGroup'] = 'Group 1'
                tf_row['tctStepId'] = next(step_counter)
                tf_row['Action'] = first_step
                tf_row['Input'] = ''
                if row['results']:
                    results = row['results'].splitlines()
                    first_result = results[0][3::] # remove the "1." from the results since we just don't need it
                    tf_row['Expected result'] = first_result
                else:
                    tf_row['Expected result'] = ''

                ##### probably want to debug print stuff here if you have issues
                writer.writerow(tf_row)
                row_counter += 1
                #print(tf_row)
                if len(steps) > 1:
                    for idx, step in enumerate(steps[1::]):
                        tf_row = {}
                        tf_row['issueIndex'] = tf_idx
                        tf_row['tctStepId'] = next(step_counter)
                        tf_row['Action'] = step[3::] or ''
                        tf_row['Expected result'] = results[idx+1][3::] or ''
                        for key in ['summary', 'description', 'stepGroup', 'Input', 'components', 'assigneeId', 'textCfValue', 'requirements']:
                            tf_row[key] = ''
                        ##### probably want to debug print stuff here if you have issues
                        writer.writerow(tf_row)
                        row_counter += 1
                        #print(tf_row)
print(f'Added {row_counter} rows to /Users/nixl/test_files/test_flow_tr_import.csv') """
