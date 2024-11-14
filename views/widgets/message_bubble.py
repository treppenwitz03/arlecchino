import flet as ft

class MessageBubble(ft.Row):
    def __init__(self, sender: bool):
        super().__init__()

        self.controls = [ft.Container(
            ft.Text("HELLOWORLD", size=24),
            width = 400,
            height=48,
            padding=ft.padding.all(8),
            border_radius = 16,
            margin=ft.margin.only(8, 0, 8, 8),
            bgcolor= ft.colors.PRIMARY_CONTAINER if sender else ft.colors.SECONDARY_CONTAINER
        )]

        self.expand = True

        if sender == 0:
            self.alignment = ft.MainAxisAlignment.START
        else:
            self.alignment = ft.MainAxisAlignment.END