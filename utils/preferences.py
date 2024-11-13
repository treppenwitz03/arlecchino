import flet as ft
import asyncio

class Preferences:
    def __init__(self, page: ft.Page):
        self.page = page

        # if page.client_storage.get("currency") is None:
        #     page.client_storage.set("currency", "PHP")
        # if page.client_storage.get("dark_mode") is None:
        #     page.client_storage.set("dark_mode", False)

        # if bool(page.client_storage.get("dark_mode")):
        #     page.theme_mode = ft.ThemeMode.DARK
        # else:
        #     page.theme_mode = ft.ThemeMode.LIGHT

        # if page.client_storage.get("accent_color") is None:
        #     page.client_storage.set("accent_color", "#8C161E")
    
    async def set_preference(self, key: str, value: any):
        try:
            result = await self.page.client_storage.set(key, value)
            return result
        except:
            #never surrender
            await asyncio.sleep(1)
            self.set_preference(key, value)
    
    async def get_preference(self, key: str, default_value: any):
        try:
            result = await self.page.client_storage.get(key)
            return result
        except:
            self.set_preference(key, default_value)
            await asyncio.sleep(1)
            return self.get_preference(key)