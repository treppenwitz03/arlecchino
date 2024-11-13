import flet as ft

from services import Database
from views import HomePage
from utils import Preferences

import os

class AppearanceDialogController:
    def __init__(self, page: ft.Page, home_page: HomePage):
        self.page = page
        self.database: Database = page.session.get("database")
        self.home_page = home_page
        self.appearance_dialog = home_page.appearance_dialog
        
        # open dialog
        self.home_page.settings_view.appearance_setting.on_click = self.handle_dialog_open
        
        # handle dark mode change
        self.appearance_dialog.on_change = self.change_darkmode
        self.appearance_dialog.accent_change = self.accent_color_changed
    
    def accent_color_changed(self, event: ft.ControlEvent):
        color = event.control.value
        self.page.client_storage.set("accent_color", color)

        self.page.theme = ft.Theme(color_scheme_seed=color)
        self.page.update()
    
    # change the dark mode setting
    def change_darkmode(self, event: ft.ControlEvent):
        if event.data == "true":
            self.page.client_storage.set("dark_mode", True)
            self.page.theme_mode = ft.ThemeMode.DARK
        else:
            self.page.client_storage.set("dark_mode", False)
            self.page.theme_mode = ft.ThemeMode.LIGHT
        
        self.page.update()
    
    # open the dialog
    def handle_dialog_open(self, event):
        self.appearance_dialog.accent_color_radio.value = self.page.client_storage.get("accent_color")
        self.appearance_dialog.dark_mode_switch.value = bool(self.page.client_storage.get("dark_mode"))
        self.home_page.show_appearance_dialog()

class CurrencyDialogController:
    def __init__(self, page: ft.Page, home_page: HomePage):
        self.page = page
        self.database: Database = page.session.get("database")
        self.home_page = home_page
        self.currency_dialog = home_page.currency_dialog
        self.text_values: dict = page.session.get("text_values")
        
        # handle events
        self.home_page.settings_view.currency_setting.on_click = self.handle_dialog_open
        self.currency_dialog.on_change = self.change_currency
    
    # change the currency according to setting
    def change_currency(self, currency):
        self.page.client_storage.set("currency", currency)
        self.page.snack_bar = ft.SnackBar(ft.Text(self.text_values["currency_change_success"]))
        self.page.snack_bar.open = True
        self.page.update()
    
    # open dialog
    def handle_dialog_open(self, event: ft.ControlEvent):
        self.currency_dialog.currency_choices.value = self.page.client_storage.get("currency")
        self.home_page.show_currency_dialog()

class LanguageDialogController:
    def __init__(self, page: ft.Page, home_page: HomePage):
        self.page = page
        self.database: Database = page.session.get("database")
        self.home_page = home_page
        self.language_dialog = home_page.language_dialog

        self.home_page.settings_view.language_setting.on_click = self.handle_dialog_open
        self.language_dialog.on_change = self.change_language
    
    def handle_dialog_open(self, event):
        self.language_dialog.language_choices.value = self.page.client_storage.get("lang")
        self.home_page.show_language_dialog()
    
    def change_language(self, language):
        if (language == self.page.client_storage.get("lang")):
            return

        self.page.client_storage.set("lang", language)
        self.page.window.close()
        os.system("python main.py")