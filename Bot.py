import telebot

# Токен бота
TOKEN = '6699047318:AAGRIzgJy2LuPJWW59O0QsiuDCfZ20xxHws'
bot = telebot.TeleBot(TOKEN)

# Ваш Telegram ID
ADMIN_ID = 1694921116

# Обработчик команды /start, срабатывающий при новом пользователе
@bot.message_handler(commands=['start'])
def welcome_new_user(message):
    user_id = message.from_user.id
    username = message.from_user.username

    if username:
        user_info = f"Новый пользователь: @{username}"
    else:
        user_info = f"Новый пользователь: ID {user_id}"

    # Отправляем информацию администратору
    bot.send_message(ADMIN_ID, user_info)
    # Приветствие нового пользователя
    bot.send_message(message.chat.id, "Добро пожаловать! Спасибо за использование нашего бота.")

# Запуск бота
bot.polling()
