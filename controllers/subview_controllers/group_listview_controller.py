from views import HomePage
from services import Database
from models import User, Group, Member
from ..controller_connector import ControllerConnector
import flet as ft
from utils import Utils

class GroupListViewController:
    def __init__(self, page: ft.Page, home_page: HomePage):
        self.page = page
        self.database: Database = page.session.get("database")
        self.home_page = home_page
        self.group_listview = home_page.group_listview
        self.text_values: dict = page.session.get("text_values")
        self.utils: Utils = self.page.session.get("utils")

        self.group_listview.trigger_reload = self.fill_groups
        self.group_listview.start_group_filling = self.fill_groups
        self.group_listview.request_open_group = self.open_group
    
    # fills the group list view
    def fill_groups(self):
        email: str = ControllerConnector.get_email(self.page)

        self.database.update_refs()
        self.group_listview.refresh_grid()

        # retrieve usernames
        username = ""
        user: User = None
        for user in self.database.users:
            if user.email == email:
                username = self.utils.decrypt(user.username)
                break
        
        # set the username inside the greeter
        self.group_listview.set_greeting(f"{Utils.generate_greeting(self.text_values["__LANG__"])}, {username}!")
        
        # get the joined groups of current member
        group_buttons = dict()
        group: Group = None
        for group in self.database.groups:
            member: Member = None
            for member in group.members:
                if member.email == email:
                    image_string = Utils.convert_to_base64(self.database.download_image(group.picture_id))
                    id = self.group_listview.add_group_button(self.utils.decrypt(group.group_name), image_string)
                    group_buttons[id] = group
        
        ControllerConnector.set_group_buttons(self.page, group_buttons)
        
        # if joined_groups is 0, show warning
        if len(group_buttons.values()) == 0:
            self.group_listview.empty_warning_text_container.visible = True
            self.group_listview.empty_warning_text_container.offset = ft.transform.Offset(0, 0)
        else:
            self.group_listview.empty_warning_text_container.offset = ft.transform.Offset(-1, 0)
            self.group_listview.empty_warning_text_container.visible = False
    
    def open_group(self, group_name: str, group_image: str, from_reload: bool):
        self.group_listview.items_view.request_open_group(group_name, group_image, from_reload)