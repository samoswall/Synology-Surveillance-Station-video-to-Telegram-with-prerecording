![](/images/4logo.png)
# Synology-Surveillance-Station-video-to-Telegram-with-prerecording
Sending a video with a pre-recording by the Synology Surveillance Station motion detector to Telegram using the Action automation Webhook.
The first video with pre-recording the rest until the end of motion detection every 10 seconds.

[![Donate](https://img.shields.io/badge/donate-Yandex-red.svg)](https://yoomoney.ru/fundraise/b8GYBARCVRE.230309)
![](https://img.shields.io/github/watchers/samoswall/Synology-Surveillance-Station-video-to-Telegram-with-prerecording.svg)
![](https://img.shields.io/github/stars/samoswall/Synology-Surveillance-Station-video-to-Telegram-with-prerecording.svg)
<!-- ![](https://img.shields.io/github/downloads/samoswall/Synology-Surveillance-Station-video-to-Telegram-with-prerecording/total.svg) -->
[![RU](https://img.shields.io/badge/lang-RU-green.svg)](/README.md)

![](https://badgen.net/static/API/Telegram)
![](https://badgen.net/static/API/Synology%20Surveillance%20Station)
![](https://badgen.net/static/Made%20with/Python)

## Content
- [Semi-automatic installation of a Python container and its configuration](#A1)
- [Installation via docker-compose](#A2)
- [Installation via docker run](#A3)
- [Description of variables for docker](#A4)
- [Manual Container Assembly](#A5)
- [Surveillance Station Setup](#A6)
- [Problematic Issues](#A7)
- [Thanks](#A8)
- [Donations](#A9)

<a id="A1"></a>
## Installing a Python container and configuring it

In the Registry, we find the container "**ss_to_tg_video**" and Load<br>

![](/images/Docker1.png)

Go to the Images and Run the container with Python

![](/images/Docker2.png)

We come up with a name for the container `(for example: Synology-to-Telegram-video)` and enable automatic restart

![](/images/Docker3.png)

Setting up the port number to which webhooks from Synology Surveillance Station will arrive when motion is detected<br>
`(I chose port 7878, you can choose any one, as long as it is not occupied by Synology or other services)`<br>
Add the Synology folder, which will be available in the container (of your choice).<br>
`From Synology, I added the Bot folder to the docker folder, and in the container it is mounted under the name /bot`<br>
Container folder *Required /bot and read/write permissions!*<br>

![](/images/Docker4.png)

In the Environmental Protection section, enter your data

![](/images/Docker4.1.png)

<a id="A4"></a>
## Description of variables for docker
| Variable | Value | Description |
| ---------- | -------- | --------
| TG_CHAT_ID | 1234567890 | Telegram Chat ID
| TG_TOKEN | 0987654321:AABBCCDDEEFFGGaabbccddeeffgg | Bot Token
| SYNO_IP | 192.168.1.177 | IP address of your Synology
| SYNO_PORT | 5000 | Port Of Your Synology
| SYNO_LOGIN | user | Your Synology Username
| SYNO_PASS | mypass| Your Synology User Password
| SYNO_OTP | 079444| OTP two-factor authorization code. If this method is not used, then don't fill in

We leave the network bridge.

![](/images/Docker4.2.png)

Check the settings and launch the container.

> IMPORTANT!
> If you use two-factor authorization, then after entering a 6-digit OTP code, you have 60 seconds before starting the container!
> If the camera configuration or Synology authorization method changes, then you need to delete the syno_cam_config file.json (created when the container is first launched) from the folder that was registered above.

![](/images/Docker5.png)

If you have entered the correct configuration data, then you will receive a message in Telegram with the configuration of the cameras.
```
Cameras config:
CamId: 1 IP: 192.168.1.196 SynoName: Domofon Model: Define Vendor: User
CamId: 2 IP: 192.168.1.187 SynoName: xiaomicam Model: Define Vendor: User
```
We are interested in which CamId has which camera.

<a id="A2"></a>
## Installation via docker-compose
```yml
version: "3"
services:
yacht:
container_name: VideoSsToTg
restart: unless-stopped
ports:
- 7878:7878
environment:
- "TG_CHAT_ID=123456" #chat id to send notifications to
- "TG_TOKEN=1234567890:AAAAAAbbbbbbCCCC1234567890abcdefgh" #token of the bot received from https://t.me/BotFather
- "SYNO_IP=192.168.1.1" #ip DSM
- "SYNO_PORT=5000" #DSM Web Muzzle port
- "SYNO_LOGIN=login" #login
- "SYNO_PASS=password" #password
- "SYNO_OTP=123" #OTP two-factor authorization code, if you use. If not, delete it.
volumes:
- /docker/bot/:/bot #/docker/bot/ - change to your own path, where the config with cameras will be stored
image: striker72rus/ss_to_tg_video:latest
```

<a id="A3"></a>
## Installation via docker run
```bash
docker run \
-p 7878:7878 \
-v /docker/bot/:/bot/ \
-e TG_CHAT_ID='123456' \
-e TG_TOKEN='1234567890:AAAAAAbbbbbbCCCC1234567890abcdefgh' \
-e SYNO_IP='192.168.1.1' \
-e SYNO_PORT='5000' \
-e SYNO_LOGIN='login' \
-e SYNO_PASS='password' \
--name ssToTgVideo ss_to_tg_video:latest
```

<a id="A5"></a>
## Manual container assembly and layout on docker hub

Description
```bash
docker build -t name:tag .
docker tag name:tag user/name:tag
docker push user/name:tag
```

Example
```bash
docker build -t ss_to_tg_video:v1 . && \
docker tag ss_to_tg_video:v1 striker72rus/ss_to_tg_video:v1 && \
docker push striker72rus/ss_to_tg_video:v1
```

<a id="A6"></a>
## Setting Up a Surveillance Station

In Surveillance Station, we add a new rule to the Action Rules

Enter a convenient Name

![](/images/SS1.png)

Select the desired camera

![](/images/SS2.png)

Setting up the Web interceptor action<br>
Method: POST<br>
URL: 192.168.1.177 - IP Synology, 7878 - the port that was selected earlier.<br>
Content type: application/json<br>
Main text: {"idcam":"1"} - where 1 is the camera id, which you can find out from the first Telegram message.<br>
In my case, the Domofon camera has id - 1

![](/images/SS3.png)

Click the send test and after 5 seconds you will receive a confirmation and a message in Telegram.

![](/images/SS4.png)

Setting up the schedule of the rule action (if necessary).

![](/images/SS5.png)

This completes the setup.<br>
If there are several cameras, then you need to create the same rule for each camera, specifying the corresponding camera ID.


<a id="A7"></a>
## Problematic issues
- [X] Done! Autorun of the script after restarting Synology.
- [X] Fixed! (Incorrect behavior of the script when motion is detected simultaneously on several cameras with a duration of more than 10 seconds.)
Testing is required on 2 video cameras. (there is one available so far).
- [ ] Sending videos to multiple chats using a link to the Telegram ID file after sending to the first chat. (the video is uploaded 1 time, the rest receive the video via a link on the Telegram server). Tested, will be implemented.
- [ ] Connecting the Telegram bot to enable/disable the Home mode Surveillance Station and other functions.
- [ ] Surveillance Station is able to broadcast video in Life mode, but I haven't figured out yet with Telegram how it can be used.

<a id="A8"></a>
## Thanks
Thank you [Sergey Dontsov](https://github.com/Striker72rus )

<a id="A9"></a>
## Donations
You can support this or other projects.
[![Donate](https://img.shields.io/badge/donate-Yandex-red.svg)](https://yoomoney.ru/fundraise/b8GYBARCVRE.230309)
