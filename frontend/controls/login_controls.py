import flet as ft

from requests.user import login


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
        self.email = ft.TextField(hint_text="email")
        self.password = ft.TextField(hint_text="password", password=True)
        self.login_btn = ft.ElevatedButton("Login",icon=ft.icons.LOGIN, on_click=self.on_click, bgcolor=ft.colors.BLUE_200)
        self.controls = [
            ft.Column(controls=[self.email, self.password]),
            ft.Row(controls=[self.login_btn], expand=True, alignment=ft.MainAxisAlignment.CENTER)
        ]
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.expand = True

    def on_click(self, e):
        login(self.page, self.email.value, self.password.value)

    def update(self):
        self.email.value = ""
        self.password.value = ""
        self.page.update()


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
        print(self.email.value, self.password.value)
        e.page.update()

    def update(self):
        self.email.value = ""
        self.password.value = ""
        self.page.update()


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