from datetime import datetime
from chat import ChatHistory
from elements import ElementCollector, ElementType, MessageBoard
from account import User

class Project :
    numberic_id = 0

    def __init__(self, chat_history, element_collector, creator, created_at, detail) :
        self.__project_id = int("8" + "{:07d}".format(Project.numberic_id))
        self.__project_name = detail["name"]
        self.__project_description = detail["description"]
        self.__start_date = detail["start_date"]
        self.__end_date = detail["end_date"]
        self.__element_collector = element_collector
        self.__creator = creator
        self.__created_at = created_at
        self.__accessable_users = [creator]
        self.__campfire_chat = chat_history
        self.__is_pined = False
        self.__in_trash = False
        self.__message_board = MessageBoard("Message Board")
        self.__element_collector.add_element(ElementType.FOLDER.value, {"title":"Docs & Files", "parent_id" : 0})
        self.__docs_n_files = self.__element_collector.get_element_collector(ElementType.FOLDER.value)[0]
        Project.numberic_id += 1

        print(f'message board type : {type(self.__message_board)}')

    @property
    def is_pined(self):
        return self.__is_pined
    
    @is_pined.setter
    def is_pined(self, value):
        if isinstance(value, bool):
            self.is_pined = value

    @property
    def project_id(self):
        return self.__project_id

    @property
    def project_name(self):
        return self.__project_name

    @project_name.setter
    def project_name(self, value):
        if isinstance(value, str):
            self.__project_name = value

    @property
    def project_description(self):
        return self.__project_description

    @project_description.setter
    def project_description(self, value):
        if isinstance(value, str):
            self.__project_description = value

    @property
    def creator(self):
        return self.__creator
    
    @property
    def created_at(self):
        return self.__created_at

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, value):
        if isinstance(value, datetime):
            self.__start_date = value

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, value):
        if isinstance(value, datetime):
            self.__end_date = value

    @property
    def members(self):
        return self.__accessable_users

    @members.setter
    def members(self, value):
        if isinstance(value, list):
            self.__accessable_users = value

    @property
    def element_collector(self):
        return self.__element_collector

    @property
    def campfire_chat(self):
        return self.__campfire_chat

    @campfire_chat.setter
    def campfire_chat(self, value):
        if isinstance(value, list):
            self.__campfire_chat = value

    @property
    def in_trash(self):
        return self.__in_trash

    @in_trash.setter
    def in_trash(self, value):
        if isinstance(value, bool):
            self.__in_trash = value

    @property
    def docs_n_files(self):
        return self.__docs_n_files
    
    @property
    def message_board(self):
        return self.__message_board

    def count_member(self):
        return len(self.__accessable_users)
    
    def show_user_events(self, user):
        user_events = []
        collector = self.element_collector
        events_list = collector.get_element_collector(7)
        for event in events_list:
            if user.name in event.assigned_to:
                user_events.append(event)
        return user_events

    def show_user_assignments(self, user):
        user_assignments = []
        collector = self.element_collector
        assignments_list = collector.get_element_collector(2)
        for task in assignments_list:
            if user.name in task.assigned_to:
                user_assignments.append(task)
        return user_assignments

    def check_project_for_access(self, user) :
        if isinstance(user, User):
            if user in self.__accessable_users:
                return True
            else:
                return False
            
    def add_member_to_project(self, user) :
        if user not in self.__accessable_users:
            self.__accessable_users.append(user)

    def remove_member(self, user) :
        if isinstance(user, User):
            self.__accessable_users.remove(user)

    def check_event_for_assigned(self, event, user) :
        pass

    def check_project_for_todo(self, to_do, user) :
        pass
