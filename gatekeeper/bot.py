#!/usr/bin/env python3

import logging

import audio
import privateconfig
from facerecognition import *
from SpeechRecognition import *

from io import BytesIO
from telegram import (ReplyKeyboardMarkup)
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters,\
                        ConversationHandler


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

NAME, PHOTO = range(2)

TALK = 0

name = None
chat_id = None
face_recognition = FaceRecognition()
speech_recognition = SpeechRecognition()

menu_keyboard = [['Authorize new person', 'Talk'], ['Open the door', 'Hold the door!']]

def start(bot, update):
    global chat_id
    chat_id = update.message.chat.id
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
    update.message.reply_text('Now upload a photo of %s!' %name)
    return PHOTO

def new_face(bot, update):
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    face_recognition.add_auth_person(photo_file, name)
    update.message.reply_text('Congratulation! Now %s can unlock the door.' % name, reply_markup=ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False))
    return ConversationHandler.END

def voice(bot, update):
    logging.debug("Received voice message")
    local_file_path = audio.saveVoice(bot, update.message)
    audio.playAudioFile(local_file_path)

def cancel(bot, update):
    update.message.reply_text('Process canceled.',
                              reply_markup=ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False))
    return ConversationHandler.END

def verify(bot, update):
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    path = '%s.jpg' % name
    photo_file.download(path)
    file_stream = open(path, "rb").read()
    verified_name = face_recognition.verify_face(file_stream)
    text = '%s is knocking on the door!' % verified_name
    if verified_name is None:
        text = 'Some stranger is knocking on the door. Do you want to let him in?'
    update.message.reply_text(text)

def verify_image(updater, image, name=None):
    if name:
        verified_name = name
    else:
        verified_name = face_recognition.verify_face(image)
    text = '%s is knocking on the door!' % verified_name
    if verified_name is None:
        text = 'Some stranger is knocking on the door. Do you want to let him in?'
    try:
        updater.bot.sendPhoto(chat_id, BytesIO(image))
        updater.bot.sendMessage(chat_id, text)
    except Exception:
        logging.exception("Can not send the photo of the person in front of the door to the chat.")
    return verified_name is not None

def enter_talk(bot, update):
    update.message.reply_text('Enter the text you want to say.')
    return TALK

def talk(bot, update):
    file = speech_recognition.transformToAudio(update.message.text)
    if file:
        update.message.reply_text('Your message was successfully transmitted.')
        audio.playAudioFile('temp.wav')
    else:
        update.message.reply_text('There has been a problem with your message.')

    return ConversationHandler.END

def playAudio(bot, update):
    audio.playAudioFile('temp.wav')

def sendVoiceToChat(bot, update, file_path):
    bot.sendVoice(chat_id=update.message.chat_id, voice=open(file_path, 'rb'))
    speech_recognition.transformToText("output.wav")

def voiceSenderTester(bot, update):
    file = audio.recordVoice()
    sendVoiceToChat(bot, update, file)

updater = Updater(privateconfig.telegram_token)
authorize_handler = ConversationHandler(
    entry_points = [RegexHandler('^Authorize new person', authorize)],

    states = {
        NAME: [MessageHandler(Filters.text, enter_name)],
        PHOTO: [MessageHandler(Filters.photo, new_face)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

talk_handler = ConversationHandler(
    entry_points = [RegexHandler('^Talk', enter_talk)],

    states = {
        TALK: [MessageHandler(Filters.text, talk)]
    },

    fallbacks=[RegexHandler('^Cancel', cancel)]
)

updater.dispatcher.add_handler(authorize_handler)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, verify))

updater.dispatcher.add_handler(MessageHandler(Filters.voice, audio.transmitVoice))

updater.dispatcher.add_handler(CommandHandler('play', playAudio))

updater.dispatcher.add_handler(talk_handler)

updater.dispatcher.add_handler(CommandHandler('record', voiceSenderTester))

voice_handler = MessageHandler(Filters.voice, voice)

updater.dispatcher.add_handler(voice_handler)

def run_bot():
    updater.start_polling()
    updater.idle()
