'''
created by kwanglo
adjusted @ 2021-06-22

Make RAW PKL after making INFO PKL
'''
import numpy as np
import pandas as pd
import os
import pickle
from shutil import copyfile
import copy
import timeit
import re

# Set path
txt_path = 'E:\\DATA_STORAGE_2\\EXTRACTED\\TXT\\EWHA_NA_pair_01\\af\\'
info_path = 'E:\\DATA_STORAGE_2\\1_RAW_PKL\\INFO_PKL\\'
save_path = 'E:\\DATA_STORAGE_2\\1_RAW_PKL\\RAW_PKL\\'
# Set names
save_name = 'EWHA_NA_02_AF_v1_'

start = timeit.default_timer()
first = timeit.default_timer()

info_file = os.listdir(info_path)
folder_list = os.listdir(txt_path)
#folder_list = folder_list[9:-1]


# set folder to extract
# f_num = 3
f_num = 0
for f_num in range(0,1): # len(folder_list)
    # Get info files
    infile = open(info_path + info_file[f_num], 'rb')
    df_info = pickle.load(infile)
    infile.close()


    # Get txt files
    # txt_path = txt_path + folder_list[f_num] + '\\'
    lead_list = os.listdir(txt_path)
    # Get txt filenames
    txt_files = txt_path + lead_list[0] + '\\'
    all_files_path = [val for sublist in [[os.path.join(i[0], j) for j in i[2] if j.endswith('.txt')]
                                          for i in os.walk(txt_files)] for val in sublist]
    filenames = []
    for i in all_files_path:
        filenames.append(i.split('\\')[-1][:-4])
    df_path = pd.DataFrame(all_files_path, columns=['path'])
    df_path['filename'] = filenames
    df_path['lead'] = 'lead'+lead_list[0].split('_')[1]

    # Get filenames for all leads
    for lead in range(1, len(lead_list)):
        txt_files = txt_path + lead_list[lead] + '\\'
        all_files_path = [val for sublist in [[os.path.join(i[0], j) for j in i[2] if j.endswith('.txt')]
                                              for i in os.walk(txt_files)] for val in sublist]
        filenames = []
        for i in all_files_path:
            filenames.append(i.split('\\')[-1][:-4])
        df_temp = pd.DataFrame(all_files_path, columns=['path'])
        df_temp['filename'] = filenames
        df_temp['lead'] = 'lead'+lead_list[lead].split('_')[1]
        df_path = df_path.append(df_temp)
        print(df_temp['lead'][0])

    df_path = df_path.reset_index(drop=True)
    # 모든 리드에 존재하는 파일명만 유지
    df_duplicated = df_path.groupby(['filename']).agg(['count'])['lead']
    path_delete = list(df_duplicated[df_duplicated['count'] < 12].index)

    df_path_reduced = df_path[~df_path['filename'].isin(path_delete)].reset_index(drop=True)

    # 모든 리드에 존재하는 파일명만 유지
    df_info_reduced = df_info[df_info['filename'].isin(df_path_reduced['filename'])].reset_index(drop=True)

    # Set lead according to lead list
    lead_num = 0
    for lead_num in range(0,len(lead_list)):
        # Reset previous results
        df_total = pd.DataFrame()
        df_ecg = pd.DataFrame()
        df_ecg_raw = pd.DataFrame()
        df_ecg_5000 = pd.DataFrame()
        df_ecg_integrated = pd.DataFrame()
        # For single lead
        # 각 리드별로 파일명 불러오기
        print('Reading ecg files... '+lead_list[lead_num])
        txt_files = txt_path + lead_list[lead_num] + '\\'
        all_files_path = [val for sublist in [[os.path.join(i[0], j) for j in i[2] if j.endswith('.txt')]
                                              for i in os.walk(txt_files)] for val in sublist]
        filenames = []
        for i in all_files_path:
            filenames.append(i.split('\\')[-1][:-4])
        # ECG TXT path와 파일명
        df_total = pd.DataFrame(all_files_path, columns=['path'])
        df_total['filename'] = filenames

        # 각 ecg 파일 읽어오기
        start = timeit.default_timer()
        df_ecg = copy.deepcopy(df_total)
        for path in all_files_path:
            df_from_each_file = (pd.read_csv(f, header=None, sep='\t', engine='python') for f in
                                 all_files_path)
        df_ecg_raw = pd.concat(df_from_each_file, ignore_index=True, axis=1).T
        stop = timeit.default_timer()
        print('ECG Reading time ',stop - start)

        # df_ecg 길이 조절(5000)
        df_ecg_5000 = df_ecg_raw.iloc[:, :5000].reset_index(drop=True)
        print('Integrating info & ecg...')
        df_ecg_integrated = pd.concat([df_ecg,df_ecg_5000],axis=1)
        df_ecg_integrated = df_ecg_integrated.drop(columns=['path'])

        # df_info_reduced와 df_ecg merge by path
        # ECG 통합 후 파일 갯수 통일
        df_total = df_total.merge(df_ecg_integrated, how='inner', on='filename')
        df_total = df_total[df_total['filename'].isin(df_info_reduced['filename'])].reset_index(drop=True)

        df_total = df_total.merge(df_info, how='inner', on='filename')

        info_list = ['path', 'filename', 'patient_id', 'hospital_name', 'method', 'lead',
                     'label','label1', 'label2', 'label3', 'label4', 'label5',
                     'opinion', 'age', 'hr', 'date']
        df_total_info = df_total[info_list]
        df_total_info = df_total_info.drop(columns=['path'])
        df_total_ecg = df_total.drop(columns=info_list)
        print('Processing final step...')
        df_total = pd.concat([df_total_info, df_total_ecg], axis=1)
        df_total['lead'] = 'lead'+lead_list[lead_num].split('_')[1]
        # Export PKL
        pkl_path = save_path+'EUMC_NA_Pair_02\\'
        try:
            os.mkdir(pkl_path)
        except OSError:
            pass
        else:
            pass
        pkl_name = save_name+df_total['lead'][0]+'.pkl'
        with open(pkl_path+pkl_name, 'wb') as handle:
            pickle.dump(df_total, handle, protocol=pickle.HIGHEST_PROTOCOL)
            stop = timeit.default_timer()
            print(pkl_name+' RUN Time: ', stop - start)
            start = timeit.default_timer()
    #
print('Total RUN Time: ', stop - first)


