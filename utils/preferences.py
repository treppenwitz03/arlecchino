import flet as ft
import asyncio

class Preferences:
    def __init__(self, page: ft.Page):
        self.page = page

        if page.client_storage.get("currency") is None:
            page.client_storage.set("currency", "PHP")
        if page.client_storage.get("dark_mode") is None:
            page.client_storage.set("dark_mode", False)
        if page.client_storage.get("accent_color") is None:
            page.client_storage.set("accent_color", "#8C161E")
        
        if bool(self.get_preference("dark_mode")):
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
    
    def set_preference(self, key: str, value: any):
        try:
            result = self.page.client_storage.set(key, value)
            return result
        except:
            #never surrender
            self.set_preference(key, value)
    
    def get_preference(self, key: str, default_value: any = None):
        try:
            result = self.page.client_storage.get(key)
            return result
        except KeyError:
            self.set_preference(key, default_value)
            return self.get_preference(key, default_value)
        except:
            return self.get_preference(key, default_value)