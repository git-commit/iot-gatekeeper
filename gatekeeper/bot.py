from telegram import (ReplyKeyboardMarkup, ReplyKeyboardHide)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(bot, update):
    reply_keyboard = [['Authorize new person', 'Open the door'], ['Talk']]

    update.message.reply_text(
        'Hi! I am your personal intercom assisstant. \n\n'
        'Here is a menu of all the functionality I have.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False))

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.sendMessage(chat_id=update.message.chat_id, text=text_caps)

updater = Updater('293092231:AAEVHlXq0RmYk1Dmnw43DhRyksudxPWd9YE')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))

echo_handler = MessageHandler(Filters.text, echo)
caps_handler = CommandHandler('caps', caps, pass_args=True)

updater.dispatcher.add_handler(echo_handler)
updater.dispatcher.add_handler(caps_handler)

updater.start_polling()
updater.idle()
