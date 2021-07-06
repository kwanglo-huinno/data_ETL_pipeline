import pickle
import pandas as pd
import numpy as np
import os
import warnings

#refer_path = 'D:\\DATA_STORAGE\\RAW\\XML_by_format\\EWHA\\'
save_path = 'D:\\DATA_STORAGE\\patch_clinic_test\\2_EXTRACTED\\VIP\\IMG_clustering\\selected_withGrid\\'

folder_list = os.listdir(save_path)
#dir_list = ['lead1','lead2','lead3','lead4','lead5','lead6','lead7','lead8','lead9','lead10','lead11','lead12']
#dir_list = ['normal','afib','apc','vpc','svt','vt','others']
dir_list = ['normal','af','apc','vpc','noise','others']
def make_dir(save_path, dir_list):
    for dir in dir_list:
        try:
            os.mkdir(save_path+dir+'\\')
        except OSError:
            print("Creation of the directory %s failed" % save_path)
        else:
            print("Successfully created the directory %s " % save_path)

make_dir(save_path,dir_list)