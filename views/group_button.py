import flet as ft
from models import Group

class GroupButton(ft.ElevatedButton):
    group: Group = None
    def __init__(self, group_name: str, image_string: str):
        super().__init__()
        ####################################################
        ## Make the UI for the group button
        ####################################################
        
        self.group_name = group_name
        self.image_string = image_string
        
        self.text = ft.Container(
            content=ft.Text(
                group_name,
                weight=ft.FontWeight.W_700,
                size=20
            ),
            padding=ft.padding.only(10, 10, 10, 0)
        )
        
        self.text_row = ft.Row(
            controls=[self.text],
            alignment=ft.MainAxisAlignment.CENTER
        )
            
        group_image = ft.Image(
            "/default_image.png",
            width=130,
            height=130
        )
        
        if image_string != "":
            group_image.src_base64 = self.image_string
            
        
        self.image = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[group_image]
        )
        
        column = ft.Column(
            controls=[self.text_row, ft.Container(content=self.image, padding=10)],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0
        )
        
        self.content = column
        self.on_click = lambda event: self.activate(self, group_name, self.image_string)
        self.style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    
    # make a callback for when this button is clicked
    def activate(self, this, group_name: str, image_string: str):
        pass
    
    def update_colors(self, colors):
        self.text.content.color = colors["ae8948"]

class AddReceivableButton(GroupButton):
    def __init__(self):
        super().__init__("Add", "")
        # create a groupbutton specifically for opening the group addition/creation dialog
        
        self.image.controls[0].src = "/add_icon.svg"
        self.text_row.visible = False

class AddGroupButton(ft.PopupMenuButton):
    def __init__(self):
        super().__init__()
        # create a button specifically for opening the group addition/creation dialog
            
        group_image = ft.Image(
            "/add_icon.svg",
            width=130,
            height=130
        )
            
        
        self.image = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[group_image]
        )
        
        column = ft.Column(
            controls=[ft.Container(content=self.image, padding=10)],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0
        )
        
        self.content = column
        self.style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )

        self.items = [
            ft.PopupMenuItem("Search Groups", ft.icons.SEARCH_OUTLINED, on_click = lambda e: self.on_search_groups(e)),
            ft.PopupMenuItem("Create New", ft.icons.CREATE_OUTLINED, on_click = lambda e: self.on_create_group(e)),
            ft.PopupMenuItem("Join Group", ft.icons.JOIN_LEFT_OUTLINED, on_click = lambda e: self.on_join_group(e))
        ]

    def on_search_groups(self, event):
        pass

    def on_create_group(self, event):
        pass

    def on_join_group(self, event):
        pass