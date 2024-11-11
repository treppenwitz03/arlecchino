from models import Member, Group, User, Transaction
from repository import Repository, utils
from views import *

from .controller_connector import ControllerConnector

import flet as ft

class HomeController:
    code_validated = False
    image_path = ""
    def __init__(self, page: ft.Page, repository: Repository, home_page: HomePage):
        self.page = page
        self.repository = repository
        self.home_page = home_page
        
        ################### Initialize controller for home page and all its subviews ##################
        
        self.group_listview: GroupListView = self.home_page.group_listview
        self.feedback_view: FeedbackView = self.home_page.feedback_view
        self.account_view: AccountView = self.home_page.account_view

        self.items_view: ItemsView = self.group_listview.items_view
        
        # Handle sidebutton events
        self.home_page.home_button.on_click = lambda _: self.location_change(self.home_page.home_button)
        self.home_page.settings_button.on_click = lambda _: self.location_change(self.home_page.settings_button)
        self.home_page.feedback_button.on_click = lambda _: self.location_change(self.home_page.feedback_button)
        self.home_page.profile_button.on_click = lambda _: self.location_change(self.home_page.profile_button)
        
        # Handle group items view events
        self.items_view.return_button.on_click = self.return_to_grid
        self.items_view.reload_button.on_click = self.reload_listview
        self.items_view.add_receivable_button.on_click = self.open_receivable_adding_dialog
        
        # handle reload requests
        self.items_view.on_trigger_reload = self.reload_listview
        self.group_listview.trigger_reload = self.fill_groups
        
        # handle other homepage requests
        self.home_page.on_homepage_drawn = self.start_filling_groups
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
    
    def start_filling_groups(self):
        email: str = ControllerConnector.get_email(self.page)
        self.fill_groups(email)

    # fills the group list view
    def fill_groups(self, email: str):
        self.repository.update_refs()
        self.group_listview.refresh_grid()
        
        # if keep_signed_in, notify the user of autologin
        if self.page.client_storage.get("keep_signed_in") is True and self.page.client_storage.get("recent_set_keep_signed_in") is False and self.page.client_storage.get("just_opened") is True:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"You are automatically logged in."), duration=1000)
            self.page.snack_bar.open = True
            self.page.update()
        elif self.page.client_storage.get("recent_set_keep_signed_in") is True:
            self.page.client_storage.set("recent_set_keep_signed_in", False)
            self.page.client_storage.set("just_opened", True)

        # retrieve usernames
        username = ""
        user: User = None
        for user in self.repository.users:
            if user.email == email:
                username = utils.decrypt(user.username)
                break
        
        # set the username inside the greeter
        self.group_listview.set_greeting(f"{utils.generate_greeting()}, {username}!")
        
        # get the joined groups of current member
        joined_groups = []
        group: Group = None
        for group in self.repository.groups:
            member: Member = None
            for member in group.members:
                if member.email == email:
                    image_string = utils.convert_to_base64(self.repository.download_image(group.picture_id))
                    joined_groups.append((group, image_string))
        
        # if joined_groups is 0, show warning
        if len(joined_groups) == 0:
            self.group_listview.empty_warning_text_container.visible = True
            self.group_listview.empty_warning_text_container.offset = ft.transform.Offset(0, 0)
        else:
            self.group_listview.empty_warning_text_container.offset = ft.transform.Offset(-1, 0)
            self.group_listview.empty_warning_text_container.visible = False

        # handle group button events
        group_object: Group = None
        group_image: str = ""
        for group_object, group_image in joined_groups:
            group_button = GroupButton(utils.decrypt(group_object.group_name), group_image)
            group_button.group = group_object
            group_button.activate = lambda button, group_name, image_string: self.open_group(group_name, image_string, button.group, False)
            self.group_listview.add_group_button(group_button)
    
    # shows the listview for the group
    def open_group(self, group_name: str, image_string: str, group: Group, from_reload: bool):
        self.repository.update_refs()
        
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
        for user in self.repository.users:
            #TODO: CHECK IF THE USER IS IN THE GROUP
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
        
        # set the items view indicators
        self.items_view.group_name.value = self.items_view.group_name_text.value = group_name
        self.items_view.group_image.src_base64 = image_string
        self.items_view.group_description.value = utils.decrypt(group.description)
        self.items_view.username.value = current_user
        self.items_view.group_code_text.spans[0].text = group.unique_code
        self.items_view.group = group
        self.items_view.set_creator(utils.decrypt(group.created_by))
        self.items_view.set_user_image(current_user_image)
        
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
                    group,
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
                    group,
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
            payable_button.activate = self.show_item_informations
        
        for receivable_button in self.items_view.receivable_list.controls:
            receivable_button: ItemButton = receivable_button
            receivable_button.gcash_infos = gcash_infos
            receivable_button.group = group
            receivable_button.activate = self.show_receivable_info
    
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
        for group in self.repository.groups:
            if group.group_name == self.items_view.group.group_name:
                self.open_group(group_name, image_string, group, True)
                break
    
    # returns to group_listview
    def return_to_grid(self, event: ft.ControlEvent = None):
        self.items_view.payable_list.controls = []
        self.items_view.receivable_list.controls = []
        
        for button in self.group_listview.grid.controls:
            button.disabled = False
    
        self.group_listview.content = self.group_listview.grid_view
        self.group_listview.update()
    
    # show info dialog and values when item is clicked
    def show_item_informations(self, event: ft.ControlEvent, item_name: str):
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
    
    # handle when the current subview is changed
    def location_change(self, new_button):
        if self.active_button == self.home_page.home_button:
            self.return_to_grid()
        
        if new_button == self.home_page.settings_button:
            self.home_page.settings_view.currency_setting.setting_with_current.value = f"Currently set to: {self.page.client_storage.get('currency')}"
        
        new_index = 0
        for index, button in enumerate(self.sidebar_buttons):
            if new_button == button:
                new_index = index
                button.selected = True
            else:
                button.selected = False
        
        for iter, view in enumerate(self.home_page.slider_stack.controls):
            view.show(iter - new_index)
            
        if new_button == self.home_page.profile_button:
            self.account_view.update_informations()
        
        self.active_button = new_button
        
        self.page.update()
    
    # when add receivable_button is clicked
    def open_receivable_adding_dialog(self, event: ft.ControlEvent):
        self.home_page.add_receivable_dialog.group = self.items_view.group_name.value
        self.home_page.show_add_receivable_dialog()
    
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