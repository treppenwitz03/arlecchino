import flet as ft

from flet_route import Routing, path
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
    
    # Set dark mode from prefs
    if bool(page.client_storage.get("dark_mode")):
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
    
    # Initialize Pages
    main_pages = Pages(page)
    main_pages.add_page(HomePage)
    main_pages.add_page(OpeningPage)
    main_pages.add_page(OnboardingPage)
    main_pages.add_page(LoginPage)
    main_pages.add_page(SignupPage)
    main_pages.add_page(ForgotPasswordPage)
    main_pages.add_page(ConfirmEmailPage)
    
    Routing(page = page, app_routes = main_pages.routes)
    page.go(page.route)
    
    if page.client_storage.get("currency") is None:
        page.client_storage.set("currency", "PHP")
    if page.client_storage.get("dark_mode") is None:
        page.client_storage.set("dark_mode", False)
    
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