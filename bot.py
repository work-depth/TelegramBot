import logging
from turtle import back
from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import os
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
# import mongoDB

logger = logging.getLogger(__name__)

TOKEN = "5070020632:AAF8FSn_WUBQBLRdAuSXmjqjjC_y3MjfCf8"
allMembers = []

# register command for each user. call addUser
# admin command to add or remove admins
# 

roles = []
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

# Helper function to check is a person is an admin or not.
def get_admin_ids(bot, chat_id):
    """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]

# Command handler for registering a user.
def registerUser(update, context):
    # print(update)
    temp = update.message.text.split()
    if(len(temp)<2):
        update.message.reply_text("Oops! You forgot to mention the role. Try again.")
    else:
        currUser = update.message.from_user
        currId = currUser.id
        currName = currUser.first_name+" "+currUser.last_name
        currIsAdmin = currId in get_admin_ids(updater.bot, update.message.chat.id)
        currGrpId = update.message.chat.id
        print(update)
        print()
        print(currId, currName, temp[1], currIsAdmin, currGrpId)
        print()
        # mongoDB.addUser(currId, currName, temp[1], currIsAdmin, currGrpId)

      

def addMemberIfNotAdded(update, context):
    if(update.message.from_user not in allMembers):
        allMembers.append(update.message.from_user)
        print("Added")


def echo(update, context):
    addMemberIfNotAdded(update, context)
    print(update.message.chat.id)
    print("hello")
    print(update.message)
    updater.bot.send_message(update.message.chat.id,"lolok")

    
    
    """Echo the user message."""

def new_member(update, context):
    for member in update.message.new_chat_members:
        if member.username == 'bhanChod_bot':
            update.message.reply_text('Thanks for adding me.\nHope I will be able to help as much as possible. Please let me know you roles so I can enter it in my system.\nDear admin, please send me a list of all roles availbles')
            # global allMembers
            # allMembers = updater.bot.get_chat_administrators(update.message.chat.id)
            # for member in allMembers:
            #     print(member.user.first_name)
            

        elif member.username != 'YourBot':
            update.message.reply_text('Welcome lol')
            


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    

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
    dp.add_handler(CommandHandler("register", registerUser))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    updater.idle()

main()