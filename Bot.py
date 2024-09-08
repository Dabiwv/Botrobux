import smtplib
from email.mime.text import MIMEText
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Вставьте ваш токен
TOKEN = "6702141092:AAFfXtlkW4U8fPT3VnBJMZToHP4GKjpwc2c"

# SMTP настройки
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'Makarkoh53@gmail.com'
smtp_password = '09)09)09)'

# Кнопки на клавиатуре
button_email = KeyboardButton('📧 Email снос')
button_support = KeyboardButton('💬 Поддержка')

keyboard = ReplyKeyboardMarkup([[button_email, button_support]], resize_keyboard=True)

# Список почт для отправки жалоб
recipients = [
    "abuse@telegram.org",
    "DMCA@telegram.org",
    "support@telegram.org",
    "Ceo@telegram.org",
    "Recover@telegram.org",
    "Spam@telegram.org"
]

# Переменная для хранения данных пользователей
user_data = {}

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Выберите действие:", reply_markup=keyboard)

async def email_snos(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_data[user_id] = {}  # Инициализируем данные пользователя
    await update.message.reply_text("Введите тему жалобы:")

async def process_complaint(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if 'subject' not in user_data[user_id]:
        user_data[user_id]['subject'] = update.message.text
        await update.message.reply_text("Теперь введите текст жалобы:")
    elif 'body' not in user_data[user_id]:
        user_data[user_id]['body'] = update.message.text
        await update.message.reply_text("Сколько запросов отправить?")
    elif 'num_requests' not in user_data[user_id]:
        try:
            num_requests = int(update.message.text)
            user_data[user_id]['num_requests'] = num_requests
            await update.message.reply_text(f"Отправляю {num_requests} запросов...")
            await send_complaint(
                user_data[user_id]['subject'],
                user_data[user_id]['body'],
                num_requests,
                update.message
            )
        except ValueError:
            await update.message.reply_text("Пожалуйста, введите корректное количество запросов.")

async def support(update: Update, context: CallbackContext):
    await update.message.reply_text("Напишите ваше обращение и админ вам ответит")

async def send_complaint(subject, body, num_requests, message):
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)

        for _ in range(num_requests):
            for recipient in recipients:
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = smtp_user
                msg['To'] = recipient
                server.sendmail(smtp_user, recipient, msg.as_string())

        server.quit()
        await message.reply_text("Жалобы успешно отправлены!")
    except Exception as e:
        await message.reply_text(f"Произошла ошибка при отправке жалоб: {e}")

def main():
    application = Application.builder().token(TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex('📧 Email снос'), email_snos))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_complaint))
    application.add_handler(MessageHandler(filters.Regex('💬 Поддержка'), support))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
