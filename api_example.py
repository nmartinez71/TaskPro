from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton, MDTextButton
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.navigationdrawer import (
    MDNavigationLayout,
    MDNavigationDrawer,
    MDNavigationDrawerMenu,
    MDNavigationDrawerLabel,
    MDNavigationDrawerItem,
    MDNavigationDrawerDivider,
)
from kivy.uix.floatlayout import FloatLayout
from firestore_api import FirestoreAPI

class FrontEnd(MDApp):
    def build(self):
        self.api = FirestoreAPI(project_id="teamf-ae838", collection="todos")
        self.screen = MDScreen()
        float_layout = FloatLayout()
        layout = MDBoxLayout(orientation="vertical", padding=10, spacing=10)
        

        self.task_list = MDList()
        scroll = MDScrollView()
        self.dialog = MDDialog(
            title="Add Task",
            type="custom",
            content_cls=MDTextField(hint_text="Task name"),
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="Add", on_release=self.add_task),
                ],
            )
        plus = MDFloatingActionButton(
            icon="plus",
            pos_hint={"right": 1, "y": 0},
            on_release=self.show_add_task_popup
            )
        

        float_layout.add_widget(layout)
        float_layout.add_widget(plus)
        scroll.add_widget(self.task_list)
        layout.add_widget(scroll)
        self.screen.add_widget(float_layout)

        self.display_tasks()
        return MDScreen(
            MDNavigationLayout(
                MDScreenManager(
                    MDScreen(
                        MDFlatButton(
                            MDTextButton(
                                text="Open Drawer",
                            ),
                            on_release=lambda x: self.root.get_ids().nav_drawer.set_state(
                                "toggle"
                            ),
                            pos_hint={"center_x": 0.5, "center_y": 0.5},
                        ),
                    ),
                ),
                MDNavigationDrawer(
                    MDNavigationDrawerMenu(
                        MDNavigationDrawerLabel(
                            text="Mail",
                        ),
                        MDNavigationDrawerItem(
                                icon="account",
                                text="Inbox",
                            ),
                        ),
                        MDNavigationDrawerDivider(
                        ),
                    ),
                    id="nav_drawer"
                ),
            )

    def add_task(self, instance):
        task_title = self.dialog.content_cls.text.strip()
        if task_title:
            if self.api.add_task(task_title):
                self.dialog.content_cls.text = ""
                self.dialog.dismiss()
                self.display_tasks()

    def show_add_task_popup(self, instance):
        self.dialog.open()

    def display_tasks(self):
        tasks = self.api.get_tasks()
        self.task_list.clear_widgets()
        for task in tasks:
            item = OneLineListItem(
                text=task["title"],
                on_release=lambda x, doc_id=task["doc_id"]: self.remove_task(doc_id)
            )
            self.task_list.add_widget(item)

    def remove_task(self, doc_id):
        if self.api.delete_task(doc_id): #This line is the API deleting the the document in Firestore.
            self.display_tasks()

FrontEnd().run()