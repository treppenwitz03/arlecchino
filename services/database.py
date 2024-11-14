import requests
import smtplib
import ssl
import io
import base64
import flet as ft
import pyrebase
import json

from email.message import EmailMessage
from utils import Utils
from models import User, Group, Member, Transaction

class Database:
    def __init__(self, page: ft.Page):
        self.page = page

        with open("services/config.json", "rb") as f:
            self.config = json.load(f)

    def load(self):
        try:
            self.firebase = pyrebase.initialize_app({
                "apiKey": self.config["apiKey"],
                "authDomain": self.config["authDomain"],
                "databaseURL": self.config["databaseURL"],
                "storageBucket": self.config["storageBucket"],
                "serviceAccount": self.config["serviceAccount"],
                "projectId": self.config["projectId"],
                "messagingSenderId": self.config["messagingSenderId"],
                "measurementId": self.config["measurementId"],
                "appId": self.config["appId"]
            })
            self.db = self.firebase.database()
            self.storage = self.firebase.storage()
            self.auth = self.firebase.auth()
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

    def update_refs(self):
        self.dictionary = self.db.child("/").get().val()
        self.files = self.storage.list_files()

    def load_users(self):
        self.users = []
        repo_users = self.dictionary["Users"]
        
        for user_key, user_data in repo_users.items():
            self.users.append(
                User(
                    user_key,
                    user_data.get('First Run'),
                    user_data.get('GCash'),
                    user_data.get('Password'),
                    user_data.get('Picture Link'),
                    user_data.get('QR Image id'),
                    user_data.get('Username')
                )
            )

    def load_groups(self):
        self.groups = []
        repo_groups = self.dictionary["Groups"]
        
        for group_key, group_data in repo_groups.items():
            members = [Member(member[0], member[1]) for member in group_data.get("Members", {}).items()]
            transactions = self.load_transactions(group_data.get("Transactions", {}))
            
            self.groups.append(
                Group(
                    group_key,
                    group_data.get('Created by'),
                    group_data.get('Description'),
                    members,
                    group_data.get('Picture id'),
                    group_data.get('Unique code'),
                    transactions
                )
            )

    def load_transactions(self, transactions_dict):
        transactions = []
        if transactions_dict == "None":
            return transactions
        
        for transaction_name, transaction_data in transactions_dict.items():
            transaction_paid_by = "None" if transaction_data["Paid by"] == "None" else list(transaction_data["Paid by"].items())
            transaction_posted_by = next((user.email for user in self.users if user.email == transaction_data["Posted by"]["Email"]), "")
            
            transactions.append(
                Transaction(
                    transaction_name,
                    transaction_data['Description'],
                    transaction_data['Image id'],
                    transaction_paid_by,
                    transaction_posted_by,
                    transaction_data['Price'],
                    transaction_data['Time created']
                )
            )
        return transactions

    def update_group(self, group: Group):
        members = {str(member.username): str(member.email) for member in group.members}
        transactions = {t.name: {
                "Description": t.description,
                "Image id": t.image_id,
                "Price": t.price,
                "Time created": t.time_created,
                "Paid by": dict(t.paid_by) if t.paid_by != "None" else "None",
                "Posted by": {"Email": t.posted_by}
            } for t in group.transactions}
        
        self.db.child('Groups').child(group.group_name).set({
            "Created by": group.created_by,
            "Description": group.description,
            "Picture id": group.picture_id,
            "Unique code": group.unique_code,
            "Members": members,
            "Transactions": transactions if transactions else "None"
        })
        
        self.update_refs()
        self.load_groups()

    def update_user(self, user: User):
        self.db.child('Users').child(user.email).set({
            "First Run": user.first_run,
            "GCash": user.gcash_number,
            "Password": user.password,
            "Picture Link": user.picture_link,
            "QR Image id": user.qr_image_id,
            "Username": user.username
        })
        
        self.update_refs()
        self.load_users()

    def upload_image(self, buffer: io.BytesIO) -> str:
        id = Utils.generate_random_name()
        buffer.seek(0)
        self.storage.child(id).put(buffer.getvalue(), content_type='application/octet-stream')
        return id

    def download_image(self, image_id: str) -> io.BytesIO:
        if not image_id:
            return
        
        file = None
        url = self.storage.child(image_id).get_url(None)

        response = requests.get(url)
        if response.status_code == 200:
            file = io.BytesIO(response.content)

        return file

    def delete_transaction(self, group_name: str, transaction: Transaction):
        group_ref = f"Groups/{group_name}/Transactions"
        self.db.child(group_ref).child(transaction.name).remove()
        self.update_refs()
        self.load_groups()

    def send_mail(self, email, message: EmailMessage):
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(self.em, self.wp)
                smtp.sendmail(self.em, email, message.as_string())
            return True
        except smtplib.SMTPException:
            return False
