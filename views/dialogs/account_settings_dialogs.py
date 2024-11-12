import flet as ft

##################################################
## Culmination of dialogs inside the Account View
##################################################

class ProfilePictureChangeDialog(ft.AlertDialog):
    def __init__(self, text_values: dict):
        super().__init__()
        ####################################################
        ## Make the ui for the profile picture changing
        ####################################################

        self.save_changes_button = ft.TextButton(
            text_values["save_changes"],
            disabled=True
        )
        
        self.cancel_button = ft.TextButton(
            text_values["cancel"]
        )
        
        self.actions = [self.save_changes_button, self.cancel_button]
        
        self.user_image = ft.Image(
            src = "/empty_user_image.png",
            width=200,
            height = 200
        )
        
        self.upload_profile = ft.ElevatedButton(
            text_values["upload"]
        )
        
        content_column = ft.Column(
            controls=[self.user_image, self.upload_profile],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=300,
            height=300
        )
        
        self.content = content_column

class EditUsernameDialog(ft.AlertDialog):
    def __init__(self, text_values: dict):
        super().__init__()
        ######################################################
        ## Make ui for changing the username
        ######################################################

        self.save_changes_button = ft.TextButton(
            text_values["save_changes"],
            disabled=True
        )
        
        self.cancel_button = ft.TextButton(
            text_values["cancel"]
        )
        
        self.actions = [self.save_changes_button, self.cancel_button]
        self.title = ft.Text(text_values["edit_profile"])
        
        new_username = ft.Text(
            text_values["enter_new_username"],
            width=150
        )
        
        self.new_username_textfield = ft.TextField(
            hint_text=text_values["username_label"]
        )
        
        username_row = ft.Row(
            controls=[new_username, self.new_username_textfield]
        )
        
        content_column = ft.Column(
            controls=[username_row],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=500,
            height=200
        )
        
        self.content = content_column

class EditPasswordDialog(ft.AlertDialog):
    def __init__(self, text_values: dict):
        super().__init__()
        ##########################################################
        ## Make the UI for editing the password
        ##########################################################

        self.save_changes_button = ft.TextButton(
            text_values["save_changes"],
            disabled=True
        )
        
        self.cancel_button = ft.TextButton(
            text_values["cancel"]
        )
        
        self.actions = [self.save_changes_button, self.cancel_button]
        self.title = ft.Text(text_values["edit_profile"])
        
        new_password = ft.Text(
            text_values["enter_new_pw"],
            width=150
        )
        
        self.new_password_textfield = ft.TextField(
            hint_text=text_values["new_pw"],
            password=True,
            can_reveal_password=True
        )
        
        reenter_password = ft.Text(
            text_values["reenter_new_pw"],
            width=150       
        )
        
        self.reenter_password_textfield = ft.TextField(
            hint_text=text_values["confirm_password_label"],
            password=True,
            can_reveal_password=True
        )
        
        password_row = ft.Row(
            controls=[new_password, self.new_password_textfield]
        )
        
        reenter_password_row = ft.Row(
            controls=[reenter_password, self.reenter_password_textfield]
        )
        
        content_column = ft.Column(
            controls=[password_row, reenter_password_row],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=500,
            height=200
        )
        
        self.content = content_column

class EditGcashDialog(ft.AlertDialog):
    def __init__(self, text_values: dict):
        super().__init__()
        ####################################################
        ## Make the UI for editing the GCash Credentials
        ####################################################

        self.save_changes_button = ft.TextButton(
            text_values["save_changes"],
            disabled=True
        )
        
        self.cancel_button = ft.TextButton(
            text_values["cancel"]
        )
        
        self.actions = [self.save_changes_button, self.cancel_button]
        self.title = ft.Text(text_values["gcash_settings"])
        
        self.qr_image = ft.Image(
            src = "/sample_qr.png",
            width=100,
            height = 100
        )
        
        self.upload_qr_button = ft.ElevatedButton(
            text_values["upload_qr"]
        )
        
        qr_column = ft.Column(
            controls=[self.qr_image, self.upload_qr_button],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        enter_gcash = ft.Text(
            text_values["enter_gcash"]
        )
        
        self.number_textfield = ft.TextField(
            hint_text = text_values["gcash_num"]
        )
        
        number_column = ft.Column(
            controls = [enter_gcash, self.number_textfield],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.content_container = ft.Container(
            content = ft.Row(
                controls = [qr_column, number_column]
            ),
            width=500,
            height=200,
            padding=20
        )
        
        self.content = self.content_container