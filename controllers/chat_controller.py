from services import Database
from utils import Preferences
from views import *

import flet as ft

class ChatController:
    code_validated = False
    image_path = ""
    def __init__(self, page: ft.Page, chat_page: ChatPage):
        self.page = page
        self.database: Database = page.session.get("database")
        self.chat_page = chat_page
        self.text_values: dict = page.session.get("text_values")
        self.prefs: Preferences = page.session.get("prefs")

        self.chat_page.appbar.leading.on_click = self.return_to_itemsview
    
    def return_to_itemsview(self, event):
        self.page.go("/home")
        self.page.update()
