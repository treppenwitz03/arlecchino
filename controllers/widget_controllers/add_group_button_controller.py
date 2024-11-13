from views import HomePage
import flet as ft

class AddGroupButtonController:
    def __init__(self, page: ft.Page, home_page: HomePage):
        self.page = page
        self.home_page = home_page
        self.add_button = home_page.group_listview.add_button

        self.add_button.on_join_group = self.show_join_group_dialog
        self.add_button.on_create_group = self.show_create_group_dialog
        self.add_button.on_search_groups = self.show_search_groups_dialog
        
     # shows the group adding/joining dialog
    def show_join_group_dialog(self, event: ft.ControlEvent):
        self.home_page.show_join_group_dialog()
    
    def show_create_group_dialog(self, event: ft.ControlEvent):
        self.home_page.show_create_group_dialog()
    
    def show_search_groups_dialog(self, event: ft.ControlEvent):
        self.home_page.show_search_groups_dialog()