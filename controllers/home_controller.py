from services import Database
from utils import Preferences
from views import *

import flet as ft

class HomeController:
    code_validated = False
    image_path = ""
    def __init__(self, page: ft.Page, home_page: HomePage):
        self.page = page
        self.database: Database = page.session.get("database")
        self.home_page = home_page
        self.text_values: dict = page.session.get("text_values")
        self.prefs: Preferences = page.session.get("prefs")
        
        ################### Initialize controller for home page and all its subviews ##################
        
        self.group_listview: GroupListView = self.home_page.group_listview

        self.items_view: ItemsView = self.group_listview.items_view
        
        # Handle sidebutton events
        self.home_page.home_button.on_click = lambda _: self.location_change(self.home_page.home_button)
        self.home_page.settings_button.on_click = lambda _: self.location_change(self.home_page.settings_button)
        self.home_page.feedback_button.on_click = lambda _: self.location_change(self.home_page.feedback_button)
        self.home_page.profile_button.on_click = lambda _: self.location_change(self.home_page.profile_button)
        
        # Handle group items view events
        self.items_view.return_button.on_click = self.return_to_grid
        self.items_view.add_receivable_button.on_click = self.open_receivable_adding_dialog
        
        # handle other homepage requests
        self.home_page.on_homepage_drawn = self.trigger_startup_commands
        self.home_page.prepare_exit = self.prepare_home_page_exit
        
        self.sidebar_buttons = [
            self.home_page.home_button,
            self.home_page.settings_button,
            self.home_page.feedback_button,
            self.home_page.profile_button
        ]

        self.active_button = self.sidebar_buttons[0]
    
    def prepare_home_page_exit(self):
        self.location_change(self.home_page.home_button)
        self.return_to_grid()
    
    def trigger_startup_commands(self):
        self.group_listview.start_group_filling()
        self.home_page.account_view.update_informations()

        # if keep_signed_in, notify the user of autologin
        if self.prefs.get_preference("keep_signed_in", False) is True and self.prefs.get_preference("recent_set_keep_signed_in", False) is False and self.prefs.get_preference("just_opened", False) is True:
            self.page.snack_bar = ft.SnackBar(ft.Text(self.text_values["autologged_in"]), duration=1000)
            self.page.snack_bar.open = True
            self.page.update()
        elif self.prefs.get_preference("recent_set_keep_signed_in", False) is True:
            self.prefs.set_preference("recent_set_keep_signed_in", False)
            self.prefs.set_preference("just_opened", True)
        
        self.home_page.settings_view.currency_setting.setting_with_current.value = self.text_values["current_currency_setting"].format(self.prefs.get_preference('currency', "PHP"))
    
    # returns to group_listview
    def return_to_grid(self, event: ft.ControlEvent = None):
        self.items_view.payable_list.controls = []
        self.items_view.receivable_list.controls = []
        
        for button in self.group_listview.grid.controls:
            button.disabled = False
    
        self.group_listview.content = self.group_listview.grid_view
        self.group_listview.update()
    
    # handle when the current subview is changed
    def location_change(self, new_button):
        if self.active_button == self.home_page.home_button:
            self.return_to_grid()
        
        new_index = 0
        for index, button in enumerate(self.sidebar_buttons):
            if new_button == button:
                new_index = index
                button.selected = True
            else:
                button.selected = False
        
        for iter, view in enumerate(self.home_page.slider_stack.controls):
            view.show(iter - new_index)
        
        self.active_button = new_button
        
        self.page.update()
    
    # when add receivable_button is clicked
    def open_receivable_adding_dialog(self, event: ft.ControlEvent):
        self.home_page.add_receivable_dialog.group = self.items_view.group_name.value
        self.home_page.show_add_receivable_dialog()