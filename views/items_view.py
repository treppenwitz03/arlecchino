import flet as ft
from views.item_button import ItemButton
from views.group_button import AddReceivableButton

class ItemsView(ft.Column):
    group = None
    def __init__(self):
        super().__init__(
            expand=True,
            spacing=0
        )
        ########################################################
        ## Make the view for individual groups
        #######################################################
        
        self.group_image = ft.Image(
            "/default_image.png",
            height=80,
            width=80
        )
        
        self.group_name = ft.Text(
            expand=True,
            value=" ",
            weight=ft.FontWeight.W_600,
            size=44
        )
        
        header_left = ft.Row(
            expand=True,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=[self.group_image, self.group_name],
            spacing=20
        )
        
        self.reload_button = ft.IconButton(
            ft.icons.RESTART_ALT_OUTLINED, icon_size=48,
            padding=15
        )
        
        self.return_button = ft.IconButton(
            ft.icons.EXIT_TO_APP, icon_size=48,
            padding=15
        )
        
        end_row = ft.Row(
            controls=[self.reload_button, self.return_button]
        )
        
        header_row = ft.Row(
            controls = [header_left, end_row],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        self.header_container = ft.Container(
            padding = ft.padding.only(10, 10, 10, 10),
            border_radius=ft.BorderRadius(0, 0, 15, 15),
            content=header_row
        )
        
        self.payable_list = ft.ListView(
            expand = True,
            spacing = 20,
            padding = 20
        )
        
        self.empty_warning_text = ft.Text(
            expand=True,
            value="Your group has no payables yet.",
            weight=ft.FontWeight.W_400,
            size=20
        )
        
        empty_warning_text_row = ft.Column(
            controls=[
                ft.Lottie(
                    "https://lottie.host/78439950-e4f0-46c9-aba1-8c0e959fed9e/XDIN6eRr0L.json",
                    width=640,
                    animate=True,
                    expand=True
                ),
                self.empty_warning_text
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        self.empty_warning_text_container = ft.Container(
            content = empty_warning_text_row,
            padding = ft.padding.only(30, 10, 30, 0),
        )
        
        self.cont = ft.AnimatedSwitcher(
            transition = ft.AnimatedSwitcherTransition.FADE,
            duration = 300,
            reverse_duration = 300,
            switch_in_curve = ft.AnimationCurve.EASE_OUT,
            switch_out_curve = ft.AnimationCurve.EASE_IN,
            expand=True,
            content = self.payable_list
        )
        
        self.receivable_list = ft.ListView(
            expand = True,
            spacing = 20,
            padding = 20
        )
        
        self.payable_column = ft.Column(
            expand=True,
            spacing=0,
            controls=[self.cont]
        )
        
        self.receivable_column =ft.Column(
            expand=True,
            spacing=0,
            controls=[self.receivable_list]
        )
        
        self.add_receivable_button = AddReceivableButton()
        
        self.list_switcher = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            indicator_tab_size=True,
            expand=True,
            tabs=[
                ft.Tab(
                    "My Payables",
                    content = self.payable_column
                ),
                ft.Tab(
                    "My Receivables",
                    content = self.receivable_column
                )
            ]
        )
        
        self.group_name_text = ft.Text(
            " ",
            weight=ft.FontWeight.W_600,
            size=28
        )
        
        self.group_description = ft.Text(
            " ",
            weight=ft.FontWeight.W_400,
            size = 20,
            max_lines = 3,
            overflow=ft.TextOverflow.ELLIPSIS
        )
        
        self.created_by_text = ft.Text(
            value = "Created by: ",
            spans = [ft.TextSpan(
                " ",
                style=ft.TextStyle(italic=True, weight=ft.FontWeight.W_300)
            )],
            weight=ft.FontWeight.W_500,
            italic=True,
        )
        
        self.group_code_text = ft.Text(
            value = "Group Code: ",
            spans = [ft.TextSpan(
                " ",
                style=ft.TextStyle(italic=True, weight=ft.FontWeight.W_300)
            )],
            weight=ft.FontWeight.W_500,
            italic=True
        )

        self.group_code_copy_button = ft.Container(
            ft.Icon(ft.icons.COPY_OUTLINED, size=16),
            width=16,
            height=16,
            on_click=lambda _: self.copy_group_code()
        )
        
        self.user_image = ft.Image(
            "/empty_user_image.png",
            width=150,
            height=150
        )
        
        self.username = ft.Text(
            " ",
            size=20
        )
        
        self.financial_recap_text = ft.Text(
            "Financial Recap: ",
            italic=True,
            weight=ft.FontWeight.W_400
        )
        
        self.total_payable_text = ft.Text(
            "Total Payable: ",
            weight=ft.FontWeight.W_600
        )
        
        self.total_receivable_text = ft.Text(
            "Total Receivable: ",
            weight=ft.FontWeight.W_600
        )
        
        info_column = ft.Column(
            controls=[self.user_image, self.username],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        recap_column = ft.Column(
            controls=[self.financial_recap_text, self.total_payable_text, self.total_receivable_text],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
        
        self.personal_info_column = ft.Column(
            controls=[info_column, recap_column],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True
        )
        
        self.personal_info_container = ft.Container(
            content=ft.Row([self.personal_info_column], expand=True),
            border_radius=ft.BorderRadius(15, 15, 15, 15),
            expand=True,
            padding = 20,
            border=ft.border.all(1),
            bgcolor=ft.colors.SURFACE_VARIANT
        )
        
        self.group_info_column = ft.Column(
            controls=[
                self.group_name_text, 
                self.group_description, 
                self.created_by_text, 
                ft.Row([
                    self.group_code_text,
                    self.group_code_copy_button
                ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
            ]
        )
        
        self.info_sidebar_column = ft.Column(
            width=250,
            expand=True,
            controls=[self.group_info_column, self.personal_info_container]
        )
        
        self.info_sidebar = ft.Container(
            content = self.info_sidebar_column,
            padding = 10
        )
        
        list_view_row = ft.Row(
            controls=[self.list_switcher, self.info_sidebar],
            expand=True
        )
        
        self.controls = [self.header_container, list_view_row]
    
    # Set the creator
    def set_creator(self, creator):
        self.created_by_text.spans[0].text = creator
    
    # Set the user image
    def set_user_image(self, user_image: str):
        if user_image != "":
            self.user_image.src_base64 = user_image
    
    # make a callback to trigger reload
    def on_trigger_reload(self, event: ft.ControlEvent):
        pass

    def set_informations(self, informations: dict):
        self.group_name.value = self.group_name_text.value = informations["group_name"]
        self.group_image.src_base64 = informations["group_image"]
        self.group_description.value = informations["group_desc"]
        self.username.value = informations["username"]
        self.group_code_text.spans[0].text = informations["group_code"]
        self.set_creator(informations["creator"])
        self.set_user_image(informations["user_image"])
    
    def request_open_group(self, group_name: str, group_image: str, from_reload: bool):
        pass

    def copy_group_code(self):
        pass