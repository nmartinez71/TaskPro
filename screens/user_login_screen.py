from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout

class UserLoginScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = MDBoxLayout()
        
        self.add_widget(self.box)