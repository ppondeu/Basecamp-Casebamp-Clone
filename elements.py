from datetime import datetime
from enum import Enum
from account import User
from activity import Notification

class ElementType(Enum):
    MESSAGEBOARD = 1
    TODO = 2
    TODOSTOPIC = 3
    DOCUMENT = 4
    FOLDER = 5
    MESSAGE = 6
    EVENT = 7

    #Exception
    ACCOUNT = 11
    USER = 12
    PROJECT = 8
    ORGANIZATION = 9
    CHATHISTORY = 10
    NOTIFICATION = 13

def collector_process(element_type: int, create_element: bool, element_detail: dict = None):
    if element_type == ElementType.TODOSTOPIC.value:
        return_value = ["todos_topics"]
        if create_element:
            return_value.append(ToDosTopic(element_detail))
        return return_value

    elif element_type == ElementType.TODO.value:
        return_value = ["todos"]
        if create_element:
            return_value.append(ToDo(element_detail))
        
        return return_value

    elif element_type == ElementType.EVENT.value:
        return_value = ["events"]
        if create_element:
            return_value.append(Event(element_detail))
        return return_value

    elif element_type == ElementType.FOLDER.value:
        return_value = ["document_folders"]
        if create_element:
            return_value.append(DocumentsAndFilesFolder(element_detail))
        return return_value

    elif element_type == ElementType.DOCUMENT.value:
        return_value = ["document_files"]
        if create_element:
            return_value.append(DocumentOrFile(element_detail))
        return return_value

    elif element_type == ElementType.MESSAGE.value:
        return_value = ["message_board"]
        if create_element:
            return_value.append(Message(element_detail))
        return return_value

class ElementCollector:
    def __init__(self):
        self.__todos_topics = []
        self.__todos = []
        self.__events = []
        self.__document_folders = []
        self.__document_files = []
        self.__message_board = []
    
    @property
    def todos_topics(self):
        return self.__todos_topics
    @property
    def todos(self):
        return self.__todos
    @property
    def events(self):
        return self.__events
    @property
    def document_folders(self):
        return self.__document_folders
    @property
    def document_files(self):
        return self.__document_files
    @property
    def message_board(self):
        return self.__message_board
    
    def add_element(self, element_type: int, element_detail: dict):
        return_value = collector_process(element_type, True, element_detail)
        element_attribute = return_value[0]
        sub_element = return_value[1]
        getattr(self, element_attribute).append(sub_element)
        
    def get_element_collector(self, element_type: int):
        element_attribute = collector_process(element_type, False)[0]
        element_list = getattr(self, element_attribute)
        return element_list

    def get_element(self, element_type: int, element_id: int):
        element_list = self.get_element_collector(element_type)
        for element in element_list:
            if element.id == int(element_id):
                return element

    def edit_element(self, element_type: int, element_id: int, attribute: str, value):
        element = self.get_element(element_type, element_id)
        element.set_attribute(attribute, value)

class Element:
    def __init__(self, title, id):
        self.__title = title
        self.__id = int(id)
        self.__in_trash = False
    @property
    def title(self):
        return self.__title
    @title.setter
    def title(self, value):
        print("set title")
        self.__title = value
    @property
    def id(self):
        return self.__id

    @property
    def in_trash(self):
        return self.__in_trash
    @in_trash.setter
    def in_trash(self, value):
        self.__in_trash = value

    def set_attribute(self, attribute, value):
        setattr(self, attribute, value)

    def convert_date_to_datetime(self, date):
        if date != "":
            return datetime.strptime(date, "%Y-%m-%d")

class ToDo(Element):
    numberic_id = 0
    
    def __init__(self, detail):
        super().__init__(detail["title"], id = str(ElementType.TODO.value) + "{:07d}".format(ToDo.numberic_id))
        self.__collector_id = int(detail["todos_topic_id"])
        self.__content = detail["content"]
        self.__start_date = detail["start_date"]
        self.__end_date = detail["end_date"]
        self.__completed = False
        self.__over_due = False
        self.__added_by = detail["added_by"]
        self.__assigned_to = []
        self.__notify_who_when_done = detail["notify_who_when_done"]
        ToDo.numberic_id += 1

    @property
    def collector_id(self):
        return self.__collector_id

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        if isinstance(value, str):
            self.__content = value

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
    def completed(self):
        return self.__completed

    @completed.setter
    def completed(self, value):
        if isinstance(value, bool):
            self.__completed = value

    @property
    def over_due(self):
        return self.__over_due

    @over_due.setter
    def over_due(self, value):
        if isinstance(value, bool):
            self.__over_due = value

    @property
    def added_by(self):
        return self.__added_by

    @added_by.setter
    def added_by(self, value):
        if isinstance(value): #user
            self.__added_by = value

    @property
    def assigned_to(self):
        return self.__assigned_to

    @assigned_to.setter
    def assigned_to(self, value):
        if isinstance(value): #user
            self.__assigned_to = value

    @property
    def notify_who_when_done(self):
        return self.__notify_who_when_done

    @notify_who_when_done.setter
    def notify_who_when_done(self, value):
        if isinstance(value): #user
            self.__notify_who_when_done = value

    def count_overdue(self):
        end_date = self.convert_date_to_datetime(self.__end_date)
        if end_date is not None:
            overdue_day = datetime.now() - end_date
            return overdue_day.days
    
    def set_overdue(self):
        overdue_day = self.count_overdue()
        if overdue_day is not None and overdue_day > 0:
            self.over_due = True

    def add_assignee(self, assignee):
        if isinstance(assignee, list):
            self.__assigned_to.extend(assignee)
        else:
            self.__assigned_to.append(assignee)
            
class ToDosTopic(Element):
    numberic_id = 0
    #**kwargs

    def __init__(self, detail):
        super().__init__(detail["title"], id = str(ElementType.TODOSTOPIC.value) + "{:07d}".format(ToDosTopic.numberic_id))
        self.__description = detail["description"]
        self.__list_of_to_dos = []
        ToDosTopic.numberic_id += 1

        print("Created {}".format(self.title))

    @property
    def description(self):
        return self.__description
    @description.setter
    def description(self, value):
        self.__description = value

    def add_to_do(self, to_do):
        if to_do not in self.__list_of_to_dos:
            self.__list_of_to_dos.append(to_do)
    
    def edit_to_do(self, to_do, attribute, value):
        to_do.set_attribute(attribute, value)

    def get_todos(self, todos):
        respond_todos = []
        for todo in todos:
            if self.id == todo.collector_id:
                respond_todos.append(todo)
        return respond_todos
    
class DocumentOrFile(Element):
    numberic_id = 0
    
    def __init__(self, details: dict):
        super().__init__(details['title'], id = int(str(ElementType.DOCUMENT.value) + "{:07d}".format(DocumentOrFile.numberic_id)))
        self.__content = details['content']
        self.__file_content = details['file_content']
        self.__added_by = details['added_by']
        self.__timestamp = details['timestamp']
        self.__parent_id = details['parent_id']
        print(self.__file_content)
        DocumentOrFile.numberic_id += 1
        
    @property
    def content(self):
        return self.__content
    @content.setter
    def content(self, value):
        self.__content = value

    @property
    def file_content(self):
        return self.__file_content
    
    @file_content.setter
    def file_content(self, value):
        self.__file_content = value
    
    @property
    def parent_id(self):
        return self.__parent_id
    
    @property
    def timestamp(self):
        return self.__timestamp
    
    @timestamp.setter
    def timestamp(self, value):
        self.__timestamp = value

    @property
    def added_by(self):
        return self.__added_by
    


    
class DocumentsAndFilesFolder(Element):
    numberic_id = 0
    
    def __init__(self, details:dict):
        super().__init__(details["title"], id = int(str(ElementType.FOLDER.value) + "{:07d}".format(DocumentsAndFilesFolder.numberic_id)))
        self.__parent_id = details['parent_id']
        print(f'parent_id: {self.__parent_id}')
        DocumentsAndFilesFolder.numberic_id += 1

    @property
    def parent_id(self):
        return self.__parent_id
    @parent_id.setter
    def parent_id(self, value):
        self.__parent_id = value
    
    

#Nitcharat


class Message(Element):
    numberic_id = 0
    def __init__(self, details:dict):
        super().__init__(details["title"], id = int(f'{ElementType.MESSAGE.value}' + "{:07d}".format(Message.numberic_id)))
        self.__content = details["content"]
        self.__file_content = details["file_content"]
        self.__timestamp = details["timestamp"]
        self.__sender = details["sender"]
        Message.numberic_id += 1

    @property
    def content(self):
        return self.__content
    @content.setter
    def content(self, value):
        self.__content = value
    @property
    def file_content(self):
        return self.__file_content
    @file_content.setter
    def file_content(self, value):
        self.__file_content = value
    @property
    def timestamp(self):
        return self.__timestamp
    
    @property
    def sender(self):
        return self.__sender
    

class MessageBoard:
    numberic_id = 0
    def __init__(self, title):
        self.__title = title
        self.__id = int(f'{ElementType.MESSAGEBOARD.value}' + "{:07d}".format(MessageBoard.numberic_id))
    
        MessageBoard.numberic_id += 1

    @property
    def title(self):
        return self.__title
    @title.setter
    def title(self, value):
        self.__title = value
    @property
    def id(self):
        return self.__id
    

    @property
    def id(self):
        return self.__id
    @property
    def title(self):
        return self.__title
    
class Event(Element):
    numberic_id = 0
    def __init__(self, detail):
        super().__init__(detail["title"], id = int(str(ElementType.EVENT.value) + "{:07d}".format(Event.numberic_id)))
        self.__content = detail["content"]
        self.__added_by = detail["added_by"]
        self.__start_date = detail["start_date"]
        self.__end_date = detail["end_date"]
        self.__participants = [detail["added_by"]]
        self.__notify_who_when_done = detail["notify_who_when_done"]
        Event.numberic_id += 1

    @property
    def content(self):
        return self.__content

    @property
    def start_date(self):
        return self.__start_date
    
    @property
    def end_date(self):
        return self.__end_date
    
    @property
    def added_by(self):
        return self.__added_by

    @property
    def participants(self):
        return self.__participants
    
    @property
    def notify_who_when_done(self):
        return self.__notify_who_when_done
    
    def add_participant(self, participant):
        if isinstance(participant, list):
            self.__participants.extend(participant)
        else:
            self.__participants.append(participant)