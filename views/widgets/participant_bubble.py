import flet as ft

class ParticipantBubble(ft.Container):
    def __init__(self, username: str, email: str, image: str):
        super().__init__()

        leading = ft.Image(src_base64=image, width=64, height=64)
        title = ft.Column([
            ft.Text(username, size=20),
            ft.Text(email, size=12)
        ], spacing=8, alignment=ft.MainAxisAlignment.CENTER)

        self.expand= True
        self.height=96
        self.padding=ft.padding.all(8)
        self.margin = ft.margin.only(16, 0, 16, 8)
        self.border_radius = 16
        self.bgcolor= ft.colors.SURFACE_VARIANT

        self.content = ft.Row([leading, title], vertical_alignment=ft.CrossAxisAlignment.CENTER, expand=True)