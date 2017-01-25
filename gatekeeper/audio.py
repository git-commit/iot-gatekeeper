import os
import tempfile
import logging
import wave
import pyaudio
import soundfile as sf
from pysoundcard import Stream
from subprocess import call, Popen

temp = tempfile.gettempdir()

CHUNK = 1024
BUZZER_AUDIO_FILE = 'res/buzz.wav'
AUTHORIZED_AUDIO_FILE = 'res/authorized.wav'
NOT_PERMITTED_AUDIO_FILE = 'res/no-permit.wav'
DOORBELL_AUDIO_FILE = 'res/doorbell.mp3'

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
   call(["play", path])

def playAudioFileAsync(path):
   call(["play", path, "&"])

def recordVoice():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    Rate = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT, channels = CHANNELS, rate = Rate, input = True, frames_per_buffer = CHUNK)

    logging.debug("Recording")

    frames = []

    for i in range(0, int(Rate / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    logging.debug("done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(Rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    call(["ffmpeg", "-y", "-i", WAVE_OUTPUT_FILENAME, "-acodec", "libopus", "-b:a", "44100", "output.ogg"])
    # call(["opusenc", "--bitrate", "64", WAVE_OUTPUT_FILENAME, 'output.opus'])
    return "output.ogg"
