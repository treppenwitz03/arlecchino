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
            width=150,
            height=150
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
            spacing=0,
            width=256,
            height=256
        )
        
        self.content = column
        self.on_click = lambda event: self.activate(group_name, self.image_string)
        self.style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    
    # make a callback for when this button is clicked
    def activate(self, group_name: str, image_string: str):
        pass

class AddReceivableButton(GroupButton):
    def __init__(self):
        super().__init__("Add", "")
        # create a groupbutton specifically for opening the group addition/creation dialog
        self.content.height = 175
        self.image.controls[0] = ft.Icon(
            ft.icons.ADD_ROUNDED,
            size = 150
        )
        self.text_row.visible = False

class AddGroupButton(ft.PopupMenuButton):
    def __init__(self):
        super().__init__()
        # create a button specifically for opening the group addition/creation dialog
            
        group_image = ft.Icon(
            ft.icons.ADD_ROUNDED,
            size = 130
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