import flet as ft
from flet_route import Params, Basket
from views.abstract_page import AbstractPage

class OpeningPage(AbstractPage):
    def __init__(self, text_values: dict):
        super().__init__(
            route="/",
            padding=ft.padding.all(0)
        )

        self.text_values = text_values
        ############################################
        ## Initialize the Opening Page
        ############################################

        logo = ft.Image(
            src="/logo.png",
            width=48,
            height=48
        )

        app_name = ft.Text(
            text_values["app_name"],
            weight=ft.FontWeight.W_700,
            size=24
        )

        self.signup_button = ft.ElevatedButton(
            width=200,
            height=32,
            content=ft.Text(
                value=text_values["signup_button_text"],
                size=16
            ),
        )
        
        self.about_button = ft.TextButton(
            text_values["about_button_text"]
        )

        self.support_button = ft.TextButton(
            text_values["support_button_text"]
        )
        
        logo_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
            width=250,
            height=48,
            content=ft.Text(
                value=text_values["login_button_text"],
                size=20
            ),
        )

        self.motto_text = ft.Text(
            text_values["motto_text"],
            weight=ft.FontWeight.W_900,
            size=48,
            width=300
        )

        self.sub_text = ft.Text(
            text_values["sub_text"],
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
                        height=400
                    )])
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=50
            ),
            padding=ft.padding.all(50),
            bgcolor=ft.colors.SURFACE_VARIANT,
            expand=True,
            expand_loose=True
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