from telegram import (ReplyKeyboardMarkup, ReplyKeyboardHide)
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters,\
                        ConversationHandler
import config
import audio
import privateconfig
import logging

from facerecognition import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

NAME, PHOTO = range(2)

name = None

face_recognition = FaceRecognition()

menu_keyboard = [['Authorize new person', 'Open the door'], ['Talk']]

def start(bot, update):
    update.message.reply_text(
        'Hi! I am your personal intercom assistant. \n\n'
        'Here is a menu of all the functionality I have.',
        reply_markup=ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False))

def authorize(bot, update):
    update.message.reply_text('Enter the person\'s name')
    return NAME

def enter_name(bot, update):
    global name
    name = update.message.text
    update.message.reply_text('You entered: %s\n\nPlease upload the corresponding face' %name)
    return PHOTO

def new_face(bot, update):
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    face_recognition.add_auth_person(photo_file, name)
    update.message.reply_text('Gorgeous!', reply_markup=ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False))
    return ConversationHandler.END

def voice(bot, update):
    logging.debug("Received voice message")
    local_file_path = audio.saveVoice(bot, update.message)
    audio.playAudioFile(local_file_path)

def cancel(bot, update):
    update.message.reply_text('Authorization process canceled.',
                              reply_markup=ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False))
    return ConversationHandler.END

def verify(bot, update):
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    verified_name = face_recognition.verify_face(photo_file)
    update.message.reply_text('%s' %verified_name)

updater = Updater(privateconfig.telegram_token)

authorize_handler = ConversationHandler(
    entry_points = [RegexHandler('^Authorize new person', authorize)],

    states = {
        NAME: [MessageHandler(Filters.text, enter_name)],
        PHOTO: [MessageHandler(Filters.photo, new_face)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

updater.dispatcher.add_handler(authorize_handler)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, verify))

voice_handler = MessageHandler(Filters.voice, voice)

updater.dispatcher.add_handler(voice_handler)

updater.start_polling()
updater.idle()
