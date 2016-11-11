import threading

class Intercom(object):

    """Docstring for Intercom. """

    def __init__(self):
        self.bell_button_gpio = "D4"
        self.bell_speaker_gpio = "D2"
        self.buzzer_gpio = "D3"
        self.display_i2c = "I2C-1"
        self.debug_led = "D7"
        self.gpio_thread = GPIOThread(self)

    def openDoor(self):
        pass

    def ringBell(self):
        pass
    
    def recordAudio(self, seconds=10):
        pass

    def playAudio(self, filePath):
        pass

    def registerBellPressedCallback(self, callback):
        self.bellButtonCallback = callBack

class GPIOThread(threading.Thread):
    def __init__(self, intercom):
        self.intercom = intercom

    def run(self):
        pass
