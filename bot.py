import telebot
import random
import string

TOKEN = '7243602173:AAHzqBdzqjxCKfxvhz-IxFmJlzQTuY7UzOA'
bot = telebot.TeleBot(TOKEN)

bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()


def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for length in [8, 12, 16]:
        markup.add(telebot.types.KeyboardButton(str(length)))
    bot.send_message(message.chat.id, "Выбери длину пароля:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.isdigit())
def send_password(message):
    length = int(message.text)
    if length < 4:
        bot.reply_to(message, "Минимум 4 символа.")
    else:
        password = generate_password(length)
        bot.reply_to(message, f"Вот твой пароль:\n`{password}`", parse_mode='Markdown')

bot.polling()
