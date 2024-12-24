import flet as ft
import httpx
from pathlib import Path

from .base_view import BaseView
from config import Cfg


class UsersManagementView(BaseView):
    def __init__(self, route="/users_management", name="用户管理"):
        super().__init__(route, name)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("用户ID")),
                ft.DataColumn(ft.Text("用户头像")),
                ft.DataColumn(ft.Text("用户名称")),
                ft.DataColumn(ft.Text("用户EMAIL")),
                ft.DataColumn(ft.Text("创建时间")),
                ft.DataColumn(ft.Text("更新时间")),
                ft.DataColumn(ft.Text("用户类型")),
            ],
            # border=ft.border.all(5, ft.colors.BLACK),
            # border_radius=5
        )
        self.controls = [
            self.table
        ]
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        # self.vertical_alignment = ft.MainAxisAlignment.CENTER

    
    def did_mount(self):
        token = self.page.client_storage.get("token")
        header = {
            "token": token
        }
        res = httpx.get(f"{Cfg.HOST}/user/select_all", headers=header, timeout=Cfg.TIMEOUT)
        js_res = res.json()
        for i in js_res:
            file_path = Path(f"./assets/{i['id']}/{i['img']}")
            file_path.parent.mkdir(parents=True, exist_ok=True)
            res = httpx.get(f"{Cfg.HOST}/static/{i['img']}", timeout=Cfg.TIMEOUT)
            with open(file_path, "bw")as f:
                f.write(res.content)

            r = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(i["id"])),
                    ft.DataCell(ft.Image(src=f"{i['id']}/{i['img']}")),
                    ft.DataCell(ft.Text(i["username"])),
                    ft.DataCell(ft.Text(i["email"])),
                    ft.DataCell(ft.Text(i["create_time"])),
                    ft.DataCell(ft.Text(i["update_time"])),
                    ft.DataCell(ft.Text("管理员" if i["admin"] else "普通用户")),
                ],
            )
            self.table.rows.append(r)
        super().did_mount()