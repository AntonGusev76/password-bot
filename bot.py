import telebot
import random
import string
from dotenv import load_dotenv
import os

load_dotenv()  # Загрузит переменные из .env

BOT_TOKEN = os.getenv("BOT_TOKEN") # Получаем токен бота из переменной окружения

bot = telebot.TeleBot(BOT_TOKEN) # Создаём объект бота
bot.remove_webhook()


def generate_password(length=12): # Функция генерации пароля
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

@bot.message_handler(commands=['start']) # Команда /start — показывает клавиатуру с вариантами
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for length in [8, 12]:
        markup.add(telebot.types.KeyboardButton(str(length)))
    bot.send_message(message.chat.id, "Выбери длину пароля или введи необходимую", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.isdigit()) # Обработка цифр — генерация пароля
def send_password(message):
    length = int(message.text)
    if length < 4:
        bot.reply_to(message, "Минимум 4 символа.")
    else:
        password = generate_password(length)
        bot.reply_to(message, f"Вот твой пароль:\n`{password}`", parse_mode='Markdown')

bot.polling() # Запуск бота
