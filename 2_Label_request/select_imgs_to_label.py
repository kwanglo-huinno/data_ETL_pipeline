import os
from shutil import copyfile
import pandas as pd
import numpy as np
import pickle

# Set path

#pkl_path = ''
img_path = 'D:\\DATA_STORAGE\\EXTRACTED\\IMG\\CMC\\CMCS_unlabeled\\'
copy_path = 'E:\\DATA_STORAGE_2\\EXTRACTED\\IMG\\for_labeling\\CMCS\\'
info_path = 'D:\\DATA_STORAGE\\EXTRACTED\\INFO\\CMC\\CMCS\\'
#pkl_files = os.listdir(pkl_path)

# Get info names
info_names = []
all_files_path = [val for sublist in [[os.path.join(i[0], j) for j in i[2] if j.endswith('.txt')]
                                          for i in os.walk(info_path)] for val in sublist]

for i in all_files_path:
    info_names.append(i.split('\\')[-1][:-4])

# Get info txt for files in folders
# Set target folders with imgs
target_list = ['AFF']

target = target_list[0]
img_list = os.listdir(img_path+target)
filenames = []
for i in img_list:
    filenames.append(i[:-4])

df_img = pd.DataFrame()
df_img['path'] = img_list
df_img['filename'] = filenames

# Get name only in target folder
df_path = pd.DataFrame()
df_path['path'] = all_files_path
df_path['filename'] = info_names
df_path = df_path[df_path['filename'].isin(filenames)].reset_index(drop=True)
# Read info files
for path in df_path['path']:
    df_from_each_file = (pd.read_csv(f, header=None, sep='\t', engine='python') for f in
                         df_path['path'])
# Make info PKL
concatenate_df = pd.concat(df_from_each_file, ignore_index=True, axis=1).T
df_info = concatenate_df[0].str.split('.xml,', expand=True)
df_info.columns = ['filename', 'info']
df_temp = df_info['info'].str.split(',', expand=True)
# length 5 일때 예외처리
if len(df_temp.columns) == 5:
    df_temp = df_temp.drop(columns=[4])
df_temp.columns = ['patient_id', 'age', 'hr', 'date']
df_info = df_info.drop(columns=['info'])
df_info = pd.concat([df_info, df_temp], axis=1)
df_info['patient_id'] = df_info['patient_id'].str.replace('@', '').str.replace('#', '')
df_info['age'] = df_info['age'].str.replace('-', '')
df_info['filename'] = df_path['filename']
df_info['hospital_name'] = 'CMCS'  # 수정
df_info['method'] = '12lead'
# 건국대의 경우 임의로 patient_id 지정
# df_info['patient_id'] = df_info['filename'].str[:8]

df_info['lead'] = None
df_info['label'] = None
df_info['label1'] = 'unlabeled'
df_info['label2'] = None
df_info['label3'] = None
df_info['label4'] = None
df_info['label5'] = None
df_info['opinion'] = None

order_list = ['filename', 'patient_id', 'hospital_name', 'method', 'lead',
              'label', 'label1', 'label2', 'label3', 'label4', 'label5',
              'opinion', 'age', 'hr', 'date']
df_info = df_info[order_list]
# Drop by patient_id in df_info
df_info_reduced = df_info.drop_duplicates(subset=['patient_id','label1','label2']).reset_index(drop=True)
# df_info_reduced_strong = df_info.drop_duplicates(subset=['patient_id']).reset_index(drop=True)
df_img_reduced = df_img[df_img['filename'].isin(df_info_reduced['filename'])].reset_index(drop=True)

# Copy imgs for labeling
try:
    os.mkdir(copy_path + target)
except OSError:
    pass
else:
    pass

for p in range(0,len(df_img_reduced['filename'])):
    path = img_path+target+'\\'+df_img_reduced['path'][p]
    filename = df_img_reduced['filename'][p]

    src = path
    dst = copy_path + target + '\\' + filename + '.jpg'
    copyfile(src, dst)