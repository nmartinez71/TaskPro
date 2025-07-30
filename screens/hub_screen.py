from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp

class CornerCard(MDCard):
    def __init__(self, icon_name, label_text, button_text, on_press_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = None, None
        self.size = dp(160), dp(160)
        self.elevation = 6
        self.radius = [24, 24, 24, 24]
        self.orientation = "vertical"
        self.padding = dp(10)
        self.spacing = dp(10)

        self.add_widget(MDIcon(icon=icon_name, halign="center", size_hint_y=None, height=dp(40)))
        self.add_widget(MDLabel(text=label_text, halign="center"))
        btn = (MDRaisedButton(text=button_text, pos_hint={"center_x": 0.5}, on_release=on_press_callback))
        self.add_widget(btn)


class HubScreen(MDScreen):
    def __init__(self, screen_changer=None, **kwargs):
        super().__init__(**kwargs)
        self.screen_changer = screen_changer
        self.top_left = MDAnchorLayout(
                anchor_x="left", anchor_y="top",
                padding=dp(16),
                
        )
        self.top_left.add_widget(CornerCard("note-plus-outline", "Tasks", "Go", on_press_callback=lambda *args: self.screen_changer.switch_screen("Tasks")))

        self.top_right = MDAnchorLayout(
                anchor_x="right", anchor_y="top",
                padding=dp(16),  
        )
        self.top_right.add_widget(CornerCard("cog", "Settings", "Go", on_press_callback=lambda *args: self.screen_changer.switch_screen("Settings")))
        
        
        self.add_widget(self.top_left)
        self.add_widget(self.top_right)
        