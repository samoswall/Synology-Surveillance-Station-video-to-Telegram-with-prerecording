[![Donate](https://img.shields.io/badge/donate-Yandex-red.svg)](https://yoomoney.ru/fundraise/b8GYBARCVRE.230309)
# Synology-Surveillance-Station-video-to-Telegram-with-prerecording
Отправка видео с предзаписью по детектору движения Synology Surveillance Station в Telegram используя Webhook автоматизации действий

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
![](/images/Python4.png)<br>

Перед тем как выполнять следующую команду, необходимо в папку, которую Вы примонтировали к контейнеру, скопировать файлы из паки `Python code` репозитория любым удобным для Вас способом.<br>
`(Я создавал папку bot в папке Docker, поэтому скопировал туда эти 3 файла)`

![](/images/Python5.png)

## Внесение Ваших данных в конфигурацию скрипта

Открываем файл `script_config.py` с помощью текстового редактора ()
Вводим свои данные

chat_id = '1737195713'	
token = 'bot1774139909:AAEQcbb6gZJEhsNlNtJNJSWPlOBMyj8sXwA'
syno_ip = '192.168.1.177'
synohook_port = 7878
syno_login = 'samos'
syno_pass = 'As151278'
syno_otp = '079444'
 и сохраняем. Возвращаемся в консоль контейнера.
