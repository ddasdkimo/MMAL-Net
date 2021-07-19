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
# 相關 checkpoint 下載
RUN mkdir -p /workspace/MMAL-Net/checkpoint/mmal_0715_33
RUN mkdir -p /workspace/MMAL-Net/datasets/mmal_0715_33
RUN cd /workspace/MMAL-Net/models/pretrained && wget https://ftpweb.intemotech.com/Model_Zoo/MMAL-Net/resnet50-19c8e357.pth
RUN cd /workspace/MMAL-Net/checkpoint/mmal_0715_33 && wget https://ftpweb.intemotech.com/MMALRuning/33/epoch34.pth
RUN cd /workspace/MMAL-Net && wget https://ftpweb.intemotech.com/MMALRuning/33/config.py -O config.py
RUN cd /workspace/MMAL-Net/datasets/mmal_0715_33/ && wget https://ftpweb.intemotech.com/MMALRuning/33/class.txt
WORKDIR /workspace/MMAL-Net

# docker build -t raidavid/mmfashion:v1 docker/
# docker run --gpus all -d \
# -it \
# --name mmal \
# --restart=always \
# raidavid/mmal_net bash -c "python app.py"

# docker exec -it mmal /bin/bash