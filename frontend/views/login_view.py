import flet as ft

from controls.background import BgImage
from controls.login_controls import LoginControl


class LoginView(ft.View):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.route = "/login"
        self.controls = [
            ft.Stack(
                controls=[BgImage(), LoginControl()],
                expand=True,
                alignment=ft.alignment.center
            )
        ]
        self.padding = ft.padding.all(0)

    def login(self, e):
        self.page.client_storage.set(self.page.client_ip, {"id": 1})
        self.page.go("/home")
        self.page.update()