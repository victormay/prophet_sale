import flet as ft

from views.home_view import HomeView
from views.login_view import LoginView
from views.user_center import UserCenterView
from views.users_management import UsersManagementView
from views.data_management import DataManagementView
from views.Integration_management import IntegrationManagementView
from views.model_management import ModelManagementView
from views.setting import Setting
from controls.login_controls import login_check
from random import random


def main(page: ft.Page):

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        print(page.route)

        if e.route == "/":
            page.go("/login")

        if e.route == "/home":
            page.views.append(HomeView())

        if e.route == "/user_center":
            page.views.append(UserCenterView())

        if e.route == "/users_management":
            page.views.append(UsersManagementView())

        if e.route == "/data_management":
            page.views.append(DataManagementView())

        if e.route == "/integration_management":
            page.views.append(IntegrationManagementView())

        if e.route == "/model_management":
            page.views.append(ModelManagementView())

        if e.route == "/setting":
            page.views.append(Setting())

        elif e.route == "/login":
            if login_check(page):
                page.go("/home")
            else:
                page.views.append(LoginView())

        page.update()

    page.on_route_change = route_change
    
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.go("/")
    page.update()


ft.app(target=main, port=8001, assets_dir="assets", view=ft.AppView.WEB_BROWSER)