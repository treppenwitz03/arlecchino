import flet as ft
from views.group_button import GroupButton

class FeedbackView(ft.Column):
    def __init__(self):
        super().__init__(
            offset=ft.transform.Offset(0, 3),
            animate_offset=ft.animation.Animation(300)
        )
        ######################################################
        ## Make the Feedback UI
        ######################################################
        
        self.top_text = ft.Text(
            expand=True,
            value="Help and Support",
            weight=ft.FontWeight.W_600,
            size=54
        )
        
        top_text_row = ft.Row(
            expand=True,
            controls=[self.top_text]
        )
        
        self.top_text_container = ft.Container(
            padding=ft.padding.only(30, 30, 30, 0),
            content=top_text_row
        )

        self.subtitle_text = ft.Text(
            expand=True,
            value="Having problems with the app? Please refer to the options below on how we can help you.",
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

        contact_image = ft.Icon(
            ft.icons.PERM_CONTACT_CAL_SHARP,
            size = 200
        )

        contact_image_container = ft.Container(
            content=contact_image,
            padding=30
        )

        contact_checkicon = ft.Icon(
            ft.icons.CHECK_ROUNDED,
            size = 24
        )

        contact_describeissue_text = ft.Text(
            value="Describe Issue",
            size=15
        )

        contact_describeissue_row = ft.Row(
            controls=[contact_checkicon,contact_describeissue_text]
        )

        self.describe_issue_container = ft.Container(
            content=contact_describeissue_row,
            border = ft.border.all(width=1),
            width=275,
            padding=8
        )

        contact_send_report_text = ft.Text(
            value="Send Report",
            size = 15
        )

        contact_send_report_row = ft.Row(
            controls=[contact_checkicon, contact_send_report_text]
        )

        self.send_report_container = ft.Container(
            content=contact_send_report_row,
            border=ft.border.all(width=1),
            width = 275,
            padding=8
        )

        contact_get_help_text = ft.Text(
            value="Get Help",
            size=15
        )

        contact_get_help_row = ft.Row(
            controls=[contact_checkicon, contact_get_help_text]
        )

        self.get_help_container = ft.Container(
            content=contact_get_help_row,
            border=ft.border.all(width=1),
            width=275,
            padding=8
        )

        self.button_contact_us = ft.ElevatedButton(
            text="Contact Us"
        )

        button_contact_us_container = ft.Container(
            content=self.button_contact_us,
            padding=20
        )

        contact_background_column = ft.Column(
            controls=[contact_image_container, self.describe_issue_container, self.send_report_container, self.get_help_container, button_contact_us_container],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        )

        self.background_contact_container = ft.Container(
            content=contact_background_column,
            padding=ft.padding.only(30, 0, 30, 30),
            margin=40,
            border_radius=15,
            border=ft.border.all(width=1),
            bgcolor=ft.colors.SURFACE_VARIANT
        )

        contribute_image = ft.Icon(
            ft.icons.CODE_OUTLINED,
            size = 200
        )

        contribute_image_container = ft.Container(
            content=contribute_image,
            padding=30
        )

        contribute_checkicon = ft.Icon(
            ft.icons.CHECK_ROUNDED,
            size = 24
        )

        contribute_helpproject_text = ft.Text(
            value="Help  this project become better"
        )

        contribute_helpproject_row = ft.Row(
            controls=[contribute_checkicon,contribute_helpproject_text]
        )

        self.helpproject_container_container = ft.Container(
            content=contribute_helpproject_row,
            border = ft.border.all(width=1),
            width=275,
            padding=8
        )

        contribute_contributecode_text = ft.Text(
            value="Contribute Code"
        )

        contribute_contributecode_row = ft.Row(
            controls=[contribute_checkicon, contribute_contributecode_text]
        )

        self.contributecode_container_container = ft.Container(
            content=contribute_contributecode_row,
            border=ft.border.all(width=1),
            width=275,
            padding=8
        )

        contribute_involve_text = ft.Text(
            value="Get involved with the project"
        )

        contribute_involved_row = ft.Row(
            controls=[contribute_checkicon, contribute_involve_text]
        )

        self.involve_container_container = ft.Container(
            content=contribute_involved_row,
            border=ft.border.all(width=1),
            width=275,
            padding=8
        )

        self.button_contribute = ft.ElevatedButton(
            text="Contribute Code"
        )

        button_contribute_container = ft.Container(
            content=self.button_contribute,
            padding=20
        )

        contribute_background_column = ft.Column(
            controls=[contribute_image_container, self.helpproject_container_container, self.contributecode_container_container, self.involve_container_container, button_contribute_container],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        )

        self.background_contribute_container = ft.Container(
            content=contribute_background_column,
            padding=ft.padding.only(30, 0, 30, 30),
            margin=40,
            border_radius=15,
            border=ft.border.all(width=1),
            bgcolor=ft.colors.SURFACE_VARIANT
        )

        contact_row = ft.Row(
            expand=True,
            controls=[self.background_contact_container, self.background_contribute_container],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.controls.append(self.top_text_container)
        self.controls.append(self.subtitle_text_container)
        self.controls.append(contact_row)

    # dictates whether to show or hide the feedbackview
    def show(self, delta):
        self.offset = ft.transform.Offset(0, delta)
        self.update()