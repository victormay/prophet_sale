import flet as ft

from .base_view import BaseView


class UsersManagementView(BaseView):
    def __init__(self, route="/users_management", name="用户管理"):
        super().__init__(route, name)