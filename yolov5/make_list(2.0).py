import os
import sys
import numpy as np
import glob

def create_txt(name, fileNames):
    with open(name+'.txt',"w", encoding = 'utf-8') as fileList:
      for i, fileName in enumerate(fileNames):
        fileList.write(fileName+"\n")

def cross_validation_list(DIR="",name='masung', K=5, VAL=False):
    fileNames = glob.glob(DIR+'\\**\\*.jpg',recursive=True)
    np.random.shuffle(fileNames)
    N = len(fileNames)
    # select 1/k of the files randomly 
    n = int(N/K)
    name=str(name)
    DIR = os.path.dirname(DIR) + '\\'
    print(DIR)
    create_txt(DIR+name,fileNames)
    for k in range(K):
        test = fileNames[k*n:(k+1)*n]
        train = fileNames[:k*n] + fileNames[(k+1)*n:]
        create_txt(DIR+name+'_'+str(k+1)+'_train', train)

        if VAL:
            val = test[:int(n/2)]
            test = test[int(n/2):]
            create_txt(DIR+name+'_'+str(k+1)+'_val', val)
            create_txt(DIR+name+'_'+str(k+1)+'_test', test)
        else:
            create_txt(DIR+name+'_'+str(k+1)+'_test', test)

def make_list(DIR="",name='data'):
    fileNames = glob.glob(DIR+'\\**\\*.jpg',recursive=True )
    fileNames = fileNames + glob.glob(DIR+'\\**\\*.png',recursive=True )
    # np.random.shuffle(fileNames)
    DIR_P = os.path.dirname(DIR) + '\\'
    print(DIR_P)
    create_txt(DIR_P+name,fileNames)

def main():
    DIR = r"C:\Users\GnT\Desktop\yolov5_lsr\datasets\images"
    NAME = 'lsr_230113'
    cross_validation_list(DIR, name=NAME, VAL = True)
    # make_list(DIR, name = NAME)

if __name__ == "__main__":
    # execute only if run as a script
    main()