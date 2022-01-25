FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-runtime
RUN apt-get update
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y wget
RUN apt-get install -y git-all
RUN cd /
RUN git clone https://github.com/ddasdkimo/MMAL-Net.git
RUN pip install flask Flask-Cors imageio tensorboardX opencv-python scikit-image

# 針對3090支援問題修改為預覽版
RUN pip uninstall -y torch torchvision
RUN pip install --pre torch torchvision torchaudio -f https://download.pytorch.org/whl/nightly/cu111/torch_nightly.html
# # 相關 checkpoint 下載
# RUN mkdir -p /workspace/MMAL-Net/checkpoint/mmal_0715_33
# RUN mkdir -p /workspace/MMAL-Net/datasets/mmal_0715_33
# RUN cd /workspace/MMAL-Net/models/pretrained && wget https://ftpweb.intemotech.com/Model_Zoo/MMAL-Net/resnet50-19c8e357.pth
# RUN cd /workspace/MMAL-Net/checkpoint/mmal_0715_33 && wget https://ftpweb.intemotech.com/MMALRuning/33/epoch34.pth
# RUN cd /workspace/MMAL-Net && wget https://ftpweb.intemotech.com/MMALRuning/33/config.py -O config.py
# RUN cd /workspace/MMAL-Net/datasets/mmal_0715_33/ && wget https://ftpweb.intemotech.com/MMALRuning/33/class.txt
# WORKDIR /workspace/MMAL-Net
RUN pip install tensorboard
RUN pip install psycopg2-binary
# 複製專案
RUN mkdir -p /home/ubuntu/MMAL-Net
WORKDIR /home/ubuntu/MMAL-Net
ADD ./ .


# docker build -t raidavid/rai_mmal_train:220120 .
# docker push raidavid/rai_mmal_train:220120

# docker run --gpus all -d \
# -it \
# --name mmal_train \
# -p 8013:5000 \
# --restart=always \
# raidavid/rai_mmal_train:220119 \
# bash -c "export FLASK_APP=trainapi && flask run --host 0.0.0.0"

# docker exec -it mmal /bin/bash
# docker stop mmal_train && docker rm mmal_train


# docker build -t raidavid/rai_mmal_inference:220125 .
# docker push raidavid/rai_mmal_inference:220125

# docker run --gpus all -d \
# -it \
# --name mmal_inference \
# --network=hkNetwork --ip 193.168.44.179 \
# -p 8014:5000 \
# --restart=always \
# raidavid/rai_mmal_inference:220125 \
# bash -c "export FLASK_APP=app && flask run --host 0.0.0.0"

# docker stop mmal_inference && docker rm mmal_inference