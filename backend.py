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