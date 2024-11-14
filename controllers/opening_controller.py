from views import OpeningView
import flet as ft
import webbrowser
from utils import Preferences
from services import Database

class OpeningController():
    def __init__(self, page: ft.Page, opening_page: OpeningView):
        self.page = page
        self.opening_page = opening_page
        self.database: Database = page.session.get("database")
        self.text_values: dict = page.session.get("text_values")
        self.prefs: Preferences = page.session.get("prefs")
        
        # check if autologin is enabled
        self.handle_automatic_login()
        
        self.opening_page.login_button.on_click = self.login_clicked
        self.opening_page.signup_button.on_click = self.signup_clicked

        self.opening_page.about_button.on_click = lambda e: webbrowser.open_new("https://github.com/treppenwitz03/arlecchino/blob/main/README.md")
        self.opening_page.support_button.on_click = lambda e: webbrowser.open_new("https://github.com/treppenwitz03/arlecchino/issues/new")
    
    def load_repo(self, activity: str):
        self.page.snack_bar = ft.SnackBar(ft.Text(self.text_values["loading"]))
        self.page.snack_bar.open = True
        self.page.update()

        if not self.database.load():
            self.page.snack_bar = ft.SnackBar(ft.Text(self.text_values["internet_error"].format(activity)), action=self.text_values["try_again"])
            self.page.snack_bar.on_action = lambda e: self.load_repo(activity)
            self.page.snack_bar.open = True
            self.page.update()
            return False
        
        return True

    # go to login page
    def login_clicked(self, event):
        if self.load_repo("log in"):
            self.page.go("/login")
    
    # go to signup page
    def signup_clicked(self, event):
        if self.load_repo("sign up"):
            self.page.go("/signup")
    
    # handle automatic logging in
    def handle_automatic_login(self):
        automatic_login = self.prefs.get_preference("keep_signed_in", False)
        email = self.prefs.get_preference("email", None)
        self.page.session.set("email", email)
        self.page.session.set("from_chats", False)
        
        if all([automatic_login, email, email != ""]):
            self.page.snack_bar = ft.SnackBar(ft.Text(self.text_values["autolog_notice"]))
            self.page.snack_bar.open = True
            self.page.update()
            if self.load_repo("automatically log in"):
                self.page.go("/home")