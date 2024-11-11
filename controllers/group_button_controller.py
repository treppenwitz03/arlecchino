from repository import Repository
from views import HomePage
import flet as ft

class GroupButtonController:
    def __init__(self, page: ft.Page, repository: Repository, home_page: HomePage):
        self.page = page
        self.repository = repository
        self.feedback_view = home_page.feedback_view