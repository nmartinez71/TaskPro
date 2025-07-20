from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.pickers import MDDatePicker, MDTimePicker

class TaskForm(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = MDBoxLayout(
            orientation="vertical",
            padding="20dp",
            spacing="20dp"
        )

        self.task_input = MDTextField(
            hint_text="Enter task description",
            mode="rectangle"
        )
        layout.add_widget(self.task_input)

        self.date_button = MDRaisedButton(
            text="Pick Date",
            on_release=self.show_date_picker
        )
        layout.add_widget(self.date_button)

        # Time picker
        self.time_button = MDRaisedButton(
            text="Pick Time",
            on_release=self.show_time_picker
        )
        layout.add_widget(self.time_button)

        self.add_widget(layout)

    def show_date_picker(self, instance):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected)
        date_dialog.open()

    def show_time_picker(self, instance):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.on_time_selected)
        time_dialog.open()

    def on_date_selected(self, instance, value, date_range):
        print("Selected date:", value)
        self.date_button.text = str(value)

    def on_time_selected(self, instance, time):
        print("Selected time:", time)
        self.time_button.text = str(time)
