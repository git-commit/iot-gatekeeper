import os
import tempfile
import logging
import wave
import pyaudio
import soundfile as sf
from pysoundcard import Stream
from subprocess import call

temp = tempfile.gettempdir()

CHUNK = 1024

def isVoiceMessage(message):
    return message.voice is not None

def transmitVoice(bot, update):
    file = saveVoice(bot, update.message)
    call(["ffmpeg", "-y", "-i", file, "temp.wav"])
    playAudioFile('temp.wav')

def saveVoice(bot, message):
    file_id = message.voice.file_id
    file_name = "voice_%s_%s.ogg" % (str(message.chat_id), str(message.date))
    file_name = file_name.replace(" ", "_")
    file_name = file_name.replace(":", ".")
    logging.info("Saving voice file %s" % (file_name))
    new_file = bot.getFile(file_id)
    local_file_path = os.path.join(temp, file_name)
    new_file.download(local_file_path)
    return local_file_path

def playAudioFile(path):
    f = wave.open(path, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                channels = f.getnchannels(),
                rate = f.getframerate(),
                output = True)
    #read data
    data = f.readframes(CHUNK)

    #paly stream
    while data != '':
        stream.write(data)
        data = f.readframes(CHUNK)

    #stop stream
    stream.stop_stream()
    stream.close()

    #close PyAudio
    p.terminate()
