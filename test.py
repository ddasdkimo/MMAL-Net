# coding=utf-8
import torch
import torch.nn as nn
import sys
from tqdm import tqdm
from config import input_size, root, proposalN, channels,coordinates_cat
from utils.read_dataset import read_dataset
from utils.auto_laod_resume import auto_load_resume
from utils.vis import image_with_boxes
import numpy as np
from networks.model import MainNet
from tensorboardX import SummaryWriter
import os


def testmodel(num_classes, pth_path, batch_size, set, name):
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'

    CUDA = torch.cuda.is_available()
    DEVICE = torch.device("cuda" if CUDA else "cpu")


# load dataset
    _, testloader = read_dataset(input_size, batch_size, root, set)

# 定义模型
    model = MainNet(proposalN=proposalN,
                num_classes=num_classes, channels=channels)

    model = model.to(DEVICE)
    criterion = nn.CrossEntropyLoss()

# 加载checkpoint
    if os.path.exists(pth_path):
        epoch = auto_load_resume(model, pth_path, status='test')
    else:
        sys.exit('There is not a pth exist.')

    print('Testing')
    raw_correct = 0
    object_correct = 0
    model.eval()
    runingaccuracy = 0
    with torch.no_grad():
        for i, data in enumerate(tqdm(testloader)):
            x, y = data
            x = x.to(DEVICE)
            y = y.to(DEVICE)
            local_logits, local_imgs = model(x, epoch, i, 'test', DEVICE)[-2:]
        # local
            pred = local_logits.max(1, keepdim=True)[1]
            object_correct += pred.eq(y.view_as(pred)).sum().item()
        
            with SummaryWriter(log_dir=os.path.join("testlog", name), comment='test') as writer:
                runingaccuracy = runingaccuracy + len(y)
                writer.add_scalar('Object branch accuracy',100 *  object_correct / runingaccuracy, i)
             # writer.add_image('acc image',local_imgs[0], i, dataformats='HWC')
                if pred.eq(y.view_as(pred)).sum().item() < batch_size:
                    print("")
                if i % 10 == 0 or pred.eq(y.view_as(pred)).sum().item() < batch_size:
                    acc_imgs = []
                    loss_imgs = []
                    local_imgs = local_imgs.cpu()
                    torf = pred.eq(y.view_as(pred))
                    for j, indice_ndarray in enumerate(local_imgs):
                        img = image_with_boxes(local_imgs[j])
                        if torf[j]:
                            acc_imgs.append(img)
                        else:
                            loss_imgs.append(img)
                    if len(acc_imgs)>0:
                        acc_imgs = np.concatenate(acc_imgs, axis=1)
                        writer.add_images('acc object image with windows', acc_imgs, i, dataformats='HWC')
                    if len(loss_imgs)>0:
                        loss_imgs = np.concatenate(loss_imgs, axis=1)
                        writer.add_images('loss object image with windows', loss_imgs, i, dataformats='HWC')
            
        print('\nObject branch accuracy: {}/{} ({:.2f}%)\n'.format(
        object_correct, len(testloader.dataset), 100. * object_correct / len(testloader.dataset)))
if __name__ == '__main__':
    # dataset
    # root = "../datasets/auto/1629450843.8616877/mmal/"  # dataset path
    root = ""
    num_classes = 52
    pth_path = "checkpoint/mmalhk/1629450988.27802/epoch200.pth"
    batch_size = 8
    set = "hk"
    name = "test123"
    testmodel(num_classes, pth_path, batch_size, set, name)
    
            