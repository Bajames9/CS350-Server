from socket import *
from commandManager import commands
from connections import connections
import threading
import json

from user import user


def connectToClient(connectionSocket, addr):
    u = user()
    try:




        print(f"Client connected from {addr}")
        buffer = ""

        while True:
            data = connectionSocket.recv(1024)
            if not data:
                print("Client disconnected.")
                break  # true disconnect

            decoded = data.decode()
            buffer += decoded

            # process all complete messages
            while "\x1e" in buffer:
                message, buffer = buffer.split("\x1e", 1)

                if not message.strip():
                    continue

                try:
                    msg_json = json.loads(message)
                    processCMD(msg_json, connectionSocket, u)
                except json.JSONDecodeError as e:
                    print("JSON parse failed:", e)
                    print("Raw message:", message)

    except Exception as e:
        print("Server error:", e)
    finally:
        print("Closing connection to client.")
        #server = user()
        #server.update_user("Server Msg")
        #commands.chat(connections.getUserInfo(u.get_user())["activeChat"],)
        connections.removeUser(u.get_user())

        connectionSocket.close()


def processCMD(msg, socket, user):
    try:
        print(msg["command"])
        match msg["command"]:

            case "login":
                json_obj = commands.login(msg["username"],user)
                connections.addUser(msg["username"],socket)
                print(json.dumps(json_obj))
                socket.send(f"{json.dumps(json_obj)}\x1e".encode())
            case "getChat":
                json_obj = commands.getChat(msg["name"],user)
                connections.setActiveChat(user.get_user(),msg["name"])
                print(json.dumps(json_obj))
                socket.send(f"{json.dumps(json_obj)}\x1e".encode())
            case "createChat":
                json_obj = commands.createChat(msg["name"],user)
                print(json.dumps(json_obj))
                socket.send(f"{json.dumps(json_obj)}\x1e".encode())
            case "joinChat":
                json_obj = commands.joinChat(msg["name"],user)
                print(json.dumps(json_obj))
                socket.send(f"{json.dumps(json_obj)}\x1e".encode())
            case "chat":
                json_obj = commands.chat(msg["name"],user,msg["msg"])
                if json_obj["type"] == "P":
                    updateChat(msg["name"],user.get_user())
                elif json_obj["type"] == "G":
                    updateChats(msg["name"])
                print(json.dumps(json_obj))
                socket.send(f"{json.dumps(json_obj)}\x1e".encode())
            case "getChatNames":
                json_obj = commands.getAllChatName(user)
                print(json.dumps(json_obj))
                socket.send(f"{json.dumps(json_obj)}\x1e".encode())





    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        print("Raw cmd was:", msg)


def updateChat(recipient, chat):
    json_obj = {
        "command": "update",
        "chat": chat
    }
    con = connections.getUserInfo(recipient)
    if con and con["activeChat"] == chat:
        try:
            con["connection"].send(f"{json.dumps(json_obj)}\x1e".encode())
        except Exception as e:
            print(f"[Disconnected] Removing user '{recipient}': {e}")
            connections.removeUser(recipient)


def updateChats(chatName):
    for username, user_info in connections.userMap.items():
        if user_info["activeChat"] == chatName:
            updateChat(username,chatName)

def server():
    print("Server Start")
    # port and socket for incoming connections
    serverPort = 2317
    serverSocket = socket(AF_INET, SOCK_STREAM)

    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(5)

    while True:
        connectionSocket, addr = serverSocket.accept()
        print("new connection")

        # used to spin up thread for client connection
        client_thread = threading.Thread(
            target=connectToClient,
            args=(connectionSocket, addr),
            daemon=True
        )
        # starts thread
        client_thread.start()


server()