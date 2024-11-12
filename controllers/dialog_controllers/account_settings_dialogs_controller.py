from views import HomePage, ProfilePictureChangeDialog, EditGcashDialog, EditUsernameDialog, EditPasswordDialog, AccountView
from repository import Repository, utils
from models import User
from lang import Language

from ..controller_connector import ControllerConnector

from PIL import Image
from io import BytesIO
import flet as ft
import base64
import cv2

class AccountSettingsDialogsController:
    def __init__(self, page: ft.Page, repository: Repository, home_page: HomePage, text_values: dict):
        self.page = page
        self.repository = repository
        self.home_page = home_page
        self.text_values = text_values
        
        # connect the dialogs
        self.change_dp_dialog: ProfilePictureChangeDialog = home_page.change_profile_picture_dialog
        self.change_gcash_dialog: EditGcashDialog = home_page.edit_gcash_dialog
        self.change_username_dialog: EditUsernameDialog = home_page.edit_username_dialog
        self.change_password_dialog: EditPasswordDialog = home_page.edit_password_dialog
        
        self.account_view: AccountView = home_page.account_view
        
        #################### set the file pickers ##################################
        self.qr_picker = ft.FilePicker()
        self.qr_picker.on_result = self.set_qr_image
        self.page.overlay.append(self.qr_picker)
        self.page.update()
        
        self.dp_picker = ft.FilePicker()
        self.dp_picker.on_result = self.set_dp_image
        self.page.overlay.append(self.dp_picker)
        self.page.update()
        ############################################################################
        
        self.gcash_changed = self.handle_save_changes_button
        
        # handle account view setting changes
        self.account_view.change_user_picture_button.on_click = self.show_dp_change_dialog
        self.account_view.edit_profile_button.on_click = lambda e: self.home_page.show_edit_username_dialog()
        self.account_view.change_password_button.on_click = lambda e: self.home_page.show_edit_password_dialog()
        self.account_view.gcash_button.on_click = self.show_change_gcash_dialog
        
        # close the account view dialogs
        self.change_dp_dialog.cancel_button.on_click = lambda e: self.home_page.close_dialog(e)
        self.change_username_dialog.cancel_button.on_click = lambda e: self.home_page.close_dialog(e)
        self.change_password_dialog.cancel_button.on_click = lambda e: self.home_page.close_dialog(e)
        self.change_gcash_dialog.cancel_button.on_click = lambda e: self.home_page.close_dialog(e)
        
        # set the change dp dialog
        self.change_dp_dialog.upload_profile.on_click = self.open_profile_image_chooser
        self.change_dp_dialog.save_changes_button.on_click = self.save_changed_dp
        
        # set the change username dialog
        self.change_username_dialog.new_username_textfield.on_change = self.handle_username_change
        self.change_username_dialog.save_changes_button.on_click = self.save_changed_username
        
        # set the change password dialog
        self.change_password_dialog.new_password_textfield.on_change = self.handle_password_change
        self.change_password_dialog.reenter_password_textfield.on_change = self.handle_password_change
        self.change_password_dialog.save_changes_button.on_click = self.save_changed_password
        
        # set the change gcash dialog
        self.change_gcash_dialog.upload_qr_button.on_click = self.open_qr_chooser
        self.change_gcash_dialog.save_changes_button.on_click = self.save_changed_gcash_infos
    
    # shows the gcash dialog with preliminary settings
    def show_change_gcash_dialog(self, event: ft.ControlEvent):
        self.email: str = ControllerConnector.get_email(self.page)

        user: User = None
        for user in self.repository.users:
            if user.email == self.email:
                self.change_gcash_dialog.number_textfield.value = utils.decrypt(user.gcash_number)
                image_bytes = self.repository.download_image(user.qr_image_id)
                self.change_gcash_dialog.qr_image.src_base64 = utils.convert_to_base64(image_bytes)       

        self.home_page.show_change_gcash_qr_dialog()
    
    # handle when username entry changes
    def handle_username_change(self, event: ft.ControlEvent):
        if self.change_username_dialog.new_username_textfield.value != "":
            self.change_username_dialog.save_changes_button.disabled = False
            self.change_username_dialog.save_changes_button.update()
        else:
            self.change_username_dialog.save_changes_button.disabled = True
            self.change_username_dialog.save_changes_button.update()
    
    # handle when apssword changes
    def handle_password_change(self, event: ft.ControlEvent):
        password = self.change_password_dialog.new_password_textfield.value
        confirm = self.change_password_dialog.reenter_password_textfield.value
        
        if password != "" and confirm != "" and password == confirm:
            self.change_password_dialog.save_changes_button.disabled = False
            self.change_password_dialog.save_changes_button.update()
        else:
            self.change_password_dialog.save_changes_button.disabled = True
            self.change_password_dialog.save_changes_button.update()
    
    # handle when dp change happens
    def show_dp_change_dialog(self, event: ft.ControlEvent):
        image_string = self.account_view.user_picture.src_base64
        self.change_dp_dialog.user_image.src_base64 = image_string
        self.home_page.show_profile_picture_change_dialog()
    
    # open the profile image chooser
    def open_profile_image_chooser(self, event):
        self.dp_picker.pick_files(self.text_values["image_choose_text"], allowed_extensions = ["png", "jpg", "jpeg", "PNG", "JPG"], file_type = ft.FilePickerFileType.CUSTOM)
    
    # open the qr code chooser
    def open_qr_chooser(self, event):
        self.qr_picker.pick_files(self.text_values["gcash_choose_text"], allowed_extensions = ["png", "jpg", "jpeg", "PNG", "JPG"], file_type = ft.FilePickerFileType.CUSTOM)

    # handle the output of choosing dp image
    def set_dp_image(self, event: ft.FilePickerResultEvent):
        if event.files is not None:
            self.dp_image_path = event.files[0].path
            image = Image.open(self.dp_image_path).convert("RGBA")
            pil_img = image.resize((200, 200))
            self.dp_image_buffer = BytesIO()
            pil_img.save(self.dp_image_buffer, format="PNG")
            
            self.dp_image_string = base64.b64encode(self.dp_image_buffer.getvalue()).decode("utf-8")
            self.change_dp_dialog.user_image.src_base64 = self.dp_image_string
            self.change_dp_dialog.user_image.update()
            self.change_dp_dialog.save_changes_button.disabled = False
            self.change_dp_dialog.save_changes_button.update()
        else:
            self.dp_image_path = ""
            self.change_dp_dialog.save_changes_button.disabled = True
            self.change_dp_dialog.save_changes_button.update()
    
    # save the changed dp
    def save_changed_dp(self, event: ft.ControlEvent):
        self.email: str = ControllerConnector.get_email(self.page)
        if self.dp_image_path != "":
            user: User = None
            for user in self.repository.users:
                if user.email == self.email:
                    id = self.repository.upload_image(self.dp_image_buffer)
                    user.picture_link = id
                    
                    self.repository.update_user(user)
                    
                    self.account_view.trigger_reload()
                    self.account_view.user_picture.update()
                    self.account_view.username_text.update()
                    self.account_view.email_text.update()
                    
                    self.home_page.close_dialog(event)
                    
                    self.page.snack_bar = ft.SnackBar(ft.Text(self.text_values["pfp_change_success"]))
                    self.page.snack_bar.open = True
                    self.page.update()
                    
                    return
    
    # save the changed username
    def save_changed_username(self, event: ft.ControlEvent):
        self.email: str = ControllerConnector.get_email(self.page)
        replacement = self.change_username_dialog.new_username_textfield.value
        
        user: User = None
        for user in self.repository.users:
            if user.email == self.email:
                user.username = utils.encrypt(replacement)
                self.repository.update_user(user)
                self.account_view.trigger_reload()
                self.home_page.group_listview.top_text.value = f"{utils.generate_greeting(self.text_values["__LANG__"])}, {replacement}!"
                self.home_page.group_listview.top_text.update()
                self.account_view.user_picture.update()
                self.account_view.username_text.update()
                self.account_view.email_text.update()
                
                self.home_page.close_dialog(event)
                
                return
    
    # save the changed password
    def save_changed_password(self, event: ft.ControlEvent):
        self.email: str = ControllerConnector.get_email(self.page)
        password = self.change_password_dialog.new_password_textfield.value
        
        user: User = None
        for user in self.repository.users:
            if user.email == self.email:
                user.password = utils.encrypt(password)
                self.repository.update_user(user)
                
                self.home_page.close_dialog(event)
                
                text = ft.Text(self.text_values["pw_change_success"])
                self.page.snack_bar = ft.SnackBar(text, duration=3000)
                self.page.snack_bar.open = True
                self.page.update()
                
                return
    
    # handle when qr code is set
    def set_qr_image(self, event: ft.FilePickerResultEvent):
        if event.files is not None:
            self.qr_image_path = event.files[0].path
            image = cv2.imread(self.qr_image_path)
            detector = cv2.QRCodeDetector()
            retval, data, points, _ = detector.detectAndDecodeMulti(image)
            
            if "com.p2pqrpay" not in data:
                self.gcash_qr_base64 = ""
                self.page.snack_bar = ft.SnackBar(ft.Text(self.text_values["qr_invalid"]), duration=3000)
                self.page.snack_bar.open = True
                self.page.update()
                return
            
            x, y, w, h = cv2.boundingRect(points[0])
            cropped_image = image[y: y+h, x: x+w]
            bordered_image = Image.fromarray(cv2.copyMakeBorder(
                cropped_image,
                10, 10, 10, 10,
                cv2.BORDER_CONSTANT,
                value=[255,255,255]
            ))

            self.qr_buffer = BytesIO()
            bordered_image.save(self.qr_buffer, format="JPEG")
            self.gcash_qr_base64 = base64.b64encode(self.qr_buffer.getvalue()).decode("utf-8")
            self.change_gcash_dialog.qr_image.src_base64 = self.gcash_qr_base64
            self.change_gcash_dialog.qr_image.update()
            self.gcash_changed()
        else:
            self.qr_image_path = ""
    
    # make a callback when gcash is changed
    def gcash_changed(self):
        pass

    # handle the save changes button
    def handle_save_changes_button(self):
        if self.gcash_qr_base64 != "" and len(self.change_gcash_dialog.number_textfield.value) == 11 and (self.change_gcash_dialog.number_textfield.value[:2] == "09" or self.change_gcash_dialog.number_textfield.value[:3] == "639"):
            self.change_gcash_dialog.save_changes_button.disabled = False
            self.change_gcash_dialog.save_changes_button.update()
        else:
            self.change_gcash_dialog.save_changes_button.disabled = True
            self.change_gcash_dialog.save_changes_button.update()
    
    # save the changed gcash infos
    def save_changed_gcash_infos(self, event: ft.ControlEvent):
        self.email: str = ControllerConnector.get_email(self.page)
        
        user: User = None
        for user in self.repository.users:
            if user.email == self.email:
                id = self.repository.upload_image(self.qr_buffer)
                user.qr_image_id = id
                user.gcash_number = utils.encrypt(self.change_gcash_dialog.number_textfield.value)
                self.repository.update_user(user)
                self.home_page.close_dialog(event)
                
                return
        