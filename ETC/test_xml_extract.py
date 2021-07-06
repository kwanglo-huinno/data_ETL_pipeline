import numpy as np
import pandas as pd
import os
import pickle
from shutil import copyfile
import copy
import timeit
import re

# Set path
txt_path = 'E:\\DATA_STORAGE_2\\TEST\\python_extract_test\\EXTRACTED\\TXT\\Philips\\lead_1\\'
info_path = 'E:\\DATA_STORAGE_2\\TEST\\python_extract_test\\EXTRACTED\\INFO\\Philips\\'


all_files_path = [val for sublist in [[os.path.join(i[0], j) for j in i[2] if j.endswith('.txt')]
                                      for i in os.walk(txt_path)] for val in sublist]

df_ecg = pd.read_csv(all_files_path[0], header=None, sep='\t', engine='python')
df_ecg.columns = ['ecg']
df_ecg_expand = df_ecg['ecg'].str.split(',',expand=True)
for path in all_files_path:
    df_from_each_file = (pd.read_csv(f, header=None, sep='\t', engine='python') for f in
                         all_files_path)
df_ecg_raw = pd.concat(df_from_each_file, ignore_index=True, axis=1).T

all_files_path = [val for sublist in [[os.path.join(i[0], j) for j in i[2] if j.endswith('.txt')]
                                      for i in os.walk(info_path)] for val in sublist]
df_info = pd.read_csv(all_files_path[0], header=None, sep='\t', engine='python')