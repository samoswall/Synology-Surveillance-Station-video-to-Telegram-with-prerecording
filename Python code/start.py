import script_config
import telebot
import requests
import time
import os
import json
from flask import Flask, request, abort

chat_id = script_config.chat_id
token = script_config.token

syno_ip = script_config.syno_ip
synohook_port = script_config.synohook_port
syno_url = 'http://' + syno_ip + ':5000/webapi/entry.cgi'
old_last_video_id = '0'
video_offset = 0

with open("/bot/syno_cam_config.json") as f:
    cam_load = json.load(f)
syno_sid = cam_load['SynologyAuthSid']
    
def get_last_id_video(cam_id):
    take_video_id = requests.get(syno_url,
        params={'version': '6', 'cameraIds': cam_id, 'api': 'SYNO.SurveillanceStation.Recording',
                'toTime': '0', 'offset': '0', 'limit': '1', 'fromTime': '0', 'method': 'List', '_sid': syno_sid}).json()['data']['recordings'][0]['id']
    return take_video_id

def get_last_video(video_id, offset):
    download = requests.get(syno_url + '/temp.mp4',
        params={'id': video_id, 'version': '6', 'mountId': '0', 'api': 'SYNO.SurveillanceStation.Recording',
                'method': 'Download', 'offsetTimeMs': offset, 'playTimeMs': '10000','_sid': syno_sid}, allow_redirects=True)
    open('/bot/temp.mp4', 'wb').write(download.content)
    return 
    
# Send Telegram message
def send_cammessage(cam_id):
    mycaption = "Camera " + str(cam_load[cam_id]['SynoName'])
    requests.post(f"https://api.telegram.org/{token}/sendMessage?chat_id={chat_id}&text={mycaption}")
    
    
# Send Telegram video
def send_camvideo(videofile):
    url = f"https://api.telegram.org/{token}/sendVideo"
    myfiles = {"chat_id": (None, chat_id), "video": open(videofile, 'rb')}
    send_video = requests.post(url, files=myfiles).json()
    print('Send:', send_video['ok'])
    print('File_Id:', send_video['result']['video']['file_id'])

def get_alarm_camera_state(cam_id):
    take_alarm = requests.get(syno_url,
        params={'version': '1', 'id_list': cam_id, 'api': 'SYNO.SurveillanceStation.Camera.Status',
                'method': 'OneTime', '_sid': syno_sid}).json()['data']['CamStatus']
    alarm_state = take_alarm.replace("[", "").replace("]", "").split()[7]
    return 1 if alarm_state == '1' else 0






app = Flask(__name__)

@app.route('/webhookcam', methods=['POST'])
def webhookcam():
    global old_last_video_id
    global video_offset
    if request.method == 'POST':
       cam_id = request.json['idcam']
       print("Received IDCam:", cam_id, ',', time.strftime("%d.%m.%Y, %H:%M:%S", time.localtime()))
       time.sleep(5)
       last_video_id = get_last_id_video(cam_id)
       if last_video_id != old_last_video_id:
           get_last_video(last_video_id, '0')
           send_cammessage(cam_id)
           old_last_video_id = last_video_id
           video_offset = 0
       else:
           video_offset += 10000
           get_last_video(last_video_id, str(video_offset))
       send_camvideo('/bot/temp.mp4')
       return 'success', 200
    else:
       abort(400)
       
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=synohook_port)
   
