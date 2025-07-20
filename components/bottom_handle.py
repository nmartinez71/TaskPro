from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.behaviors import ButtonBehavior
from components.bottom_sheet import BottomMenu


class HandleTrigger(ButtonBehavior, Widget):
    def __init__(self, bottom_menu=None, **kwargs):
        super().__init__(**kwargs)

        self.bottom_menu = bottom_menu or BottomMenu()

        # Bind once, no matter how bottom sheet is dismissed
        self.bottom_menu.bind(on_close=self._restore)


        self.size_hint = (None, None)
        self.size = (dp(36), dp(6))
        self.pos_hint = {"center_x": 0.5}
        self.opacity = 0.5

        with self.canvas:
            Color(0.5, 0.5, 0.5, 1)
            self.rect = RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=[dp(3)]
            )

        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_release(self):
        # Fade out when tapped
        Animation(opacity=0, duration=0.15).start(self)
        Clock.schedule_once(lambda dt: self.bottom_menu.open(), 0)

    def _restore(self, *args):
        # Always fade back in when sheet is dismissed
        Animation(opacity=0.5, duration=0.2).start(self)
