from backend import *
import pymongo
from pymongo import MongoClient
import uuid
from datetime import datetime

cluster = MongoClient("mongodb+srv://yashwardhan:PY74NORNY5OnUrH6@cluster0.1wicn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["database"]
collection = db["rooms"]
Organisations = {}
taskID=0
# organisation1 = {"_id": 2, "userList": ["Anis", "John", "Yash"], "AdminList": ["Anis", "Yash"]}
# organisation2 = {"_id": 3, "userList": ["Ani", "Joh", "Yas"], "AdminList": ["Ani", "Yas"]}
# collection.insert_many([organisation1, organisation2])
# results = collection.find({"_id": 1})

# for result in results:
#     print(result)
# collection.delete_one({"_id":2})
# collection.delete_one({"_id":3})
# collection.delete_one({"_id":1})
# def getUserID(username, groupID):
#     organisation = collection.find_one({"_id": groupID})
#     for userID in organisation["userList"].keys():
#         if(organisation["userList"][userID].username == username):
#             return userID
#     return "User not registered or the username has been updated"

def register(userID, username, profile, isAdmin, groupID):
    try:
        user = User(userID, username, profile, isAdmin)
        organisation = collection.find_one({"_id": groupID})
        if(collection.count_documents({"_id":groupID})):
            collection.insert_one({"_id": groupID, "userList": {}, "adminList": {}, "tasks": {}, "bibliography": {}, "notifyMessages": {}})
        organisation = collection.find_one({"_id": groupID})
        organisation["userList"].update({userID: user})
        collection.update_one({"_id": groupID}, {"$set": {"userList": organisation["userList"]}})
    except Exception as e:
        print(e)

# user enters task id
def catch(groupID, userID, taskID):
    organisation = collection.find_one({"_id": groupID})
    if(organisation["userList"].has_key(userID)):
        flag=0
        memory_task = organisation["tasks"][0].clone()
        for i in range(0, len(organisation["tasks"][0])):
            if(memory_task[i].ID == taskID):
                memory_task[i].assignedUser = organisation["userList"][userID]
                memory_task[i].status = "assigned"
                updated_taskList = organisation["tasks"][userID].append(memory_task[i]).clone()
                collection.update_one({"_id": groupID}, {"$set": {organisation["tasks"][userID]:updated_taskList, organisation["tasks"][0][i]:memory_task[i]}})                
                flag=1
                break
        if(flag==0):
            return "invalid task"
    else:
        return "You are not registered"

# Return the tasks 
# attr is all 
def task_list(attr, selfID, groupID):
    organisation = collection.find_one({"_id": groupID})
    if(attr=="all"):
        for task in organisation["tasks"][0]:
            print(task.ID, " ", task.message, " ", task.timeOfCreation, " ", task.deadline, " ", task.status, " ", task.assignedUser)

    elif(attr=="personal"):
        for task in organisation["tasks"][selfID]:
            print(task.ID, " ", task.message, " ", task.timeOfCreation, " ", task.deadline, " ", task.status, " ", task.assignedUser)
    else:
        if(organisation["adminList"].has_key(selfID)):
            for task in organisation["tasks"][attr]:
                print(task.ID, " ", task.message, " ", task.timeOfCreation, " ", task.deadline, " ", task.status, " ", task.assignedUser)
        else:
            return "You are not the admin"

# to promte demote admin
def admin(param, selfID, userID, groupID):
    organisation = collection.find_one({"_id": groupID})
    if(organisation["adminList"].has_key(selfID)):            
        if(param=="promote"):
            if(organisation["userList"].has_key(userID)):
                user = organisation["userList"][userID]
                if user.isAdmin==True:
                    return "User is already an Admin"
                else:
                    user.isAdmin = True
                    organisation["adminList"][userID] = user
                    collection.update_one({"_id": groupID}, {"$set": {organisation["adminList"][userID]:user, organisation["userList"][userID]:user}})                
                    return "user has been promoted to Admin"
            else:
                return "No such user is present in this group"
        elif(param=="demote"):
            if(organisation["userList"].has_key(userID)):
                if organisation["adminList"].has_key(userID):
                    user = organisation["userList"][userID]
                    user.isAdmin = True
                    collection.update_one({"_id": groupID}, {"$unset": {organisation["adminList"][userID]}})
                    collection.update_one({"_id": groupID}, {"$set": {organisation["userList"][userID]:user}})  
                    return "User demoted from Admin"
                else:
                    user = organisation["userList"][userID]
                    collection.update_one({"_id": groupID}, {"$unset": {organisation["userList"][userID]}})
                    return "User removed from group"
            else:
                return "No such user is present in this group"
        elif(param=="remove"):
            if(organisation["userList"].has_key(userID)):
                if organisation["adminList"].has_key(userID):
                    collection.update_one({"_id": groupID}, {"$unset": {organisation["adminList"][userID]}})      
                collection.update_one({"_id": groupID}, {"$unset": {organisation["userList"][userID]}})
                return "User removed from group"
            else:
                return "No such user is present in this group"
    else:
        return "You are not an admin"

def update_task(taskID, param, message, userID, groupID):#user can change the status of the task and give updates to the admin
    organisation = collection.find_one({"_id": groupID})
    for task in organisation["tasks"][0]:
        if(task.ID == taskID):
            if(task.status == "active"):
                organisation["tasks"][0].remove(task)
                organisation["tasks"][task.assignedUser.ID].remove(task)
                task.userUpdates = param
                organisation["tasks"][0].append(task)
                organisation["tasks"][task.assignedUser.ID].append(task)
                collection.update_one({"_id": groupID}, {"$set": {organisation["tasks"][0]: organisation["tasks"][0]}})
                collection.update_one({"_id": groupID}, {"$set", {organisation["tasks"][task.assignedUser]: organisation["tasks"][task.assignedUser.ID]}})
                return "Task updated successfully"
            else:
                return "Task is already completed"
    return "Task is isn't created"
  
def add_task(message, deadline, userID, groupID):
    global taskID
    organisation = collection.find_one({"_id": groupID})
    if(organisation["adminList"].has_key(userID)):
        timeOfCreation = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        task = Task(taskID, None, message, timeOfCreation, deadline, "active", "")
        taskID=taskID+1
        organisation
        organisation["tasks"][0].append(task)
        collection.update_one({"_id": groupID}, {"$set": {organisation["tasks"][0]: organisation["tasks"][0]}})
        return "Task added successfully"
    else:
        return "You are not an admin and cannot create a task"

def remove_task(taskID, userID, groupID):
    organisation = collection.find_one({"_id": groupID})
    if(organisation["adminList"].has_key(userID)):
        for task in organisation["tasks"][0]:
            if(task.ID == taskID):
                organisation["tasks"][0].remove(task)
                if(task.assignedUser!=None):
                    organisation["tasks"][task.assignedUser.ID].remove(task)
                    collection.update_one({"_id": groupID}, {"$set": {organisation["tasks"][task.assignedUser.ID]: organisation["tasks"][task.assignedUser.ID]}})
                collection.update_one({"_id": groupID}, {"$set": {organisation["tasks"][0]: organisation["tasks"][0]}})
                return "Task removed successfully"
        return "Task not found"
    else:
        return "You are not an Admin and can't delete a task"

def update_bibliography(param, link, message, groupID):
    organisation = collection.find_one({"_id": groupID})
    
    if(param=="add"):
        organisation["bibliography"][message].append(link)
        collection.update_one({"_id": groupID}, {"$addToSet": {organisation["bibliography"][message]: link}})
    elif(param=="remove"):
        if(message==""):
            for i in organisation["bibliography"]:
                if(organisation["bibliography"][i]==link):
                    collection.update_one({"_id": groupID}, {"$unset": {organisation["bibliography"][i]}})
        else:
            collection.update_one({"_id": groupID}, {"$unset": {organisation["bibliography"][message]}})


def reminder(param, message):
    pass

def notify(message):
    return
# def createRoom(groupID, userList, adminList):
#     try:
#         insertion = {"_id" : groupID}
#         userDict = {}
#         adminDict = {}
#         for user in userList:
#             userDict[user.name] = user
#         for admin in adminList:
#             userDict[admin.name] = admin
#         bibliography = {}
#         notifyMessages = {}
#         insertion["userList"] = userDict
#         insertion["adminList"] = adminDict
#         insertion["bibliography"] = bibliography
#         insertion["notifyMessages"] = notifyMessages
#         collection.insert_one(insertion)
#     except Exception as e:
#         print(e)