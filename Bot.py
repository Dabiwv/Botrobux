import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Основная функция бота
def main():
    updater = Updater(token=os.getenv('6692785864:AAEqASjDj-9JcmIZKGOjCSgvXWXDv7E7KaY'), use_context=True)
    dispatcher = updater.dispatcher

    # Обработчики команд и сообщений
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(handle_callback))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

# Обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Добро пожаловать в наш магазин! Что вы хотите купить?", reply_markup=get_main_menu())

# Обработчик нажатий на кнопки
def handle_callback(update, context):
    query = update.callback_query
    query.answer()

    if query.data == 'accounts':
        show_accounts(update, context)
    elif query.data == 'virtual_currency':
        show_virtual_currency(update, context)
    elif query.data == 'cases':
        show_cases(update, context)
    elif query.data.startswith('account_'):
        show_account_details(update, context, int(query.data.split('_')[1]))
    elif query.data.startswith('case_'):
        show_case_details(update, context, query.data.split('_')[1])
    elif query.data.startswith('payment_'):
        process_payment(update, context, query.data.split('_')[1])

# Обработчик сообщений
def handle_message(update, context):
    text = update.message.text
    if text.isdigit():
        buy_virtual_currency(update, context, int(text))

# Функция для получения главного меню
def get_main_menu():
    keyboard = [[InlineKeyboardButton("Аккаунты", callback_data='accounts')],
                [InlineKeyboardButton("Виртуальная валюта", callback_data='virtual_currency')],
                [InlineKeyboardButton("Кейсы", callback_data='cases')]]
    return InlineKeyboardMarkup(keyboard)

# Функции для показа списка аккаунтов, виртуальной валюты и кейсов
def show_accounts(update, context):
    accounts = [
        {
            'level': 6,
            'description': 'Аккаунт для начинающих. Включает в себя базовые функции.',
            'price': 100
        },
        {
            'level': 12,
            'description': 'Аккаунт среднего уровня. Включает в себя расширенные функции.',
            'price': 500
        },
        {
            'level': 18,
            'description': 'Аккаунт высокого уровня. Включает в себя передовые функции.',
            'price': 1000
        },
        {
            'level': 23,
            'description': 'Аккаунт для профессионалов. Включает в себя все возможности.',
            'price': 2000
        }
    ]

    account_list = '\n'.join([f"Аккаунт {account['level']} уровня - {account['price']} руб.\n{account['description']}" for account in accounts])
    context.bot.send_message(chat_id=update.effective_chat.id, text=account_list, reply_markup=get_account_menu(accounts))

def get_account_menu(accounts):
    keyboard = [[InlineKeyboardButton(f"Аккаунт {account['level']} уровня - {account['price']} руб.", callback_data=f"account_{account['level']}") for account in accounts]]
    return InlineKeyboardMarkup(keyboard)

def show_account_details(update, context, level):
    account = next(acc for acc in accounts if acc['level'] == level)
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Аккаунт {account['level']} уровня\n\n{account['description']}\n\nЦена: {account['price']} руб.", reply_markup=get_payment_menu())

def show_virtual_currency(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Введите количество виртуальной валюты, которое вы хотите купить (минимум 50,000, максимум 45,000,000):")

def buy_virtual_currency(update, context, amount):
    if amount < 50000 or amount > 45000000:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Недопустимое количество виртуальной валюты. Попробуйте еще раз.")
        return

    price = get_virtual_currency_price(amount)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Стоимость {amount} виртуальной валюты составляет {price} руб. Выберите способ оплаты:", reply_markup=get_payment_menu())

def get_virtual_currency_price(amount):
    return amount * 0.01

def show_cases(update, context):
    cases = [
        {
            'name': 'Бомжовский',
            'price': 140,
            'chances': {
                'cheap_item': 80,
                'medium_item': 15,
                'rare_item': 5
            }
        },
        {
            'name': 'Ежедневный',
            'price': 300,
            'chances': {
                'cheap_item': 60,
                'medium_item': 30,
                'rare_item': 10
            }
        },
        {
            'name': 'Стандартный',
            'price': 500,
            'chances': {
                'cheap_item': 40,
                'medium_item': 40,
                'rare_item': 20
            }
        },
        {
            'name': 'Особый',
            'price': 700,
            'chances': {
                'cheap_item': 20,
                'medium_item': 50,
                'rare_item': 30
            }
        },
        {
            'name': 'Кейс за Блек Коины',
            'price': 700,
            'chances': {
                'cheap_item': 10,
                'medium_item': 40,
                'rare_item': 50
            }
        }
    ]

    case_list = '\n'.join([f"{case['name']} - {case['price']} руб." for case in cases])
    context.bot.send_message(chat_id=update.effective_chat.id, text=case_list, reply_markup=get_case_menu(cases))

def get_case_menu(cases):
    keyboard = [[InlineKeyboardButton(f"{case['name']} - {case['price']} руб.", callback_data=f"case_{case['name']}") for case in cases]]
    return InlineKeyboardMarkup(keyboard)

def show_case_details(update, context, case_name):
    case = next(c for c in cases if c['name'] == case_name)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Характеристики кейса '{case['name']}':\n\nЦена: {case['price']} руб.\nШансы:\n- Дешевый предмет: {case['chances']['cheap_item']}%\n- Средний предмет: {case['chances']['medium_item']}%\n- Редкий предмет: {case['chances']['rare_item']}%", reply_markup=get_payment_menu())

def get_payment_menu():
    keyboard = [
        [InlineKeyboardButton("Телеграм кошелек", callback_data="payment_telegram")],
        [InlineKeyboardButton("Kaspi Bank", callback_data="payment_kaspi")],
        [InlineKeyboardButton("СБП", callback_data="payment_sbp")]
    ]
    return InlineKeyboardMarkup(keyboard)

def process_payment(update, context, payment_method):
    if payment_method == 'telegram':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Оплатите через Телеграм кошелек UQC8Y2ZLGUJSmAasHTw_VNvO5jQ4w4OeJC_DQBO-wnqUItAL")
    elif payment_method == 'kaspi':
        
        context.bot.send_message(chat_id=update.effective_chat.id, text="Оплатите по реквизитам на Kaspi Gold:\nНомер: 4400 4302 6934 6638\nИмя: Данил Г.\nКомментарий: НЕ ПИСАТЬ!!!")
    elif payment_method == 'sbp':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Оплатите на карту России: 2200701089399395 Аким. После оплаты свяжитесь с автором данного бота @doksformoney для дальнейших переговоров")

if __name__ == '__main__':
    main()
