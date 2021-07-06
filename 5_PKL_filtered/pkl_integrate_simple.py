import pickle
import pandas as pd
import numpy as np
import os
import warnings
import copy

# Get file location
folder_path = 'D:\\DATA_STORAGE\\PKL\\TOTAL_PKL\\SRC_TOTAL\\for_test_split\\'
save_path = 'D:\\DATA_STORAGE\\PKL\\TOTAL_PKL\\SRC_TOTAL\\for_test_split\\'

filename = 'SNUBH_model_pred_AVB_v1_'

lead_list = ['lead1','lead2','lead3','lead4','lead5','lead6','lead7','lead8',
             'lead9','lead10','lead11','lead12']


for lead in lead_list:
    pkl_path = folder_path + lead
    pkl_files = os.listdir(pkl_path)

    data_path = pkl_path + '\\'
    infile = open(data_path + pkl_files[0], 'rb')
    df_total = pickle.load(infile)
    infile.close()
    print(lead + ' ' + pkl_files[0])
    # Append other PKLs
    for pkl in range(1,len(pkl_files)):
        print(lead + ' ' + pkl_files[pkl])
        infile = open(data_path + pkl_files[pkl], 'rb')
        df_temp = pickle.load(infile)
        infile.close()

        df_total = df_total.append(df_temp)

    df_total = df_total.reset_index(drop=True)

    with open(save_path + '\\' + filename + df_total['lead'][0] + '.pkl', 'wb') as handle:
        pickle.dump(df_total, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(filename + df_total['lead'][0] + '.pkl done!')
