import flet as ft
from views.abstract_view import AbstractView

class AboutSubView(ft.Container):
    def __init__(self, text_values: dict):
        super().__init__(
            offset=ft.transform.Offset(0, 6),
            animate_offset=ft.animation.Animation(300)
        )

        self.should_clear = False
        self.text_values = text_values
        ###########################################
        ## Make the onboarding UI
        ###########################################

        logo = ft.Image(
            src = "/logo.png",
            width = 300,
            height = 300,
        )
        
        logo_row = ft.Row(
            alignment = ft.MainAxisAlignment.CENTER,
            controls=[logo]
        )

        info_column = ft.Column(
            controls= [
                ft.Text(text_values["developer"], weight=ft.FontWeight.BOLD, size=48),
                ft.Text(text_values["main_dev"], weight=ft.FontWeight.W_700, size=24),
                ft.Text(text_values["dev1"], size=24),
                ft.Text(text_values["dev2"], size=24),
                ft.Text(text_values["dev3"], size=24),
                ft.Text(text_values["dev4"], size=24),
                ft.Text(text_values["based_on"], weight=ft.FontWeight.BOLD, size=48),
                ft.Text(text_values["morax"], size=24),
                ft.Text(text_values["inspired"], weight=ft.FontWeight.BOLD, size=48),
                ft.Text(text_values["arle_from_gi"], size=24),
                ft.Text(text_values["special_thanks"], weight=ft.FontWeight.W_900, size=48),
                ft.Text(text_values["img_own"], size=24),
                ft.Text(text_values["flet_dev"], size=24),
                ft.Text(text_values["genshin"], size=24),
                ft.Text(text_values["neji"], size=24),
                ft.Container(
                    ft.Text(text_values["used_tech"], weight=ft.FontWeight.BOLD, size=48),
                    padding=24
                ),
                ft.Image(
                    "assets/flet.png",
                    width=300,
                    height=300
                ),
                ft.Text(text_values["flet_ui"], weight=ft.FontWeight.BOLD, size=24),
                ft.Image(
                    "assets/python.png",
                    width=300,
                    height=300
                ),
                ft.Text(text_values["python"], weight=ft.FontWeight.BOLD, size=24),
                ft.Image(
                    "assets/firebase.png",
                    width=300,
                    height=300
                ),
                ft.Text(text_values["firebase"], weight=ft.FontWeight.BOLD, size=24),
                ft.Image(
                    "assets/opencv.png",
                    width=300,
                    height=300
                ),
                ft.Text(text_values["opencv"], weight=ft.FontWeight.BOLD, size=24),
                ft.Image(
                    "assets/icons/loading-animation.png",
                    height=600
                ),
                ft.Container(
                    ft.Text(text_values["credits"], weight=ft.FontWeight.BOLD, size=24),
                    padding=ft.padding.only(24, 24, 24, 0)
                ),
                ft.Text(text_values["to_god"], weight=ft.FontWeight.BOLD, size=24),
                ft.Text(text_values["all_rights"], weight=ft.FontWeight.BOLD, size=24),
            ],
            spacing=32,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        self.content = ft.Column(
            controls = [
                logo_row,
                ft.Text(text_values["app_name"], weight=ft.FontWeight.BOLD, size=64),
                ft.Text(text_values["about_app"], 
                        weight=ft.FontWeight.W_400, size=20, width=600),
                ft.Container(info_column, margin=ft.margin.only(0, 64, 0, 64))
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            scroll=ft.ScrollMode.AUTO
        )
    
    def show(self, delta):
        self.offset = ft.transform.Offset(0, delta)
        self.update()