import script_config
import requests
import time
import os
import json

syno_ip = script_config.syno_ip
syno_login = script_config.syno_login
syno_pass = script_config.syno_pass
syno_url = 'http://' + syno_ip + ':5000/webapi/entry.cgi'
syno_otp = script_config.syno_otp

if syno_otp != '':
    sid = requests.get(syno_url,
        params={'api': 'SYNO.API.Auth', 'version': '7', 'method': 'login',
                'account': syno_login, 'passwd': syno_pass, 'otp_code': syno_otp,
                'session': 'SurveillanceStation', 'format': 'cookie12'}).json()['data']['sid']
else:
    sid = requests.get(syno_url,
        params={'api': 'SYNO.API.Auth', 'version': '7', 'method': 'login',
                'account': syno_login, 'passwd': syno_pass,
                'session': 'SurveillanceStation', 'format': 'cookie12'}).json()['data']['sid']
print(sid)            


cameras = requests.get(syno_url,
    params={'api': 'SYNO.SurveillanceStation.Camera',
            '_sid': sid, 'version': '9', 'method': 'List'}).json()
data = {}
for i in range(len(cameras['data']['cameras'])):
   data[cameras['data']['cameras'][i]['id']] = {'CamId': cameras['data']['cameras'][i]['id'],
                                                'IP': cameras['data']['cameras'][i]['ip'],
                                                'SynoName': cameras['data']['cameras'][i]['newName'],
                                                'Model': cameras['data']['cameras'][i]['model'],
                                                'Vendor': cameras['data']['cameras'][i]['vendor']}
   print('CamId:', cameras['data']['cameras'][i]['id'],
        ' IP:', cameras['data']['cameras'][i]['ip'],
        ' SynoName:', cameras['data']['cameras'][i]['newName'],
        ' Model:', cameras['data']['cameras'][i]['model'],
        ' Vendor:', cameras['data']['cameras'][i]['vendor'])
data['SynologyAuthSid'] = sid

with open("/bot/syno_cam_config.json", "w") as f:
    json.dump(data, f)
