from mmdet.apis import init_detector, inference_detector
import mmcv
import numpy as np
import os
import cv2
#返回人坐标
def process_image(model, image_path):
    results = inference_detector(model, image_path)
    return results[0]
#切帧
def cut_frames(video_path,output_dir):
    video = mmcv.VideoReader(video_path)
    video.cvt2frames(output_dir)
#合成视频
def frames_video(dir_path,video_path):
    mmcv.frames2video(dir_path, video_path)  
#初始化
def my_init_cfg():
    config_file = '/home/mmdetection/configs/yolox/yolox_l_8x8_300e_coco.py'
    checkpoint_file = '/home/mmdetection/checkpoints/yolox_l_8x8_300e_coco_20211126_140236-d3bd2b23.pth'
    model = init_detector(config_file, checkpoint_file, device='cuda:0')
    return model
#打开图片目录
def open_dir(dir_path):
    pathDir = os.listdir(dir_path)
    file_list=[]
    for filename in pathDir: 
        from_path = os.path.join(dir_path, filename)
        file_path=(filename,from_path)
        if (filename.split(".")[-1]=='jpg'):
            file_list.append(file_path)
    return file_list
#按照坐标将人物切出来
def cut_person(result,file_path,new_path):
    i=0
    for r in result:
        r=r.tolist()
        x=int(r[0])
        x1=int(r[2])
        y=int(r[1])
        y1=int(r[3])
        if(not i==0):
            file_path=new_path
        image = cv2.imread(file_path)
        linet = cv2.LINE_4
        image = cv2.rectangle(image, (x, y), (x1, y1), (0, 0, 255), linet,2)
        cv2.imwrite(new_path,image)
        i+=1
        

#生成视频
def demo_video(model,pic_list,out_path):
    for pic in pic_list:
        img=pic[1]
        results = process_image(model,img)
        results = results[results[:, 4] > 0.6]
        cut_person(results,img,out_path+"/"+pic[0])
#删除文件
def deldir(dir1):
    if not os.path.exists(dir1):
        return False
    if os.path.isfile(dir1):
        os.remove(dir1)
        return
    for i in os.listdir(dir1):
        t = os.path.join(dir1, i)
        if os.path.isdir(t):
            deldir(t)#重新调用次方法
        else:
            os.unlink(t)


def mmdet_video(video_path,out_path):
    model=my_init_cfg()
    cut_frames(video_path,'/home/mmdetection/pic')
    list1=open_dir('/home/mmdetection/pic')
    demo_video(model,list1,'/home/mmdetection/pic')
    frames_video('/home/mmdetection/pic',out_path)
    deldir("/home/mmdetection/pic") 
    





