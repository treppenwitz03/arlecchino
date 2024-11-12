import flet as ft
from views.settings_view_dialogs import *

class SettingsView(ft.Column):
    def __init__(self):
        super().__init__(
            offset=ft.transform.Offset(0, 1.5),
            animate_offset=ft.animation.Animation(300)
        )
        ##############################################################
        ## Make the UI for the Settings view
        ##############################################################
        
        self.top_text = ft.Text(
            expand=True,
            value="Settings",
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
            value="Modify the application's appearance and behavior through the settings below.",
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
        
        self.appearance_setting = SettingButton("Appearance", "Customize the app's visual style and layout to suit your preferences", "")
        self.currency_setting = SettingButton("Currency", "Adjust the currency settings to specify your preferred currency for transactions and display.", "Currently set to: P")
        self.language_setting = SettingButton("Language", "Modify the application language to fill your needs.", "")
        
        setting_list = ft.Column(
            controls=[
                self.appearance_setting,
                self.currency_setting,
                self.language_setting
            ]
        )
        
        self.setting_container = ft.Container(
            setting_list,
            border_radius=15,
            margin=30,
            padding=ft.padding.only(0, 40, 0, 40)
        )
        
        self.controls.append(self.top_text_container)
        self.controls.append(self.subtitle_text_container)
        self.controls.append(self.setting_container)
    
    # dictate whether to show or hide settings
    def show(self, delta):
        self.offset = ft.transform.Offset(0, delta)
        self.update()

class SettingButton(ft.ElevatedButton):
    def __init__(self, setting_name: str, setting_description: str, additonal_state: str):
        super().__init__(
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(16))
        )
        #########################################
        ## Make the UI for the buttons in settings
        #########################################
        
        self.setting_name = ft.Text(
            setting_name,
            size=24,
            weight=ft.FontWeight.W_700
        )
        
        self.setting_with_current = ft.Text(
            additonal_state,
            italic=True,
        )
        
        setting_title_row = ft.Row(
            [self.setting_name]
        )
        
        if additonal_state:
            setting_title_row.controls.append(self.setting_with_current)
        
        self.setting_description = ft.Text(
            setting_description,
            size=14,
            expand=True
        )
        
        self.setting_icon = ft.Icon(
            ft.icons.MORE_HORIZ
        )
        
        bottom_row = ft.Row(
            controls=[self.setting_description]
        )
        
        bottom_row.controls.append(self.setting_icon)
        
        main_column = ft.Column(
            controls=[
                setting_title_row,
                bottom_row
            ],
            spacing=10
        )
        
        self.content = ft.Container(main_column, padding=20)
        self.margin = ft.margin.only(40, 0, 40, 0)