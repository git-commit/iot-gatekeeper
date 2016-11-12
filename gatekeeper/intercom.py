import threading
from facerecognition import *
from grovepi import *
from time import sleep
import logging

class Intercom(object):

    """Docstring for Intercom. """

    def __init__(self):
        self.bell_button_gpio = 4
        self.bell_speaker_gpio = 2
        self.buzzer_gpio = 3
        self.display_i2c = "I2C-1"
        self.debug_led = "D7"
        self.onBellPressedCallback = None
        self.gpio_thread = GPIOThread(self)
        self.gpio_thread.start()
        pinMode(self.bell_button_gpio, "INPUT")
        pinMode(self.buzzer_gpio, "OUTPUT")

    def openDoor(self):
        pass

    def ringBell(self):
        digitalWrite(self.buzzer_gpio, 1)

    def recordAudio(self, seconds=10):
        pass

    def playAudio(self, filePath):
        pass

    def takePicture(self):
        image_name = 'temo.jpg'
        os.system('fswebcam -r 320x240 --save %s' % image_name)
        return open(image_name, 'rb').read()

    def registerOnBellPressedListener(self, callback):
        self.onBellPressedCallback = callback

    def onBellPressed(self):
        if self.onBellPressedCallback:
            logging.info("Bell is pressed")
            self.onBellPressedCallback()

    def isBellPressed(self):
        read = digitalRead(self.bell_button_gpio)
        return read == 1

class GPIOThread(threading.Thread):

    def __init__(self, intercom):
        super(GPIOThread, self).__init__()
        self.intercom = intercom

    def run(self):
        bell_is_pressed = False
        while True:
            bell_is_pressed_new = self.intercom.isBellPressed()
            if bell_is_pressed is not bell_is_pressed_new:
                self.intercom.onBellPressed()
            bell_is_pressed = bell_is_pressed_new
            sleep(0.5)
