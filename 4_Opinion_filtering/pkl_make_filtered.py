'''
created by kwanglo @ 2021-06-09

Filter data with opinion
'''
import numpy as np
import pandas as pd
import os
import pickle

### Get path
# pkl_path = 'D:\\DATA_STORAGE\\PKL\\RAW_PKL\\CMCI_RAW\\'
# label_path = 'D:\\DATA_STORAGE\\LABELS\\CMC\\CMCI_labels\\'
pkl_path = 'E:\\DATA_STORAGE_2\\3_PKL_labeled\\SNUBH\\'
opinion_path = 'E:\\DATA_STORAGE_2\\4_Opinion_filtering\\opinion\\'
save_path = 'E:\\DATA_STORAGE_2\\5_PKL_filtered\\PKL_filtered\\SNUBH\\'
niu_path = 'E:\\DATA_STORAGE_2\\5_PKL_filtered\\PKL_NIU\\SNUBH\\'

save_name = 'SNUBH_unlabeled_filtered'
niu_name = 'SNUBH_unlabeled_NIU'
pkl_files = os.listdir(pkl_path)
opinion_files = os.listdir(opinion_path)

### Filter opinion
# Get opinion file
opinion = pd.read_csv(opinion_path+opinion_files[0],encoding='cp949')
opinion = opinion.replace({np.nan: 'None'})
# Set filtering list
filter = ['strange','delete','inquiry']
opinion_filter = opinion[opinion['remark1'].isin(filter)]
df_niu = pd.DataFrame(opinion_filter)
df_niu.to_csv(niu_path+niu_name+'_opinion.csv', encoding='cp949')

# Get primary PKL
for pkl in range(0,len(pkl_files)):
    infile = open(pkl_path + pkl_files[pkl], 'rb')
    df_pkl = pickle.load(infile)
    infile.close()
    # Export filtered PKL
    df_save = df_pkl[~df_pkl['filename'].isin(opinion_filter)].reset_index(drop=True)
    df_not_using = df_pkl[df_pkl['filename'].isin(opinion_filter)].reset_index(drop=True)

    pkl_name = save_name + str(df_save['lead'][0]) + '.pkl'
    pkl_niu_name = niu_name + str(df_not_using['lead'][0]) + '.pkl'

    with open(save_path + pkl_name, 'wb') as handle:
        pickle.dump(df_save, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(pkl_name)

    with open(niu_path + pkl_niu_name, 'wb') as handle:
        pickle.dump(df_not_using, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(pkl_niu_name)



