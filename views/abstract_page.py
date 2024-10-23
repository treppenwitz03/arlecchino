from abc import ABC, abstractmethod
from flet_route import Params, Basket
import flet as ft

class AbstractPage(ABC):
    @abstractmethod
    def get_view(self, page: ft.Page, params: Params, basket: Basket):
        pass
    @abstractmethod
    def update_colors(self, colors):
        pass