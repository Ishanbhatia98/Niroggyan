import json
import csv
import re
import os
import pandas as pd
import numpy as np

#getting the path of all the jsons in the directory
files = []
d = "F:/Nirrogyan/AWS/aws logs/"
for path in os.listdir(d):
    full_path = os.path.join(d, path)
    files.append(full_path)

#extracting the dataset of the person who has taken the most number of tests (results from another script) to make a list of all the test available
tests = []
for m in range(0, len(files)):
    with open(files[m]) as f:
        for line in f:
            final_data = []
            x = re.search("{\"header\"", line)
            if x != None:
                data = (line[(x.span()[0]):])
                s = json.loads(data)

                if (s['header']['personInfo']['name']) == 'Murtaza Beawerwala':
                    for i in range (0, len(s['values'])):
                        tests.append(s['values'][i]['param'])
                break
tests = np.unique(tests)

# extracting from each file
for m in range(0, len(files)):
    with open(files[m]) as f:
        for line in f:
            final_data = []
            x = re.search("{\"header\"", line)
            if x != None:
                data = (line[(x.span()[0]):])
                s = json.loads(data)

                tests_data = {}

                patient_id = s['header']['personInfo']['name'].lower().replace(' ', '_')
                name = s['header']['personInfo']['name']
                age = int(s['header']['personInfo']['age'])
                gender = s['header']['personInfo']['gender']
                date = s['header']['date']
                order_id = int(s['values'][0]['order_id'])
                
                if gender == 'male':
                    tests_data.update(patient_id = 'm_{}_{}'.format(age, patient_id))
                else:
                    tests_data.update(patient_id = 'f_{}_{}'.format(age, patient_id))
                    
                tests_data.update(name = name)
                tests_data.update(age = age)
                tests_data.update(gender = gender)
                tests_data.update(date = date)
                tests_data.update(order_id = order_id)
                
                for j in range(0, len(tests)):
                    for i in range(0, len(s['values'])):
                        if tests[j] == s['values'][i]['param']:
 
                            try:
                                try:
                                    tests_data.update({'test{}'.format(j): float(s['values'][i]['value'])})
                                except ValueError:
                                    tests_data.update({'test{}'.format(j):s['values'][i]['value']})
                            except KeyError:
                                tests_data.update({'test{}'.format(j): '-'})
                            break
                        #checking for the tests not taken by the patient    
                        if i == (len(s['values']) - 1) and (tests[j] != s['values'][i]['param']):
                            tests_data.update({'test{}'.format(j): '{} : N/A'.format(tests[j])})
                            
                final_data.append(tests_data)
                #All the data has been stored in the dict.

                #Putting all the data in a csv
                data_file = open('testing.csv', 'a')
                csv_writer = csv.writer(data_file)
                count = 0

                for j in final_data:
                    csv_writer.writerow(j.values())
                data_file.close()

            else:
                continue