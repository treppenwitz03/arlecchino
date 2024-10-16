from models import User
from repository import Repository
from views import OnboardingPage

from io import BytesIO
from PIL import Image

import flet as ft
import qrcode
import cv2
import base64

class OnboardingController:
    def __init__(self, page: ft.Page, repository: Repository, onboarding_page: OnboardingPage):
        self.page = page
        self.repository = repository
        self.onboarding_page = onboarding_page
        
        # set preliminary variables
        self.current = 0
        self.gcash_qr_base64 = ""
        
        # initialize qr code picker
        self.qr_picker = ft.FilePicker()
        self.qr_picker.on_result = self.set_qr_image
        self.page.overlay.append(self.qr_picker)
        self.page.update()
        
        # initialize profile picture picker
        self.dp_picker = ft.FilePicker()
        self.dp_picker.on_result = self.set_dp_image
        self.page.overlay.append(self.dp_picker)
        self.page.update()
        
        # handle events
        self.gcash_changed = self.handle_next_button
        
        self.onboarding_page.next_button.on_click = self.switch_view
        self.onboarding_page.qr_upload_button.on_click = self.open_qr_chooser
        self.onboarding_page.profile_upload_button.on_click = self.open_profile_image_chooser
        self.onboarding_page.number_textfield.on_change = lambda e: self.handle_next_button()
    
    # open qr code chooser
    def open_qr_chooser(self, event):
        self.qr_picker.pick_files("Choose GCash QR Code Image", allowed_extensions = ["png", "jpg", "jpeg", "PNG", "JPG"], file_type = ft.FilePickerFileType.CUSTOM)
    
    # open profile picture chooser
    def open_profile_image_chooser(self, event):
        self.dp_picker.pick_files("Choose a User Image", allowed_extensions = ["png", "jpg", "jpeg", "PNG", "JPG"], file_type = ft.FilePickerFileType.CUSTOM)
    
    # set enablement of next_button through field check
    def handle_next_button(self):
        if self.gcash_qr_base64 != "" and len(self.onboarding_page.number_textfield.value) == 11 and (self.onboarding_page.number_textfield.value[:2] == "09" or self.onboarding_page.number_textfield.value[:3] == "639"):
            self.onboarding_page.next_button.disabled = False
            self.onboarding_page.next_button.update()
        else:
            self.onboarding_page.next_button.disabled = True
            self.onboarding_page.next_button.update()
    
    # make a GCASH info changed callback
    def gcash_changed(self):
        pass
    
    # preview the profile image
    def set_dp_image(self, event: ft.FilePickerResultEvent):
        if event.files is not None:
            self.dp_image_path = event.files[0].path
            image = Image.open(self.dp_image_path).convert("RGBA")
            pil_img = image.resize((200, 200))
            self.dp_image_buffer = BytesIO()
            pil_img.save(self.dp_image_buffer, format="PNG")
            
            self.dp_image_string = base64.b64encode(self.dp_image_buffer.getvalue()).decode("utf-8")
            self.onboarding_page.user_image.src_base64 = self.dp_image_string
            self.onboarding_page.user_image.update()
        else:
            self.dp_image_path = ""
    
    # preview the qr image
    def set_qr_image(self, event: ft.FilePickerResultEvent):
        if event.files is not None:
            self.qr_image_path = event.files[0].path
            image = cv2.imread(self.qr_image_path)
            detector = cv2.QRCodeDetector()
            data, _, _ = detector.detectAndDecode(image)
            
            if data == "" or data == None:
                self.gcash_qr_base64 = ""
                self.page.snack_bar = ft.SnackBar(ft.Text("The QR Code image is invalid"), duration=3000)
                self.page.snack_bar.open = True
                self.page.update()
                return
            
            qr = qrcode.QRCode(
                version = 1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size = 10,
                border = 4
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            image = qr.make_image()
            self.buffered = BytesIO()
            image.save(self.buffered, format="JPEG")
            self.gcash_qr_base64 = base64.b64encode(self.buffered.getvalue()).decode("utf-8")
            self.onboarding_page.qr_image.src_base64 = self.gcash_qr_base64
            self.onboarding_page.qr_image.update()
            self.gcash_changed()
        else:
            self.qr_image_path = ""
    
    # handle progression of onboarding
    def switch_view(self, event: ft.ControlEvent):
        email: str = self.page.client_storage.get("email")
        
        current_user: User = None
        for user in self.repository.users:
            if user.email == email.replace(".", ","):
                current_user = user
        
        if self.current == 0: # the introduction page
            self.onboarding_page.main_column.offset = ft.transform.Offset(-1, 0)
            self.onboarding_page.main_column.update()
            self.onboarding_page.gcash_column.offset = ft.transform.Offset(0, 0)
            self.onboarding_page.gcash_column.update()
            self.onboarding_page.profile_column.offset = ft.transform.Offset(1, 0)
            self.onboarding_page.profile_column.update()
            self.onboarding_page.next_button.disabled = True
            self.onboarding_page.next_button.update()
            self.current = 1
        elif self.current == 1: # the gcash page
            self.onboarding_page.main_column.offset = ft.transform.Offset(-2, 0)
            self.onboarding_page.main_column.update()
            self.onboarding_page.gcash_column.offset = ft.transform.Offset(-1, 0)
            self.onboarding_page.gcash_column.update()
            self.onboarding_page.profile_column.offset = ft.transform.Offset(0, 0)
            self.onboarding_page.profile_column.update()
            
            id = self.repository.upload_image(f"{current_user.email}|QRCode.png", self.buffered)
            
            current_user.qr_image_id = id
            current_user.gcash_number = self.onboarding_page.number_textfield.value
            
            self.repository.update_user(current_user)
            
            self.onboarding_page.next_button.text = "Start Morax"
            self.onboarding_page.next_button.update()
            self.current = 2
        elif self.current == 2: # the profile page
            if hasattr(self, "dp_image_path"):
                id = self.repository.upload_image(f"{current_user.email}|DP.png", self.dp_image_buffer)
                current_user.picture_link = id
            else:
                image = Image.open("assets/empty_user_image.png").convert("RGBA")
                pil_img = image.resize((200, 200))
                buff = BytesIO()
                pil_img.save(buff, format="PNG")
                id = self.repository.upload_image(f"{current_user.email}|DP.png", buff)
                current_user.picture_link = id
            
            # the first run is set to false after completion
            current_user.first_run = False
            self.repository.update_user(current_user)
            
            # go to home
            self.page.go("/home")