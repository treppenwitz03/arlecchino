import flet as ft
from views.abstract_page import AbstractPage
from utils import Utils

class ChatPage(AbstractPage):
    def __init__(self, text_values: dict):
        super().__init__(
            route="/chat",
            padding = 0
        )

        self.appbar = ft.AppBar(
            ft.IconButton(
                ft.icons.EXIT_TO_APP_ROUNDED,
                icon_size=48
            ),
            title=ft.Text("Chat Room", size=36, weight=ft.FontWeight.W_900)
        )

        colors = [ft.colors.LIGHT_BLUE, ft.colors.LIGHT_GREEN, ft.colors.ORANGE, ft.colors.PURPLE, ft.colors.PINK, ft.colors.AMBER]
        
        self.controls = [self.appbar, ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            height=500
        )]

        for x in range(0, 6):
            control = ft.Card(
                ft.Container(
                    ft.Text(Utils.generate_greeting("en"), width=160, height=90),
                    bgcolor=colors[x]
                )
            )

            self.controls[1].controls.append(control)
    
    def get_view(self, page: ft.Page, params, basket):
        return self