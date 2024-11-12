import flet as ft
from views.widgets.item_button import ItemButton

class ItemInfoDialog(ft.AlertDialog):
    group_name = None
    def __init__(self, text_values: dict):
        super().__init__()
        #################################################
        ## Make the UI when payable/receivable is clicked
        #################################################
        self.item_name = ft.Text(
            " ",
            weight=ft.FontWeight.W_700,
        )
        
        self.price = ft.Text(
            " ",
            weight=ft.FontWeight.W_700,
        )
        
        self.title = ft.Row(
            controls = [self.item_name, self.price],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        self.item_image = ft.Image(
            "/default_image.png",
            width=120,
            height=120
        )
        
        self.account_image = ft.Image(
            "/empty_user_image.png",
            width = 36,
            height = 36
        )
        
        self.account_name_info = ft.Text(
            " "
        )
        
        account_row = ft.Row(
            controls=[self.account_image, self.account_name_info],
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        self.description = ft.Text(
            " ",
            weight=ft.FontWeight.W_400
        )
        
        description_column = ft.Column(
            controls=[self.description],
            height=100,
            scroll=ft.ScrollMode.ALWAYS
        )
        
        self.item_post_time = ft.Text(
            value = text_values["date_posted"],
            spans = [ft.TextSpan(
                f" ",
                style=ft.TextStyle(italic=True, weight=ft.FontWeight.W_300)
            )],
            weight=ft.FontWeight.W_500,
            italic=True,
        )
        
        info_column = ft.Column(
            controls=[account_row, description_column, self.item_post_time],
            width = 350,
            height = 150
        )
        
        self.main_row = ft.Row(
            controls = [self.item_image, info_column]
        )
        
        qr_indicator = ft.Text(
            text_values["pay_with_qr"]
        )
        
        self.qr_code = ft.Image(
            "/sample_qr.png",
            width = 120,
            height = 120
        )
        
        qr_column = ft.Column(
            controls=[qr_indicator, self.qr_code],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        self.account_image = ft.Image(
            "/empty_user_image.png",
            width = 30,
            height = 30
        )
        
        self.account_name_payment = ft.Text(
            " ",
            size=12
        )
        
        gcash_acct_user = ft.Column(
            controls=[self.account_image, self.account_name_payment],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        )
        
        self.gcash_number = ft.Text(
            value = text_values["gcash_field"],
            size=14,
            spans = [ft.TextSpan(
                f" ",
            )],
        )
        
        gcash_info_row = ft.Row(
            controls=[gcash_acct_user, self.gcash_number],
            spacing=10
        )
        
        self.payment_item_name = ft.Text(
            value = text_values["item_field"],
            spans = [ft.TextSpan(
                f" ",
            )],
        )
        
        self.item_price = ft.Text(
            value = text_values["amount_2b_paid"],
            spans = [ft.TextSpan(
                " ",
            )],
        )
        
        gcash_info_column = ft.Column(
            controls=[gcash_info_row, self.payment_item_name, self.item_price],
            width = 300,
            spacing=30
        )
        
        self.gcash_container = ft.Container(
            content=gcash_info_column,
            padding=5
        )
        
        self.payment_row = ft.Row(
            controls=[qr_column, self.gcash_container],
            spacing = 50,
            width = 480,
            height = 150
        )
        
        self.payment_preview_image = ft.Image(
            src="/default_image.png",
            width=120,
            height=120
        )
        
        self.upload_proof_button = ft.ElevatedButton(
            content=ft.Text(
                value=text_values["upload_proof"]
            )
        )
        
        self.proof_column = ft.Column(
            width = 480,
            height = 150,
            controls=[self.payment_preview_image, self.upload_proof_button],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.switcher = ft.AnimatedSwitcher(
            content = self.main_row,
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=300,
            reverse_duration=300,
            switch_in_curve=ft.AnimationCurve.LINEAR,
            switch_out_curve=ft.AnimationCurve.LINEAR,
        )
        
        self.pay_button = ft.TextButton(text_values["pay_now"])
        self.cancel_button = ft.TextButton(text_values["cancel"])
        
        self.content=self.switcher
        self.actions=[
            self.pay_button,
            self.cancel_button,
        ]
        self.actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    
    # shwo the payment details
    def show_payment_details(self):
        self.switcher.content = self.payment_row
        self.switcher.update()