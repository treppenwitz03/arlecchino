from .opening_controller import OpeningController
from .login_controller import LoginController
from .signup_controller import SignupController
from .forgot_controller import ForgotController
from .confirm_email_controller import ConfirmEmailController
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
from repository import Repository

def initialize_controllers(page: ft.Page, repository: Repository, main_pages: Pages, text_values: dict):
    HomeController(page, repository, main_pages.get("HomePage"), text_values)
    JoinDialogController(page, repository, main_pages.get("HomePage"), text_values)
    GroupListViewController(page, repository, main_pages.get("HomePage"), text_values)
    AddGroupButtonController(page, repository, main_pages.get("HomePage"))
    ItemsViewController(page, repository, main_pages.get("HomePage"), text_values)
    FeedbackViewController(page, repository, main_pages.get("HomePage"))
    AccountViewController(page, repository, main_pages.get("HomePage"))
    CreateGroupDialogController(page, repository, main_pages.get("HomePage"), text_values)
    SearchGroupsDialogController(page, repository, main_pages.get("HomePage"), text_values)
    ItemInfoDialogController(page, repository, main_pages.get("HomePage"), text_values)
    AddReceivableDialogController(page, repository, main_pages.get("HomePage"), text_values)
    AccountSettingsDialogsController(page, repository, main_pages.get("HomePage"), text_values)
    ReceivableInfoDialogController(page, repository, main_pages.get("HomePage"))
    AppearanceDialogController(page, repository, main_pages.get("HomePage"))
    CurrencyDialogController(page, repository, main_pages.get("HomePage"), text_values)
    LanguageDialogController(page, repository, main_pages.get("HomePage"), text_values)
    OpeningController(page, repository, main_pages.get("OpeningPage"), text_values)
    OnboardingController(page, repository, main_pages.get("OnboardingPage"), text_values)
    LoginController(page, repository, main_pages.get("LoginPage"), text_values)
    SignupController(page, repository, main_pages.get("SignupPage"), text_values)
    ForgotController(page, repository, main_pages.get("ForgotPasswordPage"), text_values)
    ConfirmEmailController(page, repository, main_pages.get("ConfirmEmailPage"), text_values)