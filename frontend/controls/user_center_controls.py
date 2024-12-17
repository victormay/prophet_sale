import flet as ft


class UserInfoControl(ft.Container):
    def __init__(self, width):
        super().__init__()
        self.id = ft.TextField("", label="用户ID", width=width)
        self.username = ft.TextField("", label="用户名称", width=width)
        self.email = ft.TextField("", label="用户EMAIL", width=width)
        self.create_time = ft.TextField("", label="创建时间", width=width)
        self.update_time = ft.TextField("", label="更新时间", width=width)
        self.user_type = ft.TextField("", label="用户类型", width=width)
        self.content = ft.Column([
            self.id,
            self.username,
            self.email,
            self.create_time,
            self.update_time,
            self.user_type
        ])

    def did_mount(self):
        self.id.value = self.page.client_storage.get("id")
        self.username.value = self.page.client_storage.get("username")
        self.email.value = self.page.client_storage.get("email")
        self.create_time.value = self.page.client_storage.get("create_time")
        self.update_time.value = self.page.client_storage.get("update_time")
        self.user_type.value = "管理员" if self.page.client_storage.get("admin") else "普通用户"
        self.page.update()
