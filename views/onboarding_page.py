import flet as ft
from flet_route import Params, Basket
from views.abstract_page import AbstractPage

class OnboardingPage(AbstractPage):
    def __init__(self, text_values: dict):
        super().__init__(
            route = "/onboarding",
            vertical_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            padding=30
        )

        self.should_clear = False
        self.text_values = text_values
        ###########################################
        ## Make the onboarding UI
        ###########################################

        logo = ft.Image(
            src = "/logo.png",
            width = 200,
            height = 200,
        )
        
        logo_row = ft.Row(
            alignment = ft.MainAxisAlignment.CENTER,
            controls=[logo]
        )
        
        self.help_button = SupportButton(ft.icons.HELP_OUTLINED, text_values["help_button"])
        self.contribute_button = SupportButton(ft.icons.SETTINGS_ACCESSIBILITY, text_values["contribute_button"])
        
        options_column = ft.Column(
            controls=[self.help_button, self.contribute_button],
            horizontal_alignment=ft.CrossAxisAlignment.START
        )
        
        self.main_column = ft.Column(
            controls = [
                logo_row,
                ft.Text(text_values["welcome_message"], weight=ft.FontWeight.BOLD, size=44),
                ft.Text(text_values["description_message"], weight=ft.FontWeight.W_400, size=20),
                ft.Container(options_column, padding=ft.padding.only(30, 60, 30, 60))
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=0,
            offset=ft.transform.Offset(0, 0),
            animate_offset=ft.animation.Animation(300)
        )
        
        gcash_logo = ft.Image(
            "/gcash.png",
            width = 200,
            height = 200,
            color=ft.colors.BLUE
        )
        
        gcash_logo_row = ft.Row(
            alignment = ft.MainAxisAlignment.CENTER,
            controls=[gcash_logo]
        )
        
        self.qr_image = ft.Image(
            "/sample_qr.png",
            width=100,
            height=100,
            color=ft.colors.ON_SURFACE
        )
        
        self.qr_upload_button = ft.ElevatedButton(
            width = 200,
            height = 44,
            content=ft.Text(
                value=text_values["upload_qr_button"],
                size=12
            )
        )
        
        qr_column = ft.Column(
            controls=[self.qr_image, self.qr_upload_button],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
        
        number_label = ft.Text(
            text_values["gcash_mobile_number_label"],
            weight=ft.FontWeight.W_600
        )
        
        self.number_textfield = ft.TextField(
            label=text_values["enter_number_placeholder"],
            border_radius = 25,
            content_padding=10
        )
        
        number_column = ft.Column(
            controls=[number_label, self.number_textfield],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
        
        options_row = ft.Row(
            controls=[qr_column, number_column],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=50
        )
        
        self.gcash_column = ft.Column(
            controls = [
                gcash_logo_row,
                ft.Text(text_values["update_profile_title"], weight=ft.FontWeight.BOLD, size=44),
                ft.Text(text_values["profile_picture_instruction_1"], weight=ft.FontWeight.W_400, size=20),
                ft.Container(options_row, padding=ft.padding.only(30, 60, 30, 60))
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=0,
            offset=ft.transform.Offset(1, 0),
            animate_offset=ft.animation.Animation(300)
        )
        
        profile_logo = ft.Image(
            src = "/logo_filled.png",
            width = 200,
            height = 200,
        )
        
        profile_logo_row = ft.Row(
            alignment = ft.MainAxisAlignment.CENTER,
            controls=[profile_logo]
        )
        
        self.user_image = ft.Image(
            "/empty_user_image.png",
            width=100,
            height=100
        )
        
        self.profile_upload_button = ft.ElevatedButton(
            width = 150,
            height = 32,
            content=ft.Text(
                value=text_values["upload_photo_button"],
                size=12
            )
        )
        
        profile_upload_column = ft.Column(
            controls=[self.user_image, self.profile_upload_button],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        self.profile_column = ft.Column(
            controls = [
                profile_logo_row,
                ft.Text(text_values["update_profile_title"], weight=ft.FontWeight.BOLD, size=44),
                ft.Text(text_values["profile_picture_instruction_2"], weight=ft.FontWeight.W_400, size=20),
                ft.Container(profile_upload_column, padding=ft.padding.only(30, 60, 30, 60))
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=0,
            offset=ft.transform.Offset(2, 0),
            animate_offset=ft.animation.Animation(300)
        )
        
        switcher = ft.Stack(
            controls=[self.main_column, self.gcash_column, self.profile_column]
        )
        
        self.next_button = ft.ElevatedButton(
            text_values["next_button"],
            width=200,
        )
        
        navigation_row = ft.Row(
            controls=[
                ft.Container(self.next_button, padding=16)
            ],
            alignment=ft.MainAxisAlignment.END
        )
        
        self.controls = [switcher, navigation_row]
    
    # get view for the page
    def get_view(self, page: ft.Page, params: Params, basket: Basket):
        return self

class SupportButton(ft.Container):
    def __init__(self, icon_name: ft.icons, button_name: str):
        super().__init__()
        self.icon = ft.Icon(icon_name, size=32)
        self.text = ft.Text(button_name, weight=ft.FontWeight.W_400, size=16, width=200)
        
        self.content = ft.Row(
            controls = [self.icon, self.text],
            alignment=ft.MainAxisAlignment.CENTER
        )
