#!/usr/bin/env python3

import bot as chat_bot
from intercom import Intercom
import logging

icom = Intercom()

def onBellPressed():
    if chat_bot.chat_id is None:
        logging.warning('Bell is pressed but we have now user in the chat')
    if chat_bot.verify_image(chat_bot.updater, icom.takePicture()):
        icom.ringBuzzer()

icom.registerOnBellPressedListener(onBellPressed)
chat_bot.registerOnSnapButtonListener(onBellPressed)

chat_bot.run_bot()
