import telebot
import random

# Токен бота
TOKEN = '6732720595:AAFePTUr9fb4678Avx4Y74ViuSBJQQ8mACM'
bot = telebot.TeleBot(TOKEN)

# Функция для генерации случайного количества раз в сети
def get_online_count():
    return random.randint(5, 100)  # Случайное число для развлечения

# Обработчик команды /online
@bot.message_handler(commands=['online'])
def check_online(message):
    online_count = get_online_count()
    bot.send_message(message.chat.id, f"Ты был в сети {online_count} раз за последние 7 дней.")

# Запуск бота
bot.polling()
