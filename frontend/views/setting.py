import flet as ft

from .base_view import BaseView


class Setting(BaseView):
    def __init__(self, route="/setting", name="设置"):
        super().__init__(route, name)