class Notification:
    numberic_id = 0
    def __init__(self, title, timestamp, sender, receivers, link):
        self.__title = title
        self.__id = int("13" + "{:07d}".format(Notification.numberic_id))
        self.__timestamp = timestamp
        self.__sender = sender
        self.__receivers = receivers
        self.__link = link
        self.__markasread = False

        Notification.numberic_id += 1

    @property
    def title(self):
        return self.__title
    
    @property
    def id(self):
        return self.__id
    
    @property
    def timestamp(self):
        return self.__timestamp
    
    @property
    def link(self):
        return self.__link
    
    @property
    def sender(self):
        return self.__sender
    
    @property
    def mark_as_read(self):
        return self.__markasread

    def send_notification(self):
        for receiver in self.__receivers:
            receiver.add_notification(self)

    def update_mark(self):
        if self.__markasread == False:
            self.__markasread = True


class Activity :
    def __init__(self, title, detail, timestamp, about, link):
        self.__title = title
        self.__detail = detail
        self.__about = about
        self.__link = link
        self.__timestamp = timestamp
        self.__accomplished_by = []

    @property
    def title(self):
        return self.__title
    
    @property
    def timestamp(self):
        return self.__timestamp
    
    @property
    def details(self):
        return self.__detail
    
    @property
    def about(self):
        return self.__about

    @property
    def link(self):
        return self.__link

    @property
    def accomplishers(self):
        return self.__accomplished_by
    
    def add_accomplisher(self, users):
        if isinstance(users, list):
            self.accomplishers.extend(users)
        else:
            self.accomplishers.append(users)