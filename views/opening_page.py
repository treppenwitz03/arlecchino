import flet as ft
from flet_route import Params, Basket
from views.abstract_page import AbstractPage

class OpeningPage(AbstractPage):
    def __init__(self, page):
        super().__init__(
            route = "/",
            padding=ft.padding.all(0)
        )

        self.page = page
        ############################################
        ## Initialize the Opening Page
        ############################################

        logo = ft.Image(
            src = "/logo.png",
            width = 48,
            height = 48
        )

        app_name = ft.Text(
            "Arlecchino",
            weight=ft.FontWeight.W_700,
            size=24
        )

        self.signup_button = ft.ElevatedButton(
            width = 200,
            height = 32,
            content = ft.Text(
                value = "Create Account",
                size = 16
            ),
        )
        
        self.about_button = ft.TextButton(
            "About"
        )

        self.support_button = ft.TextButton(
            "Support"
        )
        
        logo_row = ft.Row(
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row([
                    logo, 
                    app_name, 
                    self.about_button,
                    self.support_button
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                self.signup_button]
        )

        self.login_button = ft.ElevatedButton(
            width = 250,
            height = 48,
            content = ft.Text(
                value = "Login",
                size = 20
            ),
        )

        self.motto_text = ft.Text(
            "Service Tracking, Simplified",
            weight=ft.FontWeight.W_900,
            size=48,
            width=300
        )

        self.sub_text = ft.Text(
            "Arlecchino is a special service appointment system that blends ease of use with functionality.",
            size=16,
            width=300
        )

        main_row = ft.Container(
            ft.Row(
                controls=[
                    ft.Column([
                        self.motto_text,
                        self.sub_text,
                        self.login_button
                    ], spacing=32),
                    ft.Column([ft.Lottie(
                        src="https://lottie.host/53a2afd7-dce6-442a-a174-486a61479fe3/5YSr4u8v83.json",
                        animate=True,
                        width=620,
                    )])
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=50
            ),
            padding=ft.padding.all(50),
            bgcolor="#3E2C31",
            expand=True,
            height=720
        )

        self.controls = [
            ft.Container(
                logo_row,
                padding=ft.padding.only(16, 16, 16, 8)
            ), 
            main_row
        ]
    
    def get_view(self, page: ft.Page, params: Params, basket: Basket):
        return self