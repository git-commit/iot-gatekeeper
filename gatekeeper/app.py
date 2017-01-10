#!/usr/bin/env python3

import bot as chat_bot
from intercom import Intercom
import logging
from facerecognition import FaceRecognition
import subprocess 

icom = Intercom()
facerec = FaceRecognition()

subprocess.call(["pulseaudio", "-D"])

def onBellPressed():
    if chat_bot.chat_id is None:
        logging.warning('Bell is pressed but we have no user in the chat')
    chat_bot.verify_image(chat_bot.updater, icom.takePicture())

def onTakeSnap():
    pic = icom.takePicture()
    chat_bot.uploadSnap(chat_bot.updater, pic)

icom.registerOnBellPressedCallback(onBellPressed)
chat_bot.registerOnSnapButtonCallback(onTakeSnap)

chat_bot.run_bot()
