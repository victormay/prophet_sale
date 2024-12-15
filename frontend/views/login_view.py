import flet as ft

from controls.background import BgImage
from controls.login_controls import LoginControl, login_check


class LoginView(ft.View):
    def __init__(self):
        super().__init__()
        self.route = "/login"
        self.controls = [
            ft.Stack(
                controls=[BgImage(), LoginControl()],
                expand=True,
                alignment=ft.alignment.center
            )
        ]
        self.padding = ft.padding.all(0)