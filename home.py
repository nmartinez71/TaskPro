from kivymd.app import MDApp
from cleanup import clear_globals
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.navigationdrawer import MDNavigationLayout

from screens.tasks_screen import TasksScreen
from screens.settings_screen import SettingsScreen
from screens.task_form_screen import TaskFormScreen
from screens.user_login_screen import UserLoginScreen
from screens.sign_up_screen import SignUpScreen

from components.topbar import TopBar
from components.sidebar import Sidebar
from components.bottom_sheet import BottomMenu

class Home(MDApp):
    def build(self):
        #SMALL COMPONENTS
        self.bottom_sheet = BottomMenu(screen_changer = self)
        self.sidebar = Sidebar(screen_changer = self)
        self.topbar = TopBar(sidebar=self.sidebar)

        #UI BIG COMPONENTS
        self.root_nav_window = MDNavigationLayout()
        self.root_screen_manager = MDScreenManager()
        self.root_screen = MDScreen(name = "Root Screen")

        self.main_box = MDBoxLayout(orientation='vertical', size_hint=(1, 1), pos_hint={'top': 1}) #size hint 1, 0.85 originally
        self.main_screen_manager = MDScreenManager(size_hint=(1, 1), pos_hint={'top': 1}) #saize hint 1, 0.50 originally

        #SCREENS
        # tasks_screen = TasksScreen(name="Tasks", topbar=self.topbar, bottom_menu=self.bottom_sheet, screen_changer=self)
        # task_form_screen = TaskFormScreen(name="Task Form", screen_changer=self, tasks_screen_instance=tasks_screen)
        # settings_screen = SettingsScreen(name="Settings")

        #ROOT SCREENS
        user_login_screen = UserLoginScreen(name="Login", screen_changer=self)
        sign_up_screen = SignUpScreen(name="Sign Up", screen_changer=self)

        #UI ORDERING
        #screen assigning
        # self.main_screen_manager.add_widget(tasks_screen)
        # self.main_screen_manager.add_widget(settings_screen)
        # self.main_screen_manager.add_widget(task_form_screen)

        self.root_screen_manager.add_widget(user_login_screen)
        self.root_screen_manager.add_widget(sign_up_screen)

        #content area
        self.main_box.add_widget(self.topbar)
        self.main_box.add_widget(self.main_screen_manager)


        #root window
        self.root_screen.add_widget(self.main_box)
        self.root_screen.add_widget(self.bottom_sheet)
        self.root_screen_manager.add_widget(self.root_screen)
        self.root_nav_window.add_widget(self.root_screen_manager)
        self.root_nav_window.add_widget(self.sidebar)       

        return self.root_nav_window

    def switch_screen(self, screen_name: str):
        print("switch to", screen_name)
        self.main_screen_manager.current = screen_name
        self.topbar.title = screen_name

    def switch_root_screen(self, screen_name: str):
        print("switch to", screen_name)
        self.root_screen_manager.current = screen_name
        self.topbar.title = screen_name

    def change_topbar_icons(self):
        pass

    def on_stop(self): #wehn app is closed
        clear_globals()

    def init_user_screens(self):
        print("Intializing user screens...")
        # Create screens fresh with updated globals
        tasks_screen = TasksScreen(name="Tasks", topbar=self.topbar, bottom_menu=self.bottom_sheet, screen_changer=self)
        task_form_screen = TaskFormScreen(name="Task Form", screen_changer=self, tasks_screen_instance=tasks_screen)
        settings_screen = SettingsScreen(name="Settings")

        # Clear old screens if needed
        for screen_name in ["Tasks", "Task Form", "Settings"]:
            if self.main_screen_manager.has_screen(screen_name):
                screen = self.main_screen_manager.get_screen(screen_name)
                self.main_screen_manager.remove_widget(screen)

        # Add the new screens
        self.main_screen_manager.add_widget(tasks_screen)
        self.main_screen_manager.add_widget(task_form_screen)
        self.main_screen_manager.add_widget(settings_screen)

        tasks_screen.populate_tasks()

        print("End init...")

