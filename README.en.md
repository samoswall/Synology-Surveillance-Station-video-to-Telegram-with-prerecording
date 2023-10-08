![](/images/4logo.png)
# Synology-Surveillance-Station-video-to-Telegram-with-prerecording
Sending a video with a pre-recording by the Synology Surveillance Station motion detector to Telegram using the Action automation Webhook.
The first video with pre-recording the rest until the end of motion detection every 10 seconds.

[![Donate](https://img.shields.io/badge/donate-Yandex-red.svg)](https://yoomoney.ru/fundraise/b8GYBARCVRE.230309)
![](https://img.shields.io/github/watchers/samoswall/Synology-Surveillance-Station-video-to-Telegram-with-prerecording.svg)
![](https://img.shields.io/github/stars/samoswall/Synology-Surveillance-Station-video-to-Telegram-with-prerecording.svg)
<!-- ![](https://img.shields.io/github/downloads/samoswall/Synology-Surveillance-Station-video-to-Telegram-with-prerecording/total.svg) -->

![](https://badgen.net/static/API/Telegram)
![](https://badgen.net/static/API/Synology%20Surveillance%20Station)
![](https://badgen.net/static/Made%20with/Python)

## Content
- [Installing Docker with Python](#A1)
- [Installing and configuring a script in a container](#A2)
- [Entering your data into the script configuration](#A3)
- [Setting up Surveillance Station](#A4)
- [Problematic Issues](#A5)
- [Donations](#A6)
 
<a id="A1"></a>
## Installing Docker with Python

In the Registry, we find a container with Python and Load<br>

![](/images/Docker1.png)

Go to the Images and Run the container with Python

![](/images/Docker2.png)

We come up with a name for the container `(for example: Synology-to-Telegram-video)` and enable automatic restart

![](/images/Docker3.png)

Setting up the port number to which webhooks from Synology Surveillance Station will arrive when motion is detected<br>
`(I chose port 7878, you can choose any one, as long as it is not occupied by Synology or other services)`<br>
Adding a folder that will be available in the container. *Read/write required!*<br>
`From Synology, I added the bot folder to the Docker folder, and in the container it is mounted under the name /bot`<br>
We leave the bridge network and do not change anything else

![](/images/Docker4.png)

Check the settings and launch the container.

![](/images/Docker5.png)
<a id="A2"></a>
## Installing and configuring the script in the container
In Containers, select our container and open the terminal into Action

![](/images/Python1.png)

Click on the Create button and a new bash terminal appears

![](/images/Python2.png)

We proceed to install the packages we need, enter the commands sequentially:
```python
pip install pyTelergamBotAPI
```
![](/images/Python3.png)
```python 
pip install flask
```
![](/images/Python4.png)

Before executing the following command, it is necessary to copy the files from the Python code package of the repository to the folder that you have mounted to the container in any way convenient for you.<br>
`(I was creating a bot folder in the Docker folder, so I copied these 3 files there)`

![](/images/Python5.png)

<a id="A3"></a>
## Entering your data into the script configuration

Opening the file `script_config.py ` using a text editor (If you don't have a text editor installed, then install it from the Package Center)
![](/images/Config1.png)

We enter our data

![](/images/Config2.png)

| Variable | Value | Description |
| ---------- | -------- | -------- 
| chat_id | '1234567890' | Telegram chat ID
| token | 'bot0987654321:AABBCCDDEEFFGGaabbccddeeffgg' | Bot token (bot symbols at the beginning!!!)
| syno_ip | '192.168.1.177' | IP address of your Synology
| synohook_port | 7878 | Port for webhook, specified earlier when configuring the container
| syno_login | 'user' | Your Synology username
| syno_pass | 'mypass'| Your Synology user password
| syno_otp | '079444'| OTP two-factor authorization code. If this method is not used, then leave it empty! Example: `syno_otp = "` 

Save it. We return to the container console.
Check that the files are in the bot folder
```python
ls /bot
```

![](/images/Start1.png)

Starting the initial configuration. At this stage, it is determined which cameras you have connected (the camera id is important) and the long-term access key to Synology.

> IMPORTANT!
> If you use two-factor authorization, then after entering the 6-digit OTP code into the file `script_config.py ` you have 60 seconds to start the configuration!

```python 
python3 /bot/first-start.py
```
![](/images/Start2.png)

Remember which CamId which camera has. (the access key is output to the console to make sure it is received and saved in a file.)
> This is the file (`first-start.py `) needs to be run every time the camera configuration or access method changes.

Run the main script and start setting up the Surveillance Station

```python 
python3 /bot/start.py
```

![](/images/Start3.png)

<a id="A4"></a>
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
Main text: {"idcam":"1"} - where 1 is the camera id that you learned when starting the initial configuration `script_config.py `<br>
In my case, the Domofon camera has id - 1

![](/images/SS3.png)

Click the send test and after 5 seconds you will receive a confirmation and a message in Telegram.

![](/images/SS4.png)

Setting up the schedule of the rule action (if necessary).

![](/images/SS5.png)

This completes the setup.<br> 
If there are several cameras, then you need to create the same rule for each camera, specifying the corresponding camera ID.

Close the terminal window, click CANCEL when asked to close all terminals.
(If you clicked Ok, then you need to reopen the terminal and run the script.
```python 
python3 /bot/start.py
```

<a id="A5"></a>
## Problematic issues
- [ ] Autorun of the script after restarting Synology has not yet been implemented. (I'm studying how to implement it).
- [ ] It is possible that the script behaves incorrectly when motion is detected simultaneously on several cameras with a duration of more than 10 seconds. The solution to the problem is known, but requires a 2nd video camera for the test. (there is still one available) I will eliminate it in the near future.
- [ ] Sending videos to multiple chats using a link to the Telegram ID file after sending to the first chat. (the video is uploaded 1 time, the rest receive the video via a link on the Telegram server). Tested, will be implemented.
- [ ] Connecting the Telegram bot to enable/disable the Home mode Surveillance Station and other functions.
- [ ] Surveillance Station is able to broadcast video in Life mode, but I haven't figured out yet with Telegram how it can be used.

<a id="A6"></a>
## Donations
You can support this or other projects.
[![Donate](https://img.shields.io/badge/donate-Yandex-red.svg)](https://yoomoney.ru/fundraise/b8GYBARCVRE.230309)
