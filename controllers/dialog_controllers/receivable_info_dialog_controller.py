from models import Transaction, Group
from services import Database
from utils import Utils
from views import HomeView, ShowReceivableInfoDialog

import flet as ft

class ReceivableInfoDialogController:
    def __init__(self, page: ft.Page, home_page: HomeView):
        self.page = page
        self.database: Database = page.session.get("database")
        self.home_page = home_page
        self.receivable_info_dialog: ShowReceivableInfoDialog = home_page.receivable_info_dialog
        self.utils: Utils = self.page.session.get("utils")
        
        # handle the receivable info dialog events
        self.receivable_info_dialog.completed_button.on_click = self.mark_receivable_completed
        self.receivable_info_dialog.cancel_button.on_click = lambda e: self.home_page.close_dialog(e)
        self.receivable_info_dialog.show_proof = self.show_proof
    
    # mark the receivable as completed regardless of conditions
    def mark_receivable_completed(self, event: ft.ControlEvent):
        item_name = self.utils.encrypt(self.receivable_info_dialog.title.value)
        group_name = self.receivable_info_dialog.group_name
        
        group: Group = None
        for group in self.database.groups:
            if group.group_name == group_name:
                transaction: Transaction = None
                for transaction in group.transactions:
                    if transaction.name == item_name:
                        self.database.delete_transaction(group_name, transaction)
        
        self.home_page.close_dialog(event)
        self.home_page.group_listview.items_view.on_trigger_reload(event)
    
    # preview the proof sent of payor
    def show_proof(self, picture_id: str):
        image = Utils.convert_to_base64(self.database.download_image(picture_id))

        self.home_page.proof_dialog.content.src_base64 = image
        self.home_page.show_proof_dialog()