import flet as ft

from flet_route import Routing, path
from views import *
from controllers import *
from models import *
from repository import *

# Set up Route Manager
class RouteManager(Routing):
    def route_changed(self, route):
        pass
    
    def change_route(self, route):
        self.route_changed(route)
        super().change_route(route)

def main(page: ft.Page):
    # Set window parameters
    page.window.width = 1024
    page.window.height = 768
    page.title = "Arlecchino"
    
    # Set dark mode from prefs
    if bool(page.client_storage.get("dark_mode")):
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
    
    # Initialize colors
    colors = get_colors(page.client_storage.get("dark_mode"))
    
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
    
    routing = RouteManager(page = page, app_routes = app_routes)
    page.go(page.route)
    
    # Upload colors when page changes
    def handle_route_changed(event: ft.RouteChangeEvent):
        colors = get_colors(page.client_storage.get("dark_mode"))
        for current in main_pages:
            if current.route_address == event.route:
                current.update_colors(colors)
                break

    routing.route_changed = handle_route_changed
    
    main_pages[1].update_colors(colors)
    
    # page.client_storage.clear()
    
    # Setting defaults
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