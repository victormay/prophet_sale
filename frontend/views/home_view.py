import flet as ft

from .base_view import BaseView
from controls.home_controls import HomePredShow


class HomeView(BaseView):
    def __init__(self, route="/home", name="首页"):
        super().__init__(route, name)
        self.show = HomePredShow()
        # self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.controls = [
            self.show
        ]
        self.scroll = ft.ScrollMode.AUTO