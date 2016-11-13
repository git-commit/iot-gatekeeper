#!/usr/bin/env python3

import bot as chat_bot
# from intercom import Intercom
import logging
from time import sleep
# icom = Intercom()

# def onBellPressed():
    # if chat_bot.chat_id is None:
        # logging.warning('Bell is pressed but we have now user in the chat')
    # chat_bot.verify_image(chat_bot.updater, icom.takePicture())

chat_bot.run_bot()
# icom.registerOnBellPressedListener(onBellPressed)
