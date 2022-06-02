import os
import sys
import torch
from mmaction.apis import init_recognizer, inference_recognizer,my_inference_recognizer,my_blend
sys.path.append('/home/Video-Swin-Transformer-master/demo')
from demo import get_output
sys.path.append('/home/mmdetection')
from det_video import mmdet_video
def my_test(config_file,checkpoint_file,labels,videoInfo):
    device = 'cuda:3'
    device = torch.device(device)
    model = init_recognizer(config_file, checkpoint_file, device=device)
    video = videoInfo['FilePath']  #视频位置
    #video = '/home/Video-Swin-Transformer-master/demo/demo.mp4'
    results = my_inference_recognizer(model, video, labels)
    return results
    
def getResult(videoInfo):
    config_file = '/home/Video-Swin-Transformer-master/work_dirs/k400_new/k400_new.py'
    checkpoint_file = '/home/Video-Swin-Transformer-master/work_dirs/k400_new/latest.pth'
    labels = '/home/Video-Swin-Transformer-master/data/kinetics400/danger.txt'
    k1=my_test(config_file,checkpoint_file,labels,videoInfo)
    config_file2= '/home/Video-Swin-Transformer-master/work_dirs/k400_new_4/k400_new_4.py'
    checkpoint_file2 = '/home/Video-Swin-Transformer-master/work_dirs/k400_new_4/latest.pth'
    k2=my_test(config_file2,checkpoint_file2,labels,videoInfo)
    r=my_blend(labels,k1,k2)
    return r
def getVideo(filePath,outPath,lable):
    get_output(filePath,outPath,lable,font_scale=5)

def getDet(video_path,out_path):
    mmdet_video(video_path,out_path)
