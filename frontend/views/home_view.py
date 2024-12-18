import flet as ft

from .base_view import BaseView


class HomeView(BaseView):
    def __init__(self, route="/home", name="首页"):
        super().__init__(route, name)