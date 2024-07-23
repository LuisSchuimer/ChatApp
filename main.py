from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import requests
import ast
import threading
from time import sleep

class ChatApp(QMainWindow):
    def __init__(self):
        self.server = "192.168.178.81"
        self.user = ""
        self.chats = []
        self.messages = []
        self.current_chat = ""
        super(ChatApp, self).__init__()
        loadUi("ui.ui", self)
        self.login_btn.clicked.connect(lambda: self.login(self.name_input.text()))
        self.chat_make_btn.clicked.connect(lambda: self.newChat(self.with_input.text(), self.chat_name_input.text()))
        self.chat_list.itemClicked.connect(self.select_chat)
        self.send_btn.clicked.connect(lambda: self.sendMessage(self.msg_input.text()))
        self.show()
    
    def login(self, name):
        res = requests.get(f"http://{self.server}:8000/login?username={name}")
        self.user = str(res.content.decode())

        self.name_input.setText(name)
        self.name_input.setEnabled(False)
        self.login_btn.setEnabled(False)
        self.chat_list.setEnabled(True)
        
        getchats = threading.Thread(target=self.getChats)
        getchats.daemon = True
        getchats.start()

        updateMessages = threading.Thread(target=self.updateMessages)
        updateMessages.daemon = True
        updateMessages.start()

    def sendMessage(self, msg):
        requests.get(f"http://{self.server}:8000/new/message?message={msg}&chatId={self.current_chat}&userId={self.user}")


    def select_chat(self, item):
        self.msg_list.clear()
        _, chat_id = item.text().split(" ")
        self.current_chat = chat_id

        res = requests.get(f"http://{self.server}:8000/get/messages?chatId={chat_id}")
        messages = ast.literal_eval(res.content.decode())

        self.msg_input.setEnabled(True)
        self.send_btn.setEnabled(True)
        self.msg_list.setEnabled(True)
        
        for message in messages.keys():
            res = requests.get(f"http://{self.server}:8000/get/username?userId={messages[message][1]}")
            self.msg_list.addItem(QListWidgetItem(f"{res.content.decode()}: {messages[message][0]}"))
            if message not in self.messages:
                self.messages.append(message)
            else: continue


    def updateMessages(self):
        while True:
            try:
                for chat_id in self.chats:
                    res = requests.get(f"http://{self.server}:8000/get/messages?chatId={chat_id}")
                    messages = ast.literal_eval(res.content.decode())

                    for message in messages.keys():
                        if not message in self.messages:
                            res = requests.get(f"http://{self.server}:8000/get/username?userId={messages[message][1]}")
                            if self.current_chat == chat_id:
                                self.msg_list.addItem(QListWidgetItem(f"{res.content.decode()}: {messages[message][0]}"))
                                self.messages.append(message)
                        else: continue
            
                sleep(.5)
            except: continue

        

    def getUsername(self, user_id):
        res = requests.get(f"http://{self.server}:8000/get/username?userId={user_id}")
        return str(res.content.decode())
    
    def newChat(self, user, name):
        res = requests.get(f"http://{self.server}:8000/get/userid?username={user}")
        user_id = str(res.content.decode())

        res = requests.get(f"http://{self.server}:8000/new/chat?name={name}")
        chat_id = str(res.content.decode())

        if res.status_code == 200:
            res = requests.get(f"http://{self.server}:8000/new/chatUser?chatId={chat_id}&userId={user_id}")
            res = requests.get(f"http://{self.server}:8000/new/chatUser?chatId={chat_id}&userId={self.user}")

    def getChats(self):
        while True:
            try:
                res = requests.get(f"http://{self.server}:8000/get/chats?userId={self.user}")
                chats = ast.literal_eval(res.content.decode())

                for chat in chats.keys():
                    if chat not in self.chats:
                        self.chat_list.addItem(QListWidgetItem(f"{chats[chat]} {chat}"))
                        self.chats.append(chat)

                sleep(.5)
                
            except: continue

def main():
    app = QApplication([])
    window = ChatApp()
    app.exec_()

if __name__ == "__main__":
    main()