


class _connections():

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.userMap = {}


    def addUser(self,username,connection,activeChat=None):
        self.userMap[username] = {
            "connection": connection,
            "activeChat": activeChat

        }

    def removeUser(self,username):
        if username in self.userMap:
            del self.userMap[username]

    def setActiveChat(self, username, chat):
        if username in self.userMap:
            self.userMap[username]["activeChat"] = chat

    def getUserInfo(self, username):
        return self.userMap.get(username, None)



connections = _connections()