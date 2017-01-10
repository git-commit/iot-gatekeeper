from facerecognition import *
from time import sleep
import logging
from datetime import datetime, timedelta
import audio
import nodered

class Intercom(object):

    """An intercom for the things."""

    def __init__(self):
        self.bell_button_gpio = 4
        self.bell_speaker_gpio = 2
        self.display_i2c = "I2C-1"
        self.debug_led = "D7"
        self.onBellPressedCallback = None
        self.bell_is_not_pressed = True
        self.openDoorClient = nodered.NodeRedDoorOpenClient()

    def openDoor(self):
        self.openDoorClient.sendOpenDoor()

    def ringBuzzer(self):
        audio.playAudioFile(audio.BUZZER_AUDIO_FILE)

    def takePicture(self):
        image_name = 'tmp_visitor.jpg'
        os.system('fswebcam -r 640x480 --save %s' % image_name)
        return open(image_name, 'rb').read()

    def registerOnBellPressedCallback(self, callback):
        self.onBellPressedCallback = callback

    def onBellPressed(self):
        if self.onBellPressedCallback:
            logging.info("Bell is pressed")
            self.onBellPressedCallback()

    def isBellPressed(self):
        return False
    
    def __update_bell_state(self):
        bell_is_still_not_pressed = not self.isBellPressed()
        if self.bell_is_not_pressed and not bell_is_still_not_pressed:
            self.onBellPressed()
        self.bell_is_not_pressed = bell_is_still_not_pressed

    def update_state(self):
        self.__update_bell_state()
