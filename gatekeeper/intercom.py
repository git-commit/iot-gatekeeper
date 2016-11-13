import threading
from facerecognition import *
from grovepi import *
from time import sleep
import logging
from datetime import datetime, timedelta
import audio

class Intercom(object):

    """Docstring for Intercom. """

    BUZZER_AUDIO_FILE = 'res/buzz.wav'

    def __init__(self):
        self.bell_button_gpio = 4
        self.bell_speaker_gpio = 2
        self.display_i2c = "I2C-1"
        self.debug_led = "D7"
        self.onBellPressedCallback = None
        self.onAutoBuzzCallback = None
        self.gpio_thread = GPIOThread(self)
        self.gpio_thread.start()
        self.bell_is_not_pressed = True

        pinMode(self.bell_button_gpio, "INPUT")

    def openDoor(self):
        pass

    def ringBuzzer(self):
        audio.playAudioFile(Intercom.BUZZER_AUDIO_FILE)

    def recordAudio(self, seconds=10):
        pass

    def playAudio(self, filePath):
        pass

    def takePicture(self):
        image_name = 'tmp_visitor.jpg'
        os.system('fswebcam -r 640x480 --save %s' % image_name)
        return open(image_name, 'rb').read()

    def registerOnBellPressedListener(self, callback):
        self.onBellPressedCallback = callback

    def registerOnAutoBuzzListener(self, callback):
        self.onAutoBuzzCallback = callback

    def onBellPressed(self):
        if self.onBellPressedCallback:
            logging.info("Bell is pressed")
            self.onBellPressedCallback()

    def isBellPressed(self):
        read = digitalRead(self.bell_button_gpio)
        return read == 1

    def __update_buzzer_state(self):
        if self.should_ring_the_buzzer and (datetime.now() - self.buzzer_ring_start_time).total_seconds() > Intercom.BUZZER_RING_DURATION:
            self.should_ring_the_buzzer = False
            self.buzzer_ring_start_time = None
            digitalWrite(self.bell_button_gpio, 0)

    def update_state(self):
        self.__update_buzzer_state()

class GPIOThread(threading.Thread):

    def __init__(self, intercom):
        super(GPIOThread, self).__init__()
        self.intercom = intercom
        self.auto_buzz_counter = 0

    def run(self):
        while True:
            self.intercom.update_state()
            if self.auto_buzz_counter is 0:
                self.intercom.onAutoBuzzCallback()
            self.auto_buzz_counter = (self.auto_buzz_counter + 1) % 10
            sleep(0.25)
