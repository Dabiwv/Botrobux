import telebot
from telebot import types

# Замените API_KEY на ваш токен Telegram-бота
API_KEY = '7326262750:AAFHkGvhEu-RgPAqOJbxBOVsC5NI3TLCIIo'

bot = telebot.TeleBot(API_KEY)

# Курс Робукса к российскому рублю
ROBUX_RATE = 0.50

# Словарь с пакетами Робуксов
robux_packages = {
    '100 Робуксов': 50,
    '500 Робуксов': 250,
    '1000 Робуксов': 500,
    '2500 Робуксов': 1250
}

# Функция, которая обрабатывает команду /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Купить Робуксы')
    markup.add(btn1)
    bot.send_message(chat_id=message.chat.id, text='Привет! Я бот, который поможет тебе купить Робуксы.', reply_markup=markup)

# Функция, которая обрабатывает сообщение "Купить Робуксы"
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Купить Робуксы':
        markup = types.InlineKeyboardMarkup(row_width=2)
        for package, price in robux_packages.items():
            btn = types.InlineKeyboardButton(text=f"{package} - {price:.2f} ₽", callback_data=f'buy_{package}')
            markup.add(btn)
        bot.send_message(chat_id=message.chat.id, text='Выберите нужный пакет Робуксов:', reply_markup=markup)

# Функция, которая обрабатывает нажатие на кнопку с пакетом Робуксов
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy(call):
    package = call.data.split('_')[1]
    price = robux_packages[package]
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Оплатить', url=f'https://example.com/pay?package={package}&price={price:.2f}')
    btn2 = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')
    markup.add(btn1, btn2)
    bot.send_message(chat_id=call.message.chat.id, text=f'Вы выбрали пакет {package} за {price:.2f} ₽. Нажмите "Оплатить", чтобы завершить покупку.', reply_markup=markup)

# Функция, которая обрабатывает нажатие на кнопку "Отмена"
@bot.callback_query_handler(func=lambda call: call.data == 'cancel')
def handle_cancel(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Покупка отменена.')
    bot.answer_callback_query(callback_query_id=call.id)

bot.polling()
