from views import HomePage, GroupButton, ItemButton, PaidUserButton
from repository import Repository, utils
from models import User, Group, Member, Transaction
from lang import Language
from ..controller_connector import ControllerConnector
import flet as ft
import clipboard

class ItemsViewController:
    def __init__(self, page: ft.Page, repository: Repository, home_page: HomePage, text_values: dict):
        self.page = page
        self.repository = repository
        self.home_page = home_page
        self.group_listview = home_page.group_listview
        self.items_view = home_page.group_listview.items_view

        self.items_view.request_open_group = self.open_group
        self.items_view.reload_button.on_click = self.reload_listview
        self.items_view.copy_group_code = self.copy_code_to_clipboard

        # handle reload requests
        self.items_view.on_trigger_reload = self.reload_listview
    
    def copy_code_to_clipboard(self):
        code = self.items_view.group_code_text.spans[0].text
        clipboard.copy(code)

        self.page.snack_bar = ft.SnackBar(ft.Text("Group code is now copied to clipboard."))
        self.page.snack_bar.open = True
        self.page.update()
    
    # clear and  reload the listview
    def reload_listview(self, event: ft.ControlEvent):
        group_name = self.items_view.group_name.value
        image_string = self.items_view.group_image.src_base64
        
        self.items_view.payable_list.controls = []
        self.items_view.receivable_list.controls = []
        self.page.snack_bar = ft.SnackBar(ft.Text(f"Reloading items..."), duration=3000)
        self.page.snack_bar.open = True
        self.page.update()
        
        self.repository.update_refs()
        self.repository.load_groups()

        group: Group = None
        for group in self.repository.groups:
            if group.group_name == self.items_view.group.group_name:
                self.open_group(group_name, image_string, True)
                break
    
    def open_group(self, group_name: str, image_string: str, from_reload: bool):
        self.repository.update_refs()

        group_buttons = ControllerConnector.get_group_buttons(self.page)

        group: Group = group_buttons[str(group_name.__hash__())]
        
        # if the call is from reload, update the buttons
        button: GroupButton = None
        for button in self.group_listview.grid.controls:
            button.disabled = True
            
            if not from_reload:
                button.update()
        
        # if not from reload, notify the user
        if not from_reload:
            self.page.snack_bar = ft.SnackBar(ft.Text("Loading group... Please wait."), duration=3000)
            self.page.snack_bar.open = True
            self.page.update()
        
        usernames = dict()
        user_images = dict()
        gcash_infos = dict()
        
        # get the current email
        email: str = ControllerConnector.get_email(self.page)

        # get the current usernames, images and gcash infos
        current_user = ""
        current_user_image = ""

        group_emails = [member.email for member in group.members]            

        user: User = None
        for user in self.repository.users:
            if user.email in group_emails: # CHeck if the user is in the emails
                user_image = utils.convert_to_base64(self.repository.download_image(user.picture_link))
                user_images.update({
                    utils.decrypt(user.email): user_image
                })

                usernames.update({
                    utils.decrypt(user.email) : utils.decrypt(user.username)
                })
                
                qr_image = utils.convert_to_base64(self.repository.download_image(user.qr_image_id))
                gcash_number = utils.decrypt(user.gcash_number)
                
                gcash_infos.update({
                    utils.decrypt(user.email) : {
                        "QR Image" : qr_image, 
                        "GCash number": gcash_number
                    }
                })
                
                if user.email == email:
                    current_user = utils.decrypt(user.username)
                    current_user_image = user_image

        self.items_view.set_informations({
            "group_name": group_name,
            "group_image": image_string,
            "group_desc": utils.decrypt(group.description),
            "username": current_user,
            "group_code": group.unique_code,
            "creator": utils.decrypt(group.created_by),
            "user_image": current_user_image
        })

        self.items_view.group = group
        
        #clear the payable and receivable lists
        self.items_view.payable_list.controls = []
        self.items_view.receivable_list.controls = []

        payables, receivables, total_payable, total_receivable = 0, 0, 0.0, 0.0
        
        # load transactions
        transaction: Transaction = None
        for transaction in group.transactions:
            paid_users = [user[0] for user in transaction.paid_by]
            item_image = utils.convert_to_base64(self.repository.download_image(transaction.image_id))
            
            if email in paid_users: # if paid, do not show
                continue
            elif transaction.posted_by == email: # if poster, show in rececivable
                receivables += 1
                total_receivable += float(utils.decrypt(transaction.price))
                item = ItemButton(
                    group_name,
                    self.items_view.username.value,
                    user_images[utils.decrypt(transaction.posted_by)],
                    utils.decrypt(transaction.name),
                    utils.decrypt(transaction.description),
                    utils.decrypt(transaction.time_created),
                    f"{utils.currency_symbols[self.page.client_storage.get('currency')]} {utils.decrypt(transaction.price)}",
                    item_image,
                    True
                )

                item.transaction = transaction
                self.items_view.receivable_list.controls.append(item)
            else: # if neither, must pay through payables
                payables += 1
                total_payable += float(utils.decrypt(transaction.price))
                
                item = ItemButton(
                    group_name,
                    usernames[utils.decrypt(transaction.posted_by)],
                    user_images[utils.decrypt(transaction.posted_by)],
                    utils.decrypt(transaction.name),
                    utils.decrypt(transaction.description),
                    utils.decrypt(transaction.time_created),
                    f"{utils.currency_symbols[self.page.client_storage.get('currency')]} {utils.decrypt(transaction.price)}",
                    item_image,
                    False
                )

                item.transaction = transaction
                self.items_view.payable_list.controls.append(item)
        
        # show rundown
        self.items_view.total_payable_text.value = f"Total Payable: {utils.currency_symbols[self.page.client_storage.get('currency')]} {total_payable}"
        self.items_view.total_receivable_text.value = f"Total Receivable: {utils.currency_symbols[self.page.client_storage.get('currency')]} {total_receivable}"
        
        # dictates whether to hide or show empty warner or list
        if payables == 0:
            self.items_view.cont.content = self.items_view.empty_warning_text_container
        else:
            self.items_view.cont.content = self.items_view.payable_list
        
        if self.items_view.add_receivable_button not in self.items_view.receivable_list.controls:
            self.items_view.receivable_list.controls.append(self.items_view.add_receivable_button)

        self.group_listview.content = self.items_view
        self.group_listview.update()
        
        # initialize the buttons inside payables and receivables
        for payable_button in self.items_view.payable_list.controls:
            payable_button: ItemButton = payable_button
            payable_button.gcash_infos = gcash_infos
            payable_button.group = group
            payable_button.activate = self.show_payable_infos
        
        for receivable_button in self.items_view.receivable_list.controls:
            receivable_button: ItemButton = receivable_button
            receivable_button.gcash_infos = gcash_infos
            receivable_button.group = group
            receivable_button.activate = self.show_receivable_info

    # show info dialog and values when item is clicked
    def show_payable_infos(self, event: ft.ControlEvent, item_name: str):
        usernames = dict()
        
        button: ItemButton = event.control
        group: Group = button.group
        
        user: User = None
        for user in self.repository.users:
            usernames.update({
                utils.decrypt(user.username) : utils.decrypt(user.email)
            })
        
        self.home_page.item_infos_dialog.switcher.content = self.home_page.item_infos_dialog.main_row
        self.home_page.item_infos_dialog.title.visible = True
        self.home_page.item_infos_dialog.pay_button.text = "Pay now"
        self.home_page.item_infos_dialog.group_name = group.group_name
        gcash_infos = button.gcash_infos
        
        user = ""
        qr_image_string = ""
        gcash_number = ""
        for username in usernames:
            if usernames[username] == utils.decrypt(button.transaction.posted_by):
                qr_image_string = gcash_infos[usernames[username]]["QR Image"]
                gcash_number = gcash_infos[usernames[username]]["GCash number"]
                user = username

        self.home_page.item_infos_dialog.item_name.value = self.home_page.item_infos_dialog.payment_item_name.spans[0].text = item_name
        self.home_page.item_infos_dialog.price.value = self.home_page.item_infos_dialog.item_price.spans[0].text = f"{utils.currency_symbols[self.page.client_storage.get('currency')]} {utils.decrypt(button.transaction.price)}"
        self.home_page.item_infos_dialog.item_image.src_base64 = button.item_image.src_base64
        self.home_page.item_infos_dialog.item_post_time.spans[0].text = utils.decrypt(button.transaction.time_created)
        self.home_page.item_infos_dialog.account_name_info.value = self.home_page.item_infos_dialog.account_name_payment.value = user
        self.home_page.item_infos_dialog.description.value = utils.decrypt(button.transaction.description)
        self.home_page.item_infos_dialog.qr_code.src_base64 = qr_image_string
        self.home_page.item_infos_dialog.gcash_number.spans[0].text = gcash_number
        
        if button.account_image.src_base64 != "":
            self.home_page.item_infos_dialog.account_image.src_base64 = button.account_image.src_base64
        
        self.home_page.show_info_dialog()
    
    # when receivable button is clicked
    def show_receivable_info(self, event: ft.ControlEvent, item_name: str):
        button: ItemButton = event.control
        transaction: Transaction = button.transaction
        group: Group = button.group
        
        self.home_page.receivable_info_dialog.title.value = item_name
        self.home_page.receivable_info_dialog.group_name = group.group_name

        # add paid users to view
        self.home_page.receivable_info_dialog.paid_list.controls = []
        if transaction.paid_by != "None":
            for user in transaction.paid_by:
                paid_user_button = PaidUserButton(utils.decrypt(user[0]))
                
                paid_user_button.show_proof_button.on_click = lambda e: self.home_page.receivable_info_dialog.show_proof(user[1])
                paid_user_button.reject_button.on_click = lambda e: self.reject_received_payment(paid_user_button, group, transaction, user)
                
                self.home_page.receivable_info_dialog.paid_list.controls.append(paid_user_button)

        if len(transaction.paid_by) == 0 or transaction.paid_by == "None":
            self.home_page.receivable_info_dialog.content = self.home_page.receivable_info_dialog.no_paid_label
        else:
            self.home_page.receivable_info_dialog.content = self.home_page.receivable_info_dialog.paid_list
        
        self.home_page.show_receivable_info_dialog()
    
    # allows to reject false payments
    def reject_received_payment(self, button, group: Group, transaction: Transaction, user: tuple):
        transaction.paid_by.remove(user)
        
        if len(transaction.paid_by) == 0:
            transaction.paid_by = "None"
        
        self.repository.update_group(group)
        
        self.home_page.receivable_info_dialog.paid_list.controls.remove(button)
        
        if len(transaction.paid_by) == 0 or transaction.paid_by == "None":
            self.home_page.receivable_info_dialog.content = self.home_page.receivable_info_dialog.no_paid_label
        else:
            self.home_page.receivable_info_dialog.content = self.home_page.receivable_info_dialog.paid_list
        
        self.home_page.receivable_info_dialog.update()