from kivymd.uix.toolbar import MDTopAppBar
from components.sidebar import Sidebar
from kivy.metrics import dp

class TopBar(MDTopAppBar):
    def __init__(self, sidebar=None,**kwargs):
        super().__init__(**kwargs)

        self.sidebar = sidebar

        self.title = "Home"
        self.left_action_items = [["menu", lambda x: self.sidebar.toggle_sidebar()]]
        self.right_action_items = []
        self.size_hint_y=None
        self.height=dp(56)