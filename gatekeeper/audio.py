import os
import tempfile

temp = tempfile.gettempdir()

def is_voice_message(message):
    return message.voice is not None

def save_audio(bot, message, path):
    file_id = message.voice.file_id
    new_file = bot.getFile(file_id)
    local_filename = os.path.join(temp, message.document.file_name)
    new_file.download(local_filename)
