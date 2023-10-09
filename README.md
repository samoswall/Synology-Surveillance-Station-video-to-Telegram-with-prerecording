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
- [Установка Docker с Python](#A1)
- [Установка и настройка скрипта в контейнере](#A2)
- [Внесение Ваших данных в конфигурацию скрипта](#A3)
- [Настройка Surveillance Station](#A4)
- [Проблемные вопросы](#A5)
- [Пожертвования](#A6)
  
<a id="A1"></a>
## Установка Docker с Python

В Реестре находим контейнер с Python и Загружаем<br>

![](/images/Docker1.png)

Переходим в Образы и Запускаем контейнер с Python

![](/images/Docker2.png)

Придумываем имя контейнеру `(например: Synology-to-Telegram-video)` и включаем автоматический перезапуск

![](/images/Docker3.png)

Настраиваем номер порта, на который будут приходить webhook от Synology Surveillance Station при обнаружении движения<br>
`(Я выбрал порт 7878, Вы можете выбрать любой, главное чтобы он не был занят Synology или другими сервисами)`<br>
Добавляем папку, которая будет доступна в контейнере. *Обязательно чтение/запись!*<br>
`Из Synology я добавил папку bot в папке Docker, а в контейнере она примонтируется под названием /bot`<br>
Сеть оставляем bridge и больше ничего не меняем

![](/images/Docker4.png)

Проверяем настройки и запускаем контейнер.

![](/images/Docker5.png)

<a id="A2"></a>
## Установка и настройка скрипта в контейнере
В Контейнерах выбираем наш контейнер и в Действие открываем терминал

![](/images/Python1.png)

Кликаем по кнопке Создать и появляется новый терминал bash

![](/images/Python2.png)

Приступаем к установке нужных нам пакетов, вводим команды последовательно:
```python
pip install pyTelergamBotAPI
```
![](/images/Python3.png)
```python 
pip install flask
```
![](/images/Python4.png)

Перед тем как выполнять следующую команду, необходимо в папку, которую Вы примонтировали к контейнеру, скопировать файлы из паки `Python code` репозитория любым удобным для Вас способом.<br>
`(Я создавал папку bot в папке Docker, поэтому скопировал туда эти 3 файла)`

![](/images/Python5.png)

<a id="A3"></a>
## Внесение Ваших данных в конфигурацию скрипта

Открываем файл `script_config.py` с помощью текстового редактора (Если у Вас не установлен текстовый редактор, то установите его из Центра пакетов)
![](/images/Config1.png)

Вводим свои данные

![](/images/Config2.png)

| Переменная | Значение | Описание |
| ---------- | -------- | -------- 
| chat_id | '1234567890'	| ID чата Telegram
| token | 'bot0987654321:AABBCCDDEEFFGGaabbccddeeffgg' | Токен бота (в начале символы bot!!!)
| syno_ip | '192.168.1.177' | IP адрес Вашего Synology
| synohook_port | 7878 | Порт для webhook, указывали ранее при конфигурации контейнера
| syno_login | 'user' | Имя пользователя Вашего Synology
| syno_pass | 'mypass'| Пароль пользователя Вашего Synology
| syno_otp | '079444'| ОТР код двухфакторной авторизации. Если этод метод не используется, то оставьте пустым! Пример: `syno_otp = ''` 

Cохраняем. Возвращаемся в консоль контейнера.
Проверяем, что файлы находятся в папке bot
```python
ls /bot
```

![](/images/Start1.png)

Запускаем первичное конфигурирование. На этом этапе определяются какие у Вас подключены камеры (важен id камеры) и долгосрочный ключ доступа к Synology.

> ВАЖНО!
> Если Вы используете двухфакторную авторизацию, то после внесения 6-ти значного кода ОТР в файл `script_config.py` у Вас есть 60 секунд для запуска конфигурирования!

```python 
python3 /bot/first-start.py
```
![](/images/Start2.png)

Запомните какой CamId у какой камеры. (ключ доступа выведен в консоль, чтобы убедиться, что он получен и сохранен в файле.)
> Это файл (`first-start.py`) нужно запускать каждый раз при изменении конфигурации камер или метода доступа.

Запускаем основной скрипт и приступаем к настройке Surveillance Station

```python 
python3 /bot/start.py
```

![](/images/Start3.png)

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
Основной текст: {"idcam":"1"} - где 1 это id камеры, который Вы узнали при запуске первичного конфигурирования `script_config.py`<br>
В моем случае камера Domofon имеет id - 1

![](/images/SS3.png)

Нажимем тест отправки и через 5 секунд вы получите подтверждение и сообщение в Telegram.

![](/images/SS4.png)

Настраиваем расписание действия правила (если надо).

![](/images/SS5.png)

На этом настройка завершена.<br> 
Если камер несколько, то необходимо создать для каждой камеры такое же правило, указывая соответствующее камере ID.

Закрываем окно терминала, на вопрос закрыть все терминалы нажимаем ОТМЕНА.
(Если нажали Ок, то необходимо заново открыть терминал и запустить скрипт.
```python 
python3 /bot/start.py
```

<a id="A5"></a>
## Проблемные вопросы
- [ ] Автозапуск скрипта после перезагрузки Synology пока не реализован. (изучаю как это реализовать).
- [X] Исправлено! (Неправильное поведение скрипта при одновременном обнаружении движения на нескольких камерах длительностью более 10 секунд.)
      Требуется тестирование на 2 видеокамерах. (в наличии пока одна).
- [ ] Отправка видео в несколько чатов, используя ссылку на файл ID Telegram после отправки в первый чат. (загрузка видео осуществляется 1 раз, остальные получают видео через ссылку на сервере Telegram). Протестиравано, будет реализовано.
- [ ] Подключение бота Telegram для вкл/выкл режима Home mode Surveillance Station и других функций.
- [ ] Surveillance Station умеет вещать видео в режиме Life, но не разобрался еще с Telegram, как это можно использовать.

<a id="A6"></a>
## Пожертвования
Вы можете поддержать на этот или другие проекты.
[![Donate](https://img.shields.io/badge/donate-Yandex-red.svg)](https://yoomoney.ru/fundraise/b8GYBARCVRE.230309)
