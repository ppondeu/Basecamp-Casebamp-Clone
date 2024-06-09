from project import Project, ChatHistory, ElementCollector
from account import User
from activity import Activity, Notification
from datetime import datetime, timedelta
import calendar

class Organization :
    numberic_id = 0

    def __init__(self, organization_name: str, founder) :
        self.__organization_id = int("9" + "{:07d}".format(Organization.numberic_id))
        self.__organization_name = organization_name
        self.__organization_logo = None
        self.__projects = []
        self.__activity_log = []
        self.__organization_member = [founder] 
        self.__owners = [founder]
        self.__admins = [founder]
        self.__list_of_chat_history = []

        Organization.numberic_id += 1
        
    @property
    def organization_name(self):
        return self.__organization_name
        
    @organization_name.setter
    def organization_name(self, new_organization_name):
        self.__organization_name = new_organization_name
            
    @property
    def organization_id(self):
        return self.__organization_id
    
    @property
    def activity_log(self) :
        return self.__activity_log
    
    @property
    def projects(self) :
        return self.__projects
    
    @property
    def members(self) :
        return self.__organization_member
    
    @property
    def list_of_chat_history(self):
        return self.__list_of_chat_history
    
    @property
    def owners(self):
        return self.__owners
    
    @property
    def admins(self):
        return self.__admins
    
    def show_user_assignments(self, user):
        user_assignments = []
        if self.__projects is not None:
            for proj in self.__projects:
                for todo in proj.element_collector.todos:
                    if user in todo.assigned_to:
                        user_assignments.append(todo)
            return user_assignments
    
    def show_user_activities(self, user):
        user_activities = []
        if self.__activity_log is not None:
            for act in self.activity_log:
                if user in act.accomplishers:
                    user_activities.append(act)
            return user_activities
    
    def show_user_projects(self, user) :
        user_projects = []
        if self.__projects is not None:
            for p in self.projects :
                if p.check_project_for_access(user):
                    user_projects.append(p)
            return user_projects
        
    def show_user_private_chat(self, user):
        user_private_chats = []
        for chat_history in self.__list_of_chat_history:
            if user in chat_history.members:
                user_private_chats.append(chat_history)
        for chat_history in self.__list_of_chat_history:
            for project in self.show_user_projects(user):
                if project.campfire_chat.thread_id == chat_history.thread_id:
                    user_private_chats.remove(chat_history)
        return user_private_chats
        
    def show_user_events(self, user):
        user_events = []
        for p in self.projects :
            for event in p.element_collector.events:
                if user in event.participants:
                    user_events.append(event)
        return user_events
    

    def add_project(self, project: Project) :
        if isinstance(project, Project):
            self.__projects.append(project)
            return {"data" : "A Project is Added!"}
        
    def add_activity(self, activity: Activity) :
        if isinstance(activity, Activity):
            self.__activity_log.append(activity)
            return {"data" : "A Activity is Added!"}
        
    def add_role(self, user, role) :
        if isinstance(user, User):
            if role == "owners":
                self.__owners.append(user)
                if user not in self.__admins:
                    self.__admins.append(user)
            elif role == "administrators":
                self.__admins.append(user)

    def remove_role(self, user, role) :
        if isinstance(user, User):
            if role == "owners":
                self.__owners.remove(user)
            elif role == "administrators":
                self.__admins.remove(user)

    def get_admin_with_owner_permission(self):
        owners_list = []
        for admin in self.__admins:
            if admin in self.__owners:
                owners_list.append(admin)
        return owners_list
                    
    def add_member(self, user) :
        if isinstance(user, list):
            self.__organization_member.extend(user)
        else:
            self.__organization_member.append(user)

    def create_chat_history(self, sender, receiver):
        new_chat_history = ChatHistory(sender)
        new_chat_history.add_receivers(receiver)
        self.add_chat_history(new_chat_history)
        return new_chat_history
            
    def add_chat_history(self, chat_history):
        self.__list_of_chat_history.append(chat_history)

    def gather_receivers(self, sender, receiver):
        if isinstance(receiver, list):
            if not self.check_repeat_receiver(receiver):
                return receiver + [sender]
            else:
                return "Invalid Receivers"
            
    def check_chat_history(self, sender, receiver):
        count = 0
        receivers = self.gather_receivers(sender, receiver)
        for chat_history in self.__list_of_chat_history:
            for rec in chat_history.members:
                for rec_arg in receivers:
                    if rec_arg.email == rec.email:
                        count += 1
            if count == len(receivers):
                return chat_history
            else:
                count = 0
        if count == 0:
            new_chat_history = self.create_chat_history(sender, receiver)
            return new_chat_history
        
    def check_repeat_receiver(self, receivers):
        for index in range(len(receivers)):
            if len(receivers) == 1:
                return False
            elif receivers[index].email == receivers[index + 1].email:
                return True
            else:
                return False
    
    def check_user_role(self, user, role):
        if user in role:
            return True
        else:
            return False
        
    def check_overdue_todos(self):
        overdue_todos = []
        for project in self.__projects:
            for todo in project.element_collector.todos:
                todo.set_overdue()
                if todo.over_due:
                    overdue_todos.append(todo)
        return overdue_todos
    
    def find_events_date(self, find_from, system):
        events_all_year, events_date = {}, {}
        if find_from != []:
            for event in find_from:
                events_date_focus_month_list, events_date_next_month_list =[], []
                time_delta = self.find_between_dates(event.start_date, event.end_date)
                start_date = system.split_data(event.start_date, "T", 0)
                key, year = int(system.split_data(start_date, "-", 1)), system.split_data(start_date, "-", 0)
                events_date_focus_month, events_date_next_month = self.check_timedelta_skip_month(time_delta)
                focus_month, next_month = calendar.month_name[key], calendar.month_name[key + 1]
                events_date_focus_month_list.extend(events_date_focus_month)
                events_date_next_month_list.extend(events_date_next_month)
                events_date[f"{focus_month}"] = events_date_focus_month_list
                events_date[f"{next_month}"] = events_date_next_month_list
                events_all_year[f"{year}"] = events_date
            return events_all_year
        else:
            return {}

    def find_between_dates(self, start_date, end_date):
        between_dates = []
        start_datetime = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
        time_delta = end_datetime - start_datetime
        for i in range(0, time_delta.days + 1):
            day = start_datetime + timedelta(days=i)
            between_dates.append(int(day.strftime("%d")))
        return between_dates
    
    def check_timedelta_skip_month(self, between_dates):
        status = ""
        focus_month_dates, next_month_dates = [], []
        for i in range(len(between_dates)):
            if between_dates[i] < between_dates[i - 1] and i != 0:
                status = "next"
            if status == "next":
                next_month_dates.append(between_dates[i])
            elif status == "":
                focus_month_dates.append(between_dates[i])
        return focus_month_dates, next_month_dates
    
    def check_events_date_overlap(self, events_date_list):
        dates = []
        for i in range(len(events_date_list)):
            if events_date_list[i] < events_date_list[i - 1] and i != 0:
                start_overlap_index = i
        for j in range(start_overlap_index):
            dates.append(events_date_list[j])
        return dates

    def find_todos_topic(self, topic_id):
        for proj in self.__projects:
            for topic in proj.element_collector.todos_topics:
                if topic.id == topic_id:
                    return topic