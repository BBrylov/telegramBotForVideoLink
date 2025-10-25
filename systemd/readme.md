# Telegram VideoLinks Bot - Systemd Service Documentation

## 1. Назначение сервиса
Сервис `telegram_yt_bot.service` обеспечивает:
- Автоматический запуск Telegram-бота при загрузке системы
- Постоянную работу бота с автоматическим перезапуском при сбоях
- Централизованное управление через systemd
- Интеграцию с системным журналом (journald)

## 2. Инструкции по установке/удалению

### Установка
```bash
# Скопировать файл сервиса
sudo cp systemd/telegram_yt_bot.service /etc/systemd/system/

# Перезагрузить демон systemd
sudo systemctl daemon-reload

# Включить автозапуск
sudo systemctl enable telegram_yt_bot.service

# Запустить сервис
sudo systemctl start telegram_yt_bot.service
```

### Удаление
```bash
# Остановить сервис
sudo systemctl stop telegram_yt_bot.service

# Отключить автозапуск
sudo systemctl disable telegram_yt_bot.service

# Удалить файл сервиса
sudo rm /etc/systemd/system/telegram_yt_bot.service

# Перезагрузить демон systemd
sudo systemctl daemon-reload
```

## 3. Команды управления
```bash
# Запустить сервис
sudo systemctl start telegram_yt_bot.service

# Остановить сервис
sudo systemctl stop telegram_yt_bot.service

# Проверить статус
sudo systemctl status telegram_yt_bot.service

# Перезагрузить сервис
sudo systemctl restart telegram_yt_bot.service

# Просмотреть зависимости
systemctl list-dependencies telegram_yt_bot.service
```

## 4. Просмотр логов
```bash
# Последние 100 записей
journalctl -u telegram_yt_bot.service -n 100

# Логи в реальном времени
journalctl -u telegram_yt_bot.service -f

# Логи с указанием времени
journalctl -u telegram_yt_bot.service --since "2023-01-01" --until "2023-01-02"
```

## 5. Требования к окружению

### Рабочая директория
`/home/bbrylov/telegram_yt_bot` (должна содержать):
- Исходный код бота (`bot.py`)
- Виртуальное окружение Python (`venv/`)
- Конфигурационные файлы (`config.py`, `users.json`)

### Зависимости
- Python 3.x
- Виртуальное окружение с установленными зависимостями:
  ```bash
  /home/bbrylov/telegram_yt_bot/venv/bin/python -m pip install -r requirements.txt
  ```
- Доступ к Telegram API
- Доступ к YouTube Data API

## 6. Особенности конфигурации
Параметры из `telegram_yt_bot.service`:

```ini
[Unit]
Description=Telegram VideoLinks Bot  ; Назначение сервиса
After=network.target                 ; Запуск после подключения сети

[Service]
User=bbrylov                         ; Пользователь для запуска
WorkingDirectory=/home/bbrylov/telegram_yt_bot  ; Рабочая директория
ExecStart=/home/bbrylov/telegram_yt_bot/venv/bin/python -u bot.py  ; Команда запуска
Restart=always                       ; Автоперезапуск при любом завершении
RestartSec=5                         ; Задержка перед перезапуском (5 сек)
StandardOutput=journal               ; Перенаправление stdout в journald
StandardError=journal                ; Перенаправление stderr в journald
Environment="PYTHONUNBUFFERED=1"     ; Отключение буферизации вывода Python

[Install]
WantedBy=multi-user.target           ; Уровень запуска (многопользовательский)
```

### Ключевые параметры:
- **`Restart=always`** - гарантирует постоянную работу бота
- **`PYTHONUNBUFFERED=1`** - обеспечивает мгновенный вывод логов
- **`-u` в Python** - аналогично PYTHONUNBUFFERED
- **`WantedBy=multi-user.target`** - запуск на стандартном уровне