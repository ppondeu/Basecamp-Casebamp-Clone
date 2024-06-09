from chat import ChatHistory
from datetime import datetime
from activity import Notification

class User:
    numberic_id = 0
    def __init__(self, email, name):
        self.__id = int("12" + "{:07d}".format(User.numberic_id))
        self.__email = email
        self.__name  = name
        self.__job_title = ""
        self.__list_of_notification = []
        User.numberic_id += 1

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def job_title(self):
        return self.__job_title
    
    @job_title.setter
    def job_title(self, new_job_title):
        self.__job_title = new_job_title

    @property
    def email(self):
        return self.__email

    @property
    def notifications(self):
        return self.__list_of_notification
    
    def edit_profile(self, new_name, new_phone):
        if new_name != "" and new_phone != "":
            self.__name = new_name
            self.__phone = new_phone
        elif new_name != "" and new_phone == "":
            self.__name = new_name
        elif new_phone != "" and new_name == "":
            self.__phone = new_phone
        return "Edit profile success"
        
    def check_user_for_chat_history(self, user, chat_history):
        if isinstance(user, User) and isinstance(chat_history, ChatHistory):
            if user in chat_history.members:
                return True
            else:
                return False
            
    def add_notification(self, notification):
        if isinstance(notification, Notification):
            self.__list_of_notification.append(notification)

            
    def get_notification(self, noti_id):
        for noti in self.__list_of_notification :
            if noti.id == noti_id:
                return noti
            
    def get_notifications(self):
        unreads = []
        reads = []
        for noti in self.__list_of_notification :
            if noti.mark_as_read:
                reads.append(noti)
            elif not noti.mark_as_read:
                unreads.append(noti)
        return reads, unreads

class Account:
    numeric_id = 0

    def __init__(self, name, email, password):
        self.__account_id = int("11" + "{:07d}".format(Account.numeric_id))
        self.__name = name
        self.__email = email
        self.__password = password
        self.__users_list = []
        self.__account_avatar = "https://i.ibb.co/KW3xr1m/avatar.gif"
        Account.numeric_id += 1

    @property
    def account_avatar(self):
        return self.__account_avatar
    @account_avatar.setter
    def account_avatar(self, new_avatar):
        self.__account_avatar = new_avatar
    @property
    def account_id(self):
        return self.__account_id
    
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, new_name):
        self.__name = new_name
    @property
    def users_list(self):
        return self.__users_list
    @property
    def email(self):
        return self.__email 
    @property
    def password(self):
        return self.__password
    @password.setter
    def password(self, new_password):
        self.__password = new_password

    def add_user(self, user):
        if(isinstance(user, User)):
            self.__users_list.append(user)
        else:
            print("Invalid user")

    def edit_identity(self, details:dict):
        if "name" in details:
            self.__name = details["name"]
        if "account_avatar" in details:
            self.__account_avatar = details["account_avatar"]