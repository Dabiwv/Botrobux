import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Задайте ваши токены
TELEGRAM_TOKEN = '6423641572:AAFx8dMJaahZBOgm8GRItFhkRlB3_vMa3c0'
OPENAI_API_KEY = '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'

# Переменная для хранения роли
user_role = {}

# Функция для отправки запросов к OpenAI
def get_openai_response(prompt: str, role: str) -> str:
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }

    # Изменяем поведение в зависимости от роли
    if role == 'arrogant':
        system_message = "You are a very arrogant assistant. You think you're superior to everyone."
    elif role == 'selfish':
        system_message = "You are a selfish assistant. You only care about your own interests."
    elif role == 'programmer':
        system_message = "You are a knowledgeable programmer assistant, ready to help with programming questions."
    else:
        system_message = "You are a helpful assistant."

    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'system', 'content': system_message},
                     {'role': 'user', 'content': prompt}],
        'max_tokens': 100,
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Ошибка при обращении к OpenAI API."

# Функция для обработки команд выбора роли
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Высокомерный", callback_data='arrogant')],
        [InlineKeyboardButton("Эгоист", callback_data='selfish')],
        [InlineKeyboardButton("Программист", callback_data='programmer')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите роль:', reply_markup=reply_markup)

# Функция для обработки выбора роли
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    role = query.data
    user_role[query.from_user.id] = role  # Сохраняем роль пользователя

    query.edit_message_text(text=f"Вы выбрали роль: {role}. Теперь вы можете задавать вопросы!")

# Функция для обработки текстовых сообщений
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    role = user_role.get(update.message.from_user.id, None)  # Получаем роль пользователя

    if role is None:
        update.message.reply_text("Сначала выберите роль, используя /start.")
        return

    response = get_openai_response(user_message, role)
    update.message.reply_text(response)

def main():
    # Создаем Updater и передаем ему токен
    updater = Updater(TELEGRAM_TOKEN)

    # Получаем диспетчер для обработки команд
    dispatcher = updater.dispatcher

    # Обработка команд
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
