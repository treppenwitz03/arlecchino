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
                ft.Text("Developer", weight=ft.FontWeight.BOLD, size=48),
                ft.Text("Owen David P. Malicsi - (Arlecchino and MORAX)", weight=ft.FontWeight.W_700, size=24),
                ft.Text("Emmanuel James H. Comprendio - (MORAX)", size=24),
                ft.Text("Achilles Maximus M. Fernandez - (MORAX)", size=24),
                ft.Text("Ralph John H. Paña - (MORAX)", size=24),
                ft.Text("Tristan Kirby E. Torino - (MORAX)", size=24),
                ft.Text("Based on", weight=ft.FontWeight.BOLD, size=48),
                ft.Text("MORAX", size=24),
                ft.Text("Inspired from", weight=ft.FontWeight.BOLD, size=48),
                ft.Text("Arlecchino fo Genshin Impact", size=24),
                ft.Text("Special Thanks to:", weight=ft.FontWeight.W_900, size=48),
                ft.Text("Image owners", size=24),
                ft.Text("Flet developers", size=24),
                ft.Text("Genshin Impact for the inspiration", size=24),
                ft.Text("THAT GIRL FROM M.E. FOR THE EXTRA INSPIRATION", size=24),
                ft.Container(
                    ft.Text("Technologies Used", weight=ft.FontWeight.BOLD, size=48),
                    padding=24
                ),
                ft.Image(
                    "assets/flet.png",
                    width=300,
                    height=300
                ),
                ft.Text("FLET - UI Toolkit", weight=ft.FontWeight.BOLD, size=24),
                ft.Image(
                    "assets/python.png",
                    width=300,
                    height=300
                ),
                ft.Text("Python - Programming Language", weight=ft.FontWeight.BOLD, size=24),
                ft.Image(
                    "assets/firebase.png",
                    width=300,
                    height=300
                ),
                ft.Text("Firebase - Database", weight=ft.FontWeight.BOLD, size=24),
                ft.Image(
                    "assets/opencv.png",
                    width=300,
                    height=300
                ),
                ft.Text("OpenCV - Image Processing", weight=ft.FontWeight.BOLD, size=24),
                ft.Image(
                    "assets/icons/loading-animation.png",
                    height=600
                )
            ],
            spacing=32,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        self.content = ft.Column(
            controls = [
                logo_row,
                ft.Text(text_values["app_name"], weight=ft.FontWeight.BOLD, size=64),
                ft.Text("        Arlecchino is based on MORAX, the project I shared with my friends during our 2nd year days. It was originally designed to be a shared financial manager for groups of people, but I improved it so it fits into the theme of Techtopia. I got their permission before passing this project as I was the lead developer back then. This is the improved version of MORAX with my own personal touch and perspectives reflecting the application.", 
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