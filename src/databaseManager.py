from tinydb import TinyDB, Query
import threading

class _databaseManager():


    def __init__(self):
        self.users = TinyDB('src/users.json')
        self.msgs = TinyDB('src/msg.json')
        self.groupChats = TinyDB('src/groupChats.json')
        self.lock = threading.RLock()
    

    def addUser(self, username):

        with self.lock:
            existing = self.getUser(username)

            if existing:
                return False
    
            self.users.insert({'username': username})
            return True

    def getUser(self, username):

        with self.lock:
            User = Query()
            existing = self.users.search(User.username == username)
            return bool(existing)
            
    def addMsg(self, sender, receiver, msg, chatType):
        with self.lock:
            self.msgs.insert({"sender": sender, "receiver":receiver, "msg":msg, "chatType":chatType})

    def getChatsForNameAndUser(self,name,user):
        with self.lock:
            json_obj = {
                "command": "getChat",
                "success": False,
                "data": []
            }

            if database.getUser(name):
                msgs = self.msgs.search(
                    ((Query().sender == name) & (Query().receiver == user.get_user())) |
                    ((Query().sender == user.get_user()) & (Query().receiver == name))
                )

            elif database.isGroupChat(name):
                msgs = self.msgs.search(
                    (Query().receiver == name)
                )

            else:
                return  json_obj

            json_obj["success"] = True
            json_obj["data"] = [{"msg": m["msg"], "sender": m["sender"]} for m in msgs]

            return json_obj

    def getAllChatNames(self,username):
        names = set()  # use a set to avoid duplicates
        Q = Query()

        # ---- Private Chats ----
        # Find all messages sent BY the user
        sent = self.msgs.search(Q.sender == username)
        for msg in sent:
            names.add(msg["receiver"])

        # Find all messages received BY the user
        received = self.msgs.search(Q.receiver == username)
        for msg in received:
            names.add(msg["sender"])

        # Remove the username itself if somehow present
        if username in names:
            names.remove(username)

        # ---- Group Chats ----
        # Find all groups where user is a member
        groups = self.groupChats.search(Q.users.any([username]))
        for g in groups:
            names.add(g["chatName"])

        return list(names)


    def createGroupChat(self,chatName,username):
        with self.lock:
            self.groupChats.insert({"chatName": chatName,"users": [username]})

    def isGroupChat(self, chatName):
        with self.lock:
            group = Query()
            existing = self.groupChats.search(group.chatName == chatName)
            return bool(existing)

    def addUserToGroup(self, chatName, username):
        with self.lock:
            group = Query()
            chat = self.groupChats.get(group.chatName == chatName)
            if chat and username not in chat["users"]:
                chat["users"].append(username)
                self.groupChats.update({"users": chat["users"]}, group.chatName == chatName)
                return True
            return False

    def removeUserFromGroup(self, chatName, username):
        with self.lock:
            group = Query()
            chat = self.groupChats.get(group.chatName == chatName)
            if chat and username in chat["users"]:
                chat["users"].remove(username)
                self.groupChats.update({"users": chat["users"]}, group.chatName == chatName)
                return True
            return False



database = _databaseManager()