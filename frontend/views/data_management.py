import httpx
import flet as ft
from pathlib import Path

from .base_view import BaseView
from config import Cfg


class DataManagementView(BaseView):
    def __init__(self, route="/data_management", name="数据管理"):
        super().__init__(route, name)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("商品编号")),
                ft.DataColumn(ft.Text("商品编码")),
                ft.DataColumn(ft.Text("商品名称")),
                ft.DataColumn(ft.Text("商品别名")),
                ft.DataColumn(ft.Text("创建时间")),
                ft.DataColumn(ft.Text("更新时间")),
            ],
        )
        self.controls = [
            self.table
        ]
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        # self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.scroll = ft.ScrollMode.AUTO

    
    def did_mount(self):
        token = self.page.client_storage.get("token")
        header = {
            "token": token
        }
        res = httpx.get(f"{Cfg.HOST}/data/select_all", headers=header, timeout=Cfg.TIMEOUT)
        js_res = res.json()
        for i in js_res:
            r = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(i["id"])),
                    ft.DataCell(ft.Text(i["code"])),
                    ft.DataCell(ft.Text(i["name"])),
                    ft.DataCell(ft.Text(i["alias"])),
                    ft.DataCell(ft.Text(i["create_time"])),
                    ft.DataCell(ft.Text(i["update_time"])),
                ],
            )
            self.table.rows.append(r)
        super().did_mount()