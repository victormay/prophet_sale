import flet as ft

from .base_view import BaseView


class Part(ft.Container):
    def __init__(self, controls=[]):
        super().__init__()
        self.bgcolor = ft.colors.random_color()
        self.head = ft.Container(
            content=ft.Text("part", theme_style=ft.TextThemeStyle.DISPLAY_SMALL), 
            height=55,
            width=300, 
            bgcolor="green", 
            border_radius=10,
            padding=ft.padding.only(left=20)
        )
        self.content = ft.Column(
            controls=[
                ft.Row([self.head]),
                ft.Divider(thickness=2, color=ft.colors.AMBER),
                ft.Row(controls=controls, height=500),
                ft.Divider(thickness=2, color=ft.colors.AMBER)
            ]
        )


class Setting(BaseView):
    def __init__(self, route="/setting", name="设置"):
        super().__init__(route, name)
        self.p1 = Part()
        self.controls = [
            self.p1
        ]