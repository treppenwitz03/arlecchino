import flet as ft

class AddReceivableDialog(ft.AlertDialog):
    def __init__(self, text_values: dict):
        super().__init__()
        ####################################################
        ## Make the Add receivable dialog
        ####################################################
        self.group = ""
        
        self.add_item_button = ft.TextButton(text_values["add_item"], disabled=True)
        self.cancel_button = ft.TextButton(text_values["cancel"])
        
        self.actions = [
            self.add_item_button,
            self.cancel_button
        ]
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN 
        
        self.item_image = ft.Image(
            "/default_image.png",
            width = 250,
            height = 250
        )
        
        self.choose_button = ft.ElevatedButton(
            height=44,
            width=160,
            content=ft.Text(
                value=text_values["upload"],
            )
        )
        
        image_upload_column = ft.Column(
            controls=[self.item_image, self.choose_button],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        self.item_name_textfield = ft.TextField(
            label = text_values["item_name"],
            border_radius = 15,
            width=230,
            height=44,
            label_style = ft.TextStyle()
        )
        
        self.item_month_dropdown = ft.Dropdown(
            hint_text = text_values["month"],
            options = [
                ft.dropdown.Option(text_values["january"]), ft.dropdown.Option(text_values["february"]), ft.dropdown.Option(text_values["march"]), ft.dropdown.Option(text_values["april"]),
                ft.dropdown.Option(text_values["may"]), ft.dropdown.Option(text_values["june"]), ft.dropdown.Option(text_values["july"]), ft.dropdown.Option(text_values["august"]),
                ft.dropdown.Option(text_values["september"]), ft.dropdown.Option(text_values["october"]), ft.dropdown.Option(text_values["november"]), ft.dropdown.Option(text_values["december"])
            ],
            border_radius = 15,
            width=85,
            height=54,
            autofocus=True
        )
        
        self.item_day_dropdown = ft.Dropdown(
            hint_text = text_values["day"],
            border_radius = 15,
            width=60,
            height=54
        )
        
        self.item_year_dropdown = ft.Dropdown(
            hint_text = text_values["year"],
            border_radius = 15,
            width=65,
            height=54
        )
        
        item_date_row = ft.Row(
            controls=[self.item_month_dropdown, self.item_day_dropdown, self.item_year_dropdown],
            spacing=10
        )
        
        self.item_amount_textfield = ft.TextField(
            label = text_values["amount"],
            border_radius = 15,
            width=230,
            height=44,
            input_filter=ft.NumbersOnlyInputFilter()
        )
        
        self.item_description_textfield = ft.TextField(
            label = text_values["description"],
            border_radius = 15,
            width = 230,
            height = 290,
            multiline=True,
            min_lines=5,
            max_lines=5,
            label_style = ft.TextStyle()
        )
        
        info_column = ft.Column(
            controls=[self.item_name_textfield, item_date_row, self.item_amount_textfield, self.item_description_textfield]
        )
        
        main_row = ft.Row(
            controls=[image_upload_column, info_column],
            width = 500,
            height = 300,
        )
        
        self.content = main_row
        self.modal = False

        for day in range(31):
            self.item_day_dropdown.options.append(ft.dropdown.Option(day + 1))
        
        for year in range(2020, 2024):
            self.item_year_dropdown.options.append(ft.dropdown.Option(year + 1))
    
    # get entered item name
    def get_item_name(self):
        return self.item_name_textfield.value
    
    # get entered creation month
    def get_item_creation_month(self):
        return self.item_month_dropdown.value
    
    # get entered creation day
    def get_item_creation_day(self):
        return self.item_day_dropdown.value
    
    # get entered creation year
    def get_item_creation_year(self):
        return self.item_year_dropdown.value
    
    # get the entered item amount
    def get_item_amount(self):
        return self.item_amount_textfield.value
    
    # get the item description
    def get_item_description(self):
        return self.item_description_textfield.value