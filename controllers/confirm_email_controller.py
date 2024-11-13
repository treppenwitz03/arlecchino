from models import User
from services import Database
from views import ConfirmEmailPage
import flet as ft

class ConfirmEmailController:
    def __init__(self, page: ft.Page, confirm_email_page: ConfirmEmailPage):
        self.page = page
        self.confirm_email_page = confirm_email_page

        self.text_values: dict = self.page.session.get("text_values")
        self.database: Database = self.page.session.get("database")
        
        # handle the events in confirm email page
        self.confirm_email_page.code_sent_textfield.on_change = self.validate
        self.confirm_email_page.login_button.on_click = self.go_to_login
        self.confirm_email_page.confirm_email_button.on_click = self.confirm_email
    
    # validate whether the fields are filled
    def validate(self, event):
        if self.confirm_email_page.get_code_input() != "":
            self.confirm_email_page.allow_confirm(True)
        else:
            self.confirm_email_page.allow_confirm(False)
    
    # go to login page
    def go_to_login(self, event):
        self.page.go("/login")

    # confirm the email
    def confirm_email(self, event):
        argument_list = self.page.session.get("command_for_confirmation_email")
        command_type = argument_list[0]
        code = argument_list[1]
        if code == int(self.confirm_email_page.code_sent_textfield.value): # if the confirmation is requested by register
            if command_type == "COMMAND_REGISTER":
                self.register(argument_list)
            elif command_type == "COMMAND_CHANGE_PASSWORD": # if the confirmation is requested by password change
                self.change_password(argument_list)
            else:
                self.confirm_email_page.display_on_dialog(self.text_values["cant_do_operation"], self.text_values["process_unexpected"])
        else:
            if command_type == "COMMAND_REGISTER":
                self.confirm_email_page.display_on_dialog(self.text_values["cant_register"], self.text_values["code_mismatch"])
            elif command_type == "COMMAND_CHANGE_PASSWORD":
                self.confirm_email_page.display_on_dialog(self.text_values["cant_change_pw"], self.text_values["code_mismatch"])
    
    # register
    def register(self, argument_list: list):
        email = str(argument_list[2])

        user: User = None
        for user in self.database.users:
            if user.email == email:
                self.confirm_email_page.display_on_dialog(self.text_values["cant_register"], self.text_values["account_exists"])
                return

        new_user = User(
            email=email,
            first_run=True,
            gcash_number="",
            password=str(argument_list[4]),
            picture_link="",
            qr_image_id="",
            username=str(argument_list[3])
        )

        self.database.update_user(new_user)
        self.page.go("/login")
        self.page.snack_bar = ft.SnackBar(ft.Text(self.text_values["success_account_reg"]))
        self.page.snack_bar.open = True
        self.page.update()
    
    # change the password
    def change_password(self, argument_list: list):
        email = str(argument_list[2])

        user: User = None
        for user in self.database.users:
            if user.email == email:
                user.password = str(argument_list[3])
                self.database.update_user(user)

                self.page.go("/login")
                self.page.snack_bar = ft.SnackBar(ft.Text(self.text_values["success_pw_change"]))
                self.page.snack_bar.open = True
                self.page.update()
                return

        self.confirm_email_page.display_on_dialog(self.text_values["cant_change_pw"], self.text_values["account_doesnt_exist"])