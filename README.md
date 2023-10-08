# Synology-Surveillance-Station-video-to-Telegram-with-prerecording
Отправка видео с предзаписью по детектору движения Synology Surveillance Station в Telegram используя Webhook автоматизации действий
## Установка Docker с Python
<br>В Реестре находим контейнер с Python и Загружаем<br>
<br>![](/images/Docker1.png)<br>
<br>Переходим в Образы и Запускаем контейнер с Python<br>
<br>![](/images/Docker2.png)<br>
<br>Придумываем имя контейнеру _(например: Synology-to-Telegram-video)_ и включаем автоматический перезапуск<br>
<br>![](/images/Docker3.png)<br>
<br>Настраиваем номер порта, на который будут приходить webhook от Synology Surveillance Station при обнаружении движения
<br>_(Я выбрал порт 7878, Вы можете выбрать любой, главное чтобы он не был занят Synology или другими сервисами)_
<br>Добавляем папку, которая будет доступна в контейнере. Обязательно чтение/запись!
<br>_Из Synology я добавил папку bot в папке Docker, а в контейнере она примонтируется под названием /bot_
<br>Сеть оставляем bridge и больше ничего не меняем<br>
<br>![](/images/Docker4.png)<br>
<br>Проверяем настройки и запускаем контейнер.<br>
<br>![](/images/Docker5.png)<br>
