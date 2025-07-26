from kivymd.uix.list import TwoLineAvatarIconListItem, CheckboxLeftWidget

class TaskItem(TwoLineAvatarIconListItem):
    def __init__(self, text="Task", date=None, time=None, doc_id=None, topbar=None, parent_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.date = date or ""
        self.time = time or ""
        self.secondary_text = f"{self.date}  {self.time}" if self.date and self.time else ""
        self.parent_screen = parent_screen
        self.topbar = topbar
        self.doc_id = doc_id

        self.checkbox = CheckboxLeftWidget()
        self.checkbox.bind(active=self.on_checkbox_toggled)
        self.add_widget(self.checkbox)

    def on_checkbox_toggled(self, checkbox, value):
        print(f"Checkbox toggled ({self.text}):", value)
        if self.parent_screen:
            self.parent_screen.update_topbar_icons()

    def is_checked(self):
        return self.checkbox.active

    def set_secondary_text(self, date, time):
        self.date = date
        self.time = time
        self.secondary_text = f"{date}  {time}"

    def set_checkbox_state(self, state: bool):
        self.checkbox.active = state
