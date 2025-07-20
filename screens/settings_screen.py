from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from components.bottom_sheet import BottomMenu  # Your custom bottom sheet class
from components.bottom_handle import HandleTrigger

class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = "500dp"

        # Create once
        self.bottom_sheet = BottomMenu()
        self.add_widget(self.bottom_sheet)
        
        open_button = HandleTrigger(bottom_menu=self.bottom_sheet)

        # Layout
        layout = MDBoxLayout(orientation="vertical")
        label = MDLabel(text="Settings", halign="center")

        layout.add_widget(label)
        layout.add_widget(open_button)

        self.add_widget(layout)

    def show_bottom_sheet(self, *args):
        Clock.schedule_once(lambda dt: self.bottom_sheet.open(), 0)