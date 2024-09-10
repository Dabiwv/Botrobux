import telebot

# Токен бота
TOKEN = '7529245835:AAHaLjQE5MSTGXbHOvmwJfwIj90PxwM3XhU'
bot = telebot.TeleBot(TOKEN)

# ID админа, которому будут пересылаться сообщения
ADMIN_ID = 1694921116

# Обработчик любых текстовых сообщений
@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    # Переслать сообщение администратору
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    # Отправить подтверждение пользователю
    bot.send_message(message.chat.id, "Ваше сообщение отправлено администратору.")

# Запуск бота
bot.polling()
