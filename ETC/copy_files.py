import os
from shutil import copyfile
import pandas as pd
import numpy as np
import pickle

label_path = 'D:\\DATA_STORAGE\\LABELS\\EWHA\\NA_pair_02\\'
xml_path = 'D:\\DATA_STORAGE\\RAW\\XML_by_format\\EWHA\\'
copy_path = 'E:\\DATA_STORAGE_2\\TEST\\박준범교수님_요청자료_20210705\\xml\\'

# Read labels <- if necessary
def reading_labeled_results(path, filename):
    with open(path + filename, 'r') as file:
        tmp = file.read().split('\n')  # file read and split as \n

    tmp = [i.split('\t') for i in tmp]  # split as tab
    df = pd.DataFrame(tmp)
    df = df.loc[0::2, :]  # delete readed \n
    df = df.reset_index(drop=True)
    df = df.drop(df.tail(1).index)

    filelist = pd.DataFrame(df.iloc[:, 0])
    for i in range(len(filelist)):
        _, filelist.iloc[i][0] = os.path.split(filelist.iloc[i][0])  # get the name of file as splitting the path
        filelist.iloc[i][0] = filelist.iloc[i][0][:-4]  # delete ".jpg"
    filelist.columns = ['filename']
    opinion = pd.DataFrame(df.iloc[:, -1])
    opinion.columns = ['opinion']

    drop_cols = [0, -1]
    labels = df.drop(df.columns[drop_cols], axis=1)
    labels = labels.iloc[:, 0].str.split(expand=True)

    if len(labels.columns) == 1:
        labels[1] = None  # 빈 열 추가 (labels 개수는 최대 5개라고 생각)
        labels[2] = None
        labels[3] = None
        labels[4] = None

    elif len(labels.columns) == 2:
        labels[2] = None
        labels[3] = None
        labels[4] = None

    elif len(labels.columns) == 3:
        labels[3] = None
        labels[4] = None

    elif len(labels.columns) == 4:
        labels[4] = None

    elif len(labels.columns) == 5:
        pass

    elif len(labels.columns) > 5:
        print('label 개수 5 초과' * 100)

    labels.columns = ['label1', 'label2', 'label3', 'label4', 'label5']

    dataframe = pd.concat([filelist, labels, opinion], axis=1)
    return filelist, opinion, labels, dataframe
# Get names of XML
raw_names = []
all_files_path = [val for sublist in [[os.path.join(i[0], j) for j in i[2] if j.endswith('.xml')]
                                          for i in os.walk(xml_path)] for val in sublist]

for i in all_files_path:
    raw_names.append(i.split('\\')[-1][:-4])

df_path = pd.DataFrame(all_files_path,columns=['path'])
df_path['filename'] = raw_names
# Get predicted filenames
label_files = os.listdir(label_path)
file = label_files[0]
for file in label_files:
    # df_label = pd.read_csv(label_path + file, header=None)
    # df_label.columns = ['filename']
    _, _, _, df_label = reading_labeled_results(label_path, file)
    # Compare filenames
    df_duplicated = df_path[df_path['filename'].isin(df_label['filename'])].reset_index(drop=True)
    # Copy files in duplicated filenames
    folder = file.split('_')[2][:-4]

    for f in range(0,len(df_duplicated['path'])):
        src = df_duplicated['path'][f]
        dst = copy_path + folder + '\\' + df_duplicated['filename'][f] + '.xml'
        copyfile(src, dst)
        if f % 100 == 0:
            print(folder+': '+str(f)+'/'+ str(len(df_duplicated['path'])))

