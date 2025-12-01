from databaseManager import database
import json



# layer between server code and database to run commands and generate responses
class _commands():

    def login(self, username, user):
        try:
            isUser = database.getUser(username)
            user.update_user(username)
            if isUser:
                json_obj = {
                    "command": "login",
                    "user": username,
                    "msg": "Logged in",
                    "status": True
                }
            else:
                database.addUser(username)
                user.update_user(username)
                json_obj = {
                    "command": "login",
                    "user": username,
                    "msg": "Account Created",
                    "status": True
                }
            return json_obj
        except Exception as e:
            json_obj = {
                    "command": "login",
                    "user": username,
                    "msg": f"Login Fail Error:{e}",
                    "status": False
                }
            return json_obj

    def getChat(self,name,user):
        return  database.getChatsForNameAndUser(name,user)

    def createChat(self,name,user):
        if not database.getUser(name) and not database.isGroupChat(name):
            database.createGroupChat(name,user.get_user())
            json_obj = {
                "command": "createChat",
                "success": True,
                "msg": "group Chat created"
            }
        else:
            json_obj = {
                "command": "createChat",
                "success": False,
                "msg": "group Chat not created"
            }

        return json_obj

    def joinChat(self,name,user):
        if database.isGroupChat(name):
            added = database.addUserToGroup(name,user.get_user())
            if added:
                json_obj = {
                    "command": "joinChat",
                    "success": True,
                    "msg": "group chat joined"
                }
            else:
                # user was already in the group
                json_obj = {
                    "command": "joinChat",
                    "success": False,
                    "msg": "user already in group"
                }
        else:
            json_obj = {
                "command": "joinChat",
                "success": False,
                "msg": "group chat not joined"
            }

        return json_obj

    def getAllChatName(self,user):
        chats = database.getAllChatNames(user.get_user())
        json_obj = {
            "command": "getChatNames",
            "success": True,
            "chats" : chats
        }
        return json_obj

    def chat(self,to,user,msg):
        if database.getUser(to):
            database.addMsg(user.get_user(),to,msg,"P")
            json_obj = {
                "command": "chat",
                "success": True,
                "type": "P",
                "msg": "msg added to private chat"
            }

        elif database.isGroupChat(to):
            database.addMsg(user.get_user(), to, msg, "G")
            json_obj = {
                "command": "chat",
                "success": True,
                "type": "G",
                "msg": "msg added to Group chat"
            }
        else:
            json_obj = {
                "command": "chat",
                "success": False,
                "type": None,
                "msg": f"No user or group chat by the name {to}"
            }
        return json_obj

commands = _commands()