# coding=utf-8
from flask import Flask, escape, request, jsonify, make_response, render_template
from flask_cors import CORS
import os

import json
from createTrainData import CreateTrainData,CreateTrainDataProcess
import time

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = False
app.config['SECRET_KEY'] = "asdfsadfwe"
trainDataList = [] # 訓練排程
#訓練排程管理
mCreateTrainDataProcess = CreateTrainDataProcess(trainDataList)
mCreateTrainDataProcess.start()
@app.route("/", methods=['GET'])
def index():
    '''
    project_url=https://ftpweb.intemotech.com/test/1.mp3&&projectname=rai_220119&&project_model_path=checkpoint/rai_220119&&project_root=datasets/rai_220119
    '''
    # project_url = request.args.get('project_url')
    # projectname = request.args.get('projectname')
    # project_model_path = request.args.get('project_model_path')
    # project_root = request.args.get('project_root')
    # with open('./configT.py', 'r') as file:
    #     configT = file.read()
    #     configT = configT.replace("projectname", projectname)
    #     configT = configT.replace("project_model_path", project_model_path)
    #     configT = configT.replace("project_root", project_root)
    # with open('./config_tmp.py', 'w') as wfile:
    #     wfile.write(configT)
    #     wfile.close()
    # if not os.path.isdir(project_root):
    #     os.mkdir(project_root)

    # if not os.path.isdir(project_model_path):
    #     os.mkdir(project_model_path)

    # # 下載檔案
    # file = requests.get(project_url, stream=True)
    # with open(project_root+"/"+os.path.basename(project_url), "wb") as pdf:
    #     for chunk in file.iter_content(chunk_size=1024):
    #         if chunk:
    #             pdf.write(chunk)

    return "configT"


@app.route('/createproject', methods=['POST'])
def createproject():
    # 接受前端發來的資料
    data = json.loads(request.get_data())
    trainDataList.append(CreateTrainData(data))

    return jsonify(getTrainDataList())
    
@app.route('/getproject')
def getproject():
    return jsonify(getTrainDataList())


def getTrainDataList():
    listdata = list()
    for item in trainDataList:
        listdata.append(item.message())
    listdata.reverse()
    return  listdata