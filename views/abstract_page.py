from flet_route import Params, Basket, Routing, path
from lang import Language
import flet as ft

from typing import List

class AbstractPage(ft.View):
    route: str = ""
    should_clear: bool = True
    def get_view(self, page: ft.Page, params: Params, basket: Basket):
        pass

    def update_texts(self, texts: dict):
        pass

class Pages(object):
    def __init__(self, page: ft.Page, lang: Language):
        self.__pages = dict()
        self.flet_page = page
        self.lang = lang
        self.routes = []
    
    def __add_page__(self, page: AbstractPage):
        current_page = page(self.lang.get_text_values())
        self.routes.append(path(url=current_page.route, clear=current_page.should_clear, view=current_page.get_view))
        self.__pages[current_page.__class__.__name__] = current_page
    
    def add_pages(self, pages):
        for page in pages:
            self.__add_page__(page)
        
        Routing(page = self.flet_page, app_routes = self.routes)
        self.flet_page._set_attr("pages_object", self)
    
    def get(self, page_name: str):
        return self.__pages[page_name]
    
    def update_texts(self):
        new_texts = self.lang.get_text_values()

        page: AbstractPage = None
        for page in self.__pages.values():
            page.update_texts(new_texts)