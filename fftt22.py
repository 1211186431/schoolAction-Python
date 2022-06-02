from flask import Flask
from flask import request
import csv
import os
import json
from flask import make_response
from flask_cors import CORS
import redis
#from threading import Thread
#from redisTest import redisTest
app = Flask(__name__,static_url_path='/python',
            static_folder='static',
            template_folder='templates')

CORS(app, supports_credentials=True)

@app.route("/t1",methods=['GET','POST'])
def hello():
    b={'result':'111'}
    if request.method == 'GET':
        name =request.args.get('name','')
        b['result']=name
    #b={'result':tttt()}
    elif request.method == 'POST':
        print("111")
    return b

@app.route("/job1",methods=['GET','POST'])
def updateTaskJob():
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    updateTask=r.lpop("outlist1")
    upStr="none"
    
    if (not updateTask==None):
        updateTask=eval(updateTask)
        upStr=str(updateTask["taskId"])+","+str(updateTask["taskState"])+","+updateTask["imgPath"]
    return upStr

@app.route("/job2",methods=['GET','POST'])
def insertResultJob():
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    insertResult=r.lpop("outlist2")
    upStr="none"
    if(not insertResult==None):
        insertResult=eval(insertResult)
        upStr=insertResult["top"]+"A"+str(insertResult["taskId"])
    return upStr

@app.route("/job3",methods=['GET','POST'])
def updateTaskResultJob():
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    updateResult=r.lpop("outlist3")
    upStr="none"
    if(not updateResult==None):
        updateResult=eval(updateResult)
        upStr=str(updateResult["taskId"])+","+updateResult["filePath"]+","+updateResult["top1"]
    return upStr

@app.route("/uploadVideo",methods=['GET','POST'])
def uploadVideo():
    image = request.files['file']
    path = "/home/static/"
    file_path = path + image.filename
    image.save(file_path)
    return file_path
@app.route("/uploadModel",methods=['GET','POST'])
def uploadModel():
    image = request.files['file']
    path = "/home/model/"
    file_path = path + image.filename
    image.save(file_path)
    return "suss"
@app.route("/getvoi",methods=['GET'])
def getImg():
    #获取文件名
    ss = request.args['name']
    #文件加至返回响应
    response = make_response(ss)    
    return response

@app.route("/t3",methods=['GET','POST'])
def hello3():
    #data = {'key1':'value1','key2':'value2'}
    data=[("111","222"),("333","444")]
    data={"key1":"111","key2":2222}
    r = requests.post('http://127.0.0.1:8082/t1',data=data)
    return '200'
@app.route("/ping",methods=['GET','POST'])
def testPing():
    return '200'

@app.route("/t4",methods=['GET','POST'])
def hello4():
    p = "static/"
    dirs = os.listdir(p)
    filelist=[]
    for file in dirs:
        f={'fileName':file}
        filelist.append(f)

    return {'data':filelist}

@app.route("/uploadTask",methods=['GET','POST'])
def uploadTask():
    if request.method == 'POST':
        b1=list(request.form.to_dict().keys())
        j = json.loads(b1[0]) #dict
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        r.rpush("list0",str(j))
    return "suss"

def myFlask():
     app.run(host='0.0.0.0',
      port= 8080,
      debug=True)
#def myRedis():
#    t=redisTest()
#    t.init_Task()

if __name__ == "__main__":
    #t1 = Thread(target=myRedis)
    #t1.start()
    myFlask()
