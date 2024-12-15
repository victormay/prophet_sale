import flet as ft
from .base_view import BaseView


class UserCenterView(BaseView):
    def __init__(self, route="/user_center", name="用户中心"):
        super().__init__(route, name)