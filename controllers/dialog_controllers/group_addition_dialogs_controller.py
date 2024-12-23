from models import Group, Member, User
from services import Database
from views import HomeView, JoinGroupDialog, CreateGroupDialog, SearchGroupsDialog
from utils import Utils, Preferences

from PIL import Image

import flet as ft
import io
import base64
    
class JoinDialogController:
    code_validated = False
    def __init__(self, page: ft.Page, home_page: HomeView):
        self.page = page
        self.database: Database = page.session.get("database")
        self.home_page = home_page
        self.join_dialog: JoinGroupDialog = home_page.join_dialog
        self.text_values: dict = page.session.get("text_values")
        self.utils: Utils = self.page.session.get("utils")
        self.prefs: Preferences = self.page.session.get("prefs")

        self.join_dialog.group_code_textfield.on_change = self.validate_group_code
        self.join_dialog.close_button.on_click = self.home_page.close_dialog
        self.join_dialog.check_if_exists_button.on_click = self.check_if_code_exists
        self.join_dialog.join_button.on_click = self.join_group

    # check if group code entered is 8 chars long
    def validate_group_code(self, event: ft.ControlEvent):
        if len(self.join_dialog.get_group_code_entry()) == 8:
            self.join_dialog.check_if_exists_button.disabled = False
        else:
            self.join_dialog.check_if_exists_button.disabled = True
        self.join_dialog.update()

    def join_group(self, event):
        if self.code_validated:
            email: str = self.page.session.get("email")
            
            username = ""
            user: User = None
            for user in self.database.users:
                if user.email == email:
                    username = user.username
            
            group: Group = None
            for group in self.database.groups:
                if group.unique_code == self.join_dialog.get_group_code_entry():
                    group.members.append(Member(username, email))

                    self.database.update_group(group)
            
                    self.prefs.set_preference("just_opened", False)
                    self.home_page.group_listview.trigger_reload()
                    self.home_page.close_dialog(None)
                    self.page.update()
    
        # check if the entered group code exists
    def check_if_code_exists(self, event):
        code = self.join_dialog.get_group_code_entry()
        if code != "":
            exists = False

            group: Group = None
            for group in self.database.groups:
                if code == group.unique_code:
                    exists = True
                    break
            
            if exists:
                self.page.snack_bar = ft.SnackBar(ft.Text(self.text_values["valid_gcode"]), duration=3000)
                self.page.snack_bar.open = True
                self.page.update()
                self.code_validated = True
                self.join_dialog.join_button.disabled = False
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text(self.text_values["invalid_gcode"]), duration=3000)
                self.page.snack_bar.open = True
                self.page.update()
                self.code_validated = False
                self.join_dialog.join_button.disabled = True
            
            self.page.update()

class CreateGroupDialogController:
    def __init__(self, page: ft.Page, home_page: HomeView):
        self.page = page
        self.database: Database = page.session.get("database")
        self.home_page = home_page
        self.create_group_dialog: CreateGroupDialog = home_page.create_new_dialog
        self.text_values: dict = page.session.get("text_values")
        self.utils: Utils = self.page.session.get("utils")
        self.prefs: Preferences = self.page.session.get("prefs")

        # Initialize file picker
        self.file_picker = ft.FilePicker()
        self.file_picker.on_result = self.set_image
        self.page.overlay.append(self.file_picker)
        self.page.update()

        # handle events
        self.create_group_dialog.create_new_button.on_click = self.create_new
        self.create_group_dialog.close_button.on_click = self.home_page.close_dialog
        self.create_group_dialog.group_name_textfield.on_change = self.validate_creation_params
        self.create_group_dialog.group_desc_textfield.on_change = self.validate_creation_params
        self.create_group_dialog.image_upload_button.on_click = self.open_chooser

    # create a new group
    def create_new(self, event):
        if self.create_group_dialog.get_created_group_name() != "" and self.create_group_dialog.get_created_group_desc() != "":
            email: str = self.page.session.get("email")
            
            creator = ""
            user: User = None
            for user in self.database.users:
                if user.email == email:
                    creator = user.username
                    break
                
            image_bytes = io.BytesIO()
            image = Image.open(self.image_path).convert("RGBA")
            image = image.resize((200, 200))
            image.save(image_bytes, format="PNG")
            
            empty_list = list()
            unique_code = Utils.generate_unique_code()
            
            group_image_id = self.database.upload_image(image_bytes)
            
            new_group = Group(
                group_name=self.utils.encrypt(self.create_group_dialog.get_created_group_name()),
                created_by=creator,
                description=self.utils.encrypt(self.create_group_dialog.get_created_group_desc()),
                members=[Member(creator, email)],
                picture_id=group_image_id,
                unique_code=unique_code,
                transactions=empty_list
            )
            
            self.database.update_group(new_group)
            self.prefs.set_preference("just_opened", False)
            self.home_page.group_listview.trigger_reload()
            self.home_page.close_dialog(None)
            self.new_image_string == ""
            
            self.page.update()
    
    # validate whether the creation fields are filled
    def validate_creation_params(self, event):
        if self.create_group_dialog.get_created_group_desc() != "" and self.create_group_dialog.get_created_group_name() != "":
            self.create_group_dialog.create_new_button.disabled = False
        else:
            self.create_group_dialog.create_new_button.disabled = True

        self.page.update()
    
    # open the file chooser for group images
    def open_chooser(self, event):
        self.file_picker.pick_files(self.text_values["group_image_choose_text"], allowed_extensions = ["png", "jpg", "jpeg", "PNG", "JPG"], file_type = ft.FilePickerFileType.CUSTOM)
    
    # preview the set image
    def set_image(self, event: ft.FilePickerResultEvent):
        if event.files is not None:
            self.image_path = event.files[0].path
            image = Image.open(self.image_path).convert("RGBA")
            pil_img = image.resize((200, 200))
            buff = io.BytesIO()
            pil_img.save(buff, format="PNG")
            
            self.new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
            self.create_group_dialog.image_preview.src_base64 = self.new_image_string
            self.create_group_dialog.image_preview.update()
        else:
            self.image_path = ""

class SearchGroupsDialogController:
    chosen_group_tile: ft.ListTile = None
    def __init__(self, page: ft.Page, home_page: HomeView):
        self.page = page
        self.database: Database = page.session.get("database")
        self.home_page = home_page
        self.search_groups_dialog: SearchGroupsDialog = home_page.search_groups_dialog
        self.text_values: dict = page.session.get("text_values")
        self.utils: Utils = self.page.session.get("utils")
        self.prefs: Preferences = self.page.session.get("prefs")

        self.database.done_loading = lambda: self.populate_group_list()

        self.search_groups_dialog.search_bar.on_tap = lambda e: self.search_groups_dialog.search_bar.open_view()
        self.search_groups_dialog.load_group_button.on_click = self.load_group
        self.search_groups_dialog.close_button.on_click = self.home_page.close_dialog
        self.search_groups_dialog.join_button.on_click = self.join_group
    
    def populate_group_list(self):
        group: Group = None
        for group in self.database.groups:
            tile = ft.ListTile(
                ft.padding.all(8),
                data=self.utils.decrypt(group.group_name),
                leading=ft.Icon(ft.icons.ALBUM_OUTLINED),
                title = ft.Text(self.utils.decrypt(group.group_name)),
                subtitle = ft.Text(self.utils.decrypt(group.description)),
                on_click = self.item_clicked
            )
            tile._set_attr("created_by", group.created_by)
            tile._set_attr("picture_link", group.picture_id)

            self.search_groups_dialog.search_bar.controls.append(tile)
    
    def item_clicked(self, event: ft.ControlEvent):
        self.chosen_group_tile: ft.ListTile = event.control
        self.search_groups_dialog.search_bar.close_view(event.control.data)
        self.search_groups_dialog.load_group_button.disabled = False
        self.search_groups_dialog.load_group_button.update()
    
    def load_group(self, event):
        if self.chosen_group_tile:
            group_name = self.chosen_group_tile.title.value
            group_description = self.chosen_group_tile.subtitle.value
            group_creator = self.chosen_group_tile._get_attr("created_by")
            picture_link = self.chosen_group_tile._get_attr("picture_link")

            self.search_groups_dialog.group_name_text.value = group_name
            self.search_groups_dialog.group_desc_text.value = self.text_values["group_desc_dia"] + group_description
            self.search_groups_dialog.group_creator_text.value = self.text_values["group_creator_dia"] + self.utils.decrypt(group_creator)

            self.search_groups_dialog.image_preview.src_base64 = Utils.convert_to_base64(self.database.download_image(picture_link))
            self.search_groups_dialog.switch_to_has_value()
            self.search_groups_dialog.join_button.disabled = False
            self.search_groups_dialog.update()
    
    def join_group(self, event):
        email: str = self.page.session.get("email")
            
        username = ""
        user: User = None
        for user in self.database.users:
            if user.email == email:
                username = user.username
        
        group: Group = None
        for group in self.database.groups:
            if self.utils.decrypt(group.group_name) == self.chosen_group_tile.title.value:

                member: Member = None
                for member in group.members:
                    if member.email == email:
                        self.page.snack_bar = ft.SnackBar(ft.Text(self.text_values["in_chosen_alrd"]))
                        self.page.snack_bar.open = True
                        self.page.update()

                        return

                group.members.append(Member(username, email))

                self.database.update_group(group)
        
                self.prefs.set_preference("just_opened", False)
                self.home_page.group_listview.trigger_reload()
                self.home_page.close_dialog(None)
                self.page.update()