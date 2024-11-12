import flet as ft
from views import *
from controllers import *
from models import *
from repository import *
from lang import Language

def main(page: ft.Page):
    # Set window parameters
    page.window.width = 1100
    page.window.height = 768
    page.title = "Arlecchino"

    utils.initialize_settings(page)
    lang = Language(page)
    text_values = lang.get_text_values()

    page.theme = ft.Theme(color_scheme_seed=page.client_storage.get("accent_color"))
    
    # Initialize Pages
    main_pages = Pages(page, text_values)
    main_pages.add_pages([
        HomePage, OpeningPage,
        OnboardingPage, LoginPage,
        SignupPage, ForgotPasswordPage, ConfirmEmailPage
    ])

    page.go(page.route)
    
    # Initialize the Repository
    repository = Repository()

    #Initialize the controllers
    initialize_controllers(page, repository, main_pages, text_values)

if __name__ == "__main__":
    # Run the app with flet's method
    ft.app(
        target=main,
        assets_dir="assets"
    )