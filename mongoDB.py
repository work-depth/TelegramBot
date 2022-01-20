from backend import *
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://yashwardhan:PY74NORNY5OnUrH6@cluster0.1wicn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["database"]
collection = db["rooms"]
Organisations = {}

# organisation1 = {"_id": 2, "userList": ["Anis", "John", "Yash"], "AdminList": ["Anis", "Yash"]}
# organisation2 = {"_id": 3, "userList": ["Ani", "Joh", "Yas"], "AdminList": ["Ani", "Yas"]}
# collection.insert_many([organisation1, organisation2])
results = collection.find({"_id": 1})
if(len(list(results.clone())) == 0):
    print("no element")

for result in results:
    print(result)
collection.delete_one({"_id":2})
collection.delete_one({"_id":3})
collection.delete_one({"_id":1})

def addUser(userID, name, profile, isAdmin, groupID):
    try:
        user = User(userID, name, profile, isAdmin)
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
            print("invalid task")
    else:
        print("You are not registered")

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
            print("You are not the admin")
            return "You are not the admin"

# to promte demote admin
def admin(param, selfID, userID, groupID):
    organisation = collection.find_one({"_id": groupID})
    if(organisation["adminList"].has_key(selfID)):            
        if(param=="promote"):
            if(organisation["userList"].has_key(userID)):
                user = organisation["userList"][userID]
                if user.isAdmin==True:
                    print("User is already an Admin")
                else:
                    user.isAdmin = True
                    organisation["adminList"][userID] = user
                    collection.update_one({"_id": groupID}, {"$set": {organisation["adminList"][userID]:user, organisation["userList"][userID]:user}})                
            else:
                print("No such user is present in this group")
        elif(param=="demote"):
            if(organisation["userList"].has_key(userID)):
                if organisation["adminList"].has_key(userID):
                    user = organisation["userList"][userID]
                    collection.update_one({"_id": groupID}, {"$unset": {organisation["adminList"][userID]}})                
                    collection.update_one({"_id": groupID}, {"$set": {organisation["userList"][userID]:user}})  
                    print("User is already an Admin")
                else:
                    user = organisation["userList"][userID]
                    collection.update_one({"_id": groupID}, {"$unset": {organisation["userList"][userID]}})
            else:
                print("No such user is present in this group")
        elif(param=="remove"):
            if(organisation["userList"].has_key(userID)):
                if organisation["adminList"].has_key(userID):
                    collection.update_one({"_id": groupID}, {"$unset": {organisation["adminList"][userID]}})      
                collection.update_one({"_id": groupID}, {"$unset": {organisation["userList"][userID]}})
            else:
                print("No such user is present in this group")
    else:
        print("you are not an admin")

def update_task(taskID, param, message, userID, groupID):
    organisation = collection.find_one({"_id": groupID})
    if(organisation["adminList"].has_key(userID)):
        found=0
        for task in organisation["tasks"][0]:
            if(task.ID == taskID):
                if(param=="complete"):
                    task.assignedUser             
                    collection.update_one({"_id": groupID}, {"$unset": {organisation["tasks"][taskID]}})
                    organisation["tasks"][task.assignedUser].remove(task)
                    collection.update_one({"_id": groupID}, {"$set", {organisation["tasks"][task.assignedUser]: organisation["tasks"][task.assignedUser]}})
                elif(param=="update"):
                    pass
                found=1
                break
        if(found==0):
            print("task is already completed or isn't created")
    else:
        print("You are not an admin. So you can't update the task")
    

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