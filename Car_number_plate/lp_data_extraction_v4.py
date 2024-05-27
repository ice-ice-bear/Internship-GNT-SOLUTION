# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 09:19:24 2022

@author: yujeongchoe
"""

#%% 맨 앞 그림파일명만 추출
import os
import shutil

date = "230531"

file_path = r"R:/seatbelt/highway_send_data/"+ date + "_target"

file_list = os.listdir(file_path) #파일 목록
output_list = [] #center 파일명만 있는 리스트
for i in file_list:
    output_list.append(i)


#%% base64

import base64
import cv2


path2 = r'/'+ date +'_base64' #base64 파일이 들어갈 폴더
os.mkdir(r'R:/seatbelt/highway_send_data/'+ date +'_base64')
os.mkdir(r'R:/seatbelt/highway_send_data/'+ date +'_all')
for i in output_list:
    with open (r'R:/seatbelt/highway_send_data/'+ date + '_target/'+i, 'rb') as img:
               base64_str = base64.b64encode(img.read())
               f = open(r'R:/seatbelt/highway_send_data/'+ date +'_base64/' + i[:-4] + '.txt', 'w+')
               f.write(str(base64_str, 'utf-8'))
               f.close()
               
#%% 통신
import requests
import time
import os

#타조아이 LPR 연결 후 
url = 'http://192.168.0.77:8082/lpr'
path_in = r'R:/seatbelt/highway_send_data/'+ date +'_base64' # base64 data 있는 곳

base64_list = os.listdir(path_in) #파일 목록

plate_7 = [] #7로 시작하는 번호판 모을것임
plate_0to6 = []
plate_8to9 = []
plate_trash = []
real_count = 0;
ex1 = 0
a = 227
for i in base64_list[a:]:
    ex1 = ex1 + 1
    if ex1 > 10:
        time.sleep(0.8)
        ex1 = 0        
    real_count = real_count + 1
    print('현재 번호는 ' + str(real_count))
    file = open(path_in + '\\' + i, 'rb') #데이터 열어서
    upload = {
        'name' : 'ysw',
        'imgBuffer' : file,
        }
    res = requests.post(url, data = upload) #서버에 요청
    out = res.text #번호판 결과 나옴
    if out.startswith('7'):
        plate_7.append(i) #7로 시작하면 파일이름 저장
        print ('plate number 7: ' + str(len(plate_7)))
    elif out.startswith('8') or out.startswith('9'):
        plate_8to9.append(i)
        print ('plate number 8to9: ' + str(len(plate_8to9)))
    elif (out.startswith('0') or out.startswith('1')or out.startswith('2')
        or out.startswith('3')or out.startswith('4')or out.startswith('5')or out.startswith('6')):
        plate_0to6.append(i)  
        print ('plate number 0to6: ' + str(len(plate_0to6)))
    else:
        plate_trash.append(i)
        print ('plate number trash: '+ str(len(plate_trash)))
   
#%% 7로 시작하는 데이터 (center, side1, side2, side3) 저장
import os
import shutil


file_path = r'D:\hov_data\\' + date +'_target_all' #모든 데이터
path_7_out = r'D:\hov_data\plate_7_'+date# 7로 시작하는 데이터만 있는 폴더
path_0to6_out = r'D:\hov_data\plate_0to6_'+date # 0~6로 시작하는 데이터만 있는 폴더
path_8to9_out = r'D:\hov_data\plate_8to9_'+date # 8,9로 시작하는 데이터만 있는 폴더
#path_trash_out = r'D:\hov_data\plate_trash_'+date # 미검지 데이터

os.mkdir(path_7_out)
os.mkdir(path_0to6_out)
os.mkdir(path_8to9_out)
#os.mkdir(path_trash_out)
data_all = os.listdir(file_path) #파일목록

#7로 시작하는 번호판 이미지 모두 모으기
for i in plate_7:
    for j in data_all :
        if i[7:-6] in j:
            shutil.copy2(file_path + '\\' + j, path_7_out + '\\' + j)
            shutil.copy2(file_path + '\\' + i[:-3] + 'jpg', path_7_out + '\\' + i[:-3] + 'jpg')
'''   
#8,9로 시작하는 번호판 이미지 모두 모으기        
for i in plate_8to9:
    for j in data_all :
        if i[7:-6] in j:
            shutil.copy2(file_path + '\\' + j, path_8to9_out + '\\' + j)
            shutil.copy2(file_path + '\\' + i[:-3] + 'jpg', path_8to9_out + '\\' + i[:-3] + 'jpg')
            
#0~6으로 시작하는 번호판 이미지 모두 모으기   
for i in plate_0to6:
    for j in data_all :
        if i[7:-6] in j:
            shutil.copy2(file_path + '\\' + j, path_0to6_out + '\\' + j)
            shutil.copy2(file_path + '\\' + i[:-3] + 'jpg', path_0to6_out + '\\' + i[:-3] + 'jpg')
            
'''