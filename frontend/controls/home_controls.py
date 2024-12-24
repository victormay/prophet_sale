import httpx
import flet as ft
import pandas as pd
from flet.matplotlib_chart import MatplotlibChart
from matplotlib import pyplot as plt

from config import Cfg


class Search(ft.Container):
    def __init__(self):
        super().__init__()
        self.search = ft.SearchBar(
            controls=[],
            bar_hint_text="选择一个商品...",
            view_hint_text="选择一个下列商品",
            on_tap=lambda e: e.control.open_view(),
        )
        self.pred_range = ft.TextField(
            label=ft.Text("预测周期", size=20), 
            hint_text="预测周期",
            value=7, 
            align_label_with_hint=True,
            width=100,
        )
        self.content = ft.Row(
            controls=[
                self.search,
                self.pred_range,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.padding = ft.padding.only(bottom=150)
    
    def did_mount(self):
        token_v = self.page.client_storage.get("token")
        res = httpx.get(f"{Cfg.HOST}/data/select_all", headers={"token": token_v}, timeout=Cfg.TIMEOUT)
        js_res = res.json()
        for idx, i in enumerate(js_res):
            if idx == 0:
                self.search.value = i["alias"]
            self.search.controls.append(
                ft.ListTile(title=ft.Text(i["alias"]), data=i["id"], on_click=self.search_click)
            )
        self.page.update()
        

    def search_click(self, e: ft.ControlEvent):
        self.search.close_view(e.control.title.value)
        
        g1: SingleGallery = self.parent.parent.g1
        g2: SingleGallery = self.parent.parent.g2
        g3: SingleGallery = self.parent.parent.g3
        g4: SingleGallery = self.parent.parent.g4
        g5: SingleTable = self.parent.parent.g5
        g1.ax.clear()
        g2.ax.clear()
        g3.ax.clear()
        g4.ax.clear()
        g5.g.rows.clear()

        id = int(e.control.data)
        range = int(self.pred_range.value)
        print(id, range)
        stoken_v = self.page.client_storage.get("token")
        headers = {
            "token": stoken_v
        }
        pred_args = {
            "id": id,
            "range": range,
            "reload": False
        }

        # 获取历史销售数据
        his_res = httpx.get(f"{Cfg.HOST}/data/sale_history/{id}", headers=headers)
        pd_his_data = pd.DataFrame(his_res.json())
        pd_his_data["date"] = pd.to_datetime(pd_his_data["date"])

        # g1 更新
        pd_his_data.plot(x="date", y="quantity", ax=g1.ax)
        g1.g.update()

        # 请求预测数据
        pred_res = httpx.post(f"{Cfg.HOST}/pred/pred_one_sku", headers=headers, json=pred_args)
        pd_pred_data = pd.DataFrame(pred_res.json())
        pd_pred_data["ds"] = pd.to_datetime(pd_pred_data["ds"]).dt.date


        # g2 更新
        pd_pred_data.plot(x="ds", y="trend", ax=g2.ax)
        g2.g.update()


        # g3 更新
        pd_pred_data.plot(x="ds", y=["yhat_lower", "yhat_upper", "yhat"], ax=g3.ax)
        g3.g.update()


        # g4 更新
        pd_pred_data.tail(range).plot.bar(x="ds", y="yhat", ax=g4.ax)
        g4.text.value.replace("n", str(range))
        g4.g.update()
        g4.update()

        # g5 更新
        total = 0
        idx = 0
        for _, i in pd_pred_data.tail(range)[["ds", "yhat"]].iterrows():
            idx += 1
            r = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(idx)),
                    ft.DataCell(ft.Text(i["ds"])),
                    ft.DataCell(ft.Text(i["yhat"])),
                ]
            )
            total += i["yhat"]
            g5.g.rows.append(r)
        t_r = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("总计")),
                    ft.DataCell(ft.Text("--")),
                    ft.DataCell(ft.Text(total)),
                ]
            )
        g5.g.rows.append(t_r)
        g5.text.value.replace("n", str(range))
        g5.update()
        # pd_data.head(his).plot(x="ds", y=)


class SingleGallery(ft.Container):
    def __init__(self, text, width=600):
        super().__init__()
        self.fig = plt.figure(layout="constrained")
        self.ax = self.fig.subplots()
        self.g = MatplotlibChart(self.fig, expand=True, isolated=True)
        self.text = ft.Text(text, theme_style=ft.TextThemeStyle.DISPLAY_SMALL)
        self.head = ft.Row(
            controls=[self.text],
            height=40,
        )
        self.gallery = ft.Row(
            controls=[self.g],
        )
        self.content = ft.Column(
            controls=[
                self.head,
                self.gallery
            ], 
        )


class SingleTable(ft.Container):
    def __init__(self, text, width=600):
        super().__init__()
        self.g = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("编号")),
                ft.DataColumn(ft.Text("日期")),
                ft.DataColumn(ft.Text("当日销量")),
            ]
        )
        self.text = ft.Text(text, theme_style=ft.TextThemeStyle.DISPLAY_SMALL)
        self.head = ft.Row(
            controls=[self.text],
            height=40,
        )
        self.gallery = ft.Row(
            controls=[self.g],
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.content = ft.Column(
            controls=[
                self.head,
                self.gallery
            ], 
        )


class TwoPart(ft.Container):
    def __init__(self, g1=None, g2=None, width=800, height=500):
        super().__init__()
        self.content = ft.Row(
            controls=[
                ft.Container(width=width, height=height, content=g1),
                ft.Container(width=width, height=height, content=g2),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=50
        )
        self.padding = ft.padding.only(bottom=200)


class SinglePart(ft.Container):
    def __init__(self, g1=None, width=800, height=500):
        super().__init__()
        self.content = ft.Row(
            controls=[
                ft.Container(width=width, height=height, content=g1),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=50
        )
        self.padding = ft.padding.only(bottom=200)


class HomePredShow(ft.Container):
    def __init__(self, g1="历史销售数据", g2="历史销售趋势", g3="数据拟合情况", g4="未来n天销售预测", g5="未来n天销售预测数据表"):
        super().__init__()
        self.search = Search()
        self.g1 = SingleGallery(g1)
        self.g2 = SingleGallery(g2)
        self.g3 = SingleGallery(g3)
        self.g4 = SingleGallery(g4)
        self.g5 = SingleTable(g5)
        self.p1 = TwoPart(self.g1, self.g2)
        self.p2 = TwoPart(self.g3, self.g4)
        self.p3 = SinglePart(self.g5, height=None)
        
        self.content = ft.Column([
                self.search,
                self.p1,
                self.p2,
                self.p3
            ])