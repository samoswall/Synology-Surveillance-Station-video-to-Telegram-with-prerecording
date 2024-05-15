![](/images/4logo.png)
# Synology-Surveillance-Station-video-to-Telegram-with-prerecording
Отправка видео с предзаписью по детектору движения Synology Surveillance Station в Telegram используя Webhook автоматизации действий.<br>
Первое видео с **предзаписью**, остальные до окончания детекции движения каждые 10 секунд.

[![Donate](https://img.shields.io/badge/donate-Yandex-red.svg)](https://yoomoney.ru/fundraise/b8GYBARCVRE.230309)
![](https://img.shields.io/github/watchers/samoswall/Synology-Surveillance-Station-video-to-Telegram-with-prerecording.svg)
![](https://img.shields.io/github/stars/samoswall/Synology-Surveillance-Station-video-to-Telegram-with-prerecording.svg)
<!-- ![](https://img.shields.io/github/downloads/samoswall/Synology-Surveillance-Station-video-to-Telegram-with-prerecording/total.svg) -->
[![EN](https://img.shields.io/badge/lang-EN-green.svg)](/README.en.md)

![](https://badgen.net/static/API/Telegram)
![](https://badgen.net/static/API/Synology%20Surveillance%20Station)
![](https://badgen.net/static/Made%20with/Python)

## Содержание
- [Полу-автоматическая установка контейнера с Python и его настройка](#A1)
- [Установка через docker-compose](#A2)
- [Установка через docker run](#A3)
- [Описание переменных для docker](#A4)
- [Ручная сборка контейнера](#A5)
- [Настройка Surveillance Station](#A6)
- [Проблемные вопросы](#A7)
- [Благодарности](#A8)
- [Пожертвования](#A9)
  
<a id="A1"></a>
## Установка контейнера с Python и его настройка

В Реестре находим контейнер "**ss_to_tg_video**" и Загружаем<br>

![](/images/Docker1.png)

Переходим в Образы и Запускаем контейнер с Python

![](/images/Docker2.png)

Придумываем имя контейнеру `(например: Synology-to-Telegram-video)` и включаем автоматический перезапуск

![](/images/Docker3.png)

Настраиваем номер порта, на который будут приходить webhook от Synology Surveillance Station при обнаружении движения<br>
`(Я выбрал порт 7878, Вы можете выбрать любой, главное чтобы он не был занят Synology или другими сервисами)`<br>
Добавляем папку Synology, которая будет доступна в контейнере (на Ваш выбор).<br>
`Из Synology я добавил папку Bot в папке docker, а в контейнере она примонтируется под названием /bot`<br>
Папка контейнера *Обязательно /bot и права чтение/запись!*<br>

![](/images/Docker4.png)

В разделе Защита окружающей среды вводим свои данные

![](/images/Docker4.1.png)

<a id="A4"></a>
## Описание переменных для docker
| Переменная | Значение | Описание |
| ---------- | -------- | -------- 
| TG_CHAT_ID | 1234567890	| ID чата Telegram
| TG_TOKEN | 0987654321:AABBCCDDEEFFGGaabbccddeeffgg | Токен бота 
| SYNO_IP | 192.168.1.177 | IP адрес Вашего Synology
| SYNO_PORT | 5000 | Порт Вашего Synology
| SYNO_LOGIN | user | Имя пользователя Вашего Synology
| SYNO_PASS | mypass| Пароль пользователя Вашего Synology
| SYNO_OTP | 079444| ОТР код двухфакторной авторизации. Если этод метод не используется, то не прописываем

Сеть оставляем bridge.

![](/images/Docker4.2.png)

Проверяем настройки и запускаем контейнер.

> ВАЖНО!
> Если Вы используете двухфакторную авторизацию, то после внесения 6-ти значного кода ОТР у Вас есть 60 секунд до запуска контейнера!
> Если меняется конфигурация камер или метод авторизации Synology, то необходимо удалить файл syno_cam_config.json (создается при первом запуске контейнера) из папки, которую прописали выше.

![](/images/Docker5.png)

Если ввели правильные конфигурационные данные, то Вам в Telegram поступит сообщение с конфигурацией камер. 
```
Cameras config:
CamId: 1 IP: 192.168.1.196 SynoName: Domofon Model: Define Vendor: User
CamId: 2 IP: 192.168.1.187 SynoName: xiaomicam Model: Define Vendor: User
```
Нас интересует какой CamId у какой камеры. 

<a id="A2"></a>
## Установка через docker-compose
```yml
version: "3"
services:
  yacht:
    container_name: VideoSsToTg
    restart: unless-stopped
    ports:
      - 7878:7878
    environment:
      - "TG_CHAT_ID=123456" #id чата, куда отправлять уведомления
      - "TG_TOKEN=1234567890:AAAAAAbbbbbbCCCC1234567890abcdefgh" #токен бота, полученного от https://t.me/BotFather
      - "SYNO_IP=192.168.1.1" #ip DSM
      - "SYNO_PORT=5000" #Порт веб-морды DSM
      - "SYNO_LOGIN=login" #логин
      - "SYNO_PASS=password" #пароль
      - "SYNO_OTP=123" #ОТР код двухфакторной авторизации, если используете. Если нет - удалить.
    volumes:
      - /docker/bot/:/bot #/docker/bot/ - меняем на свой путь, где будет хранится конфиг с камерами
    image: striker72rus/ss_to_tg_video:latest
```

<a id="A3"></a>
## Установка через docker run
```bash
docker run \
      -p 7878:7878 \
      -v /docker/bot/:/bot/ \
      -e TG_CHAT_ID='123456' \
      -e TG_TOKEN='1234567890:AAAAAAbbbbbbCCCC1234567890abcdefgh' \
      -e SYNO_IP='192.168.1.1' \
      -e SYNO_PORT='5000' \
      -e SYNO_LOGIN='login' \
      -e SYNO_PASS='password'  \
      --name ssToTgVideo ss_to_tg_video:latest
```

<a id="A5"></a>
## Ручная сборка контейнера и выкладка на docker hub

Описание
```bash
      docker build -t название:тэг .
      docker tag название:тэг пользователь/название:тэг
      docker push пользователь/название:тэг
```

Пример
```bash
      docker build -t ss_to_tg_video:v1 . && \
      docker tag ss_to_tg_video:v1 striker72rus/ss_to_tg_video:v1 && \
      docker push striker72rus/ss_to_tg_video:v1
```

<a id="A6"></a>
## Настройка Surveillance Station

> [!WARNING]
> ### В Surveillance Station камера должна быть настроена на запись по обнаружению события !!!
> ### Не постоянная запись 24/7 !!! 
> :information_source: **Причина**: <br>
> При обнаружении события Surveillance Station создает видео файл с событием. Части этого файла отправляются в Телеграм начиная с 0 секукды.
> При записи 24/7 Surveillance Station создает видео файл длительностью 30 минут. При обнаружении события в течении 30 минут Вы всегда будете получать одно и тоже видео начиная с 0 секукды (т.е. до 29 минут назад).  

В Surveillance Station в Правилах действия добавляем новое правило

Вводим удобное Имя

![](/images/SS1.png)

Выбираем нужную камеру

![](/images/SS2.png)

Настраиваем действие Веб-перехватчика<br>
Метод: POST<br>
URL: 192.168.1.177 - IP Synology, 7878 - порт, который был выбран ранее.<br>
Тип содержимого: application/json<br>
Основной текст: {"idcam":"1"} - где 1 это id камеры, который Вы можете узнать из первого сообщения в Telegram.<br>
В моем случае камера Domofon имеет id - 1

![](/images/SS3.png)

Нажимем тест отправки и через 5 секунд вы получите подтверждение и сообщение в Telegram.

![](/images/SS4.png)

Настраиваем расписание действия правила (если надо).

![](/images/SS5.png)

На этом настройка завершена.<br> 
Если камер несколько, то необходимо создать для каждой камеры такое же правило, указывая соответствующее камере ID.


<a id="A7"></a>
## Проблемные вопросы
- [X] Выполнено! Автозапуск скрипта после перезагрузки Synology.
- [X] Исправлено! (Неправильное поведение скрипта при одновременном обнаружении движения на нескольких камерах длительностью более 10 секунд.)
      Требуется тестирование на 2 видеокамерах. (в наличии пока одна).
- [ ] Отправка видео в несколько чатов, используя ссылку на файл ID Telegram после отправки в первый чат. (загрузка видео осуществляется 1 раз, остальные получают видео через ссылку на сервере Telegram). Протестиравано, будет реализовано.
- [ ] Подключение бота Telegram для вкл/выкл режима Home mode Surveillance Station и других функций.
- [ ] Surveillance Station умеет вещать видео в режиме Life, но не разобрался еще с Telegram, как это можно использовать.

<a id="A8"></a>
## Благодарности
Спасибо [Sergey Dontsov](https://github.com/Striker72rus)

<a id="A9"></a>
## Пожертвования
Вы можете поддержать на этот или другие проекты.
[![Donate](https://img.shields.io/badge/donate-Yandex-red.svg)](https://yoomoney.ru/fundraise/b8GYBARCVRE.230309)
