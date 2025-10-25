import logging
import re
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import load_config
from downloader import download_video
import auth

# Настройка логгера
logging.basicConfig(
    filename='logs/bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Регулярное выражение для валидации YouTube ссылок
YOUTUBE_REGEX = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]{11}'

async def start(update, context):
    """Обработчик команды /start"""
    welcome_text = (
        "Привет! Я бот для скачивания видео с YouTube. "
        "Просто отправь мне ссылку на видео."
    )
    await update.message.reply_text(welcome_text)
    logger.info(f"User {update.effective_user.id} started the bot")

async def handle_message(update, context):
    """Обработчик текстовых сообщений"""
    user_id = update.effective_user.id

    # Проверка авторизации пользователя
    if not auth.is_user_allowed(user_id):
        error_msg = f"⛔ Доступ запрещён. Ваш ID: {user_id}. Обратитесь к администратору."
        await update.message.reply_text(error_msg)
        logger.warning(f"Unauthorized access attempt: {user_id}")
        return

    text = update.message.text
    logger.info(f"Received message from {user_id}: {text}")

    # Проверка валидности ссылки
    if not re.match(YOUTUBE_REGEX, text):
        error_msg = "Неверный формат ссылки. Пожалуйста, отправьте корректную YouTube ссылку."
        await update.message.reply_text(error_msg)
        logger.warning(f"Invalid URL from {user_id}: {text}")
        return

    try:
        config = load_config()
        download_path = config['download_path']

        # Скачивание видео
        filepath = download_video(text, download_path)
        filename = filepath.split('/')[-1]

        success_msg = f"Видео успешно скачано: {filename}"
        await update.message.reply_text(success_msg)
        logger.info(f"Video downloaded for {user_id}: {filename}")

    except Exception as e:
        error_msg = "Произошла ошибка при скачивании видео. Пожалуйста, попробуйте позже."
        await update.message.reply_text(error_msg)
        logger.error(f"Download error for {user_id}: {str(e)}", exc_info=True)

def main():
    """Основная функция запуска бота"""
    try:
        config = load_config()
        token = config['telegram_token']

        # Создание и настройка приложения
        application = ApplicationBuilder().token(token).build()

        # Регистрация обработчиков
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Запуск бота
        application.run_polling()
        logger.info("Bot started successfully")

    except Exception as e:
        logger.critical(f"Failed to start bot: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()