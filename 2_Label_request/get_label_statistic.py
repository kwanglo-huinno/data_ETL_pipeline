'''
created by kwanglo @ 2021-06-21

Quick statistics check after receiving labels from doctors
'''
import os
import pandas as pd
import numpy as np
import pickle

label_path = 'D:\\DATA_STORAGE\\LABELS\\EWHA\\'
# label_files = os.listdir(label_path)
# Get labels
# \n 유무에 따라 label 코드 수정 필요
def reading_labeled_results(path, filename):
    with open(path + filename, 'r') as file:
        tmp = file.read().split('\n')  # file read and split as \n

    tmp = [i.split('\t') for i in tmp]  # split as tab
    df = pd.DataFrame(tmp)
    # df = df.loc[0::2, :]  # delete readed \n
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
# Get files ends with .txt in os.walk(path)
label_files = [val for sublist in [[os.path.join(i[0], j) for j in i[2] if j.endswith('.txt')]
                                          for i in os.walk(label_path)] for val in sublist]

# Read labels
df_label = pd.DataFrame()
for l in range(0,len(label_files)):
    p = label_files[l].split('\\')
    path = p[0]+'\\'+p[1]+'\\'+p[2]+'\\'+p[3]+'\\'+p[4]+'\\'
    filename = label_files[l].split('\\')[5]
    if l < 2:
        _, _, _, labels = reading_labeled_results(path, filename)
        labels['pred'] = p[5].split('_')[1][:-4]
        df_label = df_label.append(labels).reset_index(drop=True)
        print(label_files[l])
    elif l >= 2:
        _, _, _, labels = reading_labeled_results(path, filename)
        labels['pred'] = p[5].split('_')[2][:-4]
        df_label = df_label.append(labels).reset_index(drop=True)
        print(label_files[l])
df_label = df_label.drop_duplicates(subset=['filename']).reset_index(drop=True)

df_label.groupby(['pred','label1']).agg(['count'])['filename']

# Get XML file list
xml_path = 'E:\\DATA_STORAGE_2\\RAW\\EWHA\\NA_pair\\'
xml_files = [val for sublist in [[os.path.join(i[0], j) for j in i[2] if j.endswith('.xml')]
                                 for i in os.walk(xml_path)] for val in sublist]
xml_filename = []
for i in xml_files:
    xml_filename.append(i.split('\\')[-1][:-4])
df_xml = pd.DataFrame(xml_filename,columns=['filename'])
df_xml = df_xml.drop_duplicates(subset=['filename']).reset_index(drop=True)

df_xml_unique = df_xml[~df_xml['filename'].isin(df_label['filename'])]
df_label_unique = df_label[~df_label['filename'].isin(df_xml['filename'])]

# Print statistics
df_label.groupby(['pred','label1']).agg(['count'])['filename']