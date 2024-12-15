import flet as ft
from controls.login_controls import logout


class BaseView(ft.View):
    def __init__(self, route, name):
        super().__init__()
        self.route = route
        self.ava = ft.CircleAvatar(
            foreground_image_src="", 
            bgcolor=ft.colors.SURFACE,
        )
        self.more = ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="个人中心", on_click=lambda x: x.page.go("/user_center")),
                    ft.PopupMenuItem(text="用户管理", on_click=lambda x: x.page.go("/users_management")),
                    ft.PopupMenuItem(text="数据管理", on_click=lambda x: x.page.go("/data_management")),
                    ft.PopupMenuItem(text="集成管理", on_click=lambda x: x.page.go("/integration_management")),
                    ft.PopupMenuItem(text="模型管理", on_click=lambda x: x.page.go("/model_management")),
                    ft.PopupMenuItem(text="设置", on_click=lambda x: x.page.go("/setting")),
                    ft.PopupMenuItem(text="登出", on_click=lambda x: logout(x.page)),
                ],
                tooltip="更多"
            )
        
        self.appbar = ft.AppBar(
                    leading=ft.IconButton(ft.icons.HOME, on_click=lambda x: x.page.go("/home")),
                    leading_width=40,
                    title=ft.Text(name),
                    center_title=False,
                    bgcolor=ft.Colors.BLUE_100,
                    actions=[
                        self.ava,
                        self.more
                    ]
                )
        self.navigation_bar
    
    def did_mount(self):
        id = self.page.client_storage.get("id")
        img = self.page.client_storage.get("img")
        email = self.page.client_storage.get("email")
        admin = self.page.client_storage.get("admin")
        self.ava.foreground_image_src = f"/{id}/{img}"
        self.ava.tooltip = email
        if not admin:
            self.more.items[1].visible = False
            self.more.items[2].visible = False
            self.more.items[3].visible = False
            self.more.items[4].visible = False
            self.more.items[5].visible = False
        self.page.update()