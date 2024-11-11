from flet_route import Params, Basket, path
import flet as ft

class AbstractPage(ft.View):
    route: str = ""
    should_clear: bool = True
    def get_view(self, page: ft.Page, params: Params, basket: Basket):
        pass

class Pages:
    def __init__(self, page):
        self.__pages = dict()
        self.flet_page = page
        self.routes = []
    
    def add_page(self, page: AbstractPage):
        current_page = page(self.flet_page)
        self.routes.append(path(url=current_page.route, clear=current_page.should_clear, view=current_page.get_view))
        self.__pages[current_page.__class__.__name__] = current_page
    
    def get(self, page_name: str):
        return self.__pages[page_name]