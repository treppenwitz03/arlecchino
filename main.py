import flet as ft
from views import *
from controllers import *
from models import *
from repository import *

def main(page: ft.Page):
    # Set window parameters
    page.window.width = 1100
    page.window.height = 768
    page.title = "Arlecchino"
    page.theme = ft.Theme(color_scheme_seed="#8C161E")
    
    # Initialize Pages
    main_pages = Pages(page)
    main_pages.add_pages([
        HomePage, OpeningPage,
        OnboardingPage, LoginPage,
        SignupPage, ForgotPasswordPage, ConfirmEmailPage
    ])

    page.go(page.route)
    
    utils.initialize_settings(page)
    
    # Initialize the Repository
    repository = Repository()

    #Initialize the controllers
    initialize_controllers(page, repository, main_pages)

if __name__ == "__main__":
    # Run the app with flet's method
    ft.app(
        target=main,
        assets_dir="assets"
    )