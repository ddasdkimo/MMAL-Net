from utils.indices2coordinates import indices2coordinates
from utils.compute_window_nums import compute_window_nums
import numpy as np

CUDA_VISIBLE_DEVICES = "0"  # The current version only supports one GPU training
TMPFILE = "/dev/shm/"
FLASK_SECRET_KEY = "asjdfliajsdoivj$%^&*("
set = "hk"
model_name = "epoch122.pth"
batch_size = 8
vis_num = batch_size  # The number of visualized images in tensorboard
eval_trainset = True  # Whether or not evaluate trainset
save_interval = 1
max_checkpoint_num = 200
end_epoch = 200
init_lr = 0.001
lr_milestones = [60, 100]
lr_decay_rate = 0.1
weight_decay = 1e-4
stride = 32
channels = 2048
input_size = 448

# The pth path of pretrained model
pretrain_path = "./models/pretrained/resnet50-19c8e357.pth"


# windows info for CAR and Aircraft
N_list = [3, 2, 1]
proposalN = sum(N_list)  # proposal window num
window_side = [192, 256, 320]
iou_threshs = [0.25, 0.25, 0.25]
ratios = [[6, 6], [5, 7], [7, 5],
          [8, 8], [6, 10], [10, 6], [7, 9], [9, 7],
          [10, 10], [9, 11], [11, 9], [8, 12], [12, 8]]
model_path = "./checkpoint/mmalhk/1629365659.061103"      # pth save path
# root = "../datasets/auto/1629365650.940147/mmal/"  # dataset path
root = "./checkpoint/mmalhk/1629365659.061103"  # dataset path
num_classes = 5
window_nums = compute_window_nums(ratios, stride, input_size)
indices_ndarrays = [np.arange(0, window_num).reshape(-1, 1)
                    for window_num in window_nums]
coordinates = [indices2coordinates(indices_ndarray, stride, input_size, ratios[i])
               for i, indices_ndarray in enumerate(indices_ndarrays)]  # 每个window在image上的坐标
coordinates_cat = np.concatenate(coordinates, 0)
window_milestones = [sum(window_nums[:i+1]) for i in range(len(window_nums))]
window_nums_sum = [0, sum(window_nums[:3]), sum(
        window_nums[3:8]), sum(window_nums[8:])]
