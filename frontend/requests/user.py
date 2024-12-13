import httpx
import flet as ft

HOST = "http://127.0.0.1:8000"


def login(page: ft.Page, email, password):
    ip = page.client_ip
    token_k = f"{ip}_token"
    admin_k = f"{ip}_admin"
    json_ = {
        "email": email,
        "password": password
    }
    res = httpx.post(f"{HOST}/user/login", json=json_)
    if res.status_code == 200:
        page.client_storage.set(token_k, res.json()["token"])
        page.client_storage.set(admin_k, res.json()["admin"])
        page.go("/")
    else:
        page.client_storage.clear()
        dlg = ft.AlertDialog(
            title=ft.Text(res.json()), on_dismiss=lambda e: page.update())
        page.open(dlg)
    page.update()


def login_check(page: ft.Page):
    ip = page.client_ip
    token_k = f"{ip}_token"
    token_v = page.client_storage.get(token_k)
    if token_v is not None:
        res = httpx.get(f"{HOST}/user/current_user", headers={"token": token_v})
        if res.status_code == 200:
            return True
    page.client_storage.clear()
    return False