from organization import Organization
from project import Project
from account import Account, User
from elements import ElementType

class System :
    def __init__(self):
        self.__organizations_list = []
        self.__accounts_list = []
    
    @property
    def organizations_list(self):
        return self.__organizations_list
    
    @property
    def accounts_list(self):
        return self.__accounts_list
    
    @property
    def users_list(self):
        return self.__users__list
    
    def get_account(self, account_id: int):
        if len(self.accounts_list) == 0:
            print("Error: No Account")
            return None
        else :
            for acc in self.accounts_list:
                if acc.account_id == account_id:
                    return acc
            print("Error: Invalid Account ID")
            return None
            
    def get_user(self, user_id: int):
        for org in self.organizations_list:
            for user in org.members:
                if user.id == user_id:
                    return user

    def get_organization(self, organization_id: int) -> Organization:
        for org in self.organizations_list:
            if org.organization_id == organization_id:
                return org

    def get_project(self, project_id: int) -> Project:
        for org in self.organizations_list:
            for project in org.projects:
                if project.project_id == project_id:
                    return project
                
    def search_chat_history(self, id):
        for org in self.organizations_list:
            for chat_history in org.list_of_chat_history:
                if chat_history.thread_id == id:
                    return chat_history

    def locater(self, organization_id: int, project_id: int):
        organization = self.get_organization(organization_id)
        project = self.get_project(project_id)
        return organization, project
    
    def add_organization(self, organization):
        if isinstance(organization, Organization):
            self.organizations_list.append(organization)
        else:
            print("Error: Invalid Type")
    
    def remove_organization(self, organization_id: int):
        organization = self.get_organization(organization_id)
        if organization in self.organizations_list:
            self.organizations_list.pop(organization)

    def add_account(self, account):
        if isinstance(account, Account):
            self.accounts_list.append(account)
        else:
            print("Error: Invalid Type")

    def remove_account(self, account_id: int):
        account = self.get_account(account_id)
        if account in self.accounts_list:
            self.accounts_list.pop(account)
            
    def show_user_name(self, users):
        if isinstance(users, list):
            user_name_list = []
            for u in users:
                user_name_list.append(u.name)
            return " ".join(user_name_list)
        else:
            return users.name
        
    def check_user_access(self, user, access_to):
        if access_to is not None:
            if user in access_to.members:
                return True
            else:
                return False
            
    def get_contacts(self, user, list):
        contacts_without_myself = []
        for someone in list:
            if someone.email != user.email:
                contacts_without_myself.append(someone)
        return contacts_without_myself
    
    def update_todos(self):
        for org in self.__organizations_list:
            org.check_overdue_todos()

    def get_account_by_user_id(self, user_id):
        for acc in self.accounts_list:
            for user in acc.users_list:
                if user.id == user_id:
                    return acc
        print("Error: Invalid User ID")
        return None
    
    def register(self, name, email, organization_name, password):
        if len(self.accounts_list) == 0:
            print("this is first account")
            new_account = Account(name, email, password)
            new_user = User(email, name)
            new_organization = Organization(organization_name, new_user)
            new_account.add_user(new_user)
            self.add_account(new_account)
            self.add_organization(new_organization)
            return new_user.id, new_account.account_id
        else:
            print("this is not first account")
            for acc in self.accounts_list:
                print(acc.email, email)
                if acc.email == email:
                    return False, False
            new_account = Account(name, email, password)
            new_user = User(email, name)
            new_organization = Organization(organization_name, new_user)
            new_account.add_user(new_user)
            self.add_account(new_account)
            self.add_organization(new_organization)
            return new_user.id, new_account.account_id
    
    def register_to_existing_organization(self, image_url, name, organization_id, email,  password):
        # check if account already exists
        for acc in self.accounts_list:
            if acc.email == email:
                print("Error: Account already exists")
                return False, False

        new_account = Account(name, email, password)
        if not image_url == '-':
            new_account.account_avatar = image_url
        new_user = User(email, name)
        new_account.add_user(new_user)
        organization = self.get_organization(organization_id)
        organization.add_member(new_user)
        self.add_account(new_account)
        return new_user.id, new_account.account_id
        
        
    def login(self, email: str, password: str):
        for acc in self.accounts_list:
            if acc.email == email and acc.password == password:
                return acc.account_id
        return False
    
    def login_to_new_organization(self, email: str, password: str, organization_id: str):
        for acc in self.accounts_list:
            if acc.email == email and acc.password == password:
                # login success
                organization = self.get_organization(organization_id)
                user = User(email, acc.name)
                organization.add_member(user)
                acc.add_user(user)
                return acc.account_id
        return False
    
    def get_organization_by_user_id(self, user_id : int):
        for org in self.organizations_list:
            for user in org.members:
                print(user.id, user_id)
                if user.id == user_id:
                    return org
        print("Error: Invalid User ID")
        return None

    def get_organizations(self, account_id: int):
        organizations = []
        for acc in self.accounts_list:
            if acc.account_id == account_id:
                for user in acc.users_list:
                    for org in self.organizations_list:
                        for u in org.members:
                            if u.id == user.id:
                                organizations.append(org)
        return organizations
    
    def get_users_by_account_id(self, account_id: int):
        for acc in self.accounts_list:
            if acc.account_id == account_id:
                return acc.users_list
        print("Error: Invalid Account ID")
        return None
    
    def invite_people_to_organization(self, sender_id: int, invitee_email: str):
        sender = self.get_user(sender_id)
        for acc in self.accounts_list:
            for user in acc.users_list:
                if user.id == sender_id:
                    sender_account = acc
        
        for acc in self.accounts_list:
            if acc.email == invitee_email:
                invitee_account = acc
                invitee = acc.users_list[0]
        
        organization = self.get_organization_by_user_id(sender_id)
        for user in organization.organization_member:
            if user.id == invitee.id:
                return False
    
    def edit_profile(self, user_id, account_id, image_url, name, job_title):
        account = self.get_account(account_id)
        if not image_url == '-':
            account.account_avatar = image_url
        
        
        account.name = name
        user = self.get_user(user_id)
        if not job_title == '-':
            user.job_title = job_title
        else:
            user.job_title = ''
        print("edit profile success")    

    def cancel_organization(self, organization_id):
        organization = self.get_organization(organization_id)
        # get list of users id in organization
        users_id = []
        for user in organization.organization_member:
            users_id.append(user.id)
        
        for acc in self.accounts_list:
            for user in acc.users_list:
                if user.id in users_id:
                    acc.users_list.remove(user)
                    # break
        self.organizations_list.remove(organization)
        # del organization

        print("cancel organization success")

    def check_account(self, account_id):
        for acc in self.accounts_list:
            if acc.account_id == account_id:
                return True
        return False

    def check_organization(self, organization_id):
        for org in self.organizations_list:
            if org.organization_id == organization_id:
                return True
        return False
    
    def process_element_type(self, project, element_type):
        if element_type == 2:
            return project.element_collector.todos
        elif element_type == 3:
            return project.element_collector.todos_topics
        elif element_type == 4:
            return project.element_collector.document_files
        elif element_type == 5:
            return project.element_collector.document_folders
        elif element_type == 6:
            return project.element_collector.message_board
        elif element_type == 7:
            return project.element_collector.events
    
    def find_element_address(self, element, element_type):
        for org in self.__organizations_list:
            for project in org.projects:
                for task in self.process_element_type(project, element_type):
                    if task.id == element.id:
                        return org, project
                    
    def find_chat_address(self, chat_history_id):
        for org in self.__organizations_list:
            for project in org.projects:
                if project.campfire_chat.thread_id == chat_history_id:
                    return project
                else:
                    pass
    
    def gather_everything(self, organization, user):
        pages = []
        for todo in organization.show_user_assignments(user):
            pages.append({"title": "todo", "url": f"/", "content": f"{todo.title}"})
        for event in organization.show_user_events(user):
            pages.append({"title": "event", "url": f"/", "content": f"{event.title}"})
        #เอา elements อื่นๆ มาใส่
        for chat_history in organization.show_user_private_chat(user):
            for chat in chat_history.thread:
                pages.append({"title": "todo", "url": f"/", "content": f"{chat.content}"})
        for project in organization.projects:
            pages.append({"title": "project", "url": f"/{organization.organization_id}/projects/{project.project_id}", "content": f"{project.project_name}"})
            for chat in project.campfire_chat.thread:
                pages.append({"title": "todo", "url": f"/", "content": f"{chat.content}"})
        for member in organization.members:
            pages.append({"title": "todo", "url": f"/", "content": f"{member.name}"})
        return pages
    
    def split_data(self, data, iterator, index):
        receiver_data = data.split(iterator)
        return receiver_data[index]
    
    def get_folder_relative_path(self, parent_id, id, project, folder_path: list):
        # recursive function
        if parent_id == 0:
            return folder_path

        for folder in project.element_collector.get_element_collector(ElementType.FOLDER.value):
            if folder.id == parent_id:
                folder_path.insert(0, folder)
                return self.get_folder_relative_path(folder.parent_id, folder.id, project, folder_path)

    def get_document_child(self, project, current_folder):
        document_child = []
        for document in project.element_collector.get_element_collector(ElementType.FOLDER.value):
            if document.parent_id == current_folder.id:
                document_child.append(document)
        
        for document in project.element_collector.get_element_collector(ElementType.DOCUMENT.value):
            if document.parent_id == current_folder.id:
                document_child.append(document)
        print('document_child')
        print(len(document_child))
                
        return document_child 