import httpx
import flet as ft

from config import Cfg


class ModelConfig(ft.Container):
    def __init__(self, width=800):
        super().__init__()
        self.c_id = ft.TextField(label="配置编号", hint_text="配置编号", align_label_with_hint=True, expand=True)
        self.c_user_id = ft.TextField(label="创建人编号", hint_text="创建人编号", align_label_with_hint=True, expand=True)
        self.c_create_time = ft.TextField(label="创建时间", hint_text="创建时间", align_label_with_hint=True, expand=True)
        self.c_growth = ft.TextField(label="配置参数_growth", hint_text="配置参数_growth", align_label_with_hint=True, expand=True)
        self.c_n_changepoints = ft.TextField(label="配置参数_n_changepoints", hint_text="配置参数_n_changepoints", align_label_with_hint=True, expand=True)
        self.c_changepoint_range = ft.TextField(label="配置参数_changepoint_range", hint_text="配置参数_changepoint_range", align_label_with_hint=True, expand=True)
        self.c_yearly_seasonality = ft.TextField(label="配置参数_yearly_seasonality", hint_text="配置参数_yearly_seasonality", align_label_with_hint=True, expand=True)
        self.c_weekly_seasonality = ft.TextField(label="配置参数_weekly_seasonality", hint_text="配置参数_weekly_seasonality", align_label_with_hint=True, expand=True)
        self.c_daily_seasonality = ft.TextField(label="配置参数_daily_seasonality", hint_text="配置参数_daily_seasonality", align_label_with_hint=True, expand=True)
        self.c_seasonality_mode = ft.TextField(label="配置参数_seasonality_mode", hint_text="配置参数_seasonality_mode", align_label_with_hint=True, expand=True)
        self.c_seasonality_prior_scale = ft.TextField(label="配置参数_seasonality_prior_scale", hint_text="配置参数_seasonality_prior_scale", align_label_with_hint=True, expand=True)
        self.c_holidays_prior_scale = ft.TextField(label="配置参数_holidays_prior_scale", hint_text="配置参数_holidays_prior_scale", align_label_with_hint=True, expand=True)
        self.c_changepoint_prior_scale = ft.TextField(label="配置参数_changepoint_prior_scale", hint_text="配置参数_changepoint_prior_scale", align_label_with_hint=True, expand=True)
        self.c_mcmc_samples = ft.TextField(label="配置参数_mcmc_samples", hint_text="配置参数_mcmc_samples", align_label_with_hint=True, expand=True)
        self.c_interval_width = ft.TextField(label="配置参数_interval_width", hint_text="配置参数_interval_width", align_label_with_hint=True, expand=True)
        self.c_uncertainty_samples = ft.TextField(label="配置参数_uncertainty_samples", hint_text="配置参数_uncertainty_samples", align_label_with_hint=True, expand=True)
        self.c_scaling = ft.TextField(label="配置参数_scaling", hint_text="配置参数_scaling", align_label_with_hint=True, expand=True)
        self.c_holidays_mode = ft.TextField(label="配置参数_holidays_mode", hint_text="配置参数_holidays_mode", align_label_with_hint=True, expand=True)
        self.edit_btn = ft.FilledTonalButton(text="编辑", icon=ft.icons.EDIT, on_click=self.edit)
        self.save_btn = ft.FilledTonalButton(text="保存", icon=ft.icons.SAVE, on_click=self.save)

        self.content = ft.Column(
            controls=[
                ft.Row(height=50, width=width),
                ft.Row([self.c_id, self.c_user_id], width=width),
                ft.Row([self.c_create_time, self.c_growth], width=width),
                ft.Row([self.c_n_changepoints, self.c_changepoint_range], width=width),
                ft.Row([self.c_yearly_seasonality, self.c_weekly_seasonality], width=width),
                ft.Row([self.c_daily_seasonality, self.c_seasonality_mode], width=width),
                ft.Row([self.c_seasonality_prior_scale, self.c_holidays_prior_scale], width=width),
                ft.Row([self.c_changepoint_prior_scale, self.c_mcmc_samples], width=width),
                ft.Row([self.c_interval_width, self.c_uncertainty_samples], width=width),
                ft.Row([self.c_scaling, self.c_holidays_mode], width=width),
                ft.Row(height=100, width=width),
                ft.Row([self.edit_btn, self.save_btn], width=width, alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ]
        )
        self.expand = True

    def did_mount(self):
        self.init()
        self.read_only(True)
        self.save_btn.disabled = True
        self.page.update()

    def edit(self, e):
        self.read_only(False)
        self.edit_btn.disabled = True
        self.save_btn.disabled = False
        self.page.update()
    
    def save(self, e):
        self.read_only(True)
        self.edit_btn.disabled = False
        self.save_btn.disabled = True
        self.page.update()

    def read_only(self, e: bool):
        for _, v in self.cfgs().items():
            v.read_only = e

    def init(self):
        headers = {
            "token": self.page.client_storage.get("token")
        }
        res = httpx.get(f"{Cfg.HOST}/pred/get_latest_pconfig", headers=headers)
        js_res = res.json()
        for k, v in self.cfgs().items():
            v.value = js_res[k]

    def cfgs(self):
        return {
            "id": self.c_id,
            "user_id": self.c_user_id,
            "create_time": self.c_create_time,
            "growth": self.c_growth,
            "n_changepoints": self.c_n_changepoints,
            "changepoint_range": self.c_changepoint_range,
            "yearly_seasonality": self.c_yearly_seasonality,
            "weekly_seasonality": self.c_weekly_seasonality,
            "daily_seasonality": self.c_daily_seasonality,
            "seasonality_mode": self.c_seasonality_mode,
            "seasonality_prior_scale": self.c_seasonality_prior_scale,
            "holidays_prior_scale": self.c_holidays_prior_scale,
            "changepoint_prior_scale": self.c_changepoint_prior_scale,
            "mcmc_samples": self.c_mcmc_samples,
            "interval_width": self.c_interval_width,
            "uncertainty_samples": self.c_uncertainty_samples,
            "scaling": self.c_scaling,
            "holidays_mode": self.c_holidays_mode,
        }
    