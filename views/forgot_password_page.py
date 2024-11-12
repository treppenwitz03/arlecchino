import flet as ft
from flet_route import Params, Basket
from views.abstract_page import AbstractPage

class ForgotPasswordPage(AbstractPage):
    def __init__(self, text_values: dict):
        super().__init__(
            route="/forgot_password",
            padding = 0
        )

        self.text_values = text_values
        #######################################
        ## MAke the forgot password UI
        #######################################

        query_icon = ft.Lottie(
            src = "https://lottie.host/bfe86450-2c5b-4ec2-bfe5-3d05e28a85f7/y8UFnI7Ksb.json",
            width = 640
        )
        
        image_container = ft.Container(
            expand=True,
            content=query_icon
        )
        
        self.fg_pass_indicator_text = ft.Text(
            value=text_values["oh_no"],
            weight=ft.FontWeight.W_700,
            size=54
        )
        
        fg_pass_indicator_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        fg_pass_indicator_row.controls.append(self.fg_pass_indicator_text)
        
        self.fg_pass_reminder_text = ft.Text(
            text_values["create_memorable"],
            size = 24
        )
        
        fg_pass_reminder_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        fg_pass_reminder_row.controls.append(self.fg_pass_reminder_text)
        
        self.email_textfield = ft.TextField(
            label = text_values["email_label"],
            border_radius = 25,
            expand=True,
            height=44,
            cursor_height=20,
            label_style = ft.TextStyle()
        )
        
        email_textfield_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        email_textfield_row.controls.append(self.email_textfield)
        
        self.new_password_textfield = ft.TextField(
            label = text_values["new_password"],
            border_radius = 25,
            cursor_height=20,
            expand = True,
            height=44,
            password=True,
            can_reveal_password=True,
            label_style = ft.TextStyle()
        )
        
        new_password_textfield_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        new_password_textfield_row.controls.append(self.new_password_textfield)
        
        self.confirm_new_password_textfield = ft.TextField(
            label = text_values["confirm_password_label"],
            border_radius = 25,
            expand = True,
            height=44,
            cursor_height=20,
            password=True,
            can_reveal_password=True,
            label_style = ft.TextStyle()
        )
        
        confirm_new_password_textfield_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        confirm_new_password_textfield_row.controls.append(self.confirm_new_password_textfield)
        
        self.change_password_btn = ft.ElevatedButton(
            width = 250,
            height = 44,
            disabled=True,
            content=ft.Text(
                value=text_values["change_your_password"],
                size=18
            )
        )
        
        change_password_btn_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        change_password_btn_row.controls.append(self.change_password_btn)
        
        change_password_btn_container = ft.Container(
            content=change_password_btn_row
        )
        
        self.signup_indicator_text = ft.Text(
            value=text_values["dont_have_account"],
            weight=ft.FontWeight.W_200,
            size=16
        )
        
        signup_indicator_text_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.signup_indicator_text]
        )
        
        self.signup_button = ft.ElevatedButton(
            width = 200,
            height = 44,
            content=ft.Text(
                value=text_values["signup_button_text"],
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
        
        sidebar_top_column = ft.Column(
            expand=True,
            spacing=20,
            controls = [
                fg_pass_indicator_row,
                fg_pass_reminder_row,
                email_textfield_row,
                new_password_textfield_row,
                confirm_new_password_textfield_row,
                change_password_btn_container
            ]
        )
        
        sidebar_bottom_column = ft.Column(
            spacing=20,
            controls= [
                signup_indicator_text_row,
                signup_btn_container
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

    
    # Make the view for the page
    def get_view(self, page: ft.Page, params: Params, basket: Basket):
        return self
    
    # get entered email
    def get_email_to_send_entry(self):
        return self.email_textfield.value

    # get entered password
    def get_new_password_entry(self):
        return self.new_password_textfield.value
    
    # get the entered password confirmation
    def get_confirm_new_password_entry(self):
        return self.confirm_new_password_textfield.value
    
    # allow changing of password
    def allow_password_change(self, allow: bool):
        self.change_password_btn.disabled = (allow == False)
        self.page.update()
    
    def update_texts(self, texts):
        return super().update_texts(texts)