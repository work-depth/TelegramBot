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
    pass

def catch(taskID):
    pass

def update_task([ID, attr, message]):
    pass

def task_list(attr):
    pass

def update_bibliography(attr, link):
    pass

def tasks(attr1, attr2):
    pass

def member(attr1, telegramID):
    pass

def admin(attr1, telegramID):
    pass

def reminder(attr1, message):
    pass
    
def notify(message):
    pass
