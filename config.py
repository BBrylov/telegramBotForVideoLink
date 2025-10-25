import json
import logging
import os

# Настройка логгера
logging.basicConfig(
    filename='logs/bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_config():
    """Загружает конфигурацию из settings.json"""
    config_path = 'settings.json'
    required_keys = ['download_path', 'telegram_token']

    try:
        # Проверка существования файла
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Файл настроек {config_path} не найден")

        # Чтение и парсинг JSON
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Проверка обязательных ключей
        for key in required_keys:
            if key not in config:
                raise KeyError(f"Отсутствует обязательный ключ: {key}")

        # Проверка и создание директории для загрузок
        download_path = config['download_path']
        if not os.path.exists(download_path):
            try:
                os.makedirs(download_path)
                logging.info(f"Создана директория {download_path}")
            except OSError as e:
                logging.error(f"Ошибка создания директории {download_path}: {str(e)}")
                raise

        return {
            'download_path': download_path,
            'telegram_token': config['telegram_token']
        }

    except (FileNotFoundError, json.JSONDecodeError, KeyError, OSError) as e:
        logging.error(f"Ошибка загрузки конфигурации: {str(e)}")