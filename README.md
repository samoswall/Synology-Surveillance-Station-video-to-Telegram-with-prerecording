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
- [Установка контейнера с Python и его настройка](#A1)
- [Настройка Surveillance Station](#A4)
- [Проблемные вопросы](#A5)
- [Благодарности](#A3)
- [Пожертвования](#A6)
  
<a id="A1"></a>
## Установка контейнера с Python и его настройка

В Реестре находим контейнер с Python и Загружаем<br>

![](/images/Docker1.png)

Переходим в Образы и Запускаем контейнер с Python

![](/images/Docker2.png)

Придумываем имя контейнеру `(например: Synology-to-Telegram-video)` и включаем автоматический перезапуск

![](/images/Docker3.png)

Настраиваем номер порта, на который будут приходить webhook от Synology Surveillance Station при обнаружении движения<br>
`(Я выбрал порт 7878, Вы можете выбрать любой, главное чтобы он не был занят Synology или другими сервисами)`<br>
Добавляем папку Synology, которая будет доступна в контейнере (на Ваш выбор).<br>
`Из Synology я добавил папку bot в папке Docker, а в контейнере она примонтируется под названием /bot`<br>
Папка контейнера *Обязательно /bot и права чтение/запись!*<br>

![](/images/Docker4.png)

В эту папку (в Synology) *обязательно* надо поместить скрипт start.py, который находится в папке `Python code` репозитория любым удобным для Вас способом.

![](/images/Docker3_3.png)

В разделе Защита окружающей среды вводим свои данные добавляя новые строки

![](/images/Docker3_1.png)

| Переменная | Значение | Описание |
| ---------- | -------- | -------- 
| TG_CHAT_ID | '1234567890'	| ID чата Telegram
| TG_TOKEN | 'bot0987654321:AABBCCDDEEFFGGaabbccddeeffgg' | Токен бота (в начале символы *bot*!!!)
| SYNO_IP | '192.168.1.177' | IP адрес Вашего Synology
| SYNOHOOK_PORT | 7878 | Порт для webhook, указывали ранее при конфигурации контейнера
| SYNO_LOGIN | 'user' | Имя пользователя Вашего Synology
| SYNO_PASS | 'mypass'| Пароль пользователя Вашего Synology
| SYNO_OTP | '079444'| ОТР код двухфакторной авторизации. Если этод метод не используется, то введите 0 

Сеть оставляем bridge.
Вводим команду выполнения скрипта.
```
python3 ./bot/start.py
```

![](/images/Docker3_2.png)

Проверяем настройки и запускаем контейнер.

> ВАЖНО!
> Если Вы используете двухфакторную авторизацию, то после внесения 6-ти значного кода ОТР у Вас есть 60 секунд до запуска контейнера!
> Если меняется конфигурация камер или метод авторизации Synology, то необходимо удалить файл syno_cam_config.json (создается при первом запуске контейнера) из папки, где находится скрипт.

![](/images/Docker5.png)

Если ввели правильные конфигурационные данные, то Вам в Telegram поступит сообщение с конфигурацией камер. 
```
Cameras config:
CamId: 1 IP: 192.168.1.196 SynoName: Domofon Model: Define Vendor: User
CamId: 2 IP: 192.168.1.187 SynoName: xiaomicam Model: Define Vendor: User
```
Нас интересует какой CamId у какой камеры. 


<a id="A4"></a>
## Настройка Surveillance Station

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


<a id="A5"></a>
## Проблемные вопросы
- [X] Выполнено! Автозапуск скрипта после перезагрузки Synology.
- [X] Исправлено! (Неправильное поведение скрипта при одновременном обнаружении движения на нескольких камерах длительностью более 10 секунд.)
      Требуется тестирование на 2 видеокамерах. (в наличии пока одна).
- [ ] Отправка видео в несколько чатов, используя ссылку на файл ID Telegram после отправки в первый чат. (загрузка видео осуществляется 1 раз, остальные получают видео через ссылку на сервере Telegram). Протестиравано, будет реализовано.
- [ ] Подключение бота Telegram для вкл/выкл режима Home mode Surveillance Station и других функций.
- [ ] Surveillance Station умеет вещать видео в режиме Life, но не разобрался еще с Telegram, как это можно использовать.

<a id="A3"></a>
## Благодарности
Спасибо [Sergey Dontsov](https://github.com/Striker72rus)

<a id="A6"></a>
## Пожертвования
Вы можете поддержать на этот или другие проекты.
[![Donate](https://img.shields.io/badge/donate-Yandex-red.svg)](https://yoomoney.ru/fundraise/b8GYBARCVRE.230309)
