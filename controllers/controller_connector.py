import flet as ft

class ControllerConnector:
    @staticmethod
    def get_email(page: ft.Page) -> str:
        return page._get_attr("email")
    
    @staticmethod
    def set_email(page: ft.Page, email):
        page._set_attr("email", email)
    
    @staticmethod
    def get_group_buttons(page: ft.Page) -> dict:
        return page._get_attr("group_buttons")
    
    @staticmethod
    def set_group_buttons(page: ft.Page, group_buttons: dict):
        page._set_attr("group_buttons", group_buttons)
    
    @staticmethod
    def set_command_for_email_confirmation(page: ft.Page, command: list):
        page._set_attr("command", command)
    
    @staticmethod
    def get_command_for_email_confirmation(page: ft.Page) -> list:
        return page._get_attr("command")