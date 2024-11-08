from views import OpeningPage
from .controller_connector import ControllerConnector
import flet as ft
import webbrowser
from repository import Repository

class OpeningController():
    def __init__(self, page: ft.Page, repository: Repository, opening_page: OpeningPage):
        self.page = page
        self.opening_page = opening_page
        self.repository = repository
        
        # check if autologin is enabled
        self.handle_automatic_login()
        
        self.opening_page.login_button.on_click = self.login_clicked
        self.opening_page.signup_button.on_click = self.signup_clicked

        self.opening_page.about_button.on_click = lambda e: webbrowser.open_new("https://github.com/treppenwitz03/arlecchino/blob/main/README.md")
        self.opening_page.support_button.on_click = lambda e: webbrowser.open_new("https://github.com/treppenwitz03/arlecchino/issues/new")
    
    def load_repo(self, activity: str):
        self.page.snack_bar = ft.SnackBar(ft.Text(f"Loading..."))
        self.page.snack_bar.open = True
        self.page.update()

        if not self.repository.load():
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Unable to {activity} due to slow internet connection..."), action="Try Again")
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
        automatic_login = self.page.client_storage.get("keep_signed_in")
        email = self.page.client_storage.get("email")
        ControllerConnector.set_email(self.page, email)
        
        if all([automatic_login, email, email != ""]):
            self.page.snack_bar = ft.SnackBar(ft.Text(f"You will be automatically logged in."))
            self.page.snack_bar.open = True
            self.page.update()
            if self.load_repo("automatically log in"):
                self.page.go("/home")