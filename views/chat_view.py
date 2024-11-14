import flet as ft
from views.abstract_view import AbstractView
from views.widgets.message_bubble import MessageBubble
from views.widgets.participant_bubble import ParticipantBubble
from utils import Utils

class ChatView(AbstractView):
    def __init__(self, text_values: dict):
        super().__init__(
            route="/chat",
            padding = 0
        )

        self.text_values = text_values
        ############################################
        ## Initialize the Opening View
        ############################################

        self.back_button = ft.IconButton(
            ft.icons.ARROW_BACK_ROUNDED,
            width=48,
            height=48
        )

        participants_text = ft.Text(
            "Group Participants",
            weight=ft.FontWeight.W_700,
            size=24,
            width=256
        )

        chat_text = ft.Text(
            "Chat with the Service Provider",
            weight=ft.FontWeight.W_700,
            size=24
        )
        
        logo_row = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.back_button, 
                participants_text,
            ]
        )

        chat_top_row = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                chat_text
            ],
            height=48
        )

        self.messages_box = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS, auto_scroll=True, spacing=0)

        main_row = ft.Container(
            ft.Row([self.messages_box], expand=True),
            bgcolor=ft.colors.SURFACE_VARIANT,
            margin=ft.margin.only(0, 0, 8, 0),
            expand=True
        )

        self.chat_box = ft.TextField(
            "Send a message...",
            expand=True,
            border_radius=32,
            border_color=ft.colors.ON_SURFACE
        )

        self.send_button = ft.IconButton(
            ft.icons.SEND_ROUNDED,
            ft.colors.PRIMARY,
            48
        )
        
        chat_row = ft.Row(
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[ 
                self.chat_box,
                self.send_button
            ],
            height=80
        )

        self.participants_column = ft.Column(
            width=300, 
            spacing=8,
        )

        self.controls = [
            ft.Row([
                ft.Column([
                    ft.Container(
                        logo_row,
                        padding=ft.padding.only(16, 16, 16, 8)
                    ),
                    self.participants_column
                ], width=300),
                ft.VerticalDivider(1),
                ft.Column([
                    ft.Container(
                        chat_top_row,
                        padding=ft.padding.only(16, 16, 16, 8)
                    ),
                    ft.Column([
                        main_row,
                        chat_row,
                    ], 
                    expand=True)
                ], expand=True)
            ], expand=True)
        ]
    
    def get_view(self, page: ft.Page, params, basket):
        self.chat_page_drawn()
        return self
    
    def chat_page_drawn(self):
        pass

    def add_participant(self, username, email, image, current_user: bool):
        new_bubble = ParticipantBubble(username, email, image)
        if current_user:
            self.participants_column.controls.insert(0, new_bubble)
            return
        
        self.participants_column.controls.append(0, new_bubble)