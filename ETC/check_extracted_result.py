import os
import pandas as pd
import numpy as np
import pickle

xml_path = 'E:\\DATA_STORAGE_2\\RAW\\EWHA\\NA_pair\\'
info_path = 'E:\\DATA_STORAGE_2\\EXTRACTED\\INFO\\EWHA_NA_pair_01\\'
img_path = 'E:\\DATA_STORAGE_2\\EXTRACTED\\IMG\\EWHA_NA_pair_01\\'
txt_path = 'E:\\DATA_STORAGE_2\\EXTRACTED\\TXT\\EWHA_NA_pair_01\\'
folder_list = ['normal']

for f in folder_list:
    xml_length = len(os.listdir(xml_path+f+'\\'))
    info_length = len(os.listdir(info_path + f + '\\'))
    img_length = len(os.listdir(img_path + f + '\\'))
    lead_list = os.listdir(txt_path+f+'\\')
    print('XML: ', str(xml_length),
          'INFO: ', str(info_length),
          'IMG: ', str(img_length)
          )
    print('TXT')
    for lead in lead_list:
        txt_length = os.listdir(txt_path + f + '\\'+ lead + '\\')
        print(lead,': ', str(len(txt_length)))