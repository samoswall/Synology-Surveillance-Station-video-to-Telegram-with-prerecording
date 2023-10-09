import pathlib
import time
import os
import json
import subprocess
import sys
import importlib.util

#import requests
#import telebot
#from flask import Flask, request, abort

# Auto pip install ----------------------------------------------------------------------------------------
try:
    import telebot
    print('The telebot module is installed')
except ModuleNotFoundError:
    print('The telebot module is NOT installed')
    print('The telebot module is Installing...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'telebot'], stdout=subprocess.DEVNULL)
finally:
    import telebot
#----------
try:
    from flask import Flask, request, abort
    print('The flask module is installed')
except ModuleNotFoundError:
    print('The flask module is NOT installed')
    print('The flask module is Installing...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask'], stdout=subprocess.DEVNULL)
finally:
    from flask import Flask, request, abort
#----------
try:
    import requests
    print('The requests module is installed')
except ModuleNotFoundError:
    print('The requests module is NOT installed')
    print('The requests module is Installing...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'], stdout=subprocess.DEVNULL)
finally:
    import requests
#----------------------------------------------------------------------------------------------------------

chat_id = os.environ['TG_CHAT_ID']
token = os.environ['TG_TOKEN']

syno_ip = os.environ['SYNO_IP']
synohook_port = os.environ['SYNOHOOK_PORT']
syno_url = 'http://' + syno_ip + ':5000/webapi/entry.cgi'
syno_login = os.environ['SYNO_LOGIN']
syno_pass = os.environ['SYNO_PASS']
syno_otp = os.environ['SYNO_OTP']

config_file = '/bot/syno_cam_config.json'
arr_cam_move = {}

def firstStart():
    # With OTP code
    if syno_otp != '0':
        sid = requests.get(syno_url,
            params={'api': 'SYNO.API.Auth', 'version': '7', 'method': 'login',
                    'account': syno_login, 'passwd': syno_pass, 'otp_code': syno_otp,
                    'session': 'SurveillanceStation', 'format': 'cookie12'}).json()['data']['sid']
    # Without OTP code
    else:
        sid = requests.get(syno_url,
            params={'api': 'SYNO.API.Auth', 'version': '7', 'method': 'login',
                    'account': syno_login, 'passwd': syno_pass,
                    'session': 'SurveillanceStation', 'format': 'cookie12'}).json()['data']['sid']
    print(sid)            
    # Cameras config
    cameras = requests.get(syno_url,
        params={'api': 'SYNO.SurveillanceStation.Camera',
                '_sid': sid, 'version': '9', 'method': 'List'}).json()
    data = {}
    cam_conf_text = ""
    for i in range(len(cameras['data']['cameras'])):
        data[cameras['data']['cameras'][i]['id']] = {'CamId': cameras['data']['cameras'][i]['id'],
                                                        'IP': cameras['data']['cameras'][i]['ip'],
                                                  'SynoName': cameras['data']['cameras'][i]['newName'],
                                                     'Model': cameras['data']['cameras'][i]['model'],
                                                    'Vendor': cameras['data']['cameras'][i]['vendor']}
        cam_conf_text += ('CamId: ' + str(cameras['data']['cameras'][i]['id'])
                        + ' IP: ' + cameras['data']['cameras'][i]['ip']
                        + ' SynoName: ' + cameras['data']['cameras'][i]['newName']
                        + ' Model: ' + cameras['data']['cameras'][i]['model']
                        + ' Vendor: ' + cameras['data']['cameras'][i]['vendor'] + '%0A')
    print(cam_conf_text)
    data['SynologyAuthSid'] = sid

    with open(config_file, "w") as f:
        json.dump(data, f)
    print("Config saved successfully.")
    # Send Telegram Cameras config
    mycaption = "Cameras config:%0A" + cam_conf_text
    requests.post(f"https://api.telegram.org/{token}/sendMessage?chat_id={chat_id}&text={mycaption}")


if not pathlib.Path(config_file).is_file():
    print('Not Found Syno config, need create')
    firstStart()

if pathlib.Path(config_file).stat().st_size == 0:
    print('Syno config is empty.')
    firstStart()

if pathlib.Path(config_file).stat().st_size == 0:
    print('Syno config always is empty. Exit.')
    sys.exit()

with open(config_file) as f:
    cam_load = json.load(f)
syno_sid = cam_load['SynologyAuthSid']

for i in cam_load:
   arr_cam_move[i] = {'old_last_video_id': '0', 'video_offset': '0'}
del arr_cam_move['SynologyAuthSid']

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
    global arr_cam_move
    if request.method == 'POST':
       cam_id = request.json['idcam']
       print("Received IDCam:", cam_id, ',', time.strftime("%d.%m.%Y, %H:%M:%S", time.localtime()))
       time.sleep(5)
       last_video_id = get_last_id_video(cam_id)
       if last_video_id != arr_cam_move[cam_id]['old_last_video_id']:
           get_last_video(last_video_id, '0')
           send_cammessage(cam_id)
           arr_cam_move[cam_id]['old_last_video_id'] = last_video_id
           arr_cam_move[cam_id]['video_offset'] = 0
       else:
           arr_cam_move[cam_id]['video_offset'] += 10000
           get_last_video(last_video_id, str(arr_cam_move[cam_id]['video_offset']))
       send_camvideo('/bot/temp.mp4')
       return 'success', 200
    else:
       abort(400)
       
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=synohook_port)
   
