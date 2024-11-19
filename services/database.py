# import requests
# import random
# import smtplib
# import ssl
# import io
# import base64
# import flet as ft
# import pyrebase
# import json

# from email.message import EmailMessage
# from utils import Utils
# from models import User, Group, Member, Transaction

# class Database:
#     def __init__(self, page: ft.Page):
#         self.page = page

#         with open("services/config.json", "rb") as f:
#             self.config = json.load(f)

#     def load(self):
#         try:
#             self.firebase = pyrebase.initialize_app({
#                 "apiKey": self.config["apiKey"],
#                 "authDomain": self.config["authDomain"],
#                 "databaseURL": self.config["databaseURL"],
#                 "storageBucket": self.config["storageBucket"],
#                 "serviceAccount": self.config["serviceAccount"],
#                 "projectId": self.config["projectId"],
#                 "messagingSenderId": self.config["messagingSenderId"],
#                 "measurementId": self.config["measurementId"],
#                 "appId": self.config["appId"]
#             })
#             self.db = self.firebase.database()
#             self.storage = self.firebase.storage()
#             self.auth = self.firebase.auth()
            # utils: Utils = self.page.session.get("utils")
            # self.wp = self.config["access_code"]
            # self.em = self.config["email"]
            # utils.set_key(base64.b64decode(self.config["key"]))
            
#             self.update_refs()
#             self.load_users()
#             self.load_groups()
#             self.done_loading()
#             return True
#         except ValueError:
#             return False

#     def done_loading(self):
#         pass

#     def update_refs(self):
#         self.dictionary = self.db.child("/").get().val()
#         self.files = self.storage.list_files()

#     def load_users(self):
#         self.users = []
#         repo_users = self.dictionary["Users"]
        
#         for user_key, user_data in repo_users.items():
#             self.users.append(
#                 User(
#                     user_key,
#                     user_data.get('First Run'),
#                     user_data.get('GCash'),
#                     user_data.get('Password'),
#                     user_data.get('Picture Link'),
#                     user_data.get('QR Image id'),
#                     user_data.get('Username')
#                 )
#             )

#     def load_groups(self):
#         self.groups = []
#         repo_groups = self.dictionary["Groups"]
        
#         for group_key, group_data in repo_groups.items():
#             members = [Member(member[0], member[1]) for member in group_data.get("Members", {}).items()]
#             transactions = self.load_transactions(group_data.get("Transactions", {}))
            
#             self.groups.append(
#                 Group(
#                     group_key,
#                     group_data.get('Created by'),
#                     group_data.get('Description'),
#                     members,
#                     group_data.get('Picture id'),
#                     group_data.get('Unique code'),
#                     transactions
#                 )
#             )

#     def load_transactions(self, transactions_dict):
#         transactions = []
#         if transactions_dict == "None":
#             return transactions
        
#         for transaction_name, transaction_data in transactions_dict.items():
#             transaction_paid_by = "None" if transaction_data["Paid by"] == "None" else list(transaction_data["Paid by"].items())
#             transaction_posted_by = next((user.email for user in self.users if user.email == transaction_data["Posted by"]["Email"]), "")
            
#             transactions.append(
#                 Transaction(
#                     transaction_name,
#                     transaction_data['Description'],
#                     transaction_data['Image id'],
#                     transaction_paid_by,
#                     transaction_posted_by,
#                     transaction_data['Price'],
#                     transaction_data['Time created']
#                 )
#             )
#         return transactions

#     def update_group(self, group: Group):
#         members = {str(member.username): str(member.email) for member in group.members}
#         transactions = {t.name: {
#                 "Description": t.description,
#                 "Image id": t.image_id,
#                 "Price": t.price,
#                 "Time created": t.time_created,
#                 "Paid by": dict(t.paid_by) if t.paid_by != "None" else "None",
#                 "Posted by": {"Email": t.posted_by}
#             } for t in group.transactions}
        
#         self.db.child('Groups').child(group.group_name).set({
#             "Created by": group.created_by,
#             "Description": group.description,
#             "Picture id": group.picture_id,
#             "Unique code": group.unique_code,
#             "Members": members,
#             "Transactions": transactions if transactions else "None"
#         })
        
#         self.update_refs()
#         self.load_groups()

#     def update_user(self, user: User):
#         self.db.child('Users').child(user.email).set({
#             "First Run": user.first_run,
#             "GCash": user.gcash_number,
#             "Password": user.password,
#             "Picture Link": user.picture_link,
#             "QR Image id": user.qr_image_id,
#             "Username": user.username
#         })
        
#         self.update_refs()
#         self.load_users()

#     def upload_image(self, buffer: io.BytesIO) -> str:
#         id = Utils.generate_random_name()
#         buffer.seek(0)
#         self.storage.child(id).put(buffer.getvalue(), content_type='application/octet-stream')
#         return id

#     def download_image(self, image_id: str) -> io.BytesIO:
#         if not image_id:
#             return
        
#         file = None
#         url = self.storage.child(image_id).get_url(None)

#         response = requests.get(url)
#         if response.status_code == 200:
#             file = io.BytesIO(response.content)

#         return file

#     def delete_transaction(self, group_name: str, transaction: Transaction):
#         group_ref = f"Groups/{group_name}/Transactions"
#         self.db.child(group_ref).child(transaction.name).remove()
#         self.update_refs()
#         self.load_groups()

#     def send_mail(self, email, message: EmailMessage):
#         try:
#             context = ssl.create_default_context()
#             with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
#                 smtp.login(self.em, self.wp)
#                 smtp.sendmail(self.em, email, message.as_string())
#             return True
#         except smtplib.SMTPException:
#             return False

#     def get_email_confirmation_code(self, email):
#         code = random.randrange(100000, 999999)
#         subject = "Do you want to reset your password with Arlecchino? "
#         body = f"""
# Someone is trying to change your password within the Arlecchino Application.
# If this is you, enter the following code on the app prompt:
#     {code}
# Ignore this message if not.
#         """
#         email_message = EmailMessage()
#         email_message["From"] = self.em
#         email_message["To"] = email
#         email_message["Subject"] = subject
#         email_message.set_content(body)
#         context = ssl.create_default_context()
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
#             smtp.login(self.em, self.wp)
#             smtp.sendmail(self.em, email, email_message.as_string())
#         return code

import firebase_admin
import json
import random
import smtplib
import ssl
import io
import base64
import flet as ft

from email.message import EmailMessage
from firebase_admin import db, credentials, storage
from googleapiclient.errors import HttpError
from socket import gaierror
from utils import Utils

from models import User, Group, Member, Transaction

from typing import List

###########################################################################
## Repository connects to the online database to get and upload user data
###########################################################################

class Database:
    def __init__(self, page: ft.Page):
        self.page = page

        with open("services/config.json", "rb") as f:
            self.config = json.load(f)

    def load(self):
        try:
            cred = credentials.Certificate("services/token.json")
            firebase_admin.initialize_app(cred, {
                "databaseURL" : "https://morax-ea133-default-rtdb.asia-southeast1.firebasedatabase.app/",
                "storageBucket": "morax-ea133.appspot.com"
            })

            self.bucket = storage.bucket()
            # blob = self.bucket.blob("ap7t10co.isus")
            
            # utils: Utils = self.page.session.get("utils")
            # utils.set_key(base64.b64decode(blob.download_as_bytes()))

            # mail_blob = self.bucket.blob("gapword")
            # self.pw, self.em = mail_blob.download_as_text().split("\n")

            utils: Utils = self.page.session.get("utils")
            self.wp = self.config["access_code"]
            self.em = self.config["email"]
            utils.set_key(base64.b64decode(self.config["key"]))

            self.update_refs()
            
            self.load_users()
            self.load_groups()
            self.done_loading()
            return True
        except ValueError:
            return False
    
    def done_loading(self):
        pass
    
    # update the references so that when the groups and users are retrieved all changes are reflected
    def update_refs(self):
        ref = db.reference("/")
        self.dictionary = dict(ref.get())
        self.files = self.bucket.list_blobs()
        
    # load the list of users
    def load_users(self):
        self.users = []
        repo_users = self.dictionary["Users"]
        
        for user in repo_users:
            self.users.append(
                User(
                    user,
                    repo_users[user]['First Run'],
                    repo_users[user]['GCash'],
                    repo_users[user]['Password'],
                    repo_users[user]['Picture Link'],
                    repo_users[user]['QR Image id'],
                    repo_users[user]['Username']
                )
            )
    
    # load the list of groups
    def load_groups(self):
        self.groups = []
        repo_groups = self.dictionary["Groups"]
        
        for group in repo_groups:
            created_by = repo_groups[group]['Created by']
            description = repo_groups[group]['Description']
            members = [Member(member[0], member[1]) for member in dict(repo_groups[group]['Members']).items()]
            picture_id = repo_groups[group]['Picture id']
            unique_code = repo_groups[group]['Unique code']
            
            transactions = []
            
            transactions_dict = repo_groups[group]['Transactions']
            
            if transactions_dict != "None":
                for transaction in transactions_dict:
                    transaction_name = transaction
                    transaction_description = transactions_dict[transaction]['Description']
                    transaction_image_id = transactions_dict[transaction]['Image id']
                    transaction_price = transactions_dict[transaction]['Price']
                    transaction_time_created = transactions_dict[transaction]['Time created']
                    
                    transaction_paid_by = None
                    if transactions_dict[transaction]['Paid by'] == "None":
                        transaction_paid_by = "None"
                    else:
                        transaction_paid_by = list(dict(transactions_dict[transaction]['Paid by']).items())
                    
                    transaction_posted_by = ""
                    for user in self.users:
                        if user.email == transactions_dict[transaction]['Posted by']["Email"]:
                            transaction_posted_by = user.email
                    
                    transactions.append(
                        Transaction(
                            transaction_name,
                            transaction_description,
                            transaction_image_id,
                            transaction_paid_by,
                            transaction_posted_by,
                            transaction_price,
                            transaction_time_created
                        )
                    )
            
            self.groups.append(
                Group(
                    group,
                    created_by,
                    description,
                    members,
                    picture_id,
                    unique_code,
                    transactions
                )
            )
    
    # update the groups with the changes
    def update_group(self, group: Group):
        members = dict()
        transactions = dict()
        
        member: Member = None
        for member in group.members:
            members.update({str(member.username) : str(member.email)})
            
        transaction: Transaction = None
        for transaction in group.transactions:
            paid_users = dict()
            
            if transaction.paid_by == "None":
                paid_users = "None"
            else:
                paid_user: tuple = None
                for paid_user in transaction.paid_by:
                    paid_users.update({str(paid_user[0]) : str(paid_user[1])})
            
            transactions.update({
                str(transaction.name) : {
                    "Description" : str(transaction.description),
                    "Image id" : str(transaction.image_id),
                    "Price" : str(transaction.price),
                    "Time created": str(transaction.time_created),
                    "Paid by": paid_users,
                    "Posted by": { "Email" : str(transaction.posted_by) },
                }
            })
        
        if len(transactions.items()) == 0:
            transactions = "None"
        
        db.reference('/Groups/').update({
            group.group_name: {
                "Created by": str(group.created_by),
                "Description": str(group.description),
                "Picture id": str(group.picture_id),
                "Unique code": str(group.unique_code),
                "Members": members,
                "Transactions": transactions
            }
        })
        
        self.update_refs()
        self.load_groups()
    
    # update the user with the changes
    def update_user(self, user: User):
        db.reference('/Users/').update({
            user.email: {
                "First Run": user.first_run,
                "GCash": str(user.gcash_number),
                "Password": str(user.password),
                "Picture Link": str(user.picture_link),
                "QR Image id": str(user.qr_image_id),
                "Username": str(user.username)
            }
        })
        
        self.update_refs()
        self.load_users()
    
    # function to upload image to the database
    def upload_image(self, buffer: io.BytesIO) -> str:
        try:
            id = Utils.generate_random_name()
            buffer.seek(0)
            self.bucket.blob(id).upload_from_file(buffer, content_type='application/octet-stream')
            return id
        except HttpError as error:
            print(f'An error occurred: {error}')
            return
    
    # function to download image
    def download_image(self, image_id: str) -> io.BytesIO:
        if image_id == "":
            return

        try:
            blob = self.bucket.blob(image_id)
            file = io.BytesIO()
            blob.download_to_file(file)
            return file
        except HttpError as error:
            print(F'An error occurred: {error}')
            return
    
    # deletes a transaction from the database
    def delete_transaction(self, group_name: str, transaction: Transaction):
        for group in self.groups:
            if group.group_name == group_name:
                if len(group.transactions) > 1:
                    db.reference(f"/Groups/{group_name}/Transactions/{transaction.name}").delete()
                else:
                    db.reference(f"/Groups/{group_name}").update({
                        "Transactions": "None"
                    })

        self.update_refs()
        self.load_groups()
    
    # send an email confirmation code and returns what is sent for forgot password
    def get_email_confirmation_code_forgot(self, email):
        code = random.randrange(100000, 999999)
        subject = "Do you want to reset your password with Arlecchino? "
        body = f"""
Someone is trying to change your password within Arlecchino.

If this is you, enter the following code on the app prompt:

    {code}

Ignore this message if not.
        """

        email_message = EmailMessage()
        email_message["From"] = self.em
        email_message["To"] = email
        email_message["Subject"] = subject
        email_message.set_content(body)

        if not self.send_mail(email, email_message):
            return False

        return code
    
    # Confirm account with Arlecchino
    def get_email_confirmation_code(self, email):
        code = random.randrange(100000, 999999)
        subject = "Confirm your account with Arlecchino"
        body = f"""
Greetings! Welcome to Arlecchino. To continue, please confirm your email.

If this is you, enter the following code on the app prompt:

    {code}

Ignore this message if not.
        """

        email_message = EmailMessage()
        email_message["From"] = self.em
        email_message["To"] = email
        email_message["Subject"] = subject
        email_message.set_content(body)

        if not self.send_mail(email, email_message):
            return False

        return code
    
    def send_mail(self, email, message: EmailMessage):
        try:
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(self.em, self.wp)
                smtp.sendmail(self.em, email, message.as_string())
            
            return True
        except gaierror:
            return False