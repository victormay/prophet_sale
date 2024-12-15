import httpx
import flet as ft
from pathlib import Path

from config import Cfg


class LoginHeadControl(ft.Row):
    def __init__(self):
        super().__init__(controls=[])
        
        self.controls=[
            ft.CupertinoSlidingSegmentedButton(
                controls=[
                    ft.Text("Login", height=50, size=25),
                    ft.Text("Register", height=50, size=25),
                ],
                selected_index=0,
                thumb_color=ft.colors.BLUE_200,
                on_change=self.on_change,
                # padding=ft.Padding(0, 10, 0, 10),
                expand=True,
            )
        ]
    
    def on_change(self, e):
        if self.controls[0].selected_index == 0:
            self.parent.parent.login_input.visible = True
            self.parent.parent.register_input.visible = False
        else:
            self.parent.parent.login_input.visible = False
            self.parent.parent.register_input.visible = True
        e.page.update()


class LoginInputControl(ft.Column):
    def __init__(self):
        super().__init__()
        self.email = ft.TextField(hint_text="email", value="admin@pdsf.com")
        self.password = ft.TextField(hint_text="password", password=True, value="pdsf123456")
        self.login_btn = ft.ElevatedButton("Login",icon=ft.icons.LOGIN, on_click=self.on_click, bgcolor=ft.colors.BLUE_200)
        self.controls = [
            ft.Column(controls=[self.email, self.password]),
            ft.Row(controls=[self.login_btn], expand=True, alignment=ft.MainAxisAlignment.CENTER)
        ]
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.expand = True

    def on_click(self, e):
        login(self.page, self.email.value, self.password.value)


class RegisterInputControl(ft.Column):
    def __init__(self):
        super().__init__(controls=[])
        self.email = ft.TextField(hint_text="email")
        self.password = ft.TextField(hint_text="password", password=True)
        self.register_btn = ft.ElevatedButton("Register",icon=ft.icons.NEW_LABEL, on_click=self.on_click, bgcolor=ft.colors.BLUE_200)
        self.controls = [
            ft.Column(controls=[self.email, self.password]),
            ft.Row(controls=[self.register_btn], expand=True, alignment=ft.MainAxisAlignment.CENTER)
        ]
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.expand = True

    def on_click(self, e):
        register(self.page, self.email.value, self.password.value)


class LoginControl(ft.Container):
    def __init__(self):
        super().__init__()
        self.head = LoginHeadControl()
        self.login_input = LoginInputControl()
        self.register_input = RegisterInputControl()
        self.register_input.visible = False
        self.content = ft.Column(
            [
                self.head,
                self.login_input,
                self.register_input
            ],
            width=360,
            height=240,
        )
        self.bgcolor = ft.colors.CYAN_50
        self.border_radius = 5


def login(page: ft.Page, email, password):
    ip = page.client_ip
    json_ = {
        "email": email,
        "password": password
    }
    res = httpx.post(f"{Cfg.HOST}/user/login", json=json_)
    if res.status_code == 200:
        js_res = res.json()
        img = js_res["img"]
        id = js_res["id"]
        file_path = Path(f"./assets/{id}/{img}")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        res = httpx.get(f"{Cfg.HOST}/static/{img}")
        with open(file_path, "bw")as f:
            f.write(res.content)
        for k, v in js_res.items():
            page.client_storage.set(k, v)
        
        page.go("/home")
    else:
        page.client_storage.clear()
        dlg = ft.AlertDialog(
            title=ft.Text(res.json()), on_dismiss=lambda e: page.update())
        page.open(dlg)
        page.update()


def login_check(page: ft.Page):
    token_v = page.client_storage.get("token")
    if token_v is not None:
        res = httpx.get(f"{Cfg.HOST}/user/current_user", headers={"token": token_v}, timeout=30)
        if res.status_code == 200:
            return True
    return False


def logout(page: ft.Page):
    page.client_storage.clear()
    page.go("/login")


def register(page, email, password):
    json_ = {
        "email": email,
        "password": password
    }
    res = httpx.post(f"{Cfg.HOST}/user/register", json=json_)
    if res.status_code == 200:
        login(page, email, password)
    else:
        dlg = ft.AlertDialog(
            title=ft.Text(res.json()), on_dismiss=lambda e: page.update())
        page.open(dlg)