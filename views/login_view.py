import flet as ft
from flet_route import Params, Basket
from views.abstract_view import AbstractView

class LoginView(AbstractView):
    def __init__(self, text_values: dict):
        super().__init__(
            route="/login",
            padding = 0
        )

        self.text_values = text_values
        #####################################
        ## Make the Login UI
        #####################################

        lock_icon = ft.Lottie(
            src = "https://lottie.host/6cc07241-1a2e-4d42-8e29-f58dd320eb87/RvVs4V1MYu.json",
            width = 640
        )
        
        image_container = ft.Container(
            expand=True,
            content=lock_icon
        )
        
        self.login_indicator_text = ft.Text(
            value=self.text_values["login_indicator_text"],
            weight=ft.FontWeight.W_700,
            size=54
        )
        
        login_indicator_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        login_indicator_row.controls.append(self.login_indicator_text)
        
        self.welcome_back_text = ft.Text(
            self.text_values["welcome_back_text"],
            size = 24
        )
        
        welcome_back_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        welcome_back_row.controls.append(self.welcome_back_text)
        
        self.email_textfield = ft.TextField(
            label = self.text_values["email_username_label"],
            border_radius = 25,
            expand=True,
            label_style = ft.TextStyle()
        )
        
        email_textfield_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        email_textfield_row.controls.append(self.email_textfield)
        
        # Make sure the password field is hidden
        self.password_textfield = ft.TextField(
            label = self.text_values["password_label"],
            border_radius = 25,
            expand=True,
            password=True,
            can_reveal_password=True,
            label_style = ft.TextStyle()
        )
        
        password_textfield_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        password_textfield_row.controls.append(self.password_textfield)
        
        self.keep_logged_check = ft.Checkbox(
            value=False
        )
        
        keep_logged_indicator_text = ft.Text(
            value=self.text_values["keep_logged_text"],
            expand=True
        )
        
        self.forgot_password_text = ft.Text(
            self.text_values["forgot_password_text"]
        )
        
        self.forgot_password_btn = ft.Container(
            content=self.forgot_password_text
        )
        
        keep_logged_check_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.keep_logged_check, keep_logged_indicator_text, self.forgot_password_btn]
        )
        
        self.login_btn = ft.FilledButton(
            width = 200,
            height = 44,
            disabled=True,
            content=ft.Text(
                value=self.text_values["login_btn_text"],
                size=24
            )
        )
        
        login_btn_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        login_btn_row.controls.append(self.login_btn)
        
        login_btn_container = ft.Container(
            content=login_btn_row,
            margin=20
        )
        
        self.signup_indicator_text = ft.Text(
            value=self.text_values["signup_indicator_text"],
            weight=ft.FontWeight.W_200,
            size=16
        )
        
        signup_indicator_text_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.signup_indicator_text]
        )
        
        self.signup_button = ft.OutlinedButton(
            width = 200,
            height = 44,
            content=ft.Text(
                value=self.text_values["signup_button_text"],
                size=24
            )
        )
        
        signup_btn_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        signup_btn_row.controls.append(self.signup_button)
        
        signup_btn_container = ft.Container(
            content=signup_btn_row
        )
        
        sidebar_column_top = ft.Column(
            spacing=20,
            controls = [
                login_indicator_row,
                welcome_back_row,
                email_textfield_row,
                password_textfield_row,
                keep_logged_check_row,
                login_btn_container,
            ]
        )
        
        sidebar_column_bottom = ft.Column(
            spacing=20,
            alignment=ft.alignment.bottom_center,
            controls = [
                signup_indicator_text_row,
                signup_btn_container
            ]
        )
        
        sidebar_main_column = ft.Column(
            controls=[sidebar_column_top,sidebar_column_bottom],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        self.sidebar_container = ft.Container(
            expand = True,
            content = sidebar_main_column,
            padding = 40,
            bgcolor=ft.colors.SURFACE_VARIANT
        )
        
        main_row = ft.Row(
            expand=True,
            controls = [
                image_container,
                self.sidebar_container
            ]
        )
        
        self.main_container = ft.Container(
            expand=True,
            content=main_row
        )

        self.controls = [self.main_container]
        
        ###### DIALOGS ######
        self.dialog_text = ft.Text(
            size=12
        )
        
        self.warning_dialog = ft.AlertDialog(
            title=ft.Text(
                value=self.text_values["dialog_title"],
                size=20
            ),
            content=self.dialog_text
        )
    
    def get_view(self, page: ft.Page, params: Params, basket: Basket):
        return self
    
    # Returns the state of keep_logged_in
    def get_keep_signed_in(self):
        return self.keep_logged_check.value
    
    # Returns the entered email
    def get_email_entry(self):
        return self.email_textfield.value
    
    # Returns the entered password
    def get_password_entry(self):
        return self.password_textfield.value
    
    # Sets whether the login button can be clicked
    def allow_login(self, allow: bool):
        self.login_btn.disabled = (allow == False)
        self.page.update()
    
    # Display dialog depending on the message
    def display_on_dialog(self, message: str):
        self.dialog_text.value = message
        self.page.dialog = self.warning_dialog
        self.warning_dialog.open = True
        self.page.update()