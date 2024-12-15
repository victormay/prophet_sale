import flet as ft

from .base_view import BaseView


class IntegrationManagementView(BaseView):
    def __init__(self, route="/Integration_management", name="集成管理"):
        super().__init__(route, name)