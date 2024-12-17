import flet as ft
from .base_view import BaseView
from controls.user_center_controls import UserInfoControl


class UserCenterView(BaseView):
    def __init__(self, route="/user_center", name="个人中心"):
        super().__init__(route, name)
        self.img = ft.Image(
            "/images/default.png",
            error_content=ft.Text("not found"),
            width=300, 
            height=300
            )
        self.info = UserInfoControl(width=600)
        
        self.controls = [
            ft.Container(
                content=ft.Column([
                    self.img,
                    self.info
                ]),

            )
        ]
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def did_mount(self):
        id = self.page.client_storage.get("id")
        img = self.page.client_storage.get("img")
        self.img.src = f"/{id}/{img}"
        super().did_mount()