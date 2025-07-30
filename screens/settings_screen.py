from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from components.bottom_sheet import BottomMenu
from components.bottom_handle import HandleTrigger

class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = "500dp"

        self.bottom_sheet = BottomMenu()
        self.add_widget(self.bottom_sheet)
        
        open_button = HandleTrigger(bottom_menu=self.bottom_sheet)

        layout = MDBoxLayout(orientation="vertical")
        label = MDLabel(text="Settings", halign="center")

        layout.add_widget(label)
        layout.add_widget(open_button)

        self.add_widget(layout)

    def show_bottom_sheet(self, *args):
        Clock.schedule_once(lambda dt: self.bottom_sheet.open(), 0)