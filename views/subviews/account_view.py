import flet as ft

class AccountView(ft.Container):
    def __init__(self):
        ####################################################
        ## Make the UI for the AccountView
        ####################################################
        super().__init__(
            offset=ft.transform.Offset(0, 4.5),
            animate_offset=ft.animation.Animation(300)
        )

        self.top_text = ft.Text(
            expand=True,
            value="Account Center",
            weight=ft.FontWeight.W_600,
            size=54
        )
        
        top_text_row = ft.Row(
            expand=True,
            controls=[self.top_text]
        )
        
        self.top_text_container = ft.Container(
            padding=ft.padding.only(30, 30, 30, 0),
            content=top_text_row
        )

        self.subtitle_text = ft.Text(
            expand=True,
            value="Do you need to change a personal infomation provided? Update through the settings below.",
            weight=ft.FontWeight.W_400,
            size=20
        )

        subtitle_text_row = ft.Row(
            expand=True,
            controls=[self.subtitle_text]
        )

        self.subtitle_text_container = ft.Container(
            padding=ft.padding.only(30, 0, 30, 0),
            content=subtitle_text_row
        )
        
        self.user_picture = ft.Image(
            src = "/empty_user_image.png",
            width=150,
            height=150,
            border_radius=16
        )
        
        user_picture_container = ft.Container(
            self.user_picture,
            border_radius=16,
            padding=32
        )
        
        self.username_text = ft.Text(
            " ",
            size=42,
            weight=ft.FontWeight.BOLD,
        )
        
        self.email_text = ft.Text(
            " ",
            size=28,
        )
        
        user_info_column = ft.Column(
            controls=[self.username_text, self.email_text],
            expand=True
        )
        
        picture_row = ft.Row(
            controls=[
                user_picture_container,
                user_info_column
            ]
        )
        
        profile_info_column = ft.Column(
            controls = [picture_row],
            expand=True
        )
        
        self.profile_info_container = ft.Container(
            profile_info_column,
            border=ft.border.all(1),
            border_radius=16,
            margin=ft.margin.symmetric(36, 50),
            bgcolor=ft.colors.SURFACE_VARIANT
        )
        
        account_labeler = ft.Text(
            "Account",
            size=18,
            weight=ft.FontWeight.BOLD
        )

        self.change_user_picture_button = ft.Container(
            content = ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.VERIFIED_USER_ROUNDED),
                            ft.Text("Change Profile Picture", weight=ft.FontWeight.W_400)
                        ]
                    ),
                    ft.Icon(ft.icons.NAVIGATE_NEXT)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )
        
        self.edit_profile_button = ft.Container(
            content = ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.LOCK),
                            ft.Text("Edit Username", weight=ft.FontWeight.W_400)
                        ]
                    ),
                    ft.Icon(ft.icons.NAVIGATE_NEXT)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )
        
        security_labeler = ft.Text(
            "Security",
            size=18,
            weight=ft.FontWeight.BOLD
        )
        
        self.change_password_button = ft.Container(
            content = ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.LOCK),
                            ft.Text("Change Password", weight=ft.FontWeight.W_400)
                        ]
                    ),
                    ft.Icon(ft.icons.NAVIGATE_NEXT)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )
        
        self.gcash_button = ft.Container(
            content = ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.ATTACH_MONEY),
                            ft.Text("GCash", weight=ft.FontWeight.W_400)
                        ]
                    ),
                    ft.Icon(ft.icons.NAVIGATE_NEXT)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )
        
        account_settings_column = ft.Column(
            controls=[
                account_labeler,
                self.edit_profile_button,
                self.change_user_picture_button,
                security_labeler,
                self.change_password_button,
                self.gcash_button
            ],
            spacing=16,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        )
        
        self.account_settings_container = ft.Container(
            account_settings_column,
            expand=True,
            padding=ft.padding.symmetric(0, 75)
        )
        
        self.logout_button = ft.ElevatedButton(
            "Log Out",
            width=200,
            height=36
        )
        
        logout_column = ft.Column(
            controls=[
                ft.Row(
                    [self.logout_button],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        )
        
        self.logout_button_container = ft.Container(
            logout_column,
            expand=True
        )
        
        self.content = ft.Column(
            [self.top_text_container, self.subtitle_text_container, self.profile_info_container, self.account_settings_container, self.logout_button_container],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing=0,
            scroll=ft.ScrollMode.ALWAYS
        )
    
    # Dictates whether the page will show or hide
    def show(self, delta):
        self.offset = ft.transform.Offset(0, delta)
        self.update()
    
    def update_informations(self):
        pass

    # make a callback to trigger reload
    def trigger_reload(self):
        pass