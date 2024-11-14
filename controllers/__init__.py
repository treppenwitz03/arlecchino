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
from views import Views

def initialize_controllers(page: ft.Page, main_pages: Views):
    HomeController(page, main_pages.get("HomeView"))
    JoinDialogController(page, main_pages.get("HomeView"))
    GroupListViewController(page, main_pages.get("HomeView"))
    AddGroupButtonController(page, main_pages.get("HomeView"))
    ItemsViewController(page, main_pages.get("HomeView"))
    FeedbackViewController(page, main_pages.get("HomeView"))
    AccountViewController(page, main_pages.get("HomeView"))
    CreateGroupDialogController(page, main_pages.get("HomeView"))
    SearchGroupsDialogController(page, main_pages.get("HomeView"))
    ItemInfoDialogController(page, main_pages.get("HomeView"))
    AddReceivableDialogController(page, main_pages.get("HomeView"))
    AccountSettingsDialogsController(page, main_pages.get("HomeView"))
    ReceivableInfoDialogController(page, main_pages.get("HomeView"))
    AppearanceDialogController(page, main_pages.get("HomeView"))
    CurrencyDialogController(page, main_pages.get("HomeView"))
    LanguageDialogController(page, main_pages.get("HomeView"))
    OpeningController(page, main_pages.get("OpeningView"))
    OnboardingController(page, main_pages.get("OnboardingView"))
    LoginController(page, main_pages.get("LoginView"))
    SignupController(page, main_pages.get("SignupView"))
    ForgotController(page, main_pages.get("ForgotPasswordView"))
    ConfirmEmailController(page, main_pages.get("ConfirmEmailView"))