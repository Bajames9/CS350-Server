
import threading
import socket



# stores information about a client
class user():

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.user = ""
            self.lock = threading.Lock()

    def update_user(self, username):
        self.user = username

    def get_user(self):
        return self.user
        




