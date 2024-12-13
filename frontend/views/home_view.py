import flet as ft
from requests.user import login_check

class HomeView(ft.View):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.route = "/home"
        self.controls = [
            ft.Text("/home")
        ]
    
    def update(self):
        if login_check(self.page):
            super().update()
        else:
            self.page.go("/login")
            self.page.update()
