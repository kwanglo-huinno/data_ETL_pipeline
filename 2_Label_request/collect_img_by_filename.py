'''
created by kwanglo @ 2021-05-21

Collect images using filenames in PKL or os.listdir()
'''
import pickle
import pandas as pd
import numpy as np
import os
from shutil import copyfile

f_list = ['train','test']
pkl_path = 'D:\\DATA_STORAGE\\PKL\\TRAIN_TEST\\by_data_source\\konkuk\\'
img_path = 'D:\\DATA_STORAGE\\EXTRACTED\\IMG\\KONKUK\\konkuk_12lead_filtered\\'
save_path = 'D:\\DATA_STORAGE\\EXTRACTED\\IMG\\KONKUK\\konkuk_train_test_12lead_filtered\\'
folder = f_list[0]
for folder in f_list:
    file_path = pkl_path + folder + '\\'
    file_list = os.listdir(file_path)
    # Get train, test pkl
    infile = open(file_path + file_list[0], 'rb')
    df_temp = pickle.load(infile)
    infile.close()

    file_names = df_temp['filename']
    # distribute imgs according to filename
    for name in file_names:
        try:
            src = img_path + name + '.jpg'
            dst = save_path + folder + '\\' + name + '.jpg'
            copyfile(src, dst)
        except:
            print(name)