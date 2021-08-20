import requests as req
from tqdm import tqdm
import time
import os
import zipfile
import toMMALByOne
url = 'http://192.168.50.100:9991/downloadfile?filename=dataset/1629364395.044881/persion.zip'
if not os.path.isdir("../datasets/auto/"):
    os.mkdir("../datasets/auto/")
topath = "../datasets/auto/"+str(time.time())+"/"
if not os.path.isdir(topath):
    os.mkdir(topath)
def download(url):
    filename = topath+url.split('/')[-1]
    r = req.get(url, stream=True)
    with open(filename, 'wb') as f:
        for data in tqdm(r.iter_content(1024)):
            f.write(data)
    return filename
download(url)

zf = zipfile.ZipFile(topath+url.split('/')[-1], 'r')
zf.extractall(topath+"/file")
classtype = []
toMMALByOne.create_mmal(classtype,topath+"file/", topath+"mmal/")

print("")
num_classes = len(classtype)
f = open('config.txt', 'r')
filestr = f.read()
checkpoint = "./checkpoint/mmalhk/"+str(time.time())
filestr = filestr.replace("modelpath",checkpoint)
filestr = filestr.replace("datasetpath",topath+"mmal/")
filestr = filestr.replace("num_classes_path",str(len(classtype)))
f = open('config.py', 'w')
f.write(filestr)
f.close()
os.popen("screen /usr/bin/env /usr/bin/python3 train.py")
os.popen("screen tensorboard --logdir="+checkpoint+" --host=0.0.0.0")
print("end")