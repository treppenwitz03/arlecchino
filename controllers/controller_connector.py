import flet as ft

class ControllerConnector:
    @staticmethod
    def get_email(page: ft.Page) -> str:
        return page._get_attr("email")
    
    @staticmethod
    def set_email(page: ft.Page, email):
        page._set_attr("email", email)