# tasksscreen.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from components.tasksitem import TaskItem
from components.bottom_sheet import BottomMenu
from components.bottom_handle import HandleTrigger
from firestore_api import FirestoreAPI

class TasksScreen(MDScreen):
    def __init__(self, topbar=None, bottom_menu=None, **kwargs):
        super().__init__(**kwargs)
        self.api = FirestoreAPI(project_id="teamf-ae838", collection="todos")

        self.tasks_bottom_sheet = bottom_menu
        
        self.topbar = topbar
        open_button = HandleTrigger(bottom_menu=self.tasks_bottom_sheet)

        self.main_content = MDBoxLayout(orientation="vertical", padding="8dp")
        self.main_content.add_widget(MDLabel(text="Main Content", size_hint_y=None, height="40dp"))

        scroll = MDScrollView()
        self.task_list = MDList()
        scroll.add_widget(self.task_list)
        self.main_content.add_widget(scroll)
        self.main_content.add_widget(open_button)
        self.add_widget(self.main_content)
        

        self.task_items = []
        self.populate_tasks()

    def populate_tasks(self):
        for i in range(10):
            task_item = TaskItem(text=f"Task {i + 1}", topbar=self.topbar, parent_screen=self)
            self.task_list.add_widget(task_item)
            self.task_items.append(task_item)

    def update_topbar_icons(self):
        checked_total = sum(item.is_checked() for item in self.task_items)
        print("Updating topbar icons. Checked total:", checked_total)

        if checked_total == 0:
            self.clear_topbar_icons()
        else:
            icons_list = []
            if checked_total == 1:
                icons_list.append(["pencil", lambda x: self.edit_selected_task()])
            icons_list.append(["delete", lambda x: self.delete_selected_tasks()])
            self.topbar.right_action_items = icons_list

    def clear_topbar_icons(self):
        self.topbar.right_action_items = []
        print("Cleared topbar icons.")

    def delete_selected_tasks(self):
        # Delete all checked tasks
        for item in self.task_items[:]:  # copy list for safe removal
            if item.is_checked():
                self.task_list.remove_widget(item)
                self.task_items.remove(item)
        # Update topbar after deletion
        self.update_topbar_icons()

    def edit_selected_task(self): #For simplicity, find the first checked task and "edit" it
        for item in self.task_items:
            if item.is_checked():
                print(f"Editing task: {item.text}")
                break
