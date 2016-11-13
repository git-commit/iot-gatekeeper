#!/usr/bin/env python3

import bot as chat_bot
from intercom import Intercom
import logging
from facerecognition import FaceRecognition

icom = Intercom()
facerec = FaceRecognition()

def onBellPressed():
    if chat_bot.chat_id is None:
        logging.warning('Bell is pressed but we have no user in the chat')
    if chat_bot.verify_image(chat_bot.updater, icom.takePicture()):
        icom.ringBuzzer()

def onAutoBuzz():
    pass
    # pic = icom.takePicture()
    # name = facerec.verify_face(pic)
    # if name:
    #     logging.debug("Auto-buzz: %s is in front of the door. Open..." % name)
    #     icom.ringBuzzer()

def onTakeSnap():
    pic = icom.takePicture()
    chat_bot.uploadSnap(chat_bot.updater, pic)

icom.registerOnBellPressedListener(onBellPressed)
icom.registerOnAutoBuzzListener(onAutoBuzz)
chat_bot.registerOnSnapButtonListener(onTakeSnap)

chat_bot.run_bot()
