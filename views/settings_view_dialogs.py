import flet as ft

class AppearanceDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        ###############################################
        ## Make the Ui for changing the app appearance
        ###############################################
        title = ft.Text("Appearance", weight=ft.FontWeight.BOLD)
        self.subtitle = ft.Text("Customize the app's visual style and layout to suit your preferences.", size=12)
        
        title_column = ft.Column(
            controls = [title, self.subtitle]
        )
        
        self.title = title_column
        
        dark_mode_text = ft.Text("Dark Mode", weight=ft.FontWeight.W_700)
        self.dark_mode_switch = ft.Switch()
        
        dark_mode_row = ft.Row(
            controls=[dark_mode_text, self.dark_mode_switch],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        self.content = dark_mode_row
        
        def close(event: ft.ControlEvent):
            self.open = False
            self.page.update()
        
        close_button = ft.TextButton("Close")
        close_button.on_click = close
        
        self.actions = [close_button]
        self.actions_alignment = ft.MainAxisAlignment.END
        
        self.dark_mode_switch.on_change = lambda e: self.on_change(e)
    
    # MAke the callback when the settings are changed
    def on_change(self, event):
        pass
    
    def update_colors(self, colors):
        self.subtitle.color = colors["a6a6a6"]
        
class CurrencyDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        #################################
        ## Make the UI for currency setting
        #################################
        title = ft.Text("Currency", weight=ft.FontWeight.BOLD)
        self.subtitle = ft.Text("Please be cautious when changing the app's currency, as this action may result in potential pricing and conversion issues for your transactions.", width=400, size=12)
        
        title_column = ft.Column(
            controls = [title, self.subtitle]
        )
        
        self.title = title_column
        
        self.currency_choices = ft.RadioGroup(
            content=ft.Row([
                ChoiceButton("PHP", "ph.png"),
                ChoiceButton("USD", "usa.png"),
                ChoiceButton("EU", "eu.png")
            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START, height=100, spacing=50),
        )
        
        self.content = self.currency_choices
        
        def close(event: ft.ControlEvent):
            self.open = False
            self.page.update()
        
        close_button = ft.TextButton("Close")
        close_button.on_click = close
        
        self.actions = [close_button]
        self.actions_alignment = ft.MainAxisAlignment.END
        self.currency_choices.on_change = lambda event: self.on_change(self.currency_choices.value)
    
    # Call on_change when settings is changed
    def on_change(self, currency):
        pass
    
    # update color with scheme
    def update_colors(self, colors):
        self.subtitle.color = colors["a6a6a6"]

class ChoiceButton(ft.Column):
    def __init__(self, label: str, source: str):
        super().__init__()
        #########################################################
        # Create the UI for the currency choices
        ########################################################
        
        supporting_image = ft.Container(
            ft.Image(
                "/" + source,
                width=50,
                height=50,
                fit=ft.ImageFit.FILL
            ),
            border_radius=5
        )
        
        button_name = ft.Text(
            label,
            weight=ft.FontWeight.W_400
        )
        
        self.controls = [
            ft.Radio(value=label),
            supporting_image,
            button_name
        ]
        
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 10