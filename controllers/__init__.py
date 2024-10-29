from .opening_controller import OpeningController
from .login_controller import LoginController
from .signup_controller import SignupController
from .forgot_controller import ForgotController
from .confirm_email_controller import ConfirmEmailController
from .home_controller import HomeController
from .add_dialog_controller import AddDialogController
from .item_info_dialog_controller import ItemInfoDialogController
from .add_receivable_dialog_controller import AddReceivableDialogController
from .onboarding_page_controller import OnboardingController
from .account_settings_dialogs_controller import AccountSettingsDialogsController
from .receivable_info_dialog_controller import ReceivableInfoDialogController
from .settings_view_dialog_controller import *

def initialize_controllers(page: ft.Page, repository, main_pages):
    HomeController(page, repository, main_pages[0])
    AddDialogController(page, repository, main_pages[0])
    ItemInfoDialogController(page, repository, main_pages[0])
    AddReceivableDialogController(page, repository, main_pages[0])
    AccountSettingsDialogsController(page, repository, main_pages[0])
    ReceivableInfoDialogController(page, repository, main_pages[0])
    AppearanceDialogController(page, repository, main_pages[0])
    CurrencyDialogController(page, repository, main_pages[0])
    OpeningController(page, repository, main_pages[1])
    OnboardingController(page, repository, main_pages[2])
    LoginController(page, repository, main_pages[3])
    SignupController(page, repository, main_pages[4])
    ForgotController(page, repository, main_pages[5])
    ConfirmEmailController(page, repository, main_pages[6])