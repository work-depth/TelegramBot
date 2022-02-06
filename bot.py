import logging
from turtle import back
from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import os
# from decouple import config
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
# import mongoDB

from telegram.bot import Bot, BotCommand

# TOKEN = os.environ.get('TOKEN')
TOKEN = '5070020632:AAF8FSn_WUBQBLRdAuSXmjqjjC_y3MjfCf8'
print(TOKEN)


command = [BotCommand("start","to start something"),BotCommand("stop", "to stop something")]
bot = Bot(TOKEN)
bot.set_my_commands(command)
logger = logging.getLogger(__name__)
# register command for each user. call addUser
# admin command to add or remove admins
# 

roles = []
print(TOKEN)
# logging.basicConfig(filename="newfile.log",
# format='%(asctime)s %(message)s', filemode='w')
def start(update, context):
    update.message.reply_text(
    "Hi! I am a bot that helps you to manage your tasks.\nChoose one of the options below",
    reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Register User', switch_inline_query_current_chat = "/register"), InlineKeyboardButton(text='Add task', switch_inline_query_current_chat = "/addtask")],
        [InlineKeyboardButton(text='Add task', switch_inline_query_current_chat = "/addtask")],
    ])
    )


def helpMe(update, context):
    update.message.reply_text("""
    /register <role> - Register yourself in the group.
    /showTasks - Show all the tasks assigned to you.
    /showTasks <all/personal> - Show all the tasks assigned to you or all the tasks assigned to all the members of the group.
    /taskInfo <task_id> - Show the details of the task.
    /help - Show this message.
    """)

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
        currName = currUser.username
        currIsAdmin = currId in get_admin_ids(updater.bot, update.message.chat.id)
        currGrpId = update.message.chat.id
        updater.bot.send_message(update.message.chat.id, mongoDB.register(currId, currName, temp[1], currIsAdmin, currGrpId))


def showTasks(update, context):
    temp = update.message.text.split()
    currUser = update.message.from_user
    currId = currUser.id
    currGrpId = update.message.chat.id
    msg = ""
    if(len(temp)<2):
        msg = mongoDB.task_list("personal", currId, currGrpId)
        updater.bot.send_message(update.message.chat.id,"Your assigned tasks are: "+msg)
    else:
        if(temp[1]=="all"):
            msg = mongoDB.task_list("all", currId, currGrpId)
            print("all", currId, currGrpId)
            updater.bot.send_message(update.message.chat.id,"All tasks are: "+msg)

        elif (temp[1]=="personal"):
            msg = mongoDB.task_list("personal", currId, currGrpId)
            print("personal", currId, currGrpId)
            updater.bot.send_message(update.message.chat.id,"Your assigned tasks are: "+msg)

        else:
            updater.bot.send_message(update.message.chat.id,"Sorry....I didn't get that.")
            return
        



def taskInfo(update, context):
    temp = update.message.text.split()
    currUser = update.message.from_user
    currId = currUser.id
    currGrpId = update.message.chat.id
    a = 1
    try:
        a = int(temp[1])
    except:
        updater.bot.send_message(update.message.chat.id,"Task ID should be a number.")
        return

    if(len(temp)<2):
        updater.bot.send_message(update.message.chat.id,"Please specify the task ID")
        return
    else:
        msg = "\n"+mongoDB.catch(currGrpId, currId, a)
        print("Getting the task id ",currGrpId, currId, a)
        updater.bot.send_message(update.message.chat.id,"Here are the details"+msg)

def promoteUser(update, context):
    temp = update.message.text.split()
    currUser = update.message.from_user
    currId = currUser.id
    currGrpId = update.message.chat.id
    if(len(temp) < 2):
        updater.bot.send_message(update.message.chat.id,"Looks like you forgot to mention who you wish to promote")
    else:
        idOfPersonToPromote = mongoDB.getUserID(temp[1][1:], currGrpId)
        if(idOfPersonToPromote == -1):
            updater.bot.send_message(update.message.chat.id,"This username is not found. Perhaps they have updated the username after registering.")
            return
        else:
            updater.bot.send_message(update.message.chat.id,mongoDB.admin("promote", currId, idOfPersonToPromote, currGrpId))
            updater.bot.promote_chat_member(currGrpId, idOfPersonToPromote)
    
def demoteUser(update, context):
    temp = update.message.text.split()
    currUser = update.message.from_user
    currId = currUser.id
    currGrpId = update.message.chat.id
    if(len(temp) < 2):
        updater.bot.send_message(update.message.chat.id,"Looks like you forgot to mention who you wish to demote")
    else:
        idOfPersonToDemote = mongoDB.getUserID(temp[1][1:], currGrpId)
        if(idOfPersonToDemote == -1):
            updater.bot.send_message(update.message.chat.id,"This username is not found. Perhaps they have updated the username after registering.")
            return
        else:
            updater.bot.send_message(update.message.chat.id,mongoDB.admin("demote", currId, idOfPersonToDemote, currGrpId))
            
            
def removeUser(update, context):
    temp = update.message.text.split()
    currUser = update.message.from_user
    currId = currUser.id
    currGrpId = update.message.chat.id
    if(len(temp) < 2):
        updater.bot.send_message(update.message.chat.id,"Looks like you forgot to mention who you wish to remote")
    else:
        idOfPersonToRemove = mongoDB.getUserID(temp[1][1:], currGrpId)
        if(idOfPersonToRemove == -1):
            updater.bot.send_message(update.message.chat.id,"This username is not found. Perhaps they have updated the username after registering.")
            return
        else:
            updater.bot.send_message(update.message.chat.id,mongoDB.admin("remove", currId, idOfPersonToRemove, currGrpId))
            # https://core.telegram.org/bots/api#banchatmember
            updater.bot.ban_chat_member(currGrpId, idOfPersonToRemove)

def addTask(update, context):
    temp = update.message.text.split()
    currUser = update.message.from_user
    currId = currUser.id
    currGrpId = update.message.chat.id
    time = temp[-1]
    date = temp[-2]
    date = date+" "+time
    message = ""
    for i in range(1, len(temp)-2):
        message += i
        message += " "

    if(len(temp) < 2):
        updater.bot.send_message(update.message.chat.id,"Looks like you forgot to mention the task details")
    else:
        # print(message, date, currId, currGrpId)
        updater.bot.send_message(mongoDB.add_task(message, date, currId, currGrpId))
        

def removeTask(update, context):
    temp = update.message.text.split()
    currUser = update.message.from_user
    currId = currUser.id
    currGrpId = update.message.chat.id

    
    if(len(temp) < 2):
        updater.bot.send_message(update.message.chat.id,"Looks like you forgot to mention the task id")
    else:
        try:
            taskID = int(temp[1])
        except:
            updater.bot.send_message(update.message.chat.id,"Task ID should be a number.")
            return 
        # print(message, date, currId, currGrpId)
        updater.bot.send_message(mongoDB.remove_task(taskID, currId, currGrpId))


# TODO: Link and Message parameters to be considered again.
def addRes(update, context):
    temp = update.message.text.split()
    currUser = update.message.from_user
    currId = currUser.id
    currGrpId = update.message.chat.id

    
    if(len(temp) < 2):
        updater.bot.send_message(update.message.chat.id,"Looks like you forgot to mention the resource details")
    else:
        updater.bot.send_message(mongoDB.update_bibliography("add", link, message, currGrpId))
      

def remRes(update, context):
   temp = update.message.text.split()
   currUser = update.message.from_user
   currId = currUser.id
   currGrpId = update.message.chat.id 
   if(len(temp) < 2):
       updater.bot.send_message(update.message.chat.id,"Looks like you forgot to mention the resource details")
   else:
       updater.bot.send_message(mongoDB.update_bibliography("remove", link, message, currGrpId))
   


def echo(update, context):
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
    dp.add_handler(CommandHandler("help", helpMe))
    dp.add_handler(CommandHandler("register", registerUser))
    dp.add_handler(CommandHandler("tasklist", showTasks))
    dp.add_handler(CommandHandler("taskinfo", taskInfo))
    dp.add_handler(CommandHandler("promote", promoteUser))
    dp.add_handler(CommandHandler("demote", demoteUser))
    dp.add_handler(CommandHandler("remove", removeUser))
    dp.add_handler(CommandHandler("addtask", addTask))
    dp.add_handler(CommandHandler("removetask", removeTask))
    dp.add_handler(CommandHandler("addresource", addRes))
    dp.add_handler(CommandHandler("removeresource", remRes))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    updater.idle()

main()