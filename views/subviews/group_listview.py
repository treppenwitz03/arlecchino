import flet as ft
from views.widgets.group_button import GroupButton, AddGroupButton
from views.subviews.items_view import ItemsView

class GroupListView(ft.AnimatedSwitcher):
    def __init__(self, text_values: dict):
        super().__init__(
            offset=ft.transform.Offset(0, 0),
            animate_offset = ft.animation.Animation(300),
            transition = ft.AnimatedSwitcherTransition.SCALE,
            duration = 300,
            reverse_duration = 300,
            switch_in_curve = ft.AnimationCurve.EASE_OUT,
            switch_out_curve = ft.AnimationCurve.EASE_IN, content=ft.Text("")
        )
        
        ############################################################
        ## Make the UI for the group list
        ############################################################
        
        self.top_text = ft.Text(
            expand=True,
            value="Hello User",
            weight=ft.FontWeight.W_600,
            size=54
        )
        
        top_text_row = ft.Row(
            expand=True,
            controls=[self.top_text]
        )
        
        self.top_text_container = ft.Container(
            padding = ft.padding.only(30, 30, 30, 0),
            content=top_text_row
        )

        self.subtitle_text = ft.Text(
            expand=True,
            value=text_values["grouplistview_subtitle"],
            weight=ft.FontWeight.W_400,
            size=20
        )

        subtitle_text_row = ft.Row(
            expand=True,
            controls=[self.subtitle_text]
        )

        self.subtitle_text_container = ft.Container(
            padding=ft.padding.only(30, 0, 30, 0),
            content=subtitle_text_row
        )
        
        self.empty_warning_text = ft.Text(
            expand=True,
            value=text_values["group_empty_warning"],
            weight=ft.FontWeight.W_400,
            size=20
        )
        
        empty_warning_text_row = ft.Row(
            controls=[self.empty_warning_text]
        )
        
        self.empty_warning_text_container = ft.Container(
            content = empty_warning_text_row,
            padding = ft.padding.only(30, 10, 30, 0),
            offset=ft.transform.Offset(0, 0),
            animate_offset=ft.animation.Animation(250)
        )
        
        self.grid = ft.GridView(
            expand = True,
            runs_count=5,
            max_extent=256,
            child_aspect_ratio=1.0,
            spacing=20,
            run_spacing=20,
            padding = 30
        )
        
        self.items_view = ItemsView(text_values)
        
        self.grid_view = ft.Column(
            controls=[
                self.top_text_container,
                self.subtitle_text_container,
                self.empty_warning_text_container,
                self.grid
            ]
        )
        
        self.content = self.grid_view
        self.add_button = AddGroupButton()

    # dictates whether the show or hide the group list view
    def show(self, delta):
        self.offset = ft.transform.Offset(0, delta)
        self.update()
    
    # make a callback for triggering reload
    def trigger_reload(self, email: str):
        pass

    def add_group_button(self, group_name: str, group_image: str):
        group_button = GroupButton(group_name, group_image)
        group_button.activate = lambda group_name, group_image: self.request_open_group(group_name, group_image, False)
        self.grid.controls.insert(len(self.grid.controls) -2, group_button)

        button_id = str(group_name.__hash__())
        return button_id
    
    def request_open_group(self, group_name: str, group_image: str, from_reload: bool):
        pass

    def start_group_filling(self):
        pass
    
    def refresh_grid(self):
        self.grid.controls = []
        self.grid.controls.append(self.add_button)
    
    def set_greeting(self, greeting):
        self.top_text.value = greeting