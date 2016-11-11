from telegram import (ReplyKeyboardMarkup, ReplyKeyboardHide)
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters,\
                        ConversationHandler

NAME, PHOTO = range(2)

menu_keyboard = [['Authorize new person', 'Open the door'], ['Talk']]

def start(bot, update):
    update.message.reply_text(
        'Hi! I am your personal intercom assisstant. \n\n'
        'Here is a menu of all the functionality I have.',
        reply_markup=ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False))

def authorize(bot, update):
    update.message.reply_text('Enter the person\'s name')
    return NAME

def enter_name(bot, update):
    name = update.message.text
    update.message.reply_text('You entered: %s\n\nPlease upload the corresponding face' %name)
    return PHOTO

def new_face(bot, update):
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    photo_file.download('user_photo.jpg')
    update.message.reply_text('Gorgeous!', reply_markup=ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False))
    return ConversationHandler.END

def cancel(bot, update):
    update.message.reply_text('Authorization process canceled.',
                              reply_markup=ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False))
    return ConversationHandler.END

updater = Updater('290587333:AAG9wahnftHOWXeT00JIQolmgVwmEk0pqEU')

updater.dispatcher.add_handler(CommandHandler('start', start))

authorize_handler = ConversationHandler(
    entry_points = [RegexHandler('^Authorize new person', authorize)],

    states = {
        NAME: [MessageHandler(Filters.text, enter_name)],
        PHOTO: [MessageHandler(Filters.photo, new_face)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

updater.dispatcher.add_handler(authorize_handler)

updater.start_polling()
updater.idle()
