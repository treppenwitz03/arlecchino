from .opening_controller import OpeningController
from .login_controller import LoginController
from .signup_controller import SignupController
from .forgot_controller import ForgotController
from .confirm_email_controller import ConfirmEmailController
from .chat_controller import ChatController
from .home_controller import HomeController
from .dialog_controllers.group_addition_dialogs_controller import JoinDialogController, CreateGroupDialogController, SearchGroupsDialogController
from .dialog_controllers.item_info_dialog_controller import ItemInfoDialogController
from .dialog_controllers.add_receivable_dialog_controller import AddReceivableDialogController
from .onboarding_page_controller import OnboardingController
from .dialog_controllers.account_settings_dialogs_controller import AccountSettingsDialogsController
from .dialog_controllers.receivable_info_dialog_controller import ReceivableInfoDialogController
from .subview_controllers.feedback_view_controller import FeedbackViewController
from .subview_controllers.account_view_controller import AccountViewController
from .widget_controllers.add_group_button_controller import AddGroupButtonController
from .subview_controllers.group_listview_controller import GroupListViewController
from .subview_controllers.items_view_controller import ItemsViewController
from .dialog_controllers.settings_view_dialog_controller import *
from .controller_connector import *
from views import Pages

def initialize_controllers(page: ft.Page, main_pages: Pages):
    HomeController(page, main_pages.get("HomePage"))
    JoinDialogController(page, main_pages.get("HomePage"))
    GroupListViewController(page, main_pages.get("HomePage"))
    AddGroupButtonController(page, main_pages.get("HomePage"))
    ItemsViewController(page, main_pages.get("HomePage"))
    FeedbackViewController(page, main_pages.get("HomePage"))
    AccountViewController(page, main_pages.get("HomePage"))
    CreateGroupDialogController(page, main_pages.get("HomePage"))
    SearchGroupsDialogController(page, main_pages.get("HomePage"))
    ItemInfoDialogController(page, main_pages.get("HomePage"))
    AddReceivableDialogController(page, main_pages.get("HomePage"))
    AccountSettingsDialogsController(page, main_pages.get("HomePage"))
    ReceivableInfoDialogController(page, main_pages.get("HomePage"))
    AppearanceDialogController(page, main_pages.get("HomePage"))
    CurrencyDialogController(page, main_pages.get("HomePage"))
    LanguageDialogController(page, main_pages.get("HomePage"))
    OpeningController(page, main_pages.get("OpeningPage"))
    OnboardingController(page, main_pages.get("OnboardingPage"))
    LoginController(page, main_pages.get("LoginPage"))
    SignupController(page, main_pages.get("SignupPage"))
    ForgotController(page, main_pages.get("ForgotPasswordPage"))
    ConfirmEmailController(page, main_pages.get("ConfirmEmailPage"))
    ChatController(page, main_pages.get("ChatPage"))