from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

_dialog_instance = None  #To hold a reference to avoid duplicate dialogs

def show_dialog(parent, title, message):
    global _dialog_instance

    #Close existing dialog if open
    if _dialog_instance:
        _dialog_instance.dismiss()

    _dialog_instance = MDDialog(
        title=title,
        text=message,
        buttons=[
            MDFlatButton(
                text="OK",
                on_release=lambda x: _dialog_instance.dismiss()
            )
        ]
    )
    _dialog_instance.open()
