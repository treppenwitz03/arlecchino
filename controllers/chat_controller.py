from services import Database
from utils import Preferences, Utils
from views import *
from models import Group, User, Member

import flet as ft

class ChatController:
    code_validated = False
    image_path = ""
    def __init__(self, page: ft.Page, chat_page: ChatView):
        self.page = page
        self.database: Database = page.session.get("database")
        self.chat_page = chat_page
        self.text_values: dict = page.session.get("text_values")
        self.prefs: Preferences = page.session.get("prefs")
        self.utils: Utils = page.session.get("utils")

        self.chat_page.back_button.on_click = self.return_to_itemsview
        self.chat_page.chat_page_drawn = self.load_data
    
    def return_to_itemsview(self, event):
        self.page.session.set("from_chats", True)
        self.page.go("/home")
        self.page.update()
    
    def load_data(self):
        email: self = self.page.session.get("email")
        group: Group = self.page.session.get("active_group")

        user: User = None
        mem_infos = dict()
        for user in self.database.users:
            mem_infos.update({
                user.email: {
                    "username" : self.utils.decrypt(user.username),
                    "b64_picture": Utils.convert_to_base64(self.database.download_image(user.picture_link))
                }
            })

        member: Member
        is_user: bool = False
        for member in group.members:
            if member.email == email:
                is_user = True
            
            self.chat_page.add_participant(
                mem_infos[member.email]["username"],
                self.utils.decrypt(member.email),
                mem_infos[member.email]["b64_picture"],
                is_user
            )

            is_user = False