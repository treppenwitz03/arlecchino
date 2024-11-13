from views import HomeView
import flet as ft
import webbrowser

class FeedbackViewController:
    def __init__(self, page: ft.Page, home_page: HomeView):
        self.page = page
        self.feedback_view = home_page.feedback_view

        # handle feedback view events
        self.feedback_view.button_contact_us.on_click = lambda e: webbrowser.open_new("https://mail.google.com/mail/u/0/#inbox?compose=GTvVlcRzCMtQddshVRjPCKJRGfFwDxvWqJcNftmXFMFqqpdvrXXBpGsrfGGNTnSswPqHpChKdBRJG")
        self.feedback_view.button_contribute.on_click = lambda e: webbrowser.open_new("https://github.com/neverbdneverw/arlecchino/issues/new")