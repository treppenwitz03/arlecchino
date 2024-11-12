import flet as ft

class JoinGroupDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        ###################################################
        ## Make the UI for joining dialog
        ###################################################
        self.title = ft.Text("Join a group")
        
        self.group_code_textfield = ft.TextField(
            label = "Enter 8 digit group code",
            border_radius = 15,
            expand = True,
            height=44,
            label_style = ft.TextStyle()
        )
        
        group_code_textfield_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        group_code_textfield_row.controls.append(self.group_code_textfield)
        
        self.check_if_exists_button = ft.ElevatedButton(
            disabled=True,
            content=ft.Text(
                value="Verify group code",
            )
        )
        
        check_if_exists_btn_container = ft.Container(
            content=self.check_if_exists_button,
            padding=10
        )
        
        check_if_exists_row = ft.Row(
            controls=[check_if_exists_btn_container],
            alignment=ft.MainAxisAlignment.END
        )
        
        self.join_column = ft.Column(
            controls=[group_code_textfield_row, check_if_exists_row],
            alignment=ft.MainAxisAlignment.CENTER,
            width=400,
            height=100
        )
        
        self.join_button = ft.TextButton("Join", disabled=True)
        self.close_button = ft.TextButton("Cancel")
        
        self.content = self.join_column
        self.actions = [
            self.join_button,
            self.close_button
        ]
        self.actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    
    # get the entered group code
    def get_group_code_entry(self):
        return self.group_code_textfield.value
    
    # update the colors with scheme
    def update_colors(self, colors):
        self.group_code_textfield.border_color = colors["d6d6d6"]
        self.group_code_textfield.cursor_color = colors["black"]
        self.group_code_textfield.bgcolor = colors["d6d6d6"]
        self.group_code_textfield.color = colors["black"]
        self.group_code_textfield.label_style.color = colors["black"]
        
        self.check_if_exists_button.bgcolor = colors["d6d6d6"]
        self.check_if_exists_button.content.color = colors["ae8948"]

class CreateGroupDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        ###################################################
        ## Make the UI for group adding and joining dialog
        ###################################################
        self.title = ft.Text("Create group")
        
        self.image_preview = ft.Image(
            "/default_image.png",
            width=160,
            height=160
        )
        
        image_preview_row = ft.Row(
            controls=[self.image_preview],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.image_upload_button = ft.ElevatedButton(
            height=30,
            width=160,
            content=ft.Text(
                value="Upload image",
            )
        )
        
        image_upload_button_row = ft.Row(
            controls=[self.image_upload_button],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        image_upload_column = ft.Column(
            controls=[image_preview_row, image_upload_button_row],
            spacing=20
        )
        
        self.group_name_textfield = ft.TextField(
            label = "Group Name",
            border_radius = 15,
            width=220,
            height=44,
            label_style = ft.TextStyle()
        )
        
        group_name_textfield_row = ft.Row(
            controls=[self.group_name_textfield],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.group_desc_textfield = ft.TextField(
            label = "Group Description",
            border_radius = 15,
            width = 220,
            height = 300,
            multiline=True,
            min_lines=5,
            max_lines=5,
            label_style = ft.TextStyle()
        )
        
        group_desc_textfield_row = ft.Row(
            controls=[self.group_desc_textfield],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        group_information_column = ft.Column(
            controls=[group_name_textfield_row, group_desc_textfield_row],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
        
        self.creation_row = ft.Row(
            expand=True,
            controls=[image_upload_column, group_information_column],
            spacing=18,
            width=400,
            height=200
        )
        
        self.create_new_button = ft.TextButton("Create New", disabled=True)
        self.close_button = ft.TextButton("Cancel")
        
        self.content = self.creation_row
        self.actions = [
            self.create_new_button,
            self.close_button
        ]
        self.actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    
    # get the entered group name
    def get_created_group_name(self):
        return self.group_name_textfield.value
    
    # get the entered group description
    def get_created_group_desc(self):
        return self.group_desc_textfield.value
    
    # update the colors with scheme
    def update_colors(self, colors):
        self.image_upload_button.bgcolor = colors["d6d6d6"]
        self.image_upload_button.content.color = colors["black"]
        
        self.group_name_textfield.border_color = colors["d6d6d6"]
        self.group_name_textfield.cursor_color = colors["black"]
        self.group_name_textfield.bgcolor = colors["d6d6d6"]
        self.group_name_textfield.color = colors["black"]
        self.group_name_textfield.label_style.color = colors["black"]
        
        self.group_desc_textfield.border_color = colors["d6d6d6"]
        self.group_desc_textfield.cursor_color = colors["black"]
        self.group_desc_textfield.bgcolor = colors["d6d6d6"]
        self.group_desc_textfield.color = colors["black"]
        self.group_desc_textfield.label_style.color = colors["black"]

class SearchGroupsDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        ###################################################
        ## Make the UI for searching dialog
        ###################################################
        self.title = ft.Text("Search Groups")
        
        self.search_bar = ft.SearchBar(
            width=300,
            bar_hint_text="Search groups...",
            view_hint_text="Choose a group from the suggestions..."
        )

        self.load_group_button = ft.IconButton(icon=ft.icons.SEARCH, disabled=True)
        
        self.search_column = ft.Row(
            controls=[self.search_bar, self.load_group_button],
            alignment=ft.MainAxisAlignment.CENTER,
            width=400
        )
        
        self.image_preview = ft.Image(
            "/default_image.png",
            width=160,
            height=160
        )
        
        image_preview_column = ft.Row(
            controls=[self.image_preview],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.group_name_text = ft.Text(
            "Group Name",
            size=16,
            weight=ft.FontWeight.W_700,
            width=220
        )
        
        self.group_desc_text = ft.Text(
            "Group Description: ",
            size=12,
            weight=ft.FontWeight.W_400,
            width=220
        )

        self.group_creator_text = ft.Text(
            "Created: Creator",
            size=12,
            weight=ft.FontWeight.W_400,
            width=220
        )
        
        group_information_column = ft.Column(
            controls=[self.group_name_text, self.group_creator_text, self.group_desc_text],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8
        )
        
        self.join_row = ft.Row(
            expand=True,
            controls=[image_preview_column, group_information_column],
            spacing=18
        )

        self.place_holder = ft.Text("", width=400, height=100)
        
        self.switcher = ft.AnimatedSwitcher(
            content = self.place_holder,
            width = 400,
            height = 100,
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=300,
            reverse_duration=300,
            switch_in_curve=ft.AnimationCurve.LINEAR,
            switch_out_curve=ft.AnimationCurve.LINEAR,
        )

        self.main_column = ft.Column([
            self.search_column,
            self.switcher
        ], height=200)
        
        self.join_button = ft.TextButton("Join", disabled = True)
        self.close_button = ft.TextButton("Cancel")
        
        self.content = self.main_column
        self.actions = [
            self.join_button,
            self.close_button
        ]
        self.actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN

    ################## set whether to join or create group ############################
    def switch_to_has_value(self):
        self.switcher.content = self.join_row
             
    def switch_to_placeholder(self):
        self.switcher.content = self.place_holder
    ###################################################################################