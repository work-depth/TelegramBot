from backend import *
import pymongo
from pymongo import Mongoclient

cluster = Mongoclient("mongodb+srv://yashwardhan:PY74NORNY5OnUrH6@cluster0.1wicn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["database"]
collection = db["rooms"]
Organisations = {}

def createUser(userID, name, profile, isAdmin):
    user = User(userID, name, profile, isAdmin)
    organisation = 

def createRoom(groupID, userList, adminList):
    try:
        insertion = {"_id" : groupID}
        userDict = {}
        adminDict = {}
        for user in userList:
            userDict[user.name] = user
        for admin in adminList:
            userDict[admin.name] = admin
        bibliography = {}
        notifyMessages = {}
        insertion["userList"] = userDict
        insertion["adminList"] = adminDict
        insertion["bibliography"] = bibliography
        insertion["notifyMessages"] = notifyMessages
        collection.insert_one(insertion)
    except Exception as e:
        print(e)