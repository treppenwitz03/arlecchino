import flet as ft
from flet_route import Params, Basket
from views.abstract_view import AbstractView

class ConfirmEmailView(AbstractView):
    def __init__(self, text_values: dict):
        super().__init__(
            route="/confirm_email",
            padding = 0
        )

        self.text_values = text_values
        #################################
        ## Make the email confirmation page
        ################################

        lock_icon = ft.Lottie(
            src = "https://lottie.host/ca4eb929-dd79-427f-883e-7b4a4929ebb0/gsPrmKK8Ir.json",
            width = 640
        )
        
        image_container = ft.Container(
            expand=True,
            content=lock_icon
        )
        
        self.confirm_email_indicator_text = ft.Text(
            value=text_values["confirm_email"],
            weight=ft.FontWeight.W_700,
            size=54
        )
        
        confirm_email_indicator_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        confirm_email_indicator_row.controls.append(self.confirm_email_indicator_text)
        
        self.code_sent_indicator_text = ft.Text(
            value=text_values["a_code_was_sent"],
            size = 24
        )
        
        code_sent_indicator_text_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.code_sent_indicator_text]
        )
        
        self.code_sent_textfield = ft.TextField(
            label = text_values["code_sent"],
            border_radius = 25,
            expand=True,
            label_style = ft.TextStyle()
        )
        
        code_sent_textfield_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        code_sent_textfield_row.controls.append(self.code_sent_textfield)
        
        self.confirm_email_button = ft.FilledButton(
            width = 250,
            height = 44,
            disabled=True,
            content=ft.Text(
                value=text_values["confirm_email"],
                size=24
            )
        )
        
        confirm_email_btn_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        confirm_email_btn_row.controls.append(self.confirm_email_button)
        
        confirm_email_btn_container = ft.Container(
            content=confirm_email_btn_row
        )
        
        self.login_indicator_text = ft.Text(
            value=text_values["already_have"],
            weight=ft.FontWeight.W_200,
            size=16
        )
        
        login_indicator_text_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.login_indicator_text]
        )
        
        self.login_button = ft.OutlinedButton(
            width = 200,
            height = 44,
            content=ft.Text(
                value=text_values["login_button_text"],
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
        
        sidebar_column_top = ft.Column(
            spacing=20,
            controls = [
                confirm_email_indicator_row,
                code_sent_indicator_text_row,
                code_sent_textfield_row,
                confirm_email_btn_container
            ]
        )
        
        sidebar_column_bottom = ft.Column(
            spacing=20,
            alignment=ft.alignment.bottom_center,
            controls = [
                login_indicator_text_row,
                login_btn_container
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
        
        self.dialog_text = ft.Text(
            size=12
        )
        
        self.warning_dialog = ft.AlertDialog(
            title=ft.Text(
                value=text_values["cant_register"],
                size=20
            ),
            content=self.dialog_text
        )
    
    # get the view for the page
    def get_view(self, page: ft.Page, params: Params, basket: Basket):
        return self
    
    # get the code entered
    def get_code_input(self):
        return self.code_sent_textfield.value
    
    # sets whether the confirmation can proceed
    def allow_confirm(self, allow: bool):
        self.confirm_email_button.disabled = (allow == False)
        self.page.update()
    
    # DIsplays the verdict based on the matching of codes
    def display_on_dialog(self, title: str, message: str):
        self.warning_dialog.title.value = title
        self.dialog_text.value = message
        self.page.dialog = self.warning_dialog
        self.warning_dialog.open = True
        self.page.update()