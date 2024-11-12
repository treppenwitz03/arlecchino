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

        accent_color_text = ft.Text("Accent Color", weight=ft.FontWeight.W_700)
        self.accent_color_radio = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="#8C161E", width=48, height=48, fill_color="#8C161E"),
                ft.Radio(value="#61A7C7", width=48, height=48, fill_color="#61A7C7"),
                ft.Radio(value="#4C64BC", width=48, height=48, fill_color="#4C64BC"),
                ft.Radio(value="#E6B6F1", width=48, height=48, fill_color="#E6B6F1"),
                ft.Radio(value="#2D3E89", width=48, height=48, fill_color="#2D3E89"),
                ft.Radio(value="#E29A21", width=48, height=48, fill_color="#E29A21"),
                ft.Radio(value="#99CE43", width=48, height=48, fill_color="#99CE43")
            ])
        )

        accent_row = ft.Row([
            accent_color_text,
            self.accent_color_radio
        ])
        
        self.content = ft.Column([
            dark_mode_row,
            accent_row
        ], height=100)
        
        def close(event: ft.ControlEvent):
            self.open = False
            self.page.update()
        
        close_button = ft.TextButton("Close")
        close_button.on_click = close
        
        self.actions = [close_button]
        self.actions_alignment = ft.MainAxisAlignment.END
        
        self.dark_mode_switch.on_change = lambda e: self.on_change(e)
        self.accent_color_radio.on_change = lambda e: self.accent_change(e)
    
    # MAke the callback when the settings are changed
    def on_change(self, event):
        pass

    def accent_change(self, event):
        pass
        
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

class LanguageDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        #################################
        ## Make the UI for currency setting
        #################################
        title = ft.Text("Language", weight=ft.FontWeight.BOLD)
        self.subtitle = ft.Text("Please be cautious in changing the application language as you may have difficulty in returning to your needed language.", width=400, size=12)
        
        title_column = ft.Column(
            controls = [title, self.subtitle]
        )
        
        self.title = title_column
        
        self.language_choices = ft.RadioGroup(
            content=ft.Column([
                ft.Radio("English", value="en"),
                ft.Radio("Tagalog", value="tag"),
                ft.Radio("Cebuano", value="ceb"),
                ft.Radio("Español", value="esp"),
                ft.Radio("日本語", value="jp")
            ], height=250, spacing=16)
        )
        
        self.content = self.language_choices
        
        def close(event: ft.ControlEvent):
            self.open = False
            self.page.update()
        
        close_button = ft.TextButton("Close")
        close_button.on_click = close

        reload = ft.FilledButton("Save and reload", style=ft.ButtonStyle(color=ft.colors.ON_ERROR, bgcolor=ft.colors.ERROR))
        reload.on_click = lambda e: self.on_change(self.language_choices.value)
        
        self.actions = [reload, close_button]
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    
    # Call on_change when settings is changed
    def on_change(self, language):
        pass

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