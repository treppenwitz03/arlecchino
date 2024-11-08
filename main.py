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
    main_pages = list()
    main_pages.append(HomePage())
    main_pages.append(OpeningPage())
    main_pages.append(OnboardingPage())
    main_pages.append(LoginPage())
    main_pages.append(SignupPage())
    main_pages.append(ForgotPasswordPage())
    main_pages.append(ConfirmEmailPage())

    app_routes = list()
    iter_page: AbstractPage = None
    for iter_page in main_pages:
        app_routes.append(path(url=iter_page.route_address, clear=iter_page.should_clear, view=iter_page.get_view))
    
    Routing(page = page, app_routes = app_routes)
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