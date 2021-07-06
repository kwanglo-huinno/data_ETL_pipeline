'''
created by kwanglo
adjusted @ 2021-06-22

Make information PKL after XML extraction
'''
import numpy as np
import pandas as pd
import os
import pickle
import timeit

# Set path
txt_path = 'E:\\DATA_STORAGE_2\\EXTRACTED\\TXT\\EWHA_NA_pair_01\\af\\'
info_path = 'E:\\DATA_STORAGE_2\\EXTRACTED\\INFO\\EWHA_NA_pair_01\\af\\'
save_path = 'E:\\DATA_STORAGE_2\\1_RAW_PKL\\INFO PKL\\'
# Set names
save_name = 'EWHA_NA_02_AF_INFO.pkl'

#############################
# Get txt files             #
#############################

first = timeit.default_timer()
lead_list = os.listdir(txt_path)

txt_files = txt_path + lead_list[0] + '\\'
all_files_path = [val for sublist in [[os.path.join(i[0], j) for j in i[2] if j.endswith('.txt')]
                                          for i in os.walk(txt_files)] for val in sublist]
filenames = []
for i in all_files_path:
    filenames.append(i.split('\\')[-1][:-4])
df_path = pd.DataFrame(all_files_path,columns=['path'])
df_path['filename'] = filenames
df_path['lead'] = lead_list[0]
# Get filenames for all leads
for lead in range(1,len(lead_list)):
    start = timeit.default_timer()
    txt_files = txt_path + lead_list[lead] + '\\'
    all_files_path = [val for sublist in [[os.path.join(i[0], j) for j in i[2] if j.endswith('.txt')]
                                          for i in os.walk(txt_files)] for val in sublist]
    filenames = []
    for i in all_files_path:
        filenames.append(i.split('\\')[-1][:-4])
    df_temp = pd.DataFrame(all_files_path, columns=['path'])
    df_temp['filename'] = filenames
    df_temp['lead'] = lead_list[lead]
    df_path = df_path.append(df_temp)
    print(lead_list[lead])
    stop = timeit.default_timer()
    print('RUN Time: ', stop - start)
    start = timeit.default_timer()

df_path = df_path.reset_index(drop=True)
# Keep filenames that only exist in all 12 leads
df_duplicated = df_path.groupby(['filename']).agg(['count'])['lead']
path_delete = list(df_duplicated[df_duplicated['count']<12].index)

df_path_reduced = df_path[~df_path['filename'].isin(path_delete)].reset_index(drop=True)
df_path_reduced = df_path_reduced.drop_duplicates(subset=['filename'],keep='first').reset_index(drop=True)

#############################
# Get info files            #
#############################

print('Reading info files...')
all_files_path = [val for sublist in [[os.path.join(i[0], j) for j in i[2] if j.endswith('.txt')]
                                          for i in os.walk(info_path)] for val in sublist]
filenames = []
for i in all_files_path:
    filenames.append(i.split('\\')[-1][:-4])
df_info = pd.DataFrame(all_files_path,columns=['path'])
df_info['filename'] = filenames

# 모든 리드에 존재하는 파일명만 유지
df_info_reduced = df_info[df_info['filename'].isin(df_path_reduced['filename'])].reset_index(drop=True)
df_info_reduced = df_info_reduced.drop_duplicates(subset=['filename'],keep='first').reset_index(drop=True)
# INFO 불러오기
read_count = 0

start = timeit.default_timer()
first = timeit.default_timer()
pkl_array = list()
# array에 바로 넣기
for path in range(0,len(df_info_reduced['path'])):
    #path = 1
    file = open(df_info_reduced['path'][path],encoding='UTF-8')
    blank = file.read()
    # blank_adj = blank.replace('\n',',')
    blank_adj = blank.split(',')
    blank_adj_2 = []
    for string in blank_adj:
        new_string = string.replace('\n','')
        blank_adj_2.append(new_string)
    pkl_array.append(blank_adj_2)
    if read_count % 5000 == 0:
        stop = timeit.default_timer()
        print('RUN Time: ', stop - start)
        print(lead_list[0] + ' processing ' + str(read_count) + '/' + str(len(df_info_reduced['path'])))
        start = timeit.default_timer()
    read_count += 1

print('Converting to dataframe')
start = timeit.default_timer()
df_info_raw = pd.DataFrame(pkl_array)
stop = timeit.default_timer()
print('RUN Time: ', stop - start)

print('Building info files...')
# Build df_save
df_save = df_info_raw.iloc[:,:5]
df_save.columns = ['path', 'patient_id','age','hr','date']
filenames = []
for i in df_save['path']:
    filenames.append(i.split('\\')[-1][:-4])
df_save['filename'] = filenames
df_save = df_save.drop(columns=['path'])
df_save['age'] = df_save['age'].str.replace('-', '')
df_save['hospital_name'] = 'EUMC' # 수정
df_save['method'] = '12lead'
# 건국대의 경우 임의로 patient_id 지정
#df_info['patient_id'] = df_info['patient_id'].str.replace('@', '').str.replace('#', '')
df_save['patient_id'] = df_save['filename'].str[:8]

df_save['lead'] = None
df_save['label'] = None
df_save['label1'] = 'unlabeled'
df_save['label2'] = None
df_save['label3'] = None
df_save['label4'] = None
df_save['label5'] = None
df_save['opinion'] = None

order_list = ['filename', 'patient_id', 'hospital_name', 'method', 'lead',
              'label','label1', 'label2', 'label3', 'label4', 'label5',
              'opinion', 'age', 'hr', 'date']
df_save = df_save[order_list]
df_save = df_save.reset_index(drop=True)
print('Exporting PKL...')
# 수정
with open(save_path + save_name, 'wb') as handle:
    pickle.dump(df_save, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(save_path + save_name + " done!")