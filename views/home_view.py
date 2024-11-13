import flet as ft
from flet_route import Params, Basket
from views.abstract_view import AbstractView

from views.subviews.group_subview import GroupSubView
from views.subviews.settings_subview import SettingsSubView
from views.subviews.feedback_subview import FeedbackSubView
from views.subviews.account_subview import AccountSubView

from views.dialogs.group_addition_dialogs import *
from views.dialogs.item_info_dialog import ItemInfoDialog
from views.dialogs.add_receivable_dialog import AddReceivableDialog
from views.dialogs.show_receivable_info_dialog import ShowReceivableInfoDialog
from views.dialogs.account_settings_dialogs import *
from views.dialogs.settings_view_dialogs import *

class HomeView(AbstractView):
    def __init__(self, text_values: dict):
        super().__init__(
            route = "/home",
            padding=0
        )

        self.text_values = text_values
        ########################################################
        ## Make the Home View UI containing the different views
        ########################################################
        
        self.group_listview = GroupSubView(text_values)
        self.settings_view = SettingsSubView(text_values)
        self.feedback_view = FeedbackSubView(text_values)
        self.account_view = AccountSubView(text_values)
        
        self.slider_stack = ft.Stack(
            expand=True,
            controls=[self.group_listview, self.settings_view, self.feedback_view, self.account_view]
        )
        
        content_area_row = ft.Row(
            expand = True,
            controls=[self.slider_stack]
        )
        
        content_area = ft.Column(
            expand=True,
            spacing=0,
            controls=[content_area_row]
        )
        
        logo = ft.Image(
            src = "/logo.png",
            width=48,
            height=48
        )
        
        logo_row = ft.Row(
            controls=[logo],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.home_button = ft.IconButton(
            selected=True,
            icon=ft.icons.HOME_OUTLINED,
            selected_icon=ft.icons.HOME_FILLED,
            width = 50,
            height = 50,
            icon_size=36,
            style=ft.ButtonStyle()
        )
        
        home_button_row = ft.Row(
            controls=[self.home_button],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.settings_button = ft.IconButton(
            selected=False,
            icon=ft.icons.SETTINGS_OUTLINED,
            selected_icon=ft.icons.SETTINGS,
            width = 50,
            height = 50,
            icon_size=36,
            style=ft.ButtonStyle()
        )
        
        settings_button_row = ft.Row(
            controls=[self.settings_button],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.feedback_button = ft.IconButton(
            selected=False,
            icon=ft.icons.FEEDBACK_OUTLINED,
            selected_icon=ft.icons.FEEDBACK,
            width = 50,
            height = 50,
            icon_size=36,
            style=ft.ButtonStyle(),
        )
        
        feedback_button_row = ft.Row(
            controls=[self.feedback_button],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.profile_button = ft.IconButton(
            selected=False,
            icon=ft.icons.ACCOUNT_CIRCLE_OUTLINED,
            selected_icon=ft.icons.ACCOUNT_CIRCLE,
            width = 50,
            height = 50,
            icon_size=36,
            style=ft.ButtonStyle()
        )
        
        profile_button_row = ft.Row(
            controls=[self.profile_button],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        profile_button_container = ft.Container(
            content=profile_button_row,
            padding=12.5
        )
        
        sidebar_top_column = ft.Column(
            expand=True,
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            controls=[logo_row, home_button_row, settings_button_row, feedback_button_row]
        )
    
        sidebar = ft.Column(
            expand = True,
            width = 75,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.MainAxisAlignment.CENTER,
            controls=[sidebar_top_column, profile_button_container]
        )
        
        self.sidebar_container = ft.Container(
            content=sidebar,
            padding=ft.padding.only(0, 16, 0, 0)
        )
        
        main_row = ft.Row(
            expand=True,
            spacing=0,
            controls=[
                self.sidebar_container,
                ft.VerticalDivider(width=1),
                content_area]
        )

        self.controls = [main_row]
        
        self.join_dialog = JoinGroupDialog(text_values)
        self.create_new_dialog = CreateGroupDialog(text_values)
        self.search_groups_dialog = SearchGroupsDialog(text_values)

        self.item_infos_dialog = ItemInfoDialog(text_values)
        self.add_receivable_dialog = AddReceivableDialog(text_values)
        self.receivable_info_dialog = ShowReceivableInfoDialog(text_values)
        
        self.change_profile_picture_dialog = ProfilePictureChangeDialog(text_values)
        self.edit_username_dialog = EditUsernameDialog(text_values)
        self.edit_password_dialog = EditPasswordDialog(text_values)
        self.edit_gcash_dialog = EditGcashDialog(text_values)
        
        self.appearance_dialog = AppearanceDialog(text_values)
        self.currency_dialog = CurrencyDialog(text_values)
        self.language_dialog = LanguageDialog(text_values)

        self.proof_dialog = ft.AlertDialog(
            title=ft.Text(text_values["proof"]),
            content=ft.Image(width=400, height=400, fit=ft.ImageFit.CONTAIN)
        )
    
    # get the view for the page
    def get_view(self, page: ft.Page, params: Params, basket: Basket):
        self.on_homepage_drawn()
        return self
    
    # make a callback when email is retrieved
    def on_homepage_drawn(self):
        pass
    
    # make a callback to check autologin
    def check_if_autologin(self):
        pass

    def prepare_exit(self):
        pass
    
    # close the currently opened dialog
    def close_dialog(self, event: ft.ControlEvent):
        self.page.dialog.open = False
        self.page.update()
    
    ##################### show dialogs ###############################
    def show_join_group_dialog(self):
        self.page.dialog = self.join_dialog
        self.join_dialog.open = True
        self.page.update()
    
    def show_create_group_dialog(self):
        self.page.dialog = self.create_new_dialog
        self.create_new_dialog.open = True
        self.page.update()
    
    def show_search_groups_dialog(self):
        self.page.dialog = self.search_groups_dialog
        self.search_groups_dialog.open = True
        self.page.update()
    
    def show_info_dialog(self):
        self.page.dialog = self.item_infos_dialog
        self.item_infos_dialog.open = True
        self.page.update()
        
    def show_add_receivable_dialog(self):
        self.page.dialog = self.add_receivable_dialog
        self.add_receivable_dialog.open = True
        self.page.update()
    
    def show_receivable_info_dialog(self):
        self.page.dialog = self.receivable_info_dialog
        self.receivable_info_dialog.open = True
        self.page.update()
    
    def show_profile_picture_change_dialog(self):
        self.page.dialog = self.change_profile_picture_dialog
        self.change_profile_picture_dialog.open = True
        self.page.update()
    
    def show_edit_username_dialog(self):
        self.page.dialog = self.edit_username_dialog
        self.edit_username_dialog.open = True
        self.page.update()
    
    def show_edit_password_dialog(self):
        self.page.dialog = self.edit_password_dialog
        self.edit_password_dialog.open = True
        self.page.update()
    
    def show_change_gcash_qr_dialog(self):
        self.page.dialog = self.edit_gcash_dialog
        self.edit_gcash_dialog.open = True
        self.page.update()
    
    def show_appearance_dialog(self):
        self.page.dialog = self.appearance_dialog
        self.appearance_dialog.open = True
        self.page.update()
    
    def show_currency_dialog(self):
        self.page.dialog = self.currency_dialog
        self.currency_dialog.open = True
        self.page.update()
    
    def show_language_dialog(self):
        self.page.dialog = self.language_dialog
        self.language_dialog.open = True
        self.page.update()
    
    def show_proof_dialog(self):
        self.page.dialog = self.proof_dialog
        self.proof_dialog.open = True
        self.page.update()
    ###########################################################