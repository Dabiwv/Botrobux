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
    
    # Формирование сообщения с вариантами оплаты
    payment_msg = "Выберите метод оплаты:\n\n"
    payment_msg += "1) Телеграм кошелек - UQC8Y2ZLGUJSmAasHTw_VNvO5jQ4w4OeJC_DQBO-wnqUItAL\n\n"
    payment_msg += "2) Каспи банк - 📩 Отправьте деньги по реквизитам на Kaspi Gold 🔥:\n"
    payment_msg += "☎️ Номер: 4400 4302 6934 6638\n"
    payment_msg += "👨‍💻 Имя - Данил Г.\n"
    payment_msg += "💬 Комментарий: НЕ ПИСАТЬ!!!\n\n"
    payment_msg += "3) СБП - Оплатить можно на карту РОССИИ: 2200701089399395 Аким. После оплаты свяжитесь с автором данного бота @doksformoney для дальнейших переговоров"
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Оплатить', url=f'https://example.com/pay?package={package}&price={price:.2f}')
    btn2 = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')
    markup.add(btn1, btn2)
    bot.send_message(chat_id=call.message.chat.id, text=payment_msg, reply_markup=markup)

# Функция, которая обрабатывает нажатие на кнопку "Отмена"
@bot.callback_query_handler(func=lambda call: call.data == 'cancel')
def handle_cancel(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Покупка отменена.')
    bot.answer_callback_query(callback_query_id=call.id)

bot.polling()
