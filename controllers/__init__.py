from .opening_controller import OpeningController
from .login_controller import LoginController
from .signup_controller import SignupController
from .forgot_controller import ForgotController
from .confirm_email_controller import ConfirmEmailController
from .home_controller import HomeController
from .group_addition_dialogs_controller import JoinDialogController, CreateGroupDialogController, SearchGroupsDialogController
from .item_info_dialog_controller import ItemInfoDialogController
from .add_receivable_dialog_controller import AddReceivableDialogController
from .onboarding_page_controller import OnboardingController
from .account_settings_dialogs_controller import AccountSettingsDialogsController
from .receivable_info_dialog_controller import ReceivableInfoDialogController
from .settings_view_dialog_controller import *
from .controller_connector import *
from views import Pages
from repository import Repository

def initialize_controllers(page: ft.Page, repository: Repository, main_pages: Pages):
    HomeController(page, repository, main_pages.get("HomePage"))
    JoinDialogController(page, repository, main_pages.get("HomePage"))
    CreateGroupDialogController(page, repository, main_pages.get("HomePage"))
    SearchGroupsDialogController(page, repository, main_pages.get("HomePage"))
    ItemInfoDialogController(page, repository, main_pages.get("HomePage"))
    AddReceivableDialogController(page, repository, main_pages.get("HomePage"))
    AccountSettingsDialogsController(page, repository, main_pages.get("HomePage"))
    ReceivableInfoDialogController(page, repository, main_pages.get("HomePage"))
    AppearanceDialogController(page, repository, main_pages.get("HomePage"))
    CurrencyDialogController(page, repository, main_pages.get("HomePage"))
    OpeningController(page, repository, main_pages.get("OpeningPage"))
    OnboardingController(page, repository, main_pages.get("OnboardingPage"))
    LoginController(page, repository, main_pages.get("LoginPage"))
    SignupController(page, repository, main_pages.get("SignupPage"))
    ForgotController(page, repository, main_pages.get("ForgotPasswordPage"))
    ConfirmEmailController(page, repository, main_pages.get("ConfirmEmailPage"))