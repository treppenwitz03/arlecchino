import flet as ft
from views import *
from controllers import *
from models import *
from services import *
from utils import Utils, Preferences
from lang import Language

def main(page: ft.Page):
    # Set window parameters
    page.window.width = 1100
    page.window.height = 768
    page.title = "Arlecchino"
    page.fonts = {"Product Sans" : "fonts/Product Sans Regular.ttf"}

    page.theme = ft.Theme(
        color_scheme_seed=page.client_storage.get("accent_color"),
        font_family="Product Sans"
    )

    prefs = Preferences(page)
    utils = Utils(page)

    page.session.set("prefs", prefs)
    page.session.set("utils", utils)

    lang = Language(page)
    text_values = lang.get_text_values()
    
    # Initialize Pages
    main_pages = Pages(page, text_values)
    main_pages.add_pages([
        HomePage, OpeningPage,
        OnboardingPage, LoginPage,
        SignupPage, ForgotPasswordPage, ConfirmEmailPage,
        ChatPage
    ])

    page.go(page.route)
    
    # Initialize the Database
    database = Database(page)

    page.session.set("database", database)
    page.session.set("text_values", text_values)

    #Initialize the controllers
    initialize_controllers(page, main_pages)

if __name__ == "__main__":
    # Run the app with flet's method
    ft.app(
        target=main,
        assets_dir="assets"
    )