# coding=utf-8
from flask import Flask, escape, request, jsonify, make_response, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = "asdfsadfwe"

@app.route("/", methods=['GET'])
def index():
    '''
    projectname=mmal_gender&&project_model_path=./checkpoint/mmal_gender&&project_root=./datasets/mmal_gender
    '''
    projectname = request.args.get('projectname')
    project_model_path = request.args.get('project_model_path')
    project_root = request.args.get('project_root')
    with open('./configT.py', 'r') as file:
        configT = file.read()
        configT = configT.replace("projectname",projectname)
        configT = configT.replace("project_model_path",project_model_path)
        configT = configT.replace("project_root",project_root)
    with open('./config_tmp.py', 'w') as wfile:
        wfile.write(configT)
        wfile.close()

    return configT