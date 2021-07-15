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
RUN pip install --pre torch torchvision -f https://download.pytorch.org/whl/nightly/cu110/torch_nightly.html
RUN mkdir -p /workspace/MMAL-Net/checkpoint/RaiFit
RUN mkdir -p /workspace/MMAL-Net/datasets/RaiFit
RUN cd /workspace/MMAL-Net/models/pretrained && wget https://ftpweb.intemotech.com/Model_Zoo/MMAL-Net/resnet50-19c8e357.pth
RUN cd /workspace/MMAL-Net/checkpoint/RaiFit && wget https://ftpweb.intemotech.com/MMALRuning/31/epoch19.pth
RUN cd /workspace/MMAL-Net && wget https://ftpweb.intemotech.com/MMALRuning/31/20210713-201410config.py -O config.py
RUN cd /workspace/MMAL-Net/datasets/RaiFit/ && wget https://ftpweb.intemotech.com/MMALRuning/31/class.txt
WORKDIR /workspace/MMAL-Net