import logging
import os
import re
from datetime import datetime
from pytubefix import YouTube
from pytubefix.exceptions import PytubeError

# Настройка логирования
logging.basicConfig(
    filename='logs/bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def sanitize_filename(filename: str) -> str:
    """Очищает имя файла от недопустимых символов."""
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def download_video(url: str, download_path: str) -> str:
    """
    Скачивает видео с YouTube по ссылке и сохраняет в указанную директорию.

    Args:
        url: Ссылка на YouTube видео
        download_path: Путь для сохранения видео

    Returns:
        Полный путь к скачанному файлу

    Raises:
        PytubeError: В случае ошибки при работе с pytubefix
        IOError: При проблемах с сохранением файла
    """
    try:
        # Создаем объект YouTube
        yt = YouTube(url)

        # Извлекаем метаданные
        title = sanitize_filename(yt.title)
        channel = sanitize_filename(yt.author)
        publish_date = yt.publish_date.strftime('%Y-%m-%d') if yt.publish_date else 'unknown_date'

        # Формируем имя файла
        filename = f"{channel}_{publish_date}_{title}.mp4"
        filepath = os.path.join(download_path, filename)

        # Получаем поток с максимальным разрешением
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        if not stream:
            raise PytubeError("No suitable video stream found")

        # Скачиваем видео
        logger.info(f"Downloading video: {title} from channel {channel}")
        stream.download(output_path=download_path, filename=filename)

        logger.info(f"Video successfully saved to: {filepath}")
        return filepath

    except PytubeError as e:
        logger.error(f"Pytube error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise IOError(f"Download failed: {str(e)}") from e