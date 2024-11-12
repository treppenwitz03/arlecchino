import flet as ft

class ShowReceivableInfoDialog(ft.AlertDialog):
    group_name = ""
    def __init__(self, text_values: dict):
        super().__init__()
        ###########################################################
        ## Make the UI for when receivable button is clicked
        ###########################################################
        self.completed_button = ft.TextButton(text_values["mark_completed"])
        self.cancel_button = ft.TextButton(text_values["cancel"])
        
        self.actions = [
            self.completed_button,
            self.cancel_button
        ]
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        
        self.paid_list = ft.ListView(spacing=5, width=400, height=200, padding=20)
        
        self.content = self.paid_list
        
        self.no_paid_label = ft.Text(text_values["no_payment_made"], width=400, height=200)
        
        self.title = ft.Text(" ", weight = ft.FontWeight.W_700)
    
    # make a callback to show proof
    def show_proof(self, id: str):
        pass