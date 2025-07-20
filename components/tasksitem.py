# tasksitem.py
from kivymd.uix.list import TwoLineAvatarIconListItem, CheckboxLeftWidget

class TaskItem(TwoLineAvatarIconListItem):
    def __init__(self, text="Task", topbar=None, parent_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.secondary_text = "Task description"
        self.parent_screen = parent_screen
        self.topbar = topbar

        self.checkbox = CheckboxLeftWidget()
        self.checkbox.bind(active=self.on_checkbox_toggled)
        self.add_widget(self.checkbox)

    def on_checkbox_toggled(self, checkbox, value):
        print(f"Checkbox toggled ({self.text}):", value)
        if self.parent_screen:
            self.parent_screen.update_topbar_icons()

    def is_checked(self):
        return self.checkbox.active
