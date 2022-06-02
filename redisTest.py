import redis
import time
import sys
import mmcv
sys.path.append('Video-Swin-Transformer-master')
from videoAction import getResult,getVideo,getDet
class redisTest:
    def __init__(self): #初始化
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        self.r=r
    def init_Task(self):  #开启处理任务
        while True:
            l=self.r.blpop(["list2", "list1","list0"],0)
            self.task_Result(l[1])
    def insert_Task(self,videoInfo):  #添加任务
        videoInfo=eval(videoInfo)
        if videoInfo['Priority'] ==0:   #按照优先级设置
            self.r.rpush("list0",videoInfo)
        elif videoInfo['Priority'] ==1:
            self.r.rpush("list1",videoInfo)
        elif videoInfo['Priority'] ==2:
            self.r.rpush("list2",videoInfo)
        
        
    def task_Result(self,videoInfo):
        videoInfo=eval(videoInfo)

        video = mmcv.VideoReader(videoInfo['FilePath'])
        img = video.read()
        mmcv.imwrite(img, '/home/static/img_'+str(videoInfo['TaskId'])+'.jpg')

        data0={"taskId":videoInfo['TaskId'],"taskState":2,"imgPath":'/home/static/img_'+str(videoInfo['TaskId'])+'.jpg'}            
        self.r.rpush("outlist1",str(data0))
        #/updateTaskState
        #url=oldurl+'/updateTaskState'
       # r = requests.post(url,data=data0)  
        
        videoResult=getResult(videoInfo)
        result=""
        for item in videoResult:
            top=item[0]
            acc=item[1]
            result+=str(top)+","+str(acc)+";"
        top1=videoResult[0][1]
        filePath="/home/static/result_"+videoInfo['FilePath'].split("/")[-1]
        #detPath="/home/static/result_det_"+videoInfo['FilePath'].split("/")[-1]
        if(videoInfo['NeedDet']==1):
            getDet(videoInfo['FilePath'],videoInfo['FilePath'])
        if(videoInfo['NeedVideo']==1):
            video_lable=videoResult[0][0];
            if(videoResult[0][1]<0.8):
                video_lable='safe'
            getVideo(videoInfo['FilePath'],filePath,video_lable)
        else:
            video_lable=videoResult[0][0];
            if(videoResult[0][1]<0.8):
                video_lable='safe'
            filePath=""
        data1={"top":result,"taskId":videoInfo['TaskId']}  #  /insertResult
        self.r.rpush("outlist2",str(data1))
        data2={"taskId":videoInfo['TaskId'],"filePath":filePath, "top1":str(top1)} #/updateTaskResult
        self.r.rpush("outlist3",str(data2))




