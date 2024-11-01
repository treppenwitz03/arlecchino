from repository import Repository
from views import SignupPage
import flet as ft
import webbrowser

class SignupController:
    def __init__(self, page: ft.Page, repository: Repository, signup_page: SignupPage):
        self.page = page
        self.repository = repository
        self.signup_page = signup_page
        
        # handle signup fields
        self.signup_page.email_textfield.on_change = self.validate
        self.signup_page.username_textfield.on_change = self.validate
        self.signup_page.password_textfield.on_change = self.validate
        self.signup_page.confirm_password_textfield.on_change = self.validate
        self.signup_page.agree_eula_check.on_change = self.validate
        self.signup_page.login_button.on_click = self.go_to_login
        self.signup_page.register_btn.on_click = self.register

        self.signup_page.agree_eula_indicator_button.on_click = lambda e: webbrowser.open_new("https://github.com/treppenwitz03/arlecchino/blob/main/LICENSE")
    
    # validate the fields before enabling proceed
    def validate(self, event):
        verdict = all([
            self.signup_page.get_email_entry() != "",
            self.signup_page.get_username_entry() != "",
            self.signup_page.get_password_entry() != "",
            self.signup_page.get_confirm_password_entry() != "",
            self.signup_page.get_agree_eula_entry(),
            self.signup_page.get_password_entry() == self.signup_page.get_confirm_password_entry()
        ])
        
        if verdict is True:
            self.signup_page.allow_register(True)
        else:
            self.signup_page.allow_register(False)
    
    # register the user if confirmed
    def register(self, event):
        code = self.repository.get_email_confirmation_code(self.signup_page.get_email_entry())

        if not code:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Cannot send code..."), action="Try again")
            self.page.snack_bar.open = True
            self.page.snack_bar.on_action = lambda e: self.register(event)
            self.page.update()
            return

        command = [
            "COMMAND_REGISTER",
            code,
            self.repository.encrypt(self.signup_page.get_email_entry()),
            self.repository.encrypt(self.signup_page.get_username_entry()),
            self.repository.encrypt(self.signup_page.get_password_entry()),
        ]
        self.signup_page.basket.command = command
        self.page.go("/confirm_email")

    # go to login
    def go_to_login(self, event):
        self.page.go("/login")