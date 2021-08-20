#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, isdir, join
from os import walk
import json
import os
from tqdm import tqdm
import shutil


def create_mmal(classtype, mypath, topath):
    if not os.path.exists(topath):
        os.makedirs(topath)
    if not os.path.exists(topath+"images"):
        os.makedirs(topath+"images")
    # test 數量
    testcount = 0.1
    # 取得所有檔案與子目錄名稱
    outputtrain = ""
    outputtest = ""
    pathcount = 0
    for root, dirs, files in walk(mypath):
        if len(files) > 100:
            pathcount += 1
            print(str(pathcount))
        count = 0
        for imgitem in tqdm(files):
        # for imgitem in files:
            if "jpg" in imgitem:
                itemtype = root.split('/')[len(root.split('/'))-1].replace(" ","_")
                if itemtype not in classtype:
                    classtype.append(itemtype)
                count += 1
                if count / len(files) < testcount:
                    outputtest = outputtest + itemtype+"_"+imgitem+" " + \
                    str(classtype.index(itemtype)+1) + "\n"
                else:
                    outputtrain = outputtrain + itemtype+"_"+imgitem+" " + \
                    str(classtype.index(itemtype)+1) + "\n"
                
                shutil.copyfile(root+"/"+imgitem, topath+"/images/"+itemtype+"_"+imgitem)
    with open(topath+"train.txt", "w") as text_file:
        text_file.write(outputtrain)
    with open(topath+"test.txt", "w") as text_file:
        text_file.write(outputtest)
    myDict = dict(enumerate(classtype, start=1))
    with open(topath+'class.txt', 'w') as file:
        file.write(json.dumps(myDict))
if __name__ == '__main__':
    classtype = []
    mypath = "../datasets/hk/"
    topath = "../datasets/mmal_hk/"
    create_mmal(classtype, mypath, topath)
    