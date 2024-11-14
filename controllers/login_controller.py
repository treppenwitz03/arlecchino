from services import Database
from utils import Utils, Preferences
from views import LoginView
from models import User
import flet as ft

class LoginController:
    def __init__(self, page: ft.Page, login_page: LoginView):
        self.page = page
        self.database: Database = page.session.get("database")
        self.login_page = login_page
        self.text_values: dict = page.session.get("text_values")
        self.utils: Utils = self.page.session.get("utils")
        self.prefs: Preferences = page.session.get("prefs")
        
        # handle login page events
        self.login_page.email_textfield.on_change = self.validate
        self.login_page.password_textfield.on_change = self.validate
        self.login_page.login_btn.on_click = self.login
        self.login_page.forgot_password_btn.on_click = self.forgot_password
        self.login_page.signup_button.on_click = self.go_to_signup
        self.login_page.keep_logged_check.on_change = self.handle_automatic_login
    
    # set whether to allow or disallow login through field check
    def validate(self, event):
        if self.login_page.get_email_entry() != "" and self.login_page.get_password_entry() != "":
            self.login_page.allow_login(True)
        else:
            self.login_page.allow_login(False)
    
    # verify the credentials and login
    def login(self, event):
        email = self.login_page.get_email_entry().strip()
        password = self.utils.encrypt(self.login_page.get_password_entry().strip())
        
        user: User = None
        for user in self.database.users:
            if (self.utils.decrypt(user.username) == email or self.utils.decrypt(user.email) == email) and user.password == password:
                if self.utils.decrypt(user.username) == email:
                    email = self.utils.decrypt(user.email)

                self.prefs.set_preference("email", self.utils.encrypt(email))
                self.page.session.set("email", self.utils.encrypt(email))
                self.page.session.set("from_chats", False)
                if user.first_run:
                    self.page.go("/onboarding")
                else:
                    self.page.go("/home")
                
                return
            elif user.email == email and user.password != password:
                self.login_page.display_on_dialog(self.text_values["password_wrong"])
                return
        
        self.login_page.display_on_dialog(self.text_values["uname_pw_wrong"])
    
    # handle if autologin is enabled
    def handle_automatic_login(self, event):
        setting = self.login_page.get_keep_signed_in()
        self.prefs.set_preference("keep_signed_in", setting)
        self.prefs.set_preference("recent_set_keep_signed_in", setting)
    
    # show signup page
    def go_to_signup(self, event):
        self.page.go("/signup")
    
    # show forgot password page
    def forgot_password(self, event):
        self.page.go("/forgot_password")