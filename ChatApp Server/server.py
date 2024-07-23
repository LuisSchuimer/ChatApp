from flask import *
from http import HTTPStatus
from server.database import DataBase

app = Flask(__name__)

db = DataBase()

@app.route("/")
def main():
    return "Test", HTTPStatus.OK

@app.route("/login")
def login():
    newUser = db.addUser(request.args.get("username"))
    print(newUser.id)
    return str(newUser.id), HTTPStatus.OK

@app.route("/new/message")
def newMessage():
    db.addMessage(msg=request.args.get("message"), chat_id=request.args.get("chatId"), user_from=request.args.get("userId"))

    return "", HTTPStatus.OK

@app.route("/get/username")
def getUsername():
    print(request.args.get("userId"))
    return db.getUserName(request.args.get("userId")), HTTPStatus.OK

@app.route("/get/userid")
def getUserId():
    return db.getUserId(request.args.get("username")), HTTPStatus.OK

@app.route("/get/messages")
def getMessages():
    return db.getMessages(request.args.get("chatId"))

@app.route("/get/chats")
def getUserChats():
    return db.getChats(request.args.get("userId")), HTTPStatus.OK

@app.route("/new/chat")
def newChat():
    newChat = db.addChat(request.args.get("name"))
    return str(newChat.chat_id), HTTPStatus.OK

@app.route("/new/chatUser")
def newChatUser():
    db.addChatMember(request.args.get("chatId"), request.args.get("userId"))
    return "", HTTPStatus.OK

if __name__ == "__main__":
    app.run("0.0.0.0", 8000, True)