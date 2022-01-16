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
                collection.update_one({"_id": groupID}, {"$set": {organisation["tasks"][userID]:updated_taskList}})                
                collection.update_one({"_id": groupID}, {"$set": {organisation["tasks"][0][i]:memory_task[i]}})                
                flag=1
                break
        if(flag==0):
            print("invalid task")
    else:
        print("You are not registered")

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

def admin(attr1, selfID, userID, groupID):
    organisation = collection.find_one({"_id": groupID})
    if(organisation["adminList"].has_key(selfID)):            
        if(attr1=="promote"):
            
            
        else if("demote"):

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