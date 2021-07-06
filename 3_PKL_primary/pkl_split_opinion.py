'''
created by kwanglo @ 2021-06-03

Filter data with opinion and split into different pkl
'''
import numpy as np
import pandas as pd
import os
import pickle

### Get path
label_path = 'E:\\DATA_STORAGE_2\\2_Label\\SNUBH\\unlabed_labeled\\'
clean_path = 'E:\\DATA_STORAGE_2\\3_PKL_labeled\\opinion_clean\\SNUBH\\'
task_path = 'E:\\DATA_STORAGE_2\\3_PKL_labeled\\opinion_task\\SNUBH\\'
opinion_path = 'E:\\DATA_STORAGE_2\\4_Opinion_filtering\\opinion\\'

clean_name = 'SNUBH_unlabeled_clean'
task_name = 'SNUBH_unlabeled_task'
opinion_name = 'SNUBH_unlabeled_comments'

# select target folder
label_files = os.listdir(label_path)

### Get labels
# \n 유무에 따라 label 코드 수정 필요
# label file 열어보고 결정!!
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

df_labels = pd.DataFrame()
# If labels are many
for l in range(1,len(label_files)):
    _, _, _, labels = reading_labeled_results(label_path, label_files[l])
    print(label_files[l]+': '+str(len(labels)))
    df_labels = df_labels.append(labels)
df_labels = df_labels.reset_index(drop=True)

# Split labels into w, w/o opinion
opinion_filter_none = ['','None',None]
df_clean = df_labels[df_labels['opinion'].isin(opinion_filter_none)].reset_index(drop=True)
df_clean['opinion'] = None
df_task = df_labels[~df_labels['opinion'].isin(opinion_filter_none)].reset_index(drop=True)

# Make opinion df
opinion = df_task.groupby(['opinion']).agg(['count'])['label1']
df_opinion = pd.DataFrame(opinion.index)
df_opinion['remark1'] = None
df_opinion['remark2'] = None
order_list = ['remark1','remark2','opinion']
df_opinion = df_opinion[order_list]

# Export opinion csv
df_opinion.to_csv(opinion_path+opinion_name+'.csv', index=False, encoding='cp949')
