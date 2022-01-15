class User:
    def __init__(self, ID, name, profile, isAdmin) -> None:
        self.ID = ID
        self.name = name
        self.profile = profile
        self.isAdmin = isAdmin

class Task:
    def __init__(self,ID, assignedUser, message, timeOfCreation, deadline, status):
        self.ID = ID
        self.assignedUser = assignedUser
        self.message = message
        self.timeOfCreation = timeOfCreation
        self.deadline = deadline
        self.status = status


def createOrganisation(gcID, Users, Admins, organisation):
    

def catch(taskID):
    

def update_task([ID, attr, “message”]):

def task_list(attr):

def update_bibliography(attr, link):

def tasks(attr1, attr2):

def member(attr1, telegramID):

def admin(attr1, telegramID):

def reminder(attr1, message):
    
def notify(message):
