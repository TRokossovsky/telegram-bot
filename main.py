import telebot
import telebot.service_utils
from telebot import types

with open('./API.txt', 'r') as file:
    API_TOKEN = file.read()

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    gb_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    gb_button1 = types.KeyboardButton(text='Gelbooru Parser')
    gb_buttons.add(gb_button1)
    if message.from_user.first_name is None:
        bot.reply_to(message, f'Welcome, {message.from_user.last_name}!',
                     reply_markup=gb_buttons)
    elif message.from_user.last_name is None:
        bot.reply_to(message, f'Welcome, {message.from_user.first_name}!',
                     reply_markup=gb_buttons)
    else:
        bot.reply_to(message, f'Welcome, {message.from_user.username}!',
                     reply_markup=gb_buttons)


@bot.message_handler(func=lambda message: message.text.lower() == 'complain')
def complain(message):
    complaint_text = bot.reply_to(message, 'Sure! Write your complaint down below.')
    bot.register_next_step_handler(complaint_text, complaint_receive)


def complaint_receive(complaint):
    complaint_message = complaint.text
    complaint_username = complaint.from_user.username
    complaint_first_name = complaint.from_user.first_name
    complaint_chat_id = complaint.chat.id
    if complaint_username is None:
        complaint_username = complaint_first_name
        file = open('./complaints.txt', 'a', encoding='utf-8')
        file.write(str(complaint_username) + f'({complaint_chat_id}) complains: ' + str(complaint_message) + '\n')
        file.close()
    else:
        file = open('./complaints.txt', 'a', encoding='utf-8')
        file.write(str(complaint_username) + f'({complaint_chat_id}) complains: ' + str(complaint_message) + '\n')
        file.close()


@bot.message_handler(func=lambda message: message.text.lower() == 'qrcode')
def qrcode_sender(message):
    photo = open('./qrcode.png', 'rb')
    bot.send_photo(message.chat.id, photo=photo)
    photo.close()


# TODO
#  @bot.message_handler(commands=['gelbooru'])
#  def gelbooru_command(message):
#    bot.reply_to(message, 'Enter the link you want to parse:')


bot.infinity_polling()
