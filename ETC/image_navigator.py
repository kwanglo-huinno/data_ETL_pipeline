import os
from shutil import copyfile
import pandas as pd
import numpy as np
import copy
import timeit
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle

print('#########################################################################')
print('####################### WELCOME TO ECG IMG SEARCH #######################')
print('#########################################################################')

# Set path
search_path = input("Set search path:\n")
print(f'Searching {search_path}...........')

search_file_path = [val for sublist in [[os.path.join(i[0], j) for j in i[2] if j.endswith('.jpg')]
                                        for i in os.walk(search_path)] for val in sublist]
search_file = []
for i in search_file_path:
    search_file.append(i.split('\\')[-1][:-4])
df_search = pd.DataFrame(search_file_path, columns=['path'])
df_search['filename'] = search_file
#
info_file = input("Set information file:\n")
print(f'Reading {info_file}...........')
infile = open(info_file, 'rb')
df_info = pickle.load(infile)
infile.close()

# 현재 label 1 기준 검색은 unlabeled라서 불가능 @ 2021-07-05 by kwanglo
# Get search criteria
match_criteria = ['filename','patient_id','label1']
right_criteria = False

while right_criteria == False:
    print('Select search criteria')
    print('1 - filename / 2 - patient_id / 3 - label1')
    criteria = input("Type Number:\n")
    criteria = str(criteria)
    # Set function according to criteria
    if criteria in ['1','2','3']:
        right_criteria = True
    else:
        print('Wrong criteria')

match_str = input("Type target string:\n")
if criteria == '1':
    df_match = df_info[df_info['filename'] == str(match_str)].reset_index(drop=True)
elif criteria == '2':
    df_match = df_info[df_info['patient_id'] == str(match_str)].reset_index(drop=True)
elif criteria == '3':
    df_match = df_info[df_info['label1'] == str(match_str)].reset_index(drop=True)
print('Matching target string.......')
# Show matching img list
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(df_match)
# Plot selected imgs
img_name = input("Type target filename:\n")
img_name = str(img_name)
target_path = df_search[df_search['filename']==img_name].reset_index(drop=True)

img = mpimg.imread(df_search['path'][0])
imgplot = plt.imshow(img)
plt.show()