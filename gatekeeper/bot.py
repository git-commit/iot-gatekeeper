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


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

NAME, PHOTO = range(2)

READY, BASIC_RESPONSES = range(2)

TALK = 0

name = None
chat_id = None
face_recognition = FaceRecognition()
speech_recognition = SpeechRecognition()

main_menu = [['Authorize new person', 'Record'], ['Text to Speech', 'Snap a Photo']]
main_menu = ReplyKeyboardMarkup(main_menu, one_time_keyboard=False)

door_menu = [['Open the door', 'Hold the door!'], ['Basic responses']]
door_menu = ReplyKeyboardMarkup(door_menu, one_time_keyboard=False)

basic_responses_menu = [["I'm not at home"], ["You're not welcome here"], ["Come back later"], ["Who are you?"]]
basic_responses_menu = ReplyKeyboardMarkup(basic_responses_menu, one_time_keyboard=False)

authorize_menu = [["Stop authorization"]]
authorize_menu = ReplyKeyboardMarkup(authorize_menu, one_time_keyboard=False)

talk_menu = [["Who are you?"], ["What is the meaning of this?"], ["Cancel"]]
talk_menu = ReplyKeyboardMarkup(talk_menu, one_time_keyboard=True)

snapTaker = None

def start(bot, update):
    global chat_id
    chat_id = update.message.chat.id
    logging.info("Current chat owner is %s" % update.message.chat.first_name)
    update.message.reply_text(
        'Hi! I am your personal intercom assistant. \n\n'
        'Here is a menu of all the functionality I have.',
        reply_markup=main_menu)

def registerOnSnapButtonListener(actor):
    global snapTaker
    snapTaker = actor

def authorize(bot, update):
    update.message.reply_text('Enter the person\'s name', reply_markup=authorize_menu)
    return NAME

def enter_name(bot, update):
    global name
    name = update.message.text
    update.message.reply_text('Now upload a photo of %s!' % name)
    return PHOTO

def new_face(bot, update):
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    face_recognition.add_auth_person(photo_file, name)
    update.message.reply_text('Congratulation! Now %s can unlock the door.' % name, reply_markup=main_menu)
    return ConversationHandler.END

def voice(bot, update):
    logging.debug("Received voice message")
    local_file_path = audio.saveVoice(bot, update.message)
    audio.playAudioFile(local_file_path)

def cancel(bot, update):
    update.message.reply_text('Process canceled.',
                              reply_markup=main_menu)
    return ConversationHandler.END

def verify(bot, update):
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    path = 'candidate.jpg'
    photo_file.download(path)
    file_stream = open(path, "rb").read()
    verified_name = face_recognition.verify_face(file_stream)
    text = '%s is knocking on the door!' % verified_name
    if verified_name is None:
        text = 'Some stranger is knocking on the door. Do you want to let him in?'
    else:
        audio.playAudioFile(audio.BUZZER_AUDIO_FILE)
    update.message.reply_text(text, reply_markup=door_menu)
    return READY

def verify_image(updater, image):
    verified_name = face_recognition.verify_face(image)
    logging.info('recognize %s' % verified_name)
    text = '%s is knocking on the door!' % verified_name
    if verified_name is None:
        text = 'Some stranger is knocking on the door. Do you want to let him in?'

    try:
        updater.bot.sendPhoto(chat_id, BytesIO(image))
        updater.bot.sendMessage(chat_id, text, reply_markup=door_menu)
        sendVoiceToChat2(updater)
    except Exception:
        logging.exception("Can not send the photo of the person in front of the door to the chat.")
    return verified_name is not None

def enter_talk(bot, update):
    update.message.reply_text('Enter the text you want to say.', reply_markup=talk_menu)
    return TALK

def talk(bot, update):
    file = speech_recognition.transformToAudio(update.message.text)
    if file:
        update.message.reply_text('Your message was successfully transmitted.', reply_markup=main_menu)
        audio.playAudioFile('temp.wav')
    else:
        update.message.reply_text('There has been a problem with your message.', reply_markup=main_menu)

    return ConversationHandler.END

def playAudio(bot, update):
    audio.playAudioFile('temp.wav')

def sendVoiceToChat(bot, update, file_path):
    bot.sendVoice(chat_id=update.message.chat_id, voice=open(file_path, 'rb'))
    speech_recognition.transformToText("output.wav")

def sendVoiceToChat2(updater):
    """
    send voice as new message
    """
    file = audio.recordVoice()
    updater.bot.sendVoice(chat_id=chat_id, voice=open(file, 'rb'))


def voiceSenderTester(bot, update):
    file = speech_recognition.transformToAudio("Say your message")
    if file:
        audio.playAudioFile(file)
    # if file:
        # update.message.reply_text('', reply_markup=main_menu)
    file = audio.recordVoice()
    sendVoiceToChat(bot, update, file)

    file = speech_recognition.transformToAudio("Stop talking")
    if file:
        audio.playAudioFile(file)

def uploadSnap(updater, image):
    try:
        updater.bot.sendPhoto(chat_id, BytesIO(image))
    except Exception:
        logging.exception("Can not send the photo of the person in front of the door to the chat.")


def open_door(bot, update):
    audio.playAudioFile(audio.BUZZER_AUDIO_FILE)
    update.message.reply_text('Door opened',
                            reply_markup=main_menu)

def hold_the_door(bot, update):
    file = speech_recognition.transformToAudio("You are not permitted to enter")
    if file:
        audio.playAudioFile('temp.wav')

    update.message.reply_text('Entrance denied',
                            reply_markup=main_menu)

def goto_basic_responses(bot, update):
    update.message.reply_text('Choose one of given responses',
                            reply_markup=basic_responses_menu)
    return BASIC_RESPONSES

def basic_response(bot, update):
    file = speech_recognition.transformToAudio(update.message.text)
    if file:
        audio.playAudioFile('temp.wav')

    update.message.reply_text('Entrance denied and message sent',
                            reply_markup=main_menu)
    return ConversationHandler.END

def take_a_snap(bot, update):
    if snapTaker:
        snapTaker()

updater = Updater(privateconfig.telegram_token)
authorize_handler = ConversationHandler(
    entry_points = [RegexHandler('^Authorize new person', authorize)],

    states = {
        NAME: [RegexHandler('(?!Stop authorization)', enter_name)],
        PHOTO: [MessageHandler(Filters.photo, new_face)]
    },

    fallbacks=[RegexHandler('^Stop authorization', cancel)]
)

talk_handler = ConversationHandler(
    entry_points = [RegexHandler('^Text to Speech', enter_talk)],

    states = {
        TALK: [RegexHandler('(?!Cancel)', talk)]
    },

    fallbacks=[RegexHandler('^Cancel', cancel)]
)

door_opening_handler = ConversationHandler(
    entry_points = [MessageHandler(Filters.photo, verify)],

    states = {
        READY: [RegexHandler('^Open the door', open_door),
                RegexHandler('^Hold the door!', hold_the_door),
                RegexHandler('^Basic responses', goto_basic_responses)],
        BASIC_RESPONSES: [MessageHandler(Filters.text, basic_response)]
    },

    fallbacks = [RegexHandler('^Cancel', cancel)]
)

updater.dispatcher.add_handler(authorize_handler)
updater.dispatcher.add_handler(CommandHandler('start', start))

updater.dispatcher.add_handler(MessageHandler(Filters.voice, audio.transmitVoice))

updater.dispatcher.add_handler(CommandHandler('play', playAudio))

updater.dispatcher.add_handler(talk_handler)
updater.dispatcher.add_handler(door_opening_handler)

updater.dispatcher.add_handler(RegexHandler('^Snap a Photo', take_a_snap))
updater.dispatcher.add_handler(RegexHandler('^Record', voiceSenderTester))

updater.dispatcher.addHandler(MessageHandler(Filters.photo, verify))

voice_handler = MessageHandler(Filters.voice, voice)

updater.dispatcher.add_handler(voice_handler)

def run_bot():
    updater.start_polling()
    updater.idle()
