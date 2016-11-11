import os
import tempfile
import logging

temp = tempfile.gettempdir()

def isVoiceMessage(message):
    return message.voice is not None

def saveVoice(bot, message):
    file_id = message.voice.file_id
    file_name = "voice_%s_%s.oga" % (str(message.chat_id), str(message.date))
    file_name = file_name.replace(" ", "_")
    file_name = file_name.replace(":", ".")
    logging.info("Saving voice file %s" % (file_name))
    new_file = bot.getFile(file_id)
    local_filename = os.path.join(temp, file_name)
    new_file.download(local_filename)
