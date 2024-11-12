import flet as ft

class PaidUserButton(ft.Container):
    def __init__(self, email: str, text_values: dict):
        super().__init__()
        # Make the UI for the buttons per paid user
        image = ft.Icon(ft.icons.PERSON, size=32)
        user_label = ft.Text(
            email
        )

        self.reject_button = ft.IconButton(
            ft.icons.REMOVE_CIRCLE_OUTLINE
        )

        self.show_proof_button = ft.Container(
            ft.Row(
                [image, user_label]
            )
        )

        row = ft.Row(
            controls=[self.show_proof_button, self.reject_button],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        self.content = row
        self.padding = 10
        self.border_radius = 15
        self.tooltip = text_values["proof_tooltip"]