'''

ECG 및 INFO reading하는 부분은 추출 코드 마무리 이후 수정

'''
import cv2
import numpy as np
import pandas as pd
import os
import sklearn
from sklearn import preprocessing
from scipy import signal
from scipy.signal import butter, lfilter
import copy
import timeit

# Get path
info_path = 'E:\\DATA_STORAGE_2\\TEST\\python_extract_test\\IMG_TEST\\INFO\\'
ecg_path = 'E:\\DATA_STORAGE_2\\TEST\\python_extract_test\\IMG_TEST\\TXT\\'
save_path = 'E:\\DATA_STORAGE_2\\TEST\\python_extract_test\\IMG_TEST\\IMG\\'
# Get filenames
info_files = os.listdir(info_path)
lead_list = ['lead_1','lead_2','lead_3','lead_4','lead_5','lead_6',
             'lead_7','lead_8','lead_9','lead_10','lead_11','lead_12']
# Read info files
df_info = pd.read_csv(info_path+info_files[0], header=None, sep='\t', engine='python')
df_info = df_info[0].str.split(',', expand=True)
df_info.columns = ['path','patient_id','age','hr','date']
df_info['filename'] = df_info['path'][0].split('\\')[7][:-4]
# Read ecg files for one patient
start = timeit.default_timer()
first = timeit.default_timer()

df_ecg = pd.DataFrame()
for lead in range(0,len(lead_list)):
    df_ecg_temp = pd.read_csv(ecg_path+lead_list[lead]+'\\'+info_files[0]
                              , header=None, sep='\t', engine='python')
    df_ecg = df_ecg.append(df_ecg_temp.T).reset_index(drop=True)
# df_ecg 길이 조절(5000)
df_ecg_5000 = df_ecg.iloc[:, :5300]
df_ecg_ref = df_ecg.iloc[:, 5300:]
ecg_notch = []
i=0
# 60hz notch
for i in range(0,len(df_ecg_5000)):
    ecg_array = np.array(df_ecg_5000.loc[i])
    b, a = signal.iirnotch(60, 3, 500)  # (target_hz, quality factor, Hz)
    df_filter_n = signal.lfilter(b, a, ecg_array)
    ecg_notch.append(df_filter_n)
df_ecg_notch = pd.DataFrame(ecg_notch)
ecg_n_high = []
# highpass 0.2
for i in range(0,len(df_ecg_notch)):
    ecg_array = np.array(df_ecg_notch.loc[i])
    sos = signal.butter(2, 0.2, btype='highpass',output='sos',fs=500)
    df_filter_nh = signal.sosfilt(sos, ecg_array)
    ecg_n_high.append(df_filter_nh)
df_ecg_n_high = pd.DataFrame(ecg_notch)
ecg_nhl = []
# lowpass 40hz
for i in range(0,len(df_ecg_n_high)):
    ecg_array = np.array(df_ecg_n_high.loc[i])
    b, a = signal.butter(2, 40, btype='lowpass',fs=500)
    df_filter_nhl = signal.filtfilt(b, a, ecg_array)
    ecg_nhl.append(df_filter_nhl)
df_filtered = pd.DataFrame(ecg_nhl)
df_ecg_filtered = pd.concat([df_filtered,df_ecg_ref],axis=1)
# df_ecg_filtered = copy.deepcopy(df_ecg)
stop = timeit.default_timer()
print('ECG Processing time ',stop - start)

# np.zeros(y,x,3 color channel)
img = np.zeros((1260,2180,3), np.uint8)
img.fill(255)
# 여기서 색상인 (255,0,0) 에 대해서는 RGB가 아닌 BGR 순서임.

# Set features
margin = 50
gridSize = 40
offset = 300
x_offset = 50
y_offset = 100
textSpace = 200
img_col = 2180
img_row = 1260
# Set grid
for y_pos in range(0,25):
    # start(x,y) / end(x,y) / color / px
    img = cv2.line(img,(margin,textSpace+margin+gridSize*y_pos),(img_col-margin,textSpace+margin+gridSize*y_pos),(100,100,255),1) #(start,ende,color,px)
for x_pos in range(0,53):
    img = cv2.line(img,(margin+gridSize*x_pos,textSpace+margin),(margin+gridSize*x_pos,img_row-margin),(100,100,255),1) #(start,ende,color,px)

# Set font features
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale = 1
fontColor = (0,0,0)
lineType = 2
# Set writing position
x_lead_std = int(margin + 10)
y_lead_std = int(textSpace + margin + 30)
x_lead_augmented = int(margin + 10 + (img_col - margin * 2 - 80) / 4)

# Write lead index
img = cv2.putText(img,'I',(x_lead_std, y_lead_std),font,fontScale,fontColor,lineType)
img = cv2.putText(img,'II',(x_lead_std, y_lead_std + gridSize * 6),font,fontScale,fontColor,lineType)
img = cv2.putText(img,'III',(x_lead_std, y_lead_std + gridSize * 12),font,fontScale,fontColor,lineType)
img = cv2.putText(img,'II',(x_lead_std, y_lead_std + gridSize * 18),font,fontScale ,fontColor,lineType)
img = cv2.putText(img,'aVR',(x_lead_augmented, y_lead_std),font,fontScale,fontColor,lineType)
img = cv2.putText(img,'aVL',(x_lead_augmented, y_lead_std + gridSize * 6),font,fontScale,fontColor,lineType)
img = cv2.putText(img,'aVF',(x_lead_augmented, y_lead_std + gridSize * 12),font,fontScale,fontColor,lineType)
img = cv2.putText(img,'V1',(x_lead_augmented * 2, y_lead_std),font,fontScale,fontColor,lineType)
img = cv2.putText(img,'V2',(x_lead_augmented * 2, y_lead_std + gridSize * 6),font,fontScale,fontColor,lineType)
img = cv2.putText(img,'V3',(x_lead_augmented * 2, y_lead_std + gridSize * 12),font,fontScale,fontColor,lineType)
img = cv2.putText(img,'V4',(x_lead_augmented * 3, y_lead_std),font,fontScale,fontColor,lineType)
img = cv2.putText(img,'V5',(x_lead_augmented * 3, y_lead_std + gridSize * 6),font,fontScale,fontColor,lineType)
img = cv2.putText(img,'V6',(x_lead_augmented * 3, y_lead_std + gridSize * 12),font,fontScale,fontColor,lineType)

# Write info
info_names = ['filename','patient_id', 'age', 'hr', 'date']
info_list = list(df_info[info_names].loc[0])
for info in range(0,len(info_list)):
    img = cv2.putText(img, info_list[info], (margin + 10, margin + 30 + info * 20), font, 0.8, fontColor,lineType)

# Data
thickness = 2
partial_lead = int(5000/4)
start = timeit.default_timer()
#Lead 1 - I
baseY = margin + gridSize * 3
startX = margin
for i in range(1, partial_lead):
    img = cv2.line(img,
                   (int(startX + (i - 1) / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[0].get(i - 1 + offset) / 200))),
                   (int(startX + i / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[0].get(i + offset) / 200))),
                   (0,0,0), thickness)
stop = timeit.default_timer()
print('Lead1 time ',stop - start)
start = timeit.default_timer()
#Lead 2 - II
baseY = margin + gridSize * 9
startX = margin
for i in range(1, partial_lead):
    img = cv2.line(img,
                   (int(startX + (i - 1) / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[1].get(i - 1 + offset) / 200))),
                   (int(startX + i / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[1].get(i + offset) / 200))),
                   (0,0,0), thickness)
stop = timeit.default_timer()
print('Lead2 time ',stop - start)
start = timeit.default_timer()
#Lead 3 - III
baseY = margin + gridSize * 15
startX = margin
for i in range(1, partial_lead):
    img = cv2.line(img,
                   (int(startX + (i - 1) / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[2].get(i - 1 + offset) / 200))),
                   (int(startX + i / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[2].get(i + offset) / 200))),
                   (0,0,0), thickness)
stop = timeit.default_timer()
print('Lead3 time ',stop - start)
start = timeit.default_timer()
#Lead 4 - aVR
baseY = margin + gridSize * 3
startX = margin + (img_col - margin * 2 - 80) / 4
for i in range(1, partial_lead):
    img = cv2.line(img,
                   (int(startX + (i - 1) / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[3].get(offset + partial_lead + i - 1) / 200))),
                   (int(startX + i / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[3].get(offset + partial_lead + i)/200))),
                   (0,0,0), thickness)
stop = timeit.default_timer()
print('Lead4 time ',stop - start)
start = timeit.default_timer()
#Lead 5 - aVL
baseY = margin + gridSize * 9
startX = margin + (img_col - margin * 2 - 80) / 4
for i in range(1, partial_lead):
    img = cv2.line(img,
                   (int(startX + (i - 1) / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[4].get(offset + partial_lead + i - 1) / 200))),
                   (int(startX + i / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[4].get(offset + partial_lead + i)/200))),
                   (0,0,0), thickness)
stop = timeit.default_timer()
print('Lead5 time ',stop - start)
start = timeit.default_timer()
#Lead 6 - aVF
baseY = margin + gridSize * 15
startX = margin + (img_col - margin * 2 - 80) / 4
for i in range(1, partial_lead):
    img = cv2.line(img,
                   (int(startX + (i - 1) / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[5].get(offset + partial_lead + i - 1) / 200))),
                   (int(startX + i / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[5].get(offset + partial_lead + i)/200))),
                   (0,0,0), thickness)
stop = timeit.default_timer()
print('Lead6 time ',stop - start)
start = timeit.default_timer()
#Lead 7 - V1
baseY = margin + gridSize * 3
startX = margin + (img_col - margin * 2 - 80) / 4 * 2;
for i in range(1, partial_lead):
    img = cv2.line(img,
                   (int(startX + (i - 1) / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[6].get(offset + partial_lead * 2 + i - 1) / 200))),
                   (int(startX + i / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[6].get(offset + partial_lead * 2 + i)/200))),
                   (0,0,0), thickness)
stop = timeit.default_timer()
print('Lead7 time ',stop - start)
start = timeit.default_timer()
#Lead 8 - V2
baseY = margin + gridSize * 9
startX = margin + (img_col - margin * 2 - 80) / 4 * 2;
for i in range(1, partial_lead):
    img = cv2.line(img,
                   (int(startX + (i - 1) / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[7].get(offset + partial_lead * 2 + i - 1) / 200))),
                   (int(startX + i / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[7].get(offset + partial_lead * 2 + i)/200))),
                   (0,0,0), thickness)
stop = timeit.default_timer()
print('Lead8 time ',stop - start)
start = timeit.default_timer()
#Lead 9 - V3
baseY = margin + gridSize * 15
startX = margin + (img_col - margin * 2 - 80) / 4 * 2;
for i in range(1, partial_lead):
    img = cv2.line(img,
                   (int(startX + (i - 1) / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[8].get(offset + partial_lead * 2 + i - 1) / 200))),
                   (int(startX + i / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[8].get(offset + partial_lead * 2 + i)/200))),
                   (0,0,0), thickness)
stop = timeit.default_timer()
print('Lead9 time ',stop - start)
start = timeit.default_timer()
#Lead 10 - V4
baseY = margin + gridSize * 3
startX = margin + (img_col - margin * 2 - 80) / 4 * 3;
for i in range(1, partial_lead + 200 - 1):
    img = cv2.line(img,
                   (int(startX + (i - 1) / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[9].get(offset + partial_lead * 3 + i - 1) / 200))),
                   (int(startX + i / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[9].get(offset + partial_lead * 3 + i)/200))),
                   (0,0,0), thickness)
stop = timeit.default_timer()
print('Lead10 time ',stop - start)
start = timeit.default_timer()
#Lead 11 - V5
baseY = margin + gridSize * 9
startX = margin + (img_col - margin * 2 - 80) / 4 * 3;
for i in range(1, partial_lead + 200 - 1):
    img = cv2.line(img,
                   (int(startX + (i - 1) / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[10].get(offset + partial_lead * 3 + i - 1) / 200))),
                   (int(startX + i / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[10].get(offset + partial_lead * 3 + i)/200))),
                   (0,0,0), thickness)
stop = timeit.default_timer()
print('Lead11 time ',stop - start)
start = timeit.default_timer()
#Lead 12 - V6
baseY = margin + gridSize * 15
startX = margin + (img_col - margin * 2 - 80) / 4 * 3;
for i in range(1, partial_lead + 200 - 1):
    img = cv2.line(img,
                   (int(startX + (i - 1) / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[11].get(offset + partial_lead * 3 + i - 1) / 200))),
                   (int(startX + i / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[11].get(offset + partial_lead * 3 + i)/200))),
                   (0,0,0), thickness)
stop = timeit.default_timer()
print('Lead12 time ',stop - start)
start = timeit.default_timer()
# Long 10s
baseY = margin + gridSize * 21
startX = margin
for i in range(1, int(5200-1)):
    img = cv2.line(img,
                   (int(startX + (i - 1) / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[1].get(i - 1 + offset) / 200))),
                   (int(startX + i / 2.5), int(textSpace + baseY - (gridSize * 2 * df_ecg_filtered.loc[1].get(i + offset) / 200))),
                   (0,0,0), thickness)
stop = timeit.default_timer()
print('Lead2 Long time ',stop - start)
# 그려진 파일을 보여준다
#cv2.imshow("image",img)
file_name = df_info['filename'][0]
cv2.imwrite(save_path+file_name+'.jpg', img)
print(file_name, ' ', stop - first)