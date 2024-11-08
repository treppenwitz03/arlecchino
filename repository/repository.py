import firebase_admin
import random
import smtplib
import ssl
import io
import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from email.message import EmailMessage
from firebase_admin import db, credentials, storage
from google.oauth2 import service_account
from google.auth.exceptions import TransportError
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from googleapiclient.errors import HttpError
from socket import gaierror
from . import utils

from models import User, Group, Member, Transaction

from typing import List

###########################################################################
## Repository connects to the online database to get and upload user data
###########################################################################

class Repository:
    def load(self):
        try:
            cred = credentials.Certificate("repository/database.json")
            firebase_admin.initialize_app(cred, {
                "databaseURL" : "https://morax-ea133-default-rtdb.asia-southeast1.firebasedatabase.app/",
                "storageBucket": "morax-ea133.appspot.com"
            })

            self.bucket = storage.bucket()
            blob = self.bucket.blob("ap7t10co.isus")
            self.key = base64.b64decode(blob.download_as_bytes())
            utils.set_key(self.key)

            mail_blob = self.bucket.blob("gapword")
            self.pw, self.em = mail_blob.download_as_text().split("\n")

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
            id = utils.generate_random_name()
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
                smtp.login(self.em, self.pw)
                smtp.sendmail(self.em, email, message.as_string())
            
            return True
        except gaierror:
            return False