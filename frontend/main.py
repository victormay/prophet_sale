import flet as ft

from views.home_view import HomeView
from views.login_view import LoginView
from requests.user import login_check


def main(page: ft.Page):

    def route_change(e: ft.RouteChangeEvent):
        if e.route in ["", "/"]:
            page.views.clear()
            page.go("/login")

        elif e.route == "/home":
            if login_check(page):
                page.views.append(HomeView(page))
            else:
                page.go("/login")

        elif e.route == "/login":
            if login_check(page):
                page.go("/home")
            else:
                page.views.append(LoginView(page))
        page.update()
        print(page.route)

    page.on_route_change = route_change
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.go("/")
    page.update()


ft.app(target=main, port=8001, assets_dir="assets", view=ft.AppView.WEB_BROWSER)