import flet as ft

class BgImage(ft.Container):
    def __init__(self, img="/images/bg.png"):
        super().__init__()
        self.image = ft.DecorationImage(img, fit=ft.ImageFit.FILL)
        self.expand = True