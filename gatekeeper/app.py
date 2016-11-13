#!/usr/bin/env python3

import bot as chat_bot
from intercom import Intercom
import logging
from facerecognition import FaceRecognition as face_recognition

icom = Intercom()

def onBellPressed():
    if chat_bot.chat_id is None:
        logging.warning('Bell is pressed but we have now user in the chat')
    if chat_bot.verify_image(chat_bot.updater, icom.takePicture()):
        icom.ringBuzzer()

def onAutoBuzz():
    pic = icom.takePicture()
    if face_recognition.verify_face(pic) and chat_bot.verify_image(chat_bot.updater, pic):
        logging.debug("Auto-buzz accepted.")
        icom.ringBuzzer()

icom.registerOnBellPressedListener(onBellPressed)
icom.registerOnAutoBuzzListener(onAutoBuzz)
chat_bot.run_bot()
