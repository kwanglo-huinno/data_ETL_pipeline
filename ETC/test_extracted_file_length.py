import os
import pandas as pd
import numpy as np

# folder_path = 'D:\\DATA_STORAGE\\EXTRACTED\\TXT\\SNUBH_RAW\\'
folder_path = 'D:\\DATA_STORAGE\\patch_clinic_test\\2_EXTRACTED\\IMG\\SNUBH_18-30_IMG\\'
folder_list = os.listdir(folder_path)

# for TXT, INFO
for f in folder_list:
    file_path = folder_path + f + '\\'

    print(f, ' / ', len(os.listdir(file_path)))

# for each lead
for f in folder_list:
    file_path = folder_path + f + '\\'
    lead_list = os.listdir(file_path)
    for l in lead_list:
        txt_path = file_path + l + '\\'
        print(f,' ',l, ' / ', len(os.listdir(txt_path)))