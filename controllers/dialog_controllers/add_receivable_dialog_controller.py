from models import Transaction, Group
from services import Database
from views import HomeView, AddReceivableDialog
from utils import Utils

import flet as ft
from PIL import Image
import io
import base64
import datetime

class AddReceivableDialogController:
    image_path = ""
    def __init__(self, page: ft.Page, home_page: HomeView):
        self.page = page
        self.database: Database = page.session.get("database")
        self.home_page = home_page
        self.add_receivable_dialog: AddReceivableDialog = home_page.add_receivable_dialog
        self.current_year = datetime.date.today().year
        self.text_values: dict = page.session.get("text_values")
        self.utils: Utils = self.page.session.get("utils")
        
        # Set the file picker
        self.file_picker = ft.FilePicker()
        self.file_picker.on_result = self.set_item_image
        self.page.overlay.append(self.file_picker)
        self.page.update()
        
        # Handle the add receivable dialog events
        self.add_receivable_dialog.choose_button.on_click = self.open_chooser
        self.add_receivable_dialog.cancel_button.on_click = self.home_page.close_dialog
        
        self.add_receivable_dialog.item_name_textfield.on_change = self.item_info_change
        self.add_receivable_dialog.item_month_dropdown.on_change = self.item_info_change
        self.add_receivable_dialog.item_day_dropdown.on_change = self.item_info_change
        self.add_receivable_dialog.item_year_dropdown.on_change = self.item_info_change
        self.add_receivable_dialog.item_amount_textfield.on_change = self.item_info_change
        self.add_receivable_dialog.item_description_textfield.on_change = self.item_info_change
        
        self.add_receivable_dialog.add_item_button.on_click = self.add_receivable
    
    # open the chooser for the receivable item
    def open_chooser(self, event: ft.ControlEvent):
        self.file_picker.pick_files(self.text_values["item_image_choose_text"], allowed_extensions = ["png", "jpg", "jpeg", "PNG", "JPG"], file_type = ft.FilePickerFileType.CUSTOM)
    
    # preview the item image
    def set_item_image(self, event: ft.FilePickerResultEvent):
        if event.files is not None:
            self.image_path = event.files[0].path
            image = Image.open(self.image_path).convert("RGBA")
            pil_img = image.resize((200, 200))
            buff = io.BytesIO()
            pil_img.save(buff, format="PNG")
            
            self.new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
            self.add_receivable_dialog.item_image.src_base64 = self.new_image_string
            self.add_receivable_dialog.item_image.update()
        else:
            self.image_path = ""

    # add the receivable
    def add_receivable(self, event: ft.ControlEvent):
        email: str = self.page.session.get("email")
        group_name = self.utils.encrypt(self.add_receivable_dialog.group)
        item_name = self.utils.encrypt(self.add_receivable_dialog.get_item_name())
        item_month = self.add_receivable_dialog.get_item_creation_month()
        item_day = self.add_receivable_dialog.get_item_creation_day()
        item_year = self.add_receivable_dialog.get_item_creation_year()
        item_date = self.utils.encrypt(f"{item_month} {item_day}, {item_year}")
        item_amount = self.utils.encrypt(self.add_receivable_dialog.get_item_amount())
        item_description = self.utils.encrypt(self.add_receivable_dialog.get_item_description())
        
        # convert the image to bytes
        image_bytes = io.BytesIO()
        image = Image.open(self.image_path).convert("RGBA")
        image = image.resize((200, 200))
        image.save(image_bytes, format="PNG")
        
        # upload the receivable image
        receivable_image_id = self.database.upload_image(image_bytes)
        
        # create a new transaction object for the receivable
        new_transaction = Transaction(
            name=item_name,
            description=item_description,
            image_id=receivable_image_id,
            paid_by="None",
            posted_by=email,
            price=item_amount,
            time_created=item_date
        )
        
        group: Group = None
        for group in self.database.groups:
            if group.group_name == group_name:
                group.transactions.append(new_transaction)
                self.database.update_group(group)
                self.home_page.close_dialog(event)
                
                self.database.update_refs()
                self.home_page.group_listview.items_view.on_trigger_reload(event)
                
                break
    
    # handle when fields change
    def item_info_change(self, event: ft.ControlEvent):
        try:
            if all([self.add_receivable_dialog.get_item_name() != "",
                    self.add_receivable_dialog.get_item_creation_month() != "",
                    self.add_receivable_dialog.get_item_creation_day() != "",
                    self.add_receivable_dialog.get_item_creation_year() != "",
                    self.add_receivable_dialog.get_item_amount() != "",
                    self.add_receivable_dialog.get_item_description() != "",
                    self.add_receivable_dialog.get_item_creation_month() in Utils.accepted_months,
                    int(self.add_receivable_dialog.get_item_creation_day()) in range(0, 32), # 31 days + 1
                    int(self.add_receivable_dialog.get_item_creation_year()) in range(2000, self.current_year + 1),
                    float(self.add_receivable_dialog.get_item_amount())]):
                
                self.add_receivable_dialog.add_item_button.disabled = False
            else:
                self.add_receivable_dialog.add_item_button.disabled = True
            self.add_receivable_dialog.update()
        except:
            self.add_receivable_dialog.add_item_button.disabled = True
            self.add_receivable_dialog.add_item_button.update()