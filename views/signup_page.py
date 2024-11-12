import flet as ft
from flet_route import Params, Basket
from views.abstract_page import AbstractPage

class SignupPage(AbstractPage):
    def __init__(self, text_values: dict):
        super().__init__(
            route="/signup",
            padding = 0
        )

        self.text_values = text_values
        #####################################
        ## Make the Signup UI
        #####################################

        query_icon = ft.Lottie(
            src = "https://lottie.host/6cc07241-1a2e-4d42-8e29-f58dd320eb87/RvVs4V1MYu.json",
            width = 640
        )
        
        image_container = ft.Container(
            expand=True,
            content=query_icon
        )
        
        self.signup_indicator_text = ft.Text(
            value=text_values["signup_button_text"],
            weight=ft.FontWeight.W_700,
            size=54
        )
        
        signup_indicator_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        signup_indicator_row.controls.append(self.signup_indicator_text)
        
        self.welcome_back_text = ft.Text(
            text_values["fill_info_text"],
            size = 24
        )
        
        welcome_back_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        welcome_back_row.controls.append(self.welcome_back_text)
        
        self.email_textfield = ft.TextField(
            label = text_values["email_label"],
            border_radius = 25,
            cursor_height=20,
            expand = True,
            height=44,
            label_style = ft.TextStyle()
        )
        
        email_textfield_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        email_textfield_row.controls.append(self.email_textfield)
        
        self.username_textfield = ft.TextField(
            label = text_values["username_label"],
            border_radius = 25,
            cursor_height=20,
            expand = True,
            height=44,
            label_style = ft.TextStyle()
        )
        
        username_textfield_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        username_textfield_row.controls.append(self.username_textfield)
        
        self.password_textfield = ft.TextField(
            label = text_values["password_label"],
            border_radius = 25,
            cursor_height=20,
            expand = True,
            height=44,
            password=True,
            can_reveal_password=True,
            label_style = ft.TextStyle()
        )
        
        password_textfield_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        password_textfield_row.controls.append(self.password_textfield)
        
        self.confirm_password_textfield = ft.TextField(
            label = text_values["confirm_password_label"],
            border_radius = 25,
            expand = True,
            height=44,
            cursor_height=20,
            password=True,
            can_reveal_password=True,
            label_style = ft.TextStyle()
        )
        
        confirm_password_textfield_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        confirm_password_textfield_row.controls.append(self.confirm_password_textfield)
        
        self.agree_eula_check = ft.Checkbox(
            value=False
        )
        
        self.agree_eula_indicator_button = ft.TextButton(
            content=ft.Text(
                text_values["i_agree"],
                spans=[
                    ft.TextSpan(text_values["terms_and_conditions"], style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)),
                    ft.TextSpan(text_values["of_using"])
                ],
                size=14
            ),
            expand=True
        )
        
        agree_eula_check_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[ self.agree_eula_check,  self.agree_eula_indicator_button]
        )
        
        self.register_btn = ft.ElevatedButton(
            width = 200,
            height = 44,
            disabled=True,
            content=ft.Text(
                value=text_values["signup_button_text"],
                size=24
            )
        )
        
        register_btn_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        register_btn_row.controls.append(self.register_btn)
        
        register_btn_container = ft.Container(
            content=register_btn_row
        )
        
        self.login_indicator_text = ft.Text(
            value=text_values["already_have"],
            size=16
        )
        
        login_indicator_text_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.login_indicator_text]
        )
        
        self.login_button = ft.ElevatedButton(
            width = 200,
            height = 44,
            content=ft.Text(
                value=text_values["login_btn_text"],
                size=24
            )
        )
        
        login_btn_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        login_btn_row.controls.append(self.login_button)
        
        login_btn_container = ft.Container(
            content=login_btn_row
        )
        
        sidebar_top_column = ft.Column(
            expand=True,
            spacing=20,
            controls = [
                signup_indicator_row,
                welcome_back_row,
                email_textfield_row,
                username_textfield_row,
                password_textfield_row,
                confirm_password_textfield_row,
                agree_eula_check_row,
                register_btn_container
            ]
        )
        
        sidebar_bottom_column = ft.Column(
            spacing=20,
            controls= [
                login_indicator_text_row,
                login_btn_container
            ]
        )
        
        sidebar_main_column = ft.Column(
            controls=[sidebar_top_column, sidebar_bottom_column],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        self.sidebar_container = ft.Container(
            expand = True,
            padding = 40,
            content = sidebar_main_column,
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
    
    # Get the email entered
    def get_email_entry(self):
        return self.email_textfield.value
    
    # get the username entered
    def get_username_entry(self):
        return self.username_textfield.value
    
    # get the password entered
    def get_password_entry(self):
        return self.password_textfield.value
    
    # get the password confirmation entered
    def get_confirm_password_entry(self):
        return self.confirm_password_textfield.value
    
    # get the state of agreeing on EULA
    def get_agree_eula_entry(self):
        return self.agree_eula_check.value
    
    # get the view for the page
    def get_view(self, page: ft.Page, params: Params, basket: Basket):
        return self
    
    # sets whether registration is allowed
    def allow_register(self, allow: bool):
        self.register_btn.disabled = (allow == False)
        self.page.update()