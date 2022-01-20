import os
import time
import cv2
import threading
import requests
import zipfile
import json
import subprocess


class ModelTrainData():
    train_raw_accuracy = 0.0
    train_local_accuracy = 0.0
    test_raw_accuracy = 0.0
    test_local_accuracy = 0.0
    epoch = 0
    modelname = ""
    def msg(self):
        return {"name":self.modelname,"train_raw_accuracy": self.train_raw_accuracy,
                "train_local_accuracy": self.train_local_accuracy, "test_raw_accuracy": self.test_raw_accuracy, "test_local_accuracy": self.test_local_accuracy, "epoch": self.epoch}

    def start(self,name):
        self.modelname = name
        p = subprocess.Popen(
            'cd /home/ubuntu/MMAL-Net ; /usr/bin/python3 train.py', shell=True, stdout=subprocess.PIPE)
        p.returncode
        p.poll()

        while p.poll() == None:
            msgstr = p.stdout.readline()
            while len(msgstr) > 0:
                print(msgstr)
                msgstr = p.stdout.readline().decode('ascii')
                if msgstr[0:9] == "Train set":
                    sp = msgstr[25:-2].split('%, local accuracy: ')
                    self.train_raw_accuracy = float(sp[0])
                    self.train_local_accuracy = float(sp[1])
                if msgstr[0:8] == "Test set":
                    sp = msgstr[24:-2].split('%, local accuracy: ')
                    self.test_raw_accuracy = float(sp[0])
                    self.test_local_accuracy = float(sp[1])
                if msgstr[0:8] == 'Training':
                    self.epoch = int(msgstr[8:].split("epoch\n")[0])
                time.sleep(0.5)


class CreateTrainData(threading.Thread):
    states = "排程中"
    runing = False
    mModelTrainDatalist = []

    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data

    def message(self):
        trainList = []
        for item in self.mModelTrainDatalist:
            trainList.append(item.msg())
        return {"projectName": self.data.get('projectName'), "modelist": self.data.get('modelist'), "states": self.states, "trainList":trainList}

    def zip_list(self, file_path, to_path, name):
        zf = zipfile.ZipFile(file_path+name, 'r')
        zf.extractall(to_path)

    def unzip(self, path, topath, name):
        self.zip_list(path, topath, name)

    def run(self):
        self.runing = True
        self.states = "啟動"
        data = self.data
        try:
            modelist = data.get('modelist')
            dwdatapathlist = data.get('dwdatapathlist')

            projectname = data.get('projectName')
            epoch = data.get('epoch')
            # project_url = 'checkpoint/'+projectname
            project_model_path = 'checkpoint/'+projectname
            project_root = 'datasets/'+projectname

            if not os.path.isdir(project_root):
                os.mkdir(project_root)

            if not os.path.isdir(project_model_path):
                os.mkdir(project_model_path)
            self.states = "開始下載檔案"
            filecount = 0
            for url in dwdatapathlist:
                filecount += 1
                count = 0
                # 下載檔案
                file = requests.get(url, stream=True)
                with open(project_root+"/"+os.path.basename(url), "wb") as zip:
                    for chunk in file.iter_content(chunk_size=1024):
                        count += 1
                        self.states = "開始下載第 " + \
                            str(filecount)+"/"+str(len(dwdatapathlist)) + \
                            " 個檔案 "+str(count)+" KB"
                        if chunk:
                            zip.write(chunk)
                # 解壓縮
                self.states = "開始解壓縮第 " + \
                    str(filecount)+"/"+str(len(dwdatapathlist))+" 個檔案"
                self.unzip(project_root+"/", project_root+"/" +
                           modelist[filecount-1], os.path.basename(url))
            # 訓練模型
            for modelname in modelist:
                self.states = "開始訓練"+modelname
                typecount = 0
                with open(project_root+"/"+modelname+'/class.txt') as f:
                    data = json.load(f)
                    typecount = len(list(data.keys()))
                with open('./configT.py', 'r') as file:
                    configT = file.read()
                    configT = configT.replace(
                        "project_num_classes", str(typecount))
                    configT = configT.replace(
                        "project_epoch", str(epoch))
                    configT = configT.replace("projectname", modelname)
                    configT = configT.replace(
                        "project_model_path", project_model_path+"/"+modelname)
                    configT = configT.replace(
                        "project_root", project_root+"/"+modelname)
                with open('./config.py', 'w') as wfile:
                    wfile.write(configT)
                    wfile.close()
                myModelTrainData = ModelTrainData()
                self.mModelTrainDatalist.append(myModelTrainData)
                myModelTrainData.start(modelname)
                

        except:
            self.states = "發生錯誤"
        self.runing = False


class CreateTrainDataProcess(threading.Thread):
    def __init__(self, list):
        threading.Thread.__init__(self)
        self.processList = list

    def run(self):
        while True:

            time.sleep(1)
            haveruning = False
            for item in self.processList:
                if item.runing:
                    haveruning = True
            if not haveruning:
                for item in self.processList:
                    if item.states == "排程中":
                        item.start()
