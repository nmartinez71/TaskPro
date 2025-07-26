from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.pickers import MDDatePicker, MDTimePicker

class TaskFormScreen(MDScreen):
    def __init__(self, screen_changer=None, tasks_screen_instance = None, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_changer
        self.tasks_screen = tasks_screen_instance
        self.doc_id = None

        self.selected_date = None
        self.selected_time = None

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

        self.time_button = MDRaisedButton(
            text="Pick Time",
            on_release=self.show_time_picker
        )
        layout.add_widget(self.time_button)

        self.task_button = MDRaisedButton(text="Add Task")
        self.task_button.bind(on_release=self.add_task)
        layout.add_widget(self.task_button)

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
        self.selected_date = value
        self.date_button.text = str(value)

    def on_time_selected(self, instance, time):
        self.selected_time = time
        self.time_button.text = str(time)

    def add_task(self, instance):
        print("adding task...")
        if self.tasks_screen:
            self.tasks_screen.add_tasks(
                task_text=self.task_input.text,
                task_date=self.date_button.text,
                task_time=self.time_button.text,
            )
            self.clear_fields()
            self.screen_manager.switch_screen("Tasks")

    def edit_task(self, instance):
        if self.tasks_screen:
            self.tasks_screen.update_task(
                task_text=self.task_input.text,
                task_date=self.date_button.text,
                task_time=self.time_button.text,
                doc_id=self.doc_id
            )
            self.clear_fields()
            self.screen_manager.switch_screen("Tasks")
            print("Edit Task finished...")

    #Only called when editing
    def populate_fields(self, editing=True, task_text='', task_date='', task_time='', doc_id=None):
        print("Populating form... editing:", editing)
        
        # Clear input fields first
        self.task_input.text = task_text if editing else ''
        self.date_button.text = task_date if editing else ''
        self.time_button.text = task_time if editing else ''
        
        # Store editing state and doc_id
        self.editing = editing
        self.doc_id = doc_id

        # Make sure we unbind previous bindings
        self.task_button.unbind(on_release=self.add_task)
        self.task_button.unbind(on_release=self.edit_task)

        # Bind appropriate function
        if editing:
            self.task_button.text = "Update Task"
            self.task_button.bind(on_release=self.edit_task)
        else:
            self.task_button.text = "Add Task"
            self.task_button.bind(on_release=self.add_task)

    def clear_fields(self):
        self.task_button.unbind(on_release=self.edit_task)
        self.task_button.bind(on_release=self.add_task)
        self.task_input.text = ""
        self.date_button.text = "Date"
        self.time_button.text = "Time"
        self.selected_date = None
        self.selected_time = None
        self.editing = False
        self.doc_id = None
        self.task_button.text = "Add Task"
