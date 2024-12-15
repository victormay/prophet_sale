import flet as ft

from .base_view import BaseView


class ModelManagementView(BaseView):
    def __init__(self, route="/model_management", name="模型管理"):
        super().__init__(route, name)