import threading
from facerecognition import *
from grovepi import *
from time import sleep
import logging
from datetime import datetime, timedelta

class Intercom(object):

    """Docstring for Intercom. """

    BUZZER_RING_DURATION = 3

    def __init__(self):
        self.bell_button_gpio = 4
        self.bell_speaker_gpio = 2
        self.buzzer_gpio = 3
        self.display_i2c = "I2C-1"
        self.debug_led = "D7"
        self.onBellPressedCallback = None
        self.gpio_thread = GPIOThread(self)
        self.gpio_thread.start()
        self.bell_is_not_pressed = True
        self.should_ring_the_buzzer = False
        self.buzzer_ring_start_time = None
        pinMode(self.bell_button_gpio, "INPUT")
        pinMode(self.buzzer_gpio, "OUTPUT")

    def openDoor(self):
        pass

    def ringBuzzer(self):
        digitalWrite(self.bell_speaker_gpio, 1)
        self.should_ring_the_buzzer = True
        self.buzzer_ring_start_time = datetime.now()

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

    def __update_bell_state(self):
        bell_is_still_not_pressed = not self.isBellPressed()
        if self.bell_is_not_pressed and not bell_is_still_not_pressed:
            self.onBellPressed()
        self.bell_is_not_pressed = bell_is_still_not_pressed

    def __update_buzzer_state(self):
        if self.should_ring_the_buzzer and (datetime.now() - self.buzzer_ring_start_time).total_seconds() > Intercom.BUZZER_RING_DURATION:
            self.should_ring_the_buzzer = False
            self.buzzer_ring_start_time = None
            digitalWrite(self.bell_button_gpio, 0)

    def update_state(self):
        self.__update_bell_state()
        self.__update_buzzer_state()

class GPIOThread(threading.Thread):

    def __init__(self, intercom):
        super(GPIOThread, self).__init__()
        self.intercom = intercom

    def run(self):
        while True:
            self.intercom.update_state()
            sleep(0.25)
