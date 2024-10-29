from models import Group, Member
from repository import Repository, utils
from views import HomePage, JoinGroupDialog, CreateGroupDialog, SearchGroupsDialog

from PIL import Image

import flet as ft
import io
import base64
    
class JoinDialogController:
    code_validated = False
    def __init__(self, page: ft.Page, repository: Repository, home_page: HomePage):
        self.page = page
        self.repository = repository
        self.home_page = home_page
        self.join_dialog: JoinGroupDialog = home_page.join_dialog

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
            email = self.page.client_storage.get("email")
            
            username = ""
            for user in self.repository.users:
                if user.email == email:
                    username = user.username
            
            for group in self.repository.groups:
                if group.unique_code == self.join_dialog.get_group_code_entry():
                    group.members.append(Member(username, email))

                    self.repository.update_group(group)
            
                    self.page.client_storage.set("just_opened", False)
                    self.home_page.group_listview.trigger_reload(email)
                    self.home_page.close_dialog(None)
                    self.page.update()
    
        # check if the entered group code exists
    def check_if_code_exists(self, event):
        code = self.join_dialog.get_group_code_entry()
        if code != "":
            exists = False
            for group in self.repository.groups:
                if code == group.unique_code:
                    exists = True
                    break
            
            if exists:
                self.page.snack_bar = ft.SnackBar(ft.Text("The group code is valid. You may now join..."), duration=3000)
                self.page.snack_bar.open = True
                self.page.update()
                self.code_validated = True
                self.join_dialog.join_button.disabled = False
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("The group code is invalid. Please try again..."), duration=3000)
                self.page.snack_bar.open = True
                self.page.update()
                self.code_validated = False
                self.join_dialog.join_button.disabled = True
            
            self.page.update()

class CreateGroupDialogController:
    def __init__(self, page: ft.Page, repository: Repository, home_page: HomePage):
        self.page = page
        self.repository = repository
        self.home_page = home_page
        self.create_group_dialog: CreateGroupDialog = home_page.create_new_dialog

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
            email: str = self.page.client_storage.get("email")
            
            creator = ""
            for user in self.repository.users:
                if user.email == email:
                    creator = user.username
                    break
                
            image_bytes = io.BytesIO()
            image = Image.open(self.image_path).convert("RGBA")
            image = image.resize((200, 200))
            image.save(image_bytes, format="PNG")
            
            empty_list = list()
            unique_code = utils.generate_unique_code()
            
            group_image_id = self.repository.upload_image(image_bytes)
            
            new_group = Group(
                group_name=self.repository.encrypt(self.create_group_dialog.get_created_group_name()),
                created_by=creator,
                description=self.repository.encrypt(self.create_group_dialog.get_created_group_desc()),
                members=[Member(creator, email)],
                picture_id=group_image_id,
                unique_code=unique_code,
                transactions=empty_list
            )
            
            self.repository.update_group(new_group)
            self.page.client_storage.set("just_opened", False)
            self.home_page.group_listview.trigger_reload(email)
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
        self.file_picker.pick_files("Choose Group Image", allowed_extensions = ["png", "jpg", "jpeg", "PNG", "JPG"], file_type = ft.FilePickerFileType.CUSTOM)
    
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
    def __init__(self, page: ft.Page, repository: Repository, home_page: HomePage):
        self.page = page
        self.repository = repository
        self.home_page = home_page
        self.search_groups_dialog: SearchGroupsDialog = home_page.search_groups_dialog

        self.repository.done_loading = lambda: self.populate_group_list()

        self.search_groups_dialog.search_bar.on_tap = lambda e: self.search_groups_dialog.search_bar.open_view()
        self.search_groups_dialog.load_group_button.on_click = self.load_group
        self.search_groups_dialog.close_button.on_click = self.home_page.close_dialog
        self.search_groups_dialog.join_button.on_click = self.join_group
    
    def populate_group_list(self):
        group: Group = None
        for group in self.repository.groups:
            tile = ft.ListTile(
                ft.padding.all(8),
                data=self.repository.decrypt(group.group_name),
                leading=ft.Icon(ft.icons.ALBUM_OUTLINED),
                title = ft.Text(self.repository.decrypt(group.group_name)),
                subtitle = ft.Text(self.repository.decrypt(group.description)),
                on_click = self.item_clicked
            )
            tile.created_by = self.repository.decrypt(group.created_by)
            tile.picture_link = group.picture_id

            self.search_groups_dialog.search_bar.controls.append(tile)
    
    def item_clicked(self, event: ft.ControlEvent):
        self.chosen_group_tile = event.control
        self.search_groups_dialog.search_bar.close_view(event.control.data)
        self.search_groups_dialog.load_group_button.disabled = False
        self.search_groups_dialog.load_group_button.update()
    
    def load_group(self, event):
        if self.chosen_group_tile:
            group_name = self.chosen_group_tile.title.value
            group_description = self.chosen_group_tile.subtitle.value
            group_creator = self.chosen_group_tile.created_by
            picture_link = self.chosen_group_tile.picture_link

            self.search_groups_dialog.group_name_text.value = group_name
            self.search_groups_dialog.group_desc_text.value = "Group Description: " + group_description
            self.search_groups_dialog.group_creator_text.value = "Creator: " + group_creator

            self.search_groups_dialog.image_preview.src_base64 = utils.convert_to_base64(self.repository.download_image(picture_link))
            self.search_groups_dialog.switch_to_has_value()
            self.search_groups_dialog.join_button.disabled = False
            self.search_groups_dialog.update()
    
    def join_group(self, event):
        email = self.page.client_storage.get("email")
            
        username = ""
        for user in self.repository.users:
            if user.email == email:
                username = user.username
        
        group: Group = None
        for group in self.repository.groups:
            if self.repository.decrypt(group.group_name) == self.chosen_group_tile.title.value:

                member: Member = None
                for member in group.members:
                    if member.email == email:
                        self.page.snack_bar = ft.SnackBar(ft.Text(f"You are already in the chosen group..."))
                        self.page.snack_bar.open = True
                        self.page.update()

                        return

                group.members.append(Member(username, email))

                self.repository.update_group(group)
        
                self.page.client_storage.set("just_opened", False)
                self.home_page.group_listview.trigger_reload(email)
                self.home_page.close_dialog(None)
                self.page.update()