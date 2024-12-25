import httpx
import flet as ft
from pathlib import Path

from .base_view import BaseView
from config import Cfg
from controls.model_controls import ModelConfig


class ModelManagementView(BaseView):
    def __init__(self, route="/model_management", name="模型管理"):
        super().__init__(route, name)
        self.model_config = ModelConfig()
        self.controls = [self.model_config]
        self.scroll = ft.ScrollMode.AUTO
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER