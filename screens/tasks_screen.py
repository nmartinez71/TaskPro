from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from components.tasksitem import TaskItem
from components.bottom_sheet import BottomMenu
from components.bottom_handle import HandleTrigger

from datetime import datetime
from firestore_api import FirestoreAPI
from utils.encryption import encrypt_text, decrypt_text
from utils.notifications import schedule_notification, cancel_notification
from utils import globals


class TasksScreen(MDScreen):
    def __init__(self,topbar=None, bottom_menu=None, screen_changer=None, **kwargs):
        super().__init__(**kwargs)
        self.user_id = globals.current_user_id
        self.encryption_key = globals.encryption_key
        self.api = FirestoreAPI(project_id="teamf-ae838", collection="todos")
        
        self.complete = False

        self.tasks_bottom_sheet = bottom_menu
        self.topbar = topbar
        self.screen_changer = screen_changer

        open_button = HandleTrigger(bottom_menu=self.tasks_bottom_sheet)

        self.main_content = MDBoxLayout(orientation="vertical", padding="8dp")
        self.main_content.add_widget(MDLabel(text="Tasks for You", size_hint_y=None, height="40dp"))

        scroll = MDScrollView()
        self.task_list = MDList()
        scroll.add_widget(self.task_list)
        self.main_content.add_widget(scroll)
        self.main_content.add_widget(open_button)
        self.add_widget(self.main_content)

        self.task_items = []

    def add_tasks(self, task_text, task_date, task_time):
        encrypted_text = encrypt_text(task_text, self.encryption_key)
        doc_id = self.api.add_task(self.user_id, encrypted_text, task_date, task_time)
        decrypted_text = decrypt_text(encrypted_text, self.encryption_key)

        if doc_id:
            task_item = TaskItem(
                text=decrypted_text,
                date=task_date,
                time=task_time,
                topbar=self.topbar,
                parent_screen=self,
                doc_id=doc_id
            )
            # schedule_notification(
            #     task_title=decrypted_text,
            #     task_datetime=datetime.strptime(f"{task_date} {task_time}", "%Y-%m-%d %H:%M"),
            #     doc_id=doc_id
            # )
            self.task_list.add_widget(task_item)
            self.task_items.append(task_item)
        else:
            print("Failed to add task to Firestore.")

    def open_task_for_editing(self):
        for item in self.task_items:
            if item.is_checked():
                if self.screen_changer:
                    print("tasks opened for editing...")
                    self.clear_topbar_icons()
                    form = self.screen_changer.main_screen_manager.get_screen('Task Form')
                    form.populate_fields(
                        editing=True,
                        task_text=item.text,
                        task_date=item.date,
                        task_time=item.time,
                        doc_id=item.doc_id
                    )
                    self.screen_changer.switch_screen('Task Form')
                break

    def update_task(self, task_text, task_date, task_time, doc_id):
        encrypted_text = encrypt_text(task_text, self.encryption_key)
        success = self.api.update_task(
            doc_id=doc_id,
            completed = self.complete,
            user_id = self.user_id,
            task_title=encrypted_text,
            task_date=task_date,
            task_time=task_time
        )
        if success:
            print("editing successful...")
            # cancel_notification(doc_id)
            # schedule_notification(
            #     task_title=task_text,
            #     task_datetime=datetime.strptime(f"{task_date} {task_time}", "%Y-%m-%d %H:%M"),
            #     doc_id=doc_id
            # )
            for item in self.task_items:
                if item.doc_id == doc_id:
                    item.text = task_text
                    item.set_secondary_text(task_date, task_time)
                    item.set_checkbox_state(False)
                    print(f"Task edited: {doc_id}")
                    break
        else:
            print("Failed to edit task.")

    def populate_tasks(self):
        if not self.user_id:
            print("No user ID set.")
            return
        else:
            print("Accessing global user ID from populate_tasks...")
        
        self.task_list.clear_widgets()
        self.task_items = []
        tasks = self.api.get_tasks(self.user_id)
        for task in tasks:
            task_item = TaskItem(
                text=decrypt_text(task.get("title", ""), self.encryption_key),
                date=task.get("date", ""),
                time=task.get("time", ""),
                topbar=self.topbar,
                parent_screen=self,
                doc_id=task.get("doc_id", "")
            )
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
                icons_list.append(["pencil", lambda x: self.open_task_for_editing()])
            icons_list.append(["delete", lambda x: self.delete_selected_tasks()])
            self.topbar.right_action_items = icons_list

    def clear_topbar_icons(self):
        self.topbar.right_action_items = []
        print("Cleared topbar icons.")

    def delete_selected_tasks(self):
        to_remove = [item for item in self.task_items if item.is_checked()]
        for item in to_remove:
            print(f"Deleting {item.text}, doc_id={item.doc_id}")
            if item.doc_id and self.api.delete_task(item.doc_id):
                self.task_list.remove_widget(item)
                self.task_items.remove(item)
        self.update_topbar_icons()