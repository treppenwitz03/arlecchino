from services import Database
from utils import Utils
from views import ForgotPasswordView
import flet as ft

class ForgotController:
    def __init__(self, page: ft.Page, forgot_password_page: ForgotPasswordView):
        self.page = page
        self.database: Database = page.session.get("database")
        self.forgot_password_page = forgot_password_page
        self.text_values: dict = page.session.get("text_values")
        self.utils: Utils = self.page.session.get("utils")
        
        ##### COntroller for the Forgot Password View #############
        
        # Handle forgot password page events
        self.forgot_password_page.new_password_textfield.on_change = self.validate
        self.forgot_password_page.confirm_new_password_textfield.on_change = self.validate
        self.forgot_password_page.email_textfield.on_change = self.validate
        self.forgot_password_page.signup_button.on_click = self.go_to_signup
        self.forgot_password_page.change_password_btn.on_click = self.change_password
    
    # enable/disable buttons depending on field completion
    def validate(self, event):
        verdict = all([
            self.forgot_password_page.get_email_to_send_entry() != "",
            self.forgot_password_page.get_new_password_entry() != "",
            self.forgot_password_page.get_confirm_new_password_entry() != "",
            self.forgot_password_page.get_new_password_entry() == self.forgot_password_page.get_confirm_new_password_entry()
        ])
        
        if verdict:
            self.forgot_password_page.allow_password_change(True)
        else:
            self.forgot_password_page.allow_password_change(False)
    
    # go to signup page
    def go_to_signup(self, event):
        self.page.go("/signup")
    
    # reflect password change on database
    def change_password(self, event):
        code = self.database.get_email_confirmation_code_forgot(self.forgot_password_page.get_email_to_send_entry())

        if not code:
            self.page.snack_bar = ft.SnackBar(ft.Text(self.text_values["code_not_send"]), action=self.text_values["try_again"])
            self.page.snack_bar.open = True
            self.page.snack_bar.on_action = lambda e: self.change_password(event)
            self.page.update()
            return

        command = [
            "COMMAND_CHANGE_PASSWORD",
            code,
            self.utils.encrypt(self.forgot_password_page.get_email_to_send_entry().strip()),
            self.utils.encrypt(self.forgot_password_page.get_new_password_entry().strip()),
        ]
        self.page.session.set("command_for_confirmation_email", command)
        self.page.go("/confirm_email")