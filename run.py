#人脸识别
from aip import AipFace
from picamera import PiCamera
import urllib.request
import RPi.GPIO as GPIO
import base64
import pygame
import time
import smtplib
#语音合成
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
#百度人脸识别API账号
APP_ID = 'XXXXXXX'
API_KEY = 'XXXXXX'
SECRET_KEY = 'XXXXXXX'
client = AipFace(APP_ID, API_KEY, SECRET_KEY) #创建一个客户端用以访问百度云
#图像编码方式
IMAGE_TYPE = 'BASE64'
camera = PiCamera() #定义一个摄像头对象
#用户组
GROUP = 'user01'

pygame.mixer.init()
pygame.mixer.music.load('/home/pi/voice/initialize.mp3')
pygame.mixer.music.play()



#写入文件
#读取文件
#语音合成函数
def readtext():
    
    f = open('/home/pi/aip-python-sdk/test.txt', 'r')
    text = f.read()
    os.system('espeak -vzh "{}"'.format(text))
    
    
#照相函数
def getimage():
    camera.resolution = (1024,768) #摄像头界面为1024*768
    camera.start_preview() #开始摄像
    time.sleep(2)
    camera.capture('faceimage.jpg') #拍照并保存
    
    time.sleep(2)
#对照片格式的转换
def transimage():
    f = open('faceimage.jpg', 'rb')
    img = base64.b64encode(f.read())
    return img
#播放声音
def playvioce(name):
    pygame.mixer.music.load('/home/pi/voice/' +name)
    pygame.mixer.music.play()   

#发送信息到微信上   
def sendmsg(name,main):
    
    url = "https://sc.ftqq.com/SCU94689T6f48cac25a397c6d637964039fb673b55e9d533e5f3ab0.send"
    urllib.request.urlopen(url + "?text="+name+"&desp="+main)

#发送信息到邮箱
def send():
    sender = 'yudaigua@163.com'
    receivers = 'XXXXXX@qq.com'
    password='XXXXXX'
    message =  MIMEMultipart('related')
    subject = '有陌生人来访！'
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receivers
    content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>','html','utf-8')
    message.attach(content)

    file=open("faceimage.jpg", "rb")
    img_data = file.read()
    file.close()

    img = MIMEImage(img_data)
    img.add_header('Content-ID', 'imageid')
    message.attach(img)

    try:
        server=smtplib.SMTP_SSL("smtp.163.com",465) #SMTP开启的邮箱和端口
        server.login(sender,password)
        server.sendmail(sender,receivers,message.as_string())
        server.quit()
        print ("邮件发送成功！")
    except smtplib.SMTPException:
        print('邮件发送失败！')
    
#上传到百度api进行人脸检测
def go_api(image):
    result = client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP) #在百度云脸库中查找是否有匹配的人脸
    if result['error_msg'] == 'SUCCESS': #如果成功了
        name = result['result']['user_list'][0]['user_id'] #获取名字
        score = result['result']['user_list'][0]['score'] #获取相似度
        if score > 80: 
            print("欢迎%s !" %name)
            if name  == 'user01':
                sendmsg("DoorOpen",name)
                #print("欢迎%S !" %name)
                time.sleep(3)
            if name  == 'user02':
                sendmsg("DoorOpen",name)
                #print("欢迎%S !" %name)
                time.sleep(3)
        else:
            print("对不起，我不认识您！")
            playvioce('recog_fail.mp3')
            send()
            name = 'Unknow'
            return 0
        current_time = time.asctime(time.localtime(time.time())) #获取当前时间
            
        #将人员出入的记录保存到log.txt中
        f = open('Log.txt', 'a')
        f.write("Person: " + name + "  " + "Time:" + str(current_time)+'\n')
        f.close()
        return 1
    if result['error_msg'] == 'pic not has face':
        print('检测不到人脸')
        playvioce('recog_fail.mp3')
        time.sleep(2)
        return 0
    else:
        print(result['error_code'] + ' ' + result['error_code'])
        return 0
#主函数
if __name__ == '__main__':
    while True:
        time.sleep(1)
        print('准备')
        if True:
            getimage() #拍照
            img = transimage() #转换照片格式
            res = go_api(img) #将转换了格式的照片上传到百度云
            if(res == 1): # 是人脸库中的人
                print("提醒成功")
                readtext() #读出信息
            else:
                print("未能识别人脸")
            print("请重新进行人脸识别")
            time.sleep(3)