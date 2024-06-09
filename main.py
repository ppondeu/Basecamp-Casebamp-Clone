#สร้าง Activity : เพิ่ม Event Todo Message, สร้าง Project, แก้ไขสิทธิ์เข้าถึง Project ของ User, มี User เข้าร่วม Project
#สร้าง Noti : ถูก assign todo, todo เรา overdue completed, campfire

import os, json
from datetime import datetime, timedelta, date
from fastapi import FastAPI, Request, Response, Cookie, BackgroundTasks, Form, UploadFile, File, status, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Union, List
from starlette.exceptions import HTTPException as StarletteHTTPException
from system import System, Organization
from elements import Element, ElementCollector, ElementType, ToDo, Event
from account import Account, User
from chat import ChatHistory, Chat
from project import Project
from activity import Activity, Notification

element_type_mapper = {
    "todos_topics": ElementType.TODOSTOPIC,
    "todos": ElementType.TODO,
    "todos_topics": ElementType.TODOSTOPIC,
    "document_files": ElementType.DOCUMENT,
    "document_folder": ElementType.FOLDER,
    "message": ElementType.MESSAGE,
    "events": ElementType.EVENT
 }

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/imgs", StaticFiles(directory="imgs"), name='imgs')

templates = Jinja2Templates(directory="templates")

system = System()


# TEST HARD CODE
acc1 = Account("tuatang", "tuatang@gmail.com", "a")
print(acc1.account_id)
acc2 = Account("pond", "pondzai@gmail.com", "a")
tuatang1 = User("tuatang@gmail.com", "tuatang")
tuatang2 = User("tuatang@gmail.com", "tuatang")
pond1 = User("pondzai@gmail.com", "pond")
pond2 = User("pondzai@gmail.com", "pond")
pun = User("punza@gmail.com", "pun")
march = User("marchkung@gmail.com", "march")
acc1.add_user(tuatang1)
acc1.add_user(tuatang2)
acc2.add_user(pond1)
acc2.add_user(pond2)
system.add_account(acc1)
system.add_account(acc2)

detail2 = {
    "title" : "China",
    "todos_topic_id": "30000000",
    "content" : "Eastern Overpower",
    "start_date" : "2023-03-23",
    "end_date" : "2023-06-23",
    "added_by" : pond1,
    "notify_who_when_done": "tuatang"
}

detail3 = {
    "title" : "USA",
    "todos_topic_id": "30000000",
    "content" : "Western Overpower",
    "start_date" : "2023-03-23",
    "end_date" : "2023-03-23",
    "added_by" : tuatang1,
    "notify_who_when_done": "tuatang"
}

project_detail1 = {
    "name" : "Project1",
    "description" : "Test",
    "start_date" : "2023-04-23",
    "end_date" : "2023-06-23"
}

project_detail2 = {
    "name" : "CE61",
    "description" : "Computer Engineering",
    "start_date" : "2023-04-23",
    "end_date" : "2023-04-30"
}

detail4 = {
    "title" : "topic1",
    "description" : "test topic"
}

event_detail1 = {
    "title" : "cocoa",
    "content" : "coffee",
    "start_date" : "2023-03-23T15:00",
    "end_date" : "2023-04-30T01:00",
    "added_by" : pond1,
    "notify_who_when_done": "tuatang"
}

event_detail2 = {
    "title" : "test",
    "content" : "test",
    "start_date" : "2023-03-23T15:00",
    "end_date" : "2023-03-23T18:00",
    "added_by" : pond1,
    "notify_who_when_done": "tuatang"
}

ul = [tuatang1, pond1]
print(tuatang1.id)
print(pond1.id)
kmitl = Organization("KMITL", tuatang1)
kmitl.add_member([pond1, pun, march])
print(kmitl.organization_id)
ce = Organization("Computer Engineering", pond2)
ce.add_member([march, tuatang2])
chat_h1_project = ChatHistory(tuatang1)
chat_h2_project = ChatHistory(tuatang1)
project1 = Project(chat_h1_project, ElementCollector(), tuatang1, datetime.now(), project_detail1)
project2 = Project(chat_h2_project, ElementCollector(), tuatang1, datetime.now(), project_detail2)
act1 = Activity("started a new project called", project1.project_description, datetime.now(), project1.project_name, f"projects/{project1.project_id}")
act1.add_accomplisher(ul)
act2 = Activity("started a new project called", project2.project_description, datetime.now(), project2.project_name, f"projects/{project2.project_id}")
act2.add_accomplisher(march)
kmitl.add_activity(act2)
print(project1.project_id)
print(project2.project_id)
kmitl.add_project(project1)
kmitl.add_project(project2)
kmitl.add_activity(act1)
system.add_organization(kmitl)
system.add_organization(ce)
chat_h1 = ChatHistory(tuatang1)
kmitl.add_chat_history(chat_h1)
kmitl.add_chat_history(chat_h1_project)
kmitl.add_chat_history(chat_h2_project)
print(project1.campfire_chat.thread_id)
print(project2.campfire_chat.thread_id)
print(chat_h1.thread_id)
chat_h1.update_chat_history(Chat("555555555", datetime.now(), tuatang1))
chat_h1_project.update_chat_history(Chat("Hello World", datetime.now(), pond1))
chat_h1_project.update_chat_history(Chat("Hello Thai", datetime.now(), tuatang1))
chat_h1.add_receivers(pond1)
kmitl.add_role(pond1, "administrators")
project1.add_member_to_project(pond1)
chat_h1_project.add_receivers(pond1)
print(project1.members)
kmitl.add_role(pond1, "owners")
project1.element_collector.add_element(3, detail4)
project1.element_collector.add_element(2, detail2)
project1.element_collector.add_element(2, detail3)
project1.element_collector.add_element(7, event_detail2)
project1.element_collector.add_element(7, event_detail1)
project1.element_collector.todos[0].add_assignee(tuatang1)
project1.element_collector.todos[1].add_assignee(tuatang1)
project1.element_collector.events[0].add_participant(tuatang1)
project1.element_collector.events[1].add_participant(tuatang1)
noti1 = Notification("send notificantion test 1", datetime.now(), pond1, [tuatang1, pond1], f"{kmitl.organization_id}/")
noti2 = Notification("send notificantion test 2", datetime.now(), march, [tuatang1, pond1], f"{kmitl.organization_id}/")
noti1.send_notification()
noti2.send_notification()
system.update_todos() # Move to bottom
print(kmitl.find_events_date(kmitl.show_user_events(tuatang1), system))

#Test Hard Code

@app.get("/favicon.ico")
async def favicon():
    return JSONResponse(status_code=404, content={"message": "Not Found"})

@app.post("/set/cookies")
def set_cookie(response: Response, user_id: int):
    response.set_cookie(key="user_id", value=f"{user_id}")

@app.get("/get/cookies")
def get_cookie(request: Request):
    user_id = request.cookies.get('user_id')
    return user_id

@app.get("/", response_class=HTMLResponse, tags=["Authentication"])
async def show_auth(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@app.get("/signup/account/new", response_class=HTMLResponse, tags=["Authentication"])
async def show_signup(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/signup/account/new")
async def signup(request: Request, name: str = Form(...), email: str = Form(...), organization_name: str = Form(...), password: str = Form(...)):
    
    user_id, account_id = system.register(name, email, organization_name, password)
    if not account_id == False:
        response = JSONResponse(content={"response": "success", "user_id": user_id})
        response.set_cookie(key="account_id", value=f'{account_id}')
        response.set_cookie(key="user_id", value=f'{user_id}')
    else:
        response = JSONResponse(content={"response": "Email already exists"})
    return response

@app.get("/signin", response_class=HTMLResponse, tags=["Authentication"])
async def show_signin(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@app.post("/signin")
async def signin(request: Request, email: str = Form(...), password: str = Form(...)):
    account_id = system.login(email, password)
    if not account_id == False:
        account = system.get_account(account_id)
        response = JSONResponse(content={"response": "success", "len_users": len(account.users_list), "user_id": account.users_list[0].id})
        response.set_cookie(key="account_id", value=f'{account_id}')
    else:
        response = JSONResponse(content={"response": "We couldn’t find that one. Want to try another?"})
    return response

@app.get("/identity", response_class=HTMLResponse, tags=["Identity"])
async def show_identity(request: Request):
    print("signin")
    account_id = int(request.cookies.get("account_id"))
    account = system.get_account(account_id)
    users = account.users_list
    organizations = system.get_organizations(account_id)

    return templates.TemplateResponse("identity.html", {"request": request, "organizations": organizations, "users": users, "account": account})

@app.get("/session", tags=["Signout"])
async def get_session(request: Request):

    response = RedirectResponse(url="/", status_code=302)
    cookies = request.cookies.keys()
    for cookie in cookies:
        response.delete_cookie(cookie)
    return response

@app.get("/identity/edit", response_class=HTMLResponse, tags=["Identity"])
async def show_identity_edit(request: Request):
    # Get the cookie values from the request object
    if not request.cookies.get("account_id") == None:
        account_id = int(request.cookies.get("account_id"))
        account = system.get_account(account_id)
    else:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("identity_edit.html", {"request": request, "account": account})

@app.put("/identity/edit", tags=["Identity"])
async def create_upload_file(request:Request, image_url:str=Form(...), name: str = Form(...)):
    account_id = int(request.cookies.get("account_id"))
    account = system.get_account(account_id)

    print(image_url)
    if not image_url == "-":
        account.edit_identity({"name": name, "account_avatar": image_url})
    else:
        account.edit_identity({"name": name, "account_avatar": account.account_avatar})

    return {"name":name, "filename": image_url}

@app.get("/{organization_id}/my/profile", response_class=HTMLResponse, tags=["Organization"])
async def show_edit_profile(request: Request, organization_id: int):

    user_id = int(request.cookies.get("user_id"))
    account_id = int(request.cookies.get("account_id"))
    account = system.get_account(account_id)
    organization = system.get_organization_by_user_id(user_id)
    user = system.get_user(user_id)
    if not organization.organization_id == organization_id:
        return HTMLResponse(content= "error")
    else:
        return templates.TemplateResponse("edit_profile.html", {"request": request, "organization": organization, "account": account, "user": user})

@app.put("/{organization_id}/my/profile", tags=["Organization"])
async def edit_profile(request:Request, image_url:str=Form(...), name: str = Form(...), job_title: str = Form(...)):
    user_id = int(request.cookies.get("user_id"))
    account_id = int(request.cookies.get("account_id"))
    system.edit_profile(user_id, account_id, image_url, name, job_title)
    return JSONResponse(content={"response": "success"})

@app.get("/{organization_id}/account/cancellation/new", response_class=HTMLResponse, tags=["Organization"])
async def show_cancellation(request: Request, organization_id: int):
    organization = system.get_organization(organization_id)
    return templates.TemplateResponse("cancel_organization.html", {"request": request, "organization": organization})

@app.post("/{organization_id}/account/cancellation", tags=["Organization"])
async def cancel_account(request:Request, response:Response, organization_id: int):
    system.cancel_organization(organization_id)
    # delete cookie
    cookies = request.cookies.keys()
    for cookie in cookies:
        response.delete_cookie(cookie)
    return templates.TemplateResponse("cancellation.html", {"request": request})

@app.get("/{organization_id}/account/name/edit", response_class=HTMLResponse, tags=["Organization"])
async def show_edit_organization_name(request: Request, organization_id: int):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    return templates.TemplateResponse("rename_organization.html", {"request": request, "organization": organization, "user": user})

@app.get("/users/{user_id}")
async def go_to_organization(request: Request, user_id: int):
    print(user_id)
    organization = system.get_organization_by_user_id(user_id)
    response = RedirectResponse(url=f"/{organization.organization_id}", status_code=302)
    response.set_cookie(key="user_id", value=f'{user_id}')
    return response

@app.post("/{organization_id}/sign_out")
async def sign_out(request: Request, organization_id: str):
        response = JSONResponse(content={"response": "success"})
        cookies = request.cookies.keys()
        for cookie_name in cookies:
            response.delete_cookie(cookie_name)
        return response
 
@app.post("/{organization_id}/account/enrollment", tags=["Invitation"])
async def invitation(request: Request, organization_id:int, email: str = Form(...), real_email: str = Form(...)):
    user_id = int(request.cookies.get("user_id"))
    organization = system.get_organization(organization_id)
    account_id = int(request.cookies.get("account_id"))
    account = system.get_account(account_id)
    print(real_email)
    # check if email is already in the organization
    for acc in system.accounts_list:
        for user in acc.users_list:
            for member in organization.members:
                if user.id == member.id:
                    if acc.email == email:
                        print("email already in organization")
                        response = JSONResponse(content={"response": "Email already exists"})  
                        return response   
    
    # Define ROT13 encoding function
    def rot13(email):
        input = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        output = 'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
        index = lambda x: input.index(x) if x in input else -1
        return ''.join(output[index(x)] if index(x) > -1 else x for x in email)

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # Set up the SMTP server
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    # from_email = input('Enter your email: ')
    # from_password = input('Enter your password: ') # get from https://myaccount.google.com/apppasswords
    # to_email = input('Enter the recipient\'s email: ')
    from_email = 'pondaeroz008y@gmail.com'
    from_password = 'nfmdtfueeamtrmeq'
    # to_email = '65010539@kmitl.ac.th'
    to_email = real_email
    smtp_server.login(from_email, from_password)

    # Compose the email message
    from_address = from_email
    to_address = to_email
    subject = 'Test email'

    # Create a MIMEMultipart message
    message = MIMEMultipart()

    html = f'''
<!DOCTYPE html>
<html>
<head>
  <title>Basecamp Invitation</title>
</head>
                <style>
                    .container {{
                        border: 1px solid #ccc;
                        padding: 20px;
                        max-width: 600px;
                        
                        font-family: Arial, sans-serif;           
                    }}
                    
                    .logo {{
                        display: block;
                        margin: 20px 0 20px 20px;
                    }}
                    
                    .btn {{
                        background-color: #28a745;
                        color: #fff;
                        display: inline-block;
                        padding: 10px 20px;
                        border-radius: 5px;
                        text-decoration: none;
                        margin: 20px auto;
                        text-align: center;
                        font-weight: bold;
                        font-size: 16px;
                        border: none;
                        cursor: pointer;                
                    }}
                    
                    .btn:hover {{
                        background-color: #218838;
                    }}
                </style>
<body>
  <div class="container">
    <p><img src="{account.account_avatar} alt="Email Avatar" style="vertical-align:middle" width="32px" height="32px"> <strong>{account.name} ({organization.organization_name})</strong> &lt;{account.email}&gt;</p>
    <hr>
    <img src="https://i.ibb.co/Jm5F4N5/paper-clip.png" alt="Logo Icon" class="logo" width="32px" height="32px">
    <p><strong>{account.name}</strong> invited you to their <strong>Basecamp ({organization.organization_name})</strong></p>
    <p>Basecamp is a place that helps everyone stay organized and on the same page. It’s really straightforward and easy. To join <strong>{account.name}</strong>, click this button:</p>
    <a href="http://127.0.0.1:8000/{organization_id}/invitations/auth?{rot13('email')}={rot13(email)}&{rot13('organization_name')}={rot13(organization.organization_name)}" class="btn">Set up your password to join <strong>{account.name}</strong></a>
    <hr>
    <p><em><frame text></em></p>
  </div>
</body>
</html>
'''

    # Attach the HTML body to the message
    message.attach(MIMEText(html, 'html'))

    # Add the subject and sender/receiver email addresses to the message
    message['Subject'] = subject
    message['From'] = from_address
    message['To'] = to_address

    # Send the email
    smtp_server.sendmail(from_address, to_address, message.as_string())

    # Close the SMTP server
    smtp_server.quit()

    response = JSONResponse(content={"response": "success"})

    return response

@app.get("/{organization_id}/account/enrollment/new", response_class=HTMLResponse, tags=["Invitation"])
async def show_invitation(request: Request, organization_id: int):
    user_id = int(request.cookies.get("user_id"))
    organization = system.get_organization_by_user_id(user_id)
    account_id = int(request.cookies.get("account_id"))
    account = system.get_account(account_id)
    if not organization.organization_id == organization_id:
        return {"status": "error"}
    else:
        return templates.TemplateResponse("invite_demo.html", {"request": request, "organization": organization, "account": account})


@app.get("/{organization_id}/invitations/auth", response_class=HTMLResponse, tags=["Invitation"])
async def show_invitation_auth(request: Request, organization_id:int, rznvy:str, betnavmngvba_anzr:str):
    def rot13(email):
        input = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        output = 'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
        index = lambda x: input.index(x) if x in input else -1
        return ''.join(output[index(x)] if index(x) > -1 else x for x in email)

    email = rot13(rznvy)
    organization_name = betnavmngvba_anzr
    # print(organization_name)
    # print(email)
    return templates.TemplateResponse("invitation_auth.html", {"request": request, "organization_id": organization_id, "email": email})

@app.get("/{organization_id}/invitations/signin", response_class=HTMLResponse, tags=["Invitation"])
async def show_invitation_signin(request: Request, organization_id: int):
    return templates.TemplateResponse("invitation_signin.html", {"request": request, "organization_id": organization_id})

@app.post("/{organization_id}/invitations/signin", tags=["Invitation"])
async def signin(request: Request, organization_id: int, email: str = Form(...), password: str = Form(...)):

    # check if user exists
    account_id = system.login_to_new_organization(email, password, organization_id)
    if not account_id == False:
        account = system.get_account(account_id)
        response = JSONResponse(content={"response": "success", "user_id": account.users_list[-1].id})
        response.set_cookie(key="account_id", value=f'{account_id}')
    else:
        response = JSONResponse(content={"response": "We couldn’t find that one. Want to try another?"})

    return response

@app.get("/{organization_id}/invitations/signup", response_class=HTMLResponse, tags=["Invitation"])
async def show_invitation_signup(request: Request, organization_id: int):
    return templates.TemplateResponse("invitation_signup_demo.html", {"request": request, "organization_id": organization_id})

@app.post("/{organization_id}/invitations/signup", tags=["Invitation"])
async def signup(request: Request, organization_id: int, image_url: str=Form(...), name: str=Form(...), email: str=Form(...), password: str=Form(...)):
    # check if image_url is not empty
    print(f'Image URL: {image_url}')
    print(organization_id)
    user_id, account_id = system.register_to_existing_organization(image_url, name, organization_id, email, password)
    if not account_id == False:
        response = JSONResponse(content={"response": "success", "user_id": user_id})
        response.set_cookie(key="account_id", value=f'{account_id}')
    else:
        response = JSONResponse(content={"response": "Email already exists."})
    
    return response



#Get -- > Raise Error
@app.get("/error", response_class=HTMLResponse)
def get_error(request: Request):
    return templates.TemplateResponse("error.html", {"request": request})

#Get -- > View Home
@app.get("/{organization_id}", response_class=HTMLResponse, tags=["Organization"])
async def view_home(request: Request, organization_id: int):
        user_id = int(request.cookies.get("user_id"))
        account_id = int(request.cookies.get("account_id"))
        organization = system.get_organization_by_user_id(user_id)
        account = system.get_account_by_user_id(user_id)
        user = system.get_user(user_id)
        organizations = system.get_organizations(account_id)

        users = account.users_list

        if (organization is None) or (not system.check_user_access(user, organization)):
            return RedirectResponse("/error")
        else:
            list_of_user_project = organization.show_user_projects(user)
            list_of_user_chat = organization.show_user_private_chat(user)
            contacts = system.get_contacts(user, organization.members)
            assignments = organization.show_user_assignments(user)
            events = organization.show_user_events(user)
            todo_project_address_list, event_project_address_list = [], []
            todo_organization_address_list = []
            events_data = organization.find_events_date(organization.show_user_events(user), system)
            for todo in assignments:
                org ,project = system.find_element_address(todo, 2)
                todo_project_address_list.append(project)
                todo_organization_address_list.append(org)
            for event in events:
                org ,project = system.find_element_address(event, 7)
                event_project_address_list.append(project)
            current_date = datetime.now()
            return templates.TemplateResponse("home.html", {"request": request, "organization": organization, "account": account, "user": user, "user_projects": list_of_user_project, "user_chats": list_of_user_chat, "assignments": assignments, "events": events, "contacts": contacts, "todo_project_address": todo_project_address_list, "todo_organization_address": todo_organization_address_list, "event_project_address_list": event_project_address_list, "current_date": current_date, "events_data": events_data, "events": events, "organizations": organizations, "users": users})

#Get -- > View Home on Date
@app.get("/{organization_id}/on/{str_date}", tags=["Homepage"], response_class=HTMLResponse)
def view_home_on_date(request: Request, organization_id: int, str_date: str):
        user_id = int(request.cookies.get("user_id"))
        organization = system.get_organization_by_user_id(user_id)
        account = system.get_account_by_user_id(user_id)
        user = system.get_user(user_id)
        date = datetime.strptime(str_date, "%Y-%m-%d")
        date_day = int(date.strftime("%d"))
        if not organization.organization_id == organization_id:
            return JSONResponse(content={"response": "error"})
        else:
            list_of_user_project = organization.show_user_projects(user)
            list_of_user_chat = organization.show_user_private_chat(user)
            contacts = system.get_contacts(user, organization.members)
            assignments = organization.show_user_assignments(user)
            events = organization.show_user_events(user)
            todo_project_address_list, event_project_address_list, todo_organization_address_list = [], [], []
            events_datetime_list, time_delta_list = [], []
            events_data = organization.find_events_date(organization.show_user_events(user), system)
            for todo in assignments:
                org ,project = system.find_element_address(todo, 2)
                todo_project_address_list.append(project)
                todo_organization_address_list.append(org)
            for event in events:
                time_delta = organization.find_between_dates(event.start_date, event.end_date)
                org ,project = system.find_element_address(event, 7)
                event_project_address_list.append(project)
                time_delta_list.append(time_delta)
                events_datetime_list.append([datetime.strptime(event.start_date, "%Y-%m-%dT%H:%M"), datetime.strptime(event.end_date, "%Y-%m-%dT%H:%M")])
            current_date = datetime.now()
            return templates.TemplateResponse("home_on_date.html", {"request": request, "organization": organization, "account": account, "user": user, "user_projects": list_of_user_project, "user_chats": list_of_user_chat, "assignments": assignments, "events": events, "contacts": contacts, "todo_project_address": todo_project_address_list, "todo_organization_address": todo_organization_address_list, "event_project_address_list": event_project_address_list, "time_delta_list": time_delta_list, "current_date": current_date, "events_data": events_data, "date": date, "events": events, "date_day": date_day, "events_datetime_list": events_datetime_list})

# Get -- > View Lineup
@app.get("/{organization_id}/projects/lineup", tags=["Lineup"], response_class=HTMLResponse)
def view_lineup(request: Request, organization_id: int):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    list_of_user_chat = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    if (organization is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    current_time = datetime.now()
    backward_time = []
    forward_time = []
    for num in range(7, 50, 7):
        range_time = timedelta(days=num)
        backward_time.append(current_time-range_time-timedelta(days=1))
        forward_time.append(current_time+range_time-timedelta(days=1))
    time_range = backward_time[-1::-1] + [current_time] + forward_time
    return templates.TemplateResponse("lineup.html", {"request": request, "organization": organization, "user": user, "time_range": time_range, "current_time": current_time, "contacts": contacts, "user_chats": list_of_user_chat})

# Get -- > New Project
@app.get("/{organization_id}/projects/new", tags=["Projects"], response_class=HTMLResponse)
def form_project(request: Request, organization_id: int):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    account = system.get_account_by_user_id(int(user_id))
    user_chats = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    if (organization is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    return templates.TemplateResponse("new_project.html", {"request": request, "organization": organization, "account": account, "user": user, "contacts": contacts, "user_chats": user_chats})

# Post -- > Create Project
@app.post("/{organization_id}/projects/add_project", tags=["Projects"])
def add_project(request: Request, organization_id: int, detail: dict):
    organization = system.get_organization(int(organization_id))
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    if (organization is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    chat_history = ChatHistory(user)
    element_collector = ElementCollector()
    project = Project(chat_history, element_collector, user, datetime.now(), detail)
    print(project.start_date)
    activity = Activity("started new project called", project.project_description, datetime.now(), project.project_name, f"/projects/{project.project_id}")
    activity.add_accomplisher(user)
    organization.add_activity(activity)
    organization.add_chat_history(chat_history)
    return organization.add_project(project)

# Get -- > Get Project
@app.get("/{organization_id}/projects/{project_id}", tags=["Projects"], response_class=HTMLResponse)
def get_project(request: Request, organization_id: int, project_id: int):
    organization, project = system.locater(organization_id, project_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    account = system.get_account_by_user_id(int(user_id))
    user_chats = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    assignments = organization.show_user_assignments(user)
    overdue_todos = organization.check_overdue_todos()
    my_overdue_todos, my_project_assignments = [], []
    if (organization is None) or (project is None) or (not system.check_user_access(user, organization)) or (not system.check_user_access(user, project)):
        return RedirectResponse("/error")
    for my_overdue_todo in overdue_todos:
        if my_overdue_todo.assigned_to == user.name and my_overdue_todo in project.element_collector.todos:
            my_overdue_todos.append(my_overdue_todo)
    for my_project_assignment in assignments:
        if my_project_assignment in project.element_collector.todos:
            my_project_assignments.append(my_project_assignment)
    return templates.TemplateResponse("view_project.html", {"request": request, "system": system, "organization": organization, "account": account, "user": user, "project": project, "contacts": contacts, "user_chats": user_chats, "my_overdue_todos": my_overdue_todos, "my_project_assignments": my_project_assignments})

# Get -- > Read Someone's Projects
@app.get("/{organization_id}/users/{user_id}/projects", tags=["Projects"])
def get_user_projects(organization_id: int, user_id: int):
    organization = system.get_organization(organization_id)
    user = system.get_user(user_id)
    if (organization is None) or (user is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    list_of_user_project = organization.show_user_projects(user)
    return list_of_user_project

# Get -- > Read Organization's Activities
@app.get("/{organization_id}/activity", tags=["Activity"], response_class=HTMLResponse)
def get_activity_list(request: Request, organization_id: int):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    account = system.get_account_by_user_id(int(user_id))
    user_chats = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    if (organization is None) or (user is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    return templates.TemplateResponse("all_activities.html", {"request": request, "organization": organization, "account": account, "user": user, "contacts": contacts, "user_chats": user_chats})

# Get -- > Read Overdue Todos
@app.get("/{organization_id}/todos/overdue", tags=["Assignments"], response_class=HTMLResponse)
def get_activity_list(request: Request, organization_id: int):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    account = system.get_account_by_user_id(int(user_id))
    user_chats = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    overdue_todos = organization.check_overdue_todos()
    todo_project_address_list, todos_topic_list = [], []
    for todo in overdue_todos:
        org ,project = system.find_element_address(todo, 2)
        todos_topic = organization.find_todos_topic(int(todo.collector_id))
        todo_project_address_list.append(project)
        todos_topic_list.append(todos_topic)
    if (organization is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    return templates.TemplateResponse("overdue_todos.html", {"request": request, "organization": organization, "account": account, "user": user, "contacts": contacts, "user_chats": user_chats, "overdue_todos": overdue_todos, "todo_project_address_list": todo_project_address_list, "todos_topic_list": todos_topic_list})

# Get -- >  Find Someone to View Their Stuff
@app.get("/{organization_id}/users/search/{target}", tags=["Activity", "Assignments"], response_class=HTMLResponse) # target รับมาใช้แสดงค่าหน้า html เฉยๆ
def form_search_user(request: Request, organization_id: int, target: str): #รับ parameter organization_id และ target จาก url
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    account = system.get_account_by_user_id(int(user_id))
    user_chats = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    if (organization is None) or (user is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    return templates.TemplateResponse("show_member.html", {"request": request, "organization": organization, "account": account, "user": user, "target": target, "contacts": contacts, "user_chats": user_chats})
    
# Get -- > Read Someone's Activities/Assignments
@app.get("/{organization_id}/users/{user_id}/{target}", tags=["Activity", "Assignments"], response_class=HTMLResponse)
def view_user_activity_list(request: Request, organization_id: int, user_id: int, target: str):
    organization = system.get_organization(organization_id)
    user = system.get_user(user_id)
    account = system.get_account_by_user_id(int(user_id))
    user_chats = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    todo_project_address_list = []
    if (organization is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    if target == "assignments":
        target_list = organization.show_user_assignments(user)
        for todo in target_list:
            org ,project = system.find_element_address(todo, 2)
            todo_project_address_list.append(project)
    elif target == "activity": # ดู activity ของคนที่จะดู
        target_list = organization.show_user_activities(user)
    return templates.TemplateResponse(f"{target}.html", {"request": request, "organization": organization, "account": account, "user": user, "target_list": target_list, "contacts": contacts, "user_chats": user_chats, "todo_project_address_list":todo_project_address_list})
        
# Get -- > Read Someone's Schedule
@app.get("/{organization_id}/users/{user_id}/schedule", tags=["Schedule"])
def get_user_schedule(organization_id: int, user_id: int):
    user_schedule = []
    organization = system.get_organization(organization_id)
    user = system.get_user(user_id)
    if (organization is None) or (user is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    for proj in organization.projects:
        user_schedule.extend(proj.show_user_events(user))
    return user_schedule

#Get -- > View Chat History
@app.get("/{organization_id}/circles/{chat_history_id}", tags=["Chat"], response_class=HTMLResponse)
def view_chat(request: Request, organization_id: int, chat_history_id: int):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    account = system.get_account_by_user_id(int(user_id))
    chat_history = system.search_chat_history(chat_history_id)
    user_chats = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    receiver = system.get_contacts(user, chat_history.members)
    current = datetime.now()
    return templates.TemplateResponse("chat_history.html", {"request": request, "organization": organization, "account": account, "user": user, "chat_history": chat_history, "receiver": receiver, "current": current, "contacts": contacts, "user_chats": user_chats})

#Post -- > Create Chat
@app.post("/{organization_id}/circles/{chat_history_id}/create_chat", tags=["Chat"])
def add_chat(request: Request, organization_id: int, chat_history_id: int, data: dict):
    organization = system.get_organization(int(organization_id))
    chat_history = system.search_chat_history(chat_history_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    project = system.find_chat_address(chat_history.thread_id)
    if isinstance(project, Project):
        notification = Notification(f"Chat: {project.project_name}", datetime.now(), user, chat_history.members, f"circles/{chat_history.thread_id}")
        notification.send_notification()
    if (organization is None) or (chat_history is None) or (not system.check_user_access(user, chat_history)):
        return RedirectResponse("/error")
    content = data["content"]
    chat = Chat(content, datetime.now(), user)
    chat_history.update_chat_history(chat)
    return {"data": "success"}

#Post -- > Create/Get Chat History
@app.post("/{organization_id}/circles", tags=["Chat"])
def create_chat_history(request: Request, organization_id: int, receivers_data: dict):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    if (organization is None) or (user is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    receivers = []
    for receiver_data in receivers_data.values():
        if receiver_data != "":
            receiver_id = system.split_data(receiver_data, " : ", 1)
            receiver = system.get_user(int(receiver_id))
            receivers.append(receiver)
    chat_history = organization.check_chat_history(user, receivers)
    return RedirectResponse(url=f"/{organization_id}/circles/{chat_history.thread_id}", status_code=status.HTTP_303_SEE_OTHER)

#Post -- > Send File
@app.post("/{organization_id}/circles/{chat_history_id}/upload_file")
async def upload_file(request: Request, organization_id: int, chat_history_id: int, file_attach: UploadFile = File(...)):
    organization = system.get_organization(int(organization_id))
    chat_history = system.search_chat_history(chat_history_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    if (organization is None) or (chat_history is None) or (not system.check_user_access(user, chat_history)):
        return RedirectResponse("/error")
    file_path = os.getcwd() + "/files/" + file_attach.filename
    with open(file_path, "wb") as f:
        f.write(await file_attach.read())
    chat = Chat(file_attach, datetime.now(), user)
    chat_history.update_chat_history(chat)
    return RedirectResponse(url=f"/{organization_id}/circles/{chat_history_id}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/download/{filename}", response_class=FileResponse)
async def download_file(filename: str):
    file_path = os.getcwd() + "/files/" + filename
    return FileResponse(path=file_path, media_type='application/octet-stream', filename=filename)

#Get -- > View Profile
@app.get("/{organization_id}/my/profile", tags=["Profile"], response_class=HTMLResponse)
def view_profile(request: Request, organization_id: int):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    if (organization is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    return templates.TemplateResponse("edit_profile.html", {"request": request, "organization": organization, "user": user})

#Get -- > View Invite People to Project Page
@app.get("/{organization_id}/projects/{project_id}/accesses/users/new", tags=["Projects"], response_class=HTMLResponse)
def view_profile(request: Request, organization_id: int, project_id: int):
    organization, project = system.locater(organization_id, project_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    user_chats = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    if (organization is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    return templates.TemplateResponse("invite_project.html", {"request": request, "organization": organization, "project": project, "user": user, "contacts": contacts, "user_chats": user_chats})

#Post -- > Add People to Project
@app.post("/{organization_id}/projects/{project_id}/accesses/users/new", tags=["Projects"])
def add_people_to_project(request: Request, organization_id: int, project_id: int, people_data: dict):
    organization, project = system.locater(organization_id, project_id)
    visitor_id = request.cookies.get('user_id')
    visitor = system.get_user(int(visitor_id))
    user_id = system.split_data(people_data["member"], " : ", 1)
    user = system.get_user(int(user_id))
    project.add_member_to_project(user)
    activity = Activity("joined the project", "", datetime.now(), project.project_name)
    activity.add_accomplisher(user)
    organization.add_activity(activity)
    if (organization is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    return {"data": "success"}

#Get -- > Go to Adminland
@app.get("/{organization_id}/account", tags=["Adminland"], response_class=HTMLResponse)
def use_adminland(request: Request, organization_id: int):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    user_chats = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    if (organization is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    owner_contacts = system.get_contacts(user, organization.owners)
    admin_contacts = system.get_contacts(user, organization.admins)
    owner_permission = organization.check_user_role(user, organization.owners)
    admin_permission = organization.check_user_role(user, organization.admins)
    return templates.TemplateResponse("adminland.html", {"request": request, "organization": organization, "user": user, "owners": owner_contacts, "admins": admin_contacts, "owner_permission": owner_permission, "admin_permission": admin_permission, "contacts": contacts, "user_chats": user_chats})

#Get -- > Go to Owners/Administrators
@app.get("/{organization_id}/account/{target}", tags=["Adminland"], response_class=HTMLResponse)
def manage_admin(request: Request, organization_id: int, target: str):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    if (organization is None) or (not organization.check_user_role(user, organization.owners)) or (not organization.check_user_role(user, organization.admins)):
        return RedirectResponse("/error")
    if target == "owners":
        target_list = system.get_contacts(user, organization.owners)
        target_permission = organization.check_user_role(user, organization.owners)
    elif target == "administrators":
        target_list = system.get_contacts(user, organization.admins)
        target_permission = organization.check_user_role(user, organization.admins)
    owners_list = organization.get_admin_with_owner_permission()
    user_chats = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    return templates.TemplateResponse(f"{target}.html", {"request": request, "organization": organization, "user": user, "target_list": target_list, "target_permission": target_permission, "owners_list": owners_list, "contacts": contacts, "user_chats": user_chats})

#Post -- > Add Role
@app.post("/{organization_id}/account/{target}/add_role", tags=["Adminland"])
def add_role(organization_id: int, target: str, data: dict):
    organization = system.get_organization(organization_id)
    user_id = system.split_data(data["member"], " : ", 1)
    user = system.get_user(int(user_id))
    organization.add_role(user, f"{target}")
    return {"data": "success"}

#Get -- > Remove Role
@app.get("/{organization_id}/account/{target}/remove_role/{user_id}", tags=["Adminland"])
def remove_role(organization_id: int, target: str, user_id: int):
    organization = system.get_organization(organization_id)
    user = system.get_user(user_id)
    organization.remove_role(user, f"{target}")
    return RedirectResponse(url=f"/{organization_id}/account/{target}", status_code=status.HTTP_303_SEE_OTHER)

#Get -- > Edit Organization
@app.get("/{organization_id}/account/name/edit", tags=["Adminland"], response_class=HTMLResponse)
def edit_organization(request: Request, organization_id: int):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    user_chats = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    if (organization is None) or (user not in organization.members) or (not organization.check_user_role(user, organization.owners)):
        return RedirectResponse("/error")
    return templates.TemplateResponse("rename_organization.html", {"request": request, "organization": organization, "contacts": contacts, "user_chats": user_chats})

#Put -- > Rename Organization
@app.put("/{organization_id}/account/name/rename", tags=["Adminland"])
def rename_organization(organization_id: int, data: dict):
    organization = system.get_organization(organization_id)
    new_name = data["account_name"]
    organization.organization_name = new_name
    return organization.organization_name

@app.get("/{organization_id}/admins")
def get_admins(organization_id: int):
    organization = system.get_organization(organization_id)
    return organization.admins

@app.get("/{organization_id}/owners")
def get_admins(organization_id: int):
    organization = system.get_organization(organization_id)
    return organization.owners

#Get -- > Show Everyone
@app.get("/{organization_id}/account/accesses/people", tags=["Adminland"], response_class=HTMLResponse)
def show_everyone(request: Request, organization_id: int):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    if (organization is None) or (not system.check_user_access(user, organization)) or (not organization.check_user_role(user, organization.admins)):
        return RedirectResponse("/error")
    user_chats = organization.show_user_private_chat(user)
    members_without_me = system.get_contacts(user, organization.members)
    return templates.TemplateResponse("show_everyone.html", {"request": request, "organization": organization, "user": user, "contacts": members_without_me, "user_chats": user_chats})

#Get -- > Edit People Accesses Page
@app.get("/{organization_id}/account/accesses/{user_id}/edit", tags=["Adminland"], response_class=HTMLResponse)
def manage_access(request: Request, organization_id: int, user_id: int):
    organization = system.get_organization(organization_id)
    visitor_id = request.cookies.get('user_id')
    visitor = system.get_user(int(visitor_id))
    user = system.get_user(user_id)
    user_chats = organization.show_user_private_chat(visitor)
    contacts = system.get_contacts(visitor, organization.members)
    if (organization is None) or (not system.check_user_access(visitor, organization)) or (not organization.check_user_role(visitor, organization.admins)):
        return RedirectResponse("/error")
    return templates.TemplateResponse("change_access.html", {"request": request, "organization": organization, "user": visitor, "access_user": user, "contacts": contacts, "user_chats": user_chats})

#Post -- > Change People Accesses
@app.post("/{organization_id}/account/accesses/{user_id}", tags=["Adminland"])
def edit_access(request: Request, organization_id: int, user_id: int, data: dict):
    organization = system.get_organization(organization_id)
    visitor_id = request.cookies.get('user_id')
    visitor = system.get_user(int(visitor_id))
    user = system.get_user(user_id)
    temp_list = data["result"].split(", ")
    index = 0
    for proj in organization.projects:
        if str(proj.project_id) == temp_list[index]:
            if user not in proj.members:
                proj.add_member_to_project(user)
        elif temp_list[index] == "":
            if user in proj.members:
                proj.remove_member(user)
        index += 1
    activity = Activity("changed who can access this project", f"{user.name} was granted access.", datetime.now(), "")
    activity.add_accomplisher(visitor)
    organization.add_activity(activity)
    if (organization is None) or (not system.check_user_access(visitor, organization)) or (not organization.check_user_role(visitor, organization.admins)):
        return RedirectResponse("/error")
    return {"data": "success"}

#Get -- > Access any Project Page
@app.get("/{organization_id}/account/accesses/overrides", tags=["Adminland"], response_class=HTMLResponse)
def view_access_project(request: Request, organization_id: int):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    user_chats = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    if (organization is None) or (not system.check_user_access(user, organization)) or (not organization.check_user_role(user, organization.owners)):
        return RedirectResponse("/error")
    return templates.TemplateResponse("owner_access.html", {"request": request, "organization": organization, "user": user, "contacts": contacts, "user_chats": user_chats})

#Get -- > Access any Project
@app.get("/{organization_id}/account/accesses/overrides/{project_id}", tags=["Adminland"])
def access_project(request: Request, organization_id: int, project_id: int):
    organization, project = system.locater(organization_id, project_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    project.add_member_to_project(user)
    if (organization is None) or (not system.check_user_access(user, organization)) or (not organization.check_user_role(user, organization.owners)):
        return RedirectResponse("/error")
    return RedirectResponse(url=f"/{organization_id}", status_code=status.HTTP_303_SEE_OTHER)

#Get -- > View Notifications
@app.get("/{organization_id}/my/readings", tags=["Notifications"], response_class=HTMLResponse)
def view_notifications(request: Request, organization_id: int):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    account = system.get_account_by_user_id(int(user_id))
    list_of_user_chat = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    if (organization is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    reads, unreads = user.get_notifications()
    return templates.TemplateResponse("notifications.html", {"request": request, "organization": organization, "account": account, "user": user, "contacts": contacts, "user_chats": list_of_user_chat, "reads": reads, "unreads": unreads})
    
@app.put('/mark-as-read/{notification_id}', tags=["Notifications"])
async def mark_as_read(request: Request, notification_id: int):
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    notification = user.get_notification(notification_id)
    notification.update_mark()
    return { 'status': 'success' }

#Get -- > Read Todos Added & Completed
@app.get("/{organization_id}/users/{user_id}/todos/summary", tags=["Assignments"], response_class=HTMLResponse)
def view_todo_summary(request: Request, organization_id: int, user_id: int):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    account = system.get_account_by_user_id(int(user_id))
    if (organization is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    assignments = organization.show_user_assignments(user)
    list_of_user_chat = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    current_date = datetime.now()
    todo_project_address_list, todo_organization_address_list = [], []
    count_checked = 0
    for todo in assignments:
        if todo.completed:
            count_checked += 1
        org ,project = system.find_element_address(todo, 2)
        todo_project_address_list.append(project)
        todo_organization_address_list.append(org)
    return templates.TemplateResponse("todo_summary.html", {"request": request, "organization": organization, "account": account, "user": user, "assignments": assignments, "contacts": contacts, "user_chats": list_of_user_chat, "todo_project_address": todo_project_address_list, "todo_organization_address": todo_organization_address_list, "current_date": current_date, "count_checked": count_checked})

#Put -- > Complete Todo
@app.put("/{organization_id}/users/{user_id}/todos/complete", tags=["Assignments"])
def complete_todo(request: Request, organization_id: int, user_id: int, data: dict):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    todo_id = int(data["todo_id"])
    for project in organization.projects:
        todo = project.element_collector.get_element(2, todo_id)
        if isinstance(todo, ToDo):
            todo.completed = True
            notification = Notification(f"Completed: {todo.title}", datetime.now(), todo.added_by, todo.assigned_to, "")
            user.add_notification(notification)
            return {"data": "success"}

#Get -- > Search Everything Page
@app.get("/{organization_id}/search")
def search_everything(request: Request, organization_id: int):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    account = system.get_account_by_user_id(int(user_id))
    if (organization is None) or (not system.check_user_access(user, organization)):
        return RedirectResponse("/error")
    return templates.TemplateResponse("search.html", {"request": request, "organization": organization, "account": account, "user": user})

@app.get("/{organization_id}/search/results")
def search_results(request: Request, organization_id: int, q: str = Query(..., min_length=1)):
    organization = system.get_organization(organization_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    pages = system.gather_everything(organization, user)
    results = []
    for page in pages:
        if q.lower() in page["content"].lower():
            results.append({"title": page["title"], "url": page["url"], "content": page["content"]})
    if len(results) > 0:
        return results
    else:
        raise HTTPException(status_code=404, detail="No matching results found")
    
    #Get -- > View All Todos-Topics
@app.get("/{organization_id}/projects/{project_id}/todos_topics", tags=["ToDosTopic"], response_class=HTMLResponse)
async def get_todos_topics(organization_id: int, project_id: int, request: Request):
    organization, project = system.locater(organization_id, project_id)
    todos_topics = project.element_collector.todos_topics
    todos = project.element_collector.todos
    respond_dict = {}
    for todos_topic in todos_topics:
        respond_dict[todos_topic] = []
        for todo in todos:
            if todos_topic.id == todo.collector_id:
                respond_dict[todos_topic].append(todo)
    return templates.TemplateResponse('todos_list_page.html', {'request': request, 'organization': organization, 'project': project, 'respond_dict': respond_dict})

#Post -- > Add Todos-Topic
@app.post("/{organization_id}/projects/{project_id}/add_todos_topics", tags=["ToDosTopic"])
async def add_todos_topics(organization_id: int, project_id: int, request: Request, element_detail: dict):
    organization, project = system.locater(organization_id, project_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    project.element_collector.add_element(ElementType.TODOSTOPIC.value, element_detail)
    return {"response" : "success"}

#Post -- > Add Todo
@app.post("/{organization_id}/projects/{project_id}/todos_topics/{todos_topic_id}/add_todo", tags=["ToDo"])
async def add_todo(request: Request, organization_id: int, project_id: int, todos_topic_id: int, element_detail: dict) :
    project = system.get_project(project_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    element_detail["added_by"] = user
    assignees = []
    for index in range(1, 5):
        if element_detail[f"assignee{index}"] != "":
            assignee_id = system.split_data(element_detail[f"assignee{index}"], " : ", 1)
            assignee = system.get_user(int(assignee_id))
            assignees.append(assignee)
    project.element_collector.add_element(ElementType.TODO.value, element_detail)
    project.element_collector.todos[-1].add_assignee(assignees)
    return {"respond": "success"}

#Post -- > Add Event
@app.post("/{organization_id}/projects/{project_id}/events/add_event", tags=["ToDo"])
async def add_event(request: Request, organization_id: int, project_id: int, element_detail: dict) :
    project = system.get_project(project_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    element_detail["added_by"] = user
    participants = []
    for index in range(1, 5):
        if element_detail[f"participant{index}"] != "":
            participant_id = system.split_data(element_detail[f"participant{index}"], " : ", 1)
            participant = system.get_user(int(participant_id))
            print(participant)
            participants.append(participant)
    project.element_collector.add_element(ElementType.EVENT.value, element_detail)
    project.element_collector.events[-1].add_participant(participants)
    return {"respond": "success"}

#Get -- > View Event
@app.get("/{organization_id}/projects/{project_id}/events/{event_id}", tags=["ToDo"], response_class=HTMLResponse)
async def get_one_event(organization_id: int, project_id: int, event_id: int, request: Request):
    organization, project = system.locater(organization_id, project_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    account = system.get_account_by_user_id(int(user_id))
    element = project.element_collector.get_element(ElementType.EVENT.value, event_id)
    list_of_user_chat = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    start_date, end_date = datetime.strptime(element.start_date, "%Y-%m-%dT%H:%M"), datetime.strptime(element.end_date, "%Y-%m-%dT%H:%M")
    return templates.TemplateResponse(f'events.html', {'request': request, 'organization': organization, 'project': project, "account": account, "user": user, 'element': element, "start_date": start_date, "end_date": end_date, "contacts": contacts, "user_chats": list_of_user_chat})

#Get -- > View Todo
@app.get("/{organization_id}/projects/{project_id}/todos/{todo_id}", tags=["ToDo"], response_class=HTMLResponse)
async def get_one_todo(organization_id: int, project_id: int, todo_id: int, request: Request):
    organization, project = system.locater(organization_id, project_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    account = system.get_account_by_user_id(int(user_id))
    element = project.element_collector.get_element(ElementType.TODO.value, todo_id)
    list_of_user_chat = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    return templates.TemplateResponse(f'todos.html', {'request': request, 'organization': organization, 'project': project, "account": account, "user": user, 'element': element, "contacts": contacts, "user_chats": list_of_user_chat})

#Get -- > View Todos-Topic
@app.get("/{organization_id}/projects/{project_id}/todos_topics/{todos_topic_id}", tags=["ToDosTopic"], response_class=HTMLResponse)
async def get_one_todos_topic(organization_id: int, project_id: int, todos_topic_id: int, request: Request):
    organization, project = system.locater(organization_id, project_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    account = system.get_account_by_user_id(int(user_id))
    respond_todos, todo_project_address, todo_organization_address= [], [], []
    element = project.element_collector.get_element(ElementType.TODOSTOPIC.value, todos_topic_id)
    respond_todos = element.get_todos(project.element_collector.todos)
    list_of_user_chat = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    for todo in respond_todos:
        org ,project = system.find_element_address(todo, 2)
        todo_project_address.append(project)
        todo_organization_address.append(org)
    return templates.TemplateResponse('todos_topics.html', {'request': request, 'organization': organization, 'project': project, "account": account, "user": user, 'element': element, 'respond_todos': respond_todos, "todo_organization_address": todo_organization_address, "todo_project_address": todo_project_address, "contacts": contacts, "user_chats": list_of_user_chat})

#Get -- > View Project Upcoming Date
@app.get("/{organization_id}/projects/{project_id}/schedule", tags=["Schedules"], response_class=HTMLResponse)
def view_upcoming_date(request: Request, organization_id: int, project_id: int):
    organization, project = system.locater(organization_id, project_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    account = system.get_account_by_user_id(int(user_id))
    user_chats = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    events_data = organization.find_events_date(project.element_collector.events, system)
    event_project_address_list, time = [], []
    for event in project.element_collector.events:
        start_date, end_date = datetime.strptime(event.start_date, "%Y-%m-%dT%H:%M"), datetime.strptime(event.end_date, "%Y-%m-%dT%H:%M")
        org ,project = system.find_element_address(event, 7)
        event_project_address_list.append(project)
        time.append([start_date, end_date])
    return templates.TemplateResponse("upcoming_date.html", {"request": request, "user": user, "organization": organization, "project": project, "account": account, "user": user, "contacts": contacts, "user_chats": user_chats, "events_data": events_data, "event_project_address_list": event_project_address_list, "time": time})

@app.get("/{organization_id}/projects/{project_id}/todos_topics/{todos_topic_id}/edit")
def edit_todos_topic(request: Request, organization_id: int, project_id: int, todos_topic_id: int):
    organization, project = system.locater(organization_id, project_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    account = system.get_account_by_user_id(int(user_id))
    user_chats = organization.show_user_private_chat(user)
    contacts = system.get_contacts(user, organization.members)
    element = project.element_collector.get_element(ElementType.TODOSTOPIC.value, todos_topic_id)
    return templates.TemplateResponse('edit_todos_topic.html', {'request': request, 'organization': organization, 'project': project, "account": account, "user": user, 'element': element, "contacts": contacts, "user_chats": user_chats})


@app.put("/{organization_id}/projects/{project_id}/todos_topic/{todos_topic_id}/edit_todos_topic")
def edit_todos_topic_detail(request: Request, organization_id: int, project_id: int, todos_topic_id: int, data: dict):
    organization, project = system.locater(organization_id, project_id)
    user_id = request.cookies.get('user_id')
    user = system.get_user(int(user_id))
    project.element_collector.edit_element(3, todos_topic_id, "title", data["title"])
    project.element_collector.edit_element(3, todos_topic_id, "description", data["description"])
    return {"data": "success"}

@app.get("/{organization_id}/projects/{project_id}/message_boards/{message_board_id}", response_class=HTMLResponse, tags=["Elements"])
async def show_message_board(request: Request, organization_id: int, project_id: int, message_board_id: int):
    print('show_message_board')
    organization, project = system.locater(organization_id, project_id)
    
    account_sender_list = []
    for message in project.element_collector.get_element_collector(ElementType.MESSAGE.value):
        print(message.sender.id)
        print(system.get_account_by_user_id(message.sender.id))
        account_sender_list.append(system.get_account_by_user_id(message.sender.id))

    message_board = project.element_collector.get_element_collector(ElementType.MESSAGE.value)
    print(message_board_id)
    
    print(f'len of message_board ::: {len(project.element_collector.message_board)}')
    
    return templates.TemplateResponse("message_board.html", {"request": request, "organization": organization, "project": project, "message_board": message_board, "account_sender_list": account_sender_list})

@app.get("/{organization_id}/projects/{project_id}/message_boards/{message_board_id}/messages/new", response_class=HTMLResponse, tags=["Elements"])
async def show_create_message(request: Request, organization_id: int, project_id: int, message_board_id: int):
    print(message_board_id)
    account_id = int(request.cookies.get("account_id"))
    account = system.get_account(account_id)
    organization, project = system.locater(organization_id, project_id)
    message_board = project.element_collector.get_element_collector(ElementType.MESSAGE.value)
    print(f'message id ::: {project.message_board.id}')
    return templates.TemplateResponse("new_message.html", {"request": request, "organization": organization, "account": account, "project": project, "message_board": message_board})

@app.post("/{organization_id}/projects/{project_id}/message_boards/{message_board_id}/messages/new", response_class=HTMLResponse, tags=["Elements"])
async def create_message(request: Request, organization_id: int, project_id: int, message_board_id: int, title : str = Form("Untitled"), content : str = Form(""), url_list: str = Form(...)):
    url_list = json.loads(url_list)
    print(f'URL LIST ::: {url_list}')
    account_id = int(request.cookies.get("account_id"))
    account = system.get_account(account_id)
    user_id = int(request.cookies.get("user_id"))
    user = system.get_user(user_id)
    print(f'User ID: {user_id}')
    print(f'Account Name: {account.name}')
    project = system.get_project(project_id)
    print(f'url_list ::: {url_list}')
    project.element_collector.add_element(ElementType.MESSAGE.value, {"title": title, "content": content, "file_content" : url_list, "sender" : user, "timestamp" : datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
    message_id = project.element_collector.get_element_collector(ElementType.MESSAGE.value)[-1].id
    print(f'message id ::: {message_id}')
    return JSONResponse(status_code=200,content={"response": "success", "message_id" : message_id})

@app.get("/{organization_id}/projects/{project_id}/messages/{message_id}", response_class=HTMLResponse, tags=["Elements"])
async def show_message(request: Request, organization_id: int, project_id: int, message_id: int):
    organization, project = system.locater(organization_id, project_id)
    message = project.element_collector.get_element(ElementType.MESSAGE.value, message_id)
    account_sender = system.get_account_by_user_id(message.sender.id)
    print(f'message title ::: {message.title}')
    print(f'message timestamp ::: {message.timestamp}')
    
    return templates.TemplateResponse("show_message.html", {"request": request, "organization": organization, "project": project, "message": message, "account_sender": account_sender, "url_list": message.file_content})

@app.get("/{organization_id}/projects/{project_id}/messages/{message_id}/edit", response_class=HTMLResponse, tags=["Elements"])
async def show_edit_message(request: Request, organization_id: int, project_id: int, message_id: int):
    organization, project = system.locater(organization_id, project_id)
    message = project.element_collector.get_element(ElementType.MESSAGE.value, message_id)
    print(f'message id ::: {message.id}')
    account_sender = system.get_account_by_user_id(message.sender.id)
    print(f'message title ::: {message.title}')
    print(f'message timestamp ::: {message.timestamp}')
    return templates.TemplateResponse("message_edit.html", {"request": request, "organization": organization, "project": project, "message": message, "account_sender": account_sender, "url_list": message.file_content})

@app.put("/{organization_id}/projects/{project_id}/messages/{message_id}/edit", response_class=HTMLResponse, tags=["Elements"])
async def edit_message(request: Request, organization_id: int, project_id: int, message_id: int, title : str = Form("Untitled"), content : str = Form(""), url_list: str = Form(...)):
    url_list = json.loads(url_list)
    print(f'URL LIST ::: {url_list}')
    account_id = int(request.cookies.get("account_id"))
    account = system.get_account(account_id)
    user_id = int(request.cookies.get("user_id"))
    user = system.get_user(user_id)

    project = system.get_project(project_id)
    project.element_collector.edit_element(ElementType.MESSAGE.value, message_id, "title", title)
    project.element_collector.edit_element(ElementType.MESSAGE.value, message_id, "content", content)
    project.element_collector.edit_element(ElementType.MESSAGE.value, message_id, "file_content", url_list)
    # project.element_collector.edit_element(ElementType.MESSAGE.value, message_id, "timestamp", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    # display attributes after edit
    message = project.element_collector.get_element(ElementType.MESSAGE.value, message_id)
    print(f'message title ::: {message.title}')
    print(f'message timestamp ::: {message.timestamp}')
    print(f'message content ::: {message.content}')
    print(f'message file_content ::: {message.file_content}')
    # edit message
    return JSONResponse(status_code=200,content={"response": "success", "message_id" : message_id})


@app.get('/{organization_id}/projects/{project_id}/folder/{folder_id}', response_class=HTMLResponse, tags=["Elements"])
async def show_folder(request: Request, organization_id: int, project_id: int, folder_id: int):
    organization, project = system.locater(organization_id, project_id)
    folder_parent = project.docs_n_files
    current_folder = project.element_collector.get_element(ElementType.FOLDER.value, folder_id)
    folder_path = system.get_folder_relative_path(current_folder.parent_id, current_folder.id, project, [])

    folder_child = system.get_document_child(project, current_folder)

    print(f'len(folder_child) ::: {len(folder_child)}')
    print(f'type(folder_child) ::: {type(folder_child)}')
    for f in folder_child:
        print(f'title ::: {f.title}')
        print(f'parent_id ::: {f.parent_id}')
        print(f'id ::: {f.id}')
    
    return templates.TemplateResponse("view_folder_v2.html", {"request": request, "organization": organization, "project": project, "folder_parent" : folder_parent, "current_folder" : current_folder, "folder_path" : folder_path, "folder_child" : folder_child})

@app.post("/{organization_id}/projects/{project_id}/folder/{folder_id}/folder/upload", response_class=HTMLResponse, tags=["Elements"])
async def upload_file(request: Request, organization_id: int, project_id: int, folder_id: int, title : str = Form("Untitled")):
    print(title)
    organization, project = system.locater(organization_id, project_id)
    current_folder = project.element_collector.get_element(ElementType.FOLDER.value, folder_id)
    
    project.element_collector.add_element(ElementType.FOLDER.value, {"title": title, "parent_id": current_folder.id})
    
    for f in project.element_collector.get_element_collector(ElementType.FOLDER.value):
        if f.parent_id == current_folder.id:
            folder_created = f
            break
    return JSONResponse(status_code=200,content={"response": "success", "element_id" : folder_created.id})

@app.get("/{organization_id}/projects/{project_id}/folder/{folder_id}/files/new", response_class=HTMLResponse, tags=["Elements"])
async def new_file(request: Request, organization_id: int, project_id: int, folder_id: int):
    organization, project = system.locater(organization_id, project_id)
    current_folder = project.element_collector.get_element(ElementType.FOLDER.value, folder_id)
    folder_path = system.get_folder_relative_path(current_folder.parent_id, current_folder.id, project, [])

    return templates.TemplateResponse("new_file.html", {"request": request, "organization": organization, "project": project, "current_folder" : current_folder, "folder_path" : folder_path})
    
@app.post("/{organization_id}/projects/{project_id}/folder/{folder_id}/files/new", response_class=HTMLResponse, tags=["Elements"])
async def post_new_file(request: Request, organization_id: int, project_id: int, folder_id: int, title : str = Form("Untitled"), content : str = Form(""), url_list: str = Form(...)):
    url_list = json.loads(url_list)
    print(f'URL LIST ::: {url_list}')
    organization, project = system.locater(organization_id, project_id)
    current_folder = project.element_collector.get_element(ElementType.FOLDER.value, folder_id)
    user_id = int(request.cookies.get("user_id"))
    user = system.get_user(user_id)
    

    project.element_collector.add_element(ElementType.DOCUMENT.value, {"title": title, "content": content, "file_content": url_list, "parent_id": current_folder.id, "added_by": user, "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
    
    file_id = project.element_collector.get_element_collector(ElementType.DOCUMENT.value)[-1].id

    return JSONResponse(status_code=200,content={"response": "success", "file_id" : file_id})

@app.get("/{organization_id}/projects/{project_id}/files/{file_id}", response_class=HTMLResponse, tags=["Elements"])
async def show_file(request: Request, organization_id: int, project_id: int, file_id: int):
    organization, project = system.locater(organization_id, project_id)
    folder_parent = project.docs_n_files
    current_file = project.element_collector.get_element(ElementType.DOCUMENT.value, file_id)
    folder_path = system.get_folder_relative_path(current_file.parent_id, current_file.id, project, [])
    account_added_by = system.get_account_by_user_id(current_file.added_by.id)

    url_list = current_file.file_content
    print(f'len(url_list) ::: {len(url_list)}')
    for url in url_list:
        print(f'URL ::: {url}')

    return templates.TemplateResponse("show_file.html", {"request": request, "organization": organization, "project": project, "current_file" : current_file, "folder_parent" : folder_parent, "folder_path" : folder_path, "account_added_by" : account_added_by, "url_list" : current_file.file_content})

@app.get("/{organization_id}/projects/{project_id}/files/{file_id}/edit", response_class=HTMLResponse, tags=["Elements"])
async def edit_file(request: Request, organization_id: int, project_id: int, file_id: int):
    organization, project = system.locater(organization_id, project_id)
    current_file = project.element_collector.get_element(ElementType.DOCUMENT.value, file_id)
    folder_path = system.get_folder_relative_path(current_file.parent_id, current_file.id, project, [])

    return templates.TemplateResponse("file_edit.html", {"request": request, "organization": organization, "project": project, "current_file" : current_file, "folder_path" : folder_path, "url_list" : current_file.file_content})

@app.put("/{organization_id}/projects/{project_id}/files/{file_id}/edit", response_class=HTMLResponse, tags=["Elements"])
async def put_edit_file(request: Request, organization_id: int, project_id: int, file_id: int, title : str = Form("Untitled"), content : str = Form(""), url_list: str = Form(...)):
    url_list = json.loads(url_list)
    print(f'URL LIST ::: {url_list}')
    organization, project = system.locater(organization_id, project_id)
    current_file = project.element_collector.get_element(ElementType.DOCUMENT.value, file_id)
    # current_file.title = title
    # current_file.content = content
    # current_file.file_content = url_list
    # current_file.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    project.element_collector.edit_element(ElementType.DOCUMENT.value, file_id, "title", title)
    project.element_collector.edit_element(ElementType.DOCUMENT.value, file_id, "content", content)
    project.element_collector.edit_element(ElementType.DOCUMENT.value, file_id, "file_content", url_list)
    project.element_collector.edit_element(ElementType.DOCUMENT.value, file_id, "timestamp", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    return JSONResponse(status_code=200,content={"response": "success", "file_id" : file_id})


@app.get("/{organization_id}/projects/{project_id}/folder/{folder_id}/edit", response_class=HTMLResponse, tags=["Element"])
async def edit_folder(request: Request, organization_id: int, project_id: int, folder_id: int):
    account_id = int(request.cookies.get("account_id"))
    account = system.get_account(account_id)
    user_id = int(request.cookies.get("user_id"))
    user = system.get_user(user_id)
    users = account.users_list
    organizations = system.get_organizations(account_id)
    
    organization, project = system.locater(organization_id, project_id)
    current_folder = project.element_collector.get_element(ElementType.FOLDER.value, folder_id)
    folder_path = system.get_folder_relative_path(current_folder.parent_id, current_folder.id, project, [])
    project = system.get_project(project_id)
    if (organization is None) or (not system.check_user_access(user, organization)):
            return RedirectResponse("/error")
    else:
        list_of_user_project = organization.show_user_projects(user)
        list_of_user_chat = organization.show_user_private_chat(user)
        contacts = system.get_contacts(user, organization.members)

        current_date = datetime.now()
        return templates.TemplateResponse("folder_edit.html", {"request": request, "organization": organization, "account": account, "user": user, "user_projects": list_of_user_project, "user_chats": list_of_user_chat, "contacts": contacts, "current_date": current_date, "organizations": organizations, "users": users, "current_folder" : current_folder, "folder_path" : folder_path, "project" : project})
    
@app.put("/{organization_id}/projects/{project_id}/folder/{folder_id}/edit", response_class=HTMLResponse, tags=["Element"])
async def put_edit_folder(request: Request, organization_id: int, project_id: int, folder_id: int, title : str = Form("Untitled")):
    print(f'FOLDER TITLE ::: {title}')
    # organization, project = system.locater(organization_id, project_id)
    project = system.get_project(project_id)
    project.element_collector.edit_element(ElementType.FOLDER.value, folder_id, "title", title)
    return JSONResponse(status_code=200,content={"response": "success", "folder_id" : folder_id})
