from views import HomePage
from services import Database
from models import User
from utils import Utils
from ..controller_connector import ControllerConnector
import flet as ft

class AccountViewController:
    def __init__(self, page: ft.Page, home_page: HomePage):
        self.page = page
        self.database: Database = page.session.get("database")
        self.home_page = home_page
        self.account_view = home_page.account_view
        self.utils: Utils = self.page.session.get("utils")

        self.account_view.logout_button.on_click = self.logout_account
        self.account_view.update_informations = self.update_account_view
        self.account_view.trigger_reload = self.update_account_view
    
        # logs current user out of the account
    def logout_account(self, event: ft.ControlEvent):
        self.page.client_storage.set("keep_signed_in", False)
        self.page.client_storage.set("recent_set_keep_signed_in", False)

        self.home_page.prepare_exit()

        self.page.go("/login")
        self.page.update()
    
        # update the account view with the new infos
    def update_account_view(self):
        email: str = ControllerConnector.get_email(self.page)
        
        user_image = ""
        username = ""

        user: User = None
        for user in self.database.users:
            if user.email == email:
                user_image = Utils.convert_to_base64(self.database.download_image(user.picture_link))
                username = self.utils.decrypt(user.username)
                break

        self.account_view.user_picture.src_base64 = user_image
        self.account_view.username_text.value = username
        self.account_view.email_text.value = self.utils.decrypt(email)