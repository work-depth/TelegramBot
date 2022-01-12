import logging
from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import os

TOKEN = "5070020632:AAF8FSn_WUBQBLRdAuSXmjqjjC_y3MjfCf8"
print(TOKEN)
# logging.basicConfig(filename="newfile.log",
#                     format='%(asctime)s %(message)s',
#                     filemode='w')
def start(update, context):
    # print(update)
    msg  = "Hello, I am bhan_chod."
    update.message.reply_text(msg)
    update.message.reply_text(
    'Cute pics',
    reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(text='on Facebook', url='https://i.guim.co.uk/img/media/fe1e34da640c5c56ed16f76ce6f994fa9343d09d/0_174_3408_2046/master/3408.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=67773a9d419786091c958b2ad08eae5e')],
        [InlineKeyboardButton(text='on Telegram', url='https://i.guim.co.uk/img/media/fe1e34da640c5c56ed16f76ce6f994fa9343d09d/0_174_3408_2046/master/3408.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=67773a9d419786091c958b2ad08eae5e')],
    ])
)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    # db.initiating_mongodb()
    global updater
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))


    # Start the Bot
    updater.start_polling()
    updater.idle()

main()