class User:
    def __init__(self, ID, username, profile, isAdmin) -> None:
        self.ID = ID
        self.username = username
        self.profile = profile
        self.isAdmin = isAdmin
    def __init__(self, document) -> None:
        self.ID = document["ID"]
        self.username = document["username"]
        self.profile = document["profile"]
        self.isAdmin = document["isAdmin"]
    def toString(self):
        return {"ID": self.ID, "username": self.username, "profile":self.profile, "isAdmin": self.isAdmin}

class Task:
    def __init__(self,ID, assignedUser, message, timeOfCreation, deadline, status, userUpdates):
        self.ID = ID
        self.assignedUser = assignedUser
        self.message = message
        self.timeOfCreation = timeOfCreation
        self.deadline = deadline
        self.status = status
        self.userUpdates = userUpdates