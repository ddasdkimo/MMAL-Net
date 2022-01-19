# coding=utf-8
from glob import glob
from flask import Flask, escape, request, jsonify, make_response, render_template
from flask_cors import CORS
import torch
import torch.nn as nn
from torch.optim.lr_scheduler import MultiStepLR
import shutil
import time
import imageio
import numpy as np
from PIL import Image
from torchvision import transforms
import json

from config import num_classes, model_name, model_path, lr_milestones, lr_decay_rate, input_size, \
    root, end_epoch, save_interval, init_lr, batch_size, CUDA_VISIBLE_DEVICES, weight_decay, \
    proposalN, set, channels, FLASK_SECRET_KEY, TMPFILE
from utils.train_model import train
from utils.read_dataset import read_dataset
from utils.auto_laod_resume import auto_load_resume
from networks.model import MainNet
import os

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
os.environ['CUDA_VISIBLE_DEVICES'] = CUDA_VISIBLE_DEVICES
filecount = 0


def loadImage(path):
    img = imageio.imread(path)
    if len(img.shape) == 2:
        img = np.stack([img] * 3, 2)
    img = Image.fromarray(img, mode='RGB')
    img = transforms.Resize((input_size, input_size), Image.BILINEAR)(img)
    img = transforms.RandomHorizontalFlip()(img)
    img = transforms.ColorJitter(brightness=0.2, contrast=0.2)(img)
    img = transforms.ToTensor()(img)
    img = transforms.Normalize([0.485, 0.456, 0.406], [
                               0.229, 0.224, 0.225])(img)
    img = img.unsqueeze(0)
    return img


def main():
    global model, classes, device
    # 讀取類型
    with open(root+'/class.txt', 'r') as file:
        jsonstr = file.read()
        classes = json.loads(jsonstr)
    model = MainNet(proposalN=proposalN,
                    num_classes=num_classes, channels=channels)
    # 加载checkpoint
    save_path = os.path.join(model_path, model_name)
    auto_load_resume(model, save_path, status='test')

    device = torch.device("cuda:0" if CUDA_VISIBLE_DEVICES != 'CPU' else "cpu")
    if CUDA_VISIBLE_DEVICES != 'CPU':
        model = model.cuda()  # 部署在GPU
        model.eval()
    

@app.route("/detect", methods=['POST'])
def detect():
    global model, classes, filecount, device
    img = request.files.get('file')
    starttime = time.time()
    fileName = str(filecount)
    filecount = filecount+1
    if not os.path.isdir(TMPFILE+"photo/"):
        os.mkdir(TMPFILE+"photo/")

    filename = TMPFILE+"photo/"+fileName+".jpg"
    img.save(filename)
    image = loadImage(filename)
    if CUDA_VISIBLE_DEVICES != 'CPU':
        image = image.cuda()
    with torch.no_grad():
        probs, indices = model(image, 0, 0, status='inference', DEVICE=device)
        # print(classes[str(int(indices[0])+1)])
    try:
        os.remove(filename)
    except OSError as e:
        print(e)
    probslist = probs.tolist()
    indicesList = [i  for i in indices.tolist()]
    print("使用時間:"+str(time.time() - starttime))
    print(classes[str(indicesList[0]+1)])
    data = {"probs":[round(i,2) for i in probslist],"indices":indicesList,"classes":classes}
    return data

@app.route("/test", methods=['POST'])
def test():
    global model, classes, filecount, device
    img = request.files.get('file')
    fileName = str(filecount)
    filecount = filecount+1
    if not os.path.isdir(TMPFILE+"photo/"):
        os.mkdir(TMPFILE+"photo/")

    filename = TMPFILE+"photo/"+fileName+".jpg"
    img.save(filename)
    image = loadImage(filename)
    if CUDA_VISIBLE_DEVICES != 'CPU':
        image = image.cuda()
    with torch.no_grad():
        probs, indices = model(image, 0, 0, status='inference', DEVICE=device)
        # print(classes[str(int(indices[0])+1)])
    try:
        os.remove(filename)
    except OSError as e:
        print(e)
    probslist = probs.tolist()
    indicesList = [i + 1 for i in indices.tolist()]
    # print(classes[str(indicesList[0])])
    
    z = list(zip([round(i,2) for i in probslist],[classes[str(i)] for i in indicesList]))
    z.sort(reverse=True)
    return jsonify(z)


# if __name__ == '__main__':
    # main()
main()
