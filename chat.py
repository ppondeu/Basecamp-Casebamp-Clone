class Chat:
    def __init__ (self, content, timestamp, sender):
        self.__content = content
        self.__timestamp = timestamp
        self.__sender = sender

    @property
    def content(self):
        return self.__content
    
    @content.setter
    def content(self, new_value):
        self.__content = new_value

    @property
    def sender(self):
        return self.__sender
    
    @property
    def timestamp(self):
        return self.__timestamp
    
class ChatHistory:
    numberic_id = 0
    def __init__(self, creator):
        self.__thread_id = int("10" + "{:07d}".format(ChatHistory.numberic_id))
        self.__thread = []
        self.__receivers = [creator]

        ChatHistory.numberic_id += 1

    @property
    def thread_id(self):
        return self.__thread_id
    
    @property
    def thread(self):
        return self.__thread

    @property
    def members(self):
        return self.__receivers

    def add_receivers(self, user):
        if isinstance(user, list):
            self.__receivers.extend(user)
        else:
            self.__receivers.append(user)

    def update_chat_history(self, chat):
        self.__thread.append(chat)
        
    def edit_chat(self, id, attribute, value):
        for chat in self.__thread:
            if chat.id == id:
                chat.set_attribute(attribute, value)