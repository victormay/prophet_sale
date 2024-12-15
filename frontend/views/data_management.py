import flet as ft

from .base_view import BaseView


class DataManagementView(BaseView):
    def __init__(self, route="/data_management", name="数据管理"):
        super().__init__(route, name)