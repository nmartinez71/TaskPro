from kivy.core.window import Window
from kivy.clock import Clock
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import sys
from kivy.app import App

tray_icon = "icon.png"

def quit_app(icon, item):
    print("[Tray] Quitting...")
    icon.stop()
    App.get_running_app().stop()
    sys.exit()

def show_window(icon, item):
    def _show(dt):
        Window.show()
        Window.restore()
        Window.raise_window()
    Clock.schedule_once(_show)

def minimize_to_tray(*args):
    print("[Tray] Minimizing to tray...")
    def _hide(dt):
        Window.hide()
    Clock.schedule_once(_hide)

def setup_tray():
    global tray_icon
    image = Image.open(tray_icon)
    tray_menu = Menu(
        MenuItem("Show", show_window),
        MenuItem("Minimize", minimize_to_tray),
        MenuItem("Quit", quit_app)
    )
    tray_icon = Icon("TaskPro", image, "TaskPro", tray_menu)
    tray_icon.run()

def start_tray_thread():
    threading.Thread(target=setup_tray, daemon=True).start()
