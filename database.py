from peewee import *
from uuid import uuid4

db = SqliteDatabase("database.db")

class Chat(Model):
    chat_id = TextField(primary_key=True)
    name = TextField()

    class Meta:
        database = db

class ChatMember(Model):
    chat_id = TextField()
    user_id = TextField()

    class Meta:
        database = db

class User(Model):
    name = TextField()
    id = TextField(primary_key=True)

    class Meta:
        database = db

class Message(Model):
    id = TextField(primary_key=True)
    chat_id = TextField()
    user_from = TextField()
    msg = TextField()

    class Meta:
        database = db

class DataBase:
    def __init__(self):
        self.db = db
        self.db.connect()
        self.db.create_tables([User, Message, ChatMember, Chat])
    
    def addUser(self, name):
        return User.create(
            name=name, 
            id=uuid4()
        )

    def addMessage(self, msg, chat_id, user_from):
        return Message.create(
            user_from=user_from, 
            chat_id=chat_id,
            msg=msg,
            id=uuid4()
        )
    
    def addChat(self, name):
        return Chat.create(
            chat_id=uuid4(),
            name=name
        )

    def addChatMember(self, chat_id, user_id):
        return ChatMember.create(
            user_id=user_id,
            chat_id=chat_id
        )
    
    def getChatName(self, chat_id):
        chat = Chat.get(Chat.chat_id == chat_id)
        return chat.name

    def getMessages(self, chat_id):
        messages = {}
        new_messages = Message.select().where(Message.chat_id == chat_id)

        for message in new_messages:
            messages[message.id] = [message.msg, message.user_from]

        return messages
    
    def getUserId(self, username):
        user = User.get(User.name == username)
        return user.id

    def getUserName(self, user_id):
        user = User.get(User.id == user_id)
        return user.name
    
    def getChats(self, user_id):
        chats = {}
        new_chats = ChatMember.select().where(ChatMember.user_id == user_id)

        for chat in new_chats:
            chats[chat.chat_id] = self.getChatName(chat.chat_id)

        return chats



if __name__ == "__main__":
    test = False
    newdb = DataBase()
    
    if test:
        user1 = newdb.addUser("Luis")
        user2 = newdb.addUser("Nora")

        chat1 = newdb.addChat("Test1")
        chat2 = newdb.addChat("Test2")

        newdb.addChatMember(chat1, user1)
        newdb.addChatMember(chat1, user2)

        newdb.addChatMember(chat2, user2)

        newdb.addMessage("Test :)", chat1, user1)
        newdb.addMessage("Nice Test :)", chat1, user2)
        newdb.addMessage("Yeah :)", chat1, user1)

        print(newdb.getChats(user2))
        print(newdb.getMessages(chat1))