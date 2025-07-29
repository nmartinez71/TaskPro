from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.card import MDCard
from kivy.utils import get_color_from_hex
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from firestore_api import FirestoreAPI
import bcrypt
import base64
from utils.encryption import generate_salt, derive_key, encode_salt



class SignUpScreen(MDScreen):
    def __init__(self, screen_changer=None, **kwargs):
        super().__init__(**kwargs)
        self.api = FirestoreAPI(project_id="teamf-ae838", collection="users")

        self.screen_changer = screen_changer

        #Helps Toggle visability for both password boxes
        self.password_visible = False
        self.confirm_visible = False

        self.md_bg_color = get_color_from_hex("#2196F3")

        layout = MDAnchorLayout(anchor_x="center", anchor_y="center")

        card = MDCard(
            orientation="vertical",
            padding=30,
            size_hint=(0.85, None),
            height="520dp",
            spacing=20,
            elevation=10,
        )
        card.md_bg_color = [1, 1, 1, 1]

        card.add_widget(MDLabel(
            text="Create Account",
            halign="center",
            font_style="H5",
            theme_text_color="Primary"
        ))

        # Username
        self.username = MDTextField(
            hint_text="Username",
            mode="rectangle",
            size_hint_x=0.92
        )
        card.add_widget(self.username)

        # Password
        password_box = MDBoxLayout(orientation="horizontal", size_hint_x=0.92, height="48dp", spacing=5)
        self.password = MDTextField(
            hint_text="Password",
            password=True,
            mode="rectangle",
            size_hint_x=0.92
        )
        self.toggle_pass = MDIconButton(
            icon="eye-off",
            on_release=self.toggle_password_visibility
        )
        password_box.add_widget(self.password)
        password_box.add_widget(self.toggle_pass)
        card.add_widget(password_box)

        # Confirm Password
        confirm_box = MDBoxLayout(orientation="horizontal", size_hint_x=0.92, height="48dp", spacing=5)
        self.confirm = MDTextField(
            hint_text="Confirm Password",
            password=True,
            mode="rectangle",
            size_hint_x=0.92
        )
        self.toggle_confirm = MDIconButton(
            icon="eye-off",
            on_release=self.toggle_confirm_visibility
        )
        confirm_box.add_widget(self.confirm)
        confirm_box.add_widget(self.toggle_confirm)
        card.add_widget(confirm_box)

        # Register Button
        register_btn = MDRaisedButton(
            text="Register",
            pos_hint={"center_x": 0.5},
            md_bg_color=(0, 0.5, 1, 1),
            text_color=(1, 1, 1, 1)
        )
        register_btn.bind(on_release=self.register)
        card.add_widget(register_btn)

        # Link to login
        login_link = MDLabel(
            text='Already have an account? [ref=login][color=#1565C0]Login[/color][/ref]', #allows you to return to login page without registering
            markup=True,
            halign="center"
        )
        login_link.bind(on_ref_press=self.on_ref_press)
        card.add_widget(login_link)

        layout.add_widget(card)
        self.add_widget(layout)
        
        #Toggles password visibility off and on
    def toggle_password_visibility(self, *args):
        self.password.password = not self.password.password
        self.toggle_pass.icon = "eye" if not self.password.password else "eye-off"
        
        #Toggles confirm password visibility off and on
    def toggle_confirm_visibility(self, *args):
        self.confirm.password = not self.confirm.password
        self.toggle_confirm.icon = "eye" if not self.confirm.password else "eye-off"

    def register(self, *args):
        if self.password.text != self.confirm.text:
            self.show_alert("Passwords do not match.") #shows alert if passwords do not match
        elif self.username.text == "" or self.password.text == "":
            self.show_alert("Please Complete All Fields") #Shows alert if boxes are left empy
        else:
            hashed_password = bcrypt.hashpw(self.password.text.encode(), bcrypt.gensalt()).decode()

            salt = generate_salt() #os.urandom(16)
            encoded_salt = base64.b64encode(salt).decode()

            encryption_key = derive_key(self.password.text, salt)

            user_id = self.api.add_user(
                username=self.username.text,
                password_hash=hashed_password,
                salt_b64=encoded_salt
            )

            if user_id:
                # Switch screen to Login after successful registration
                if self.screen_changer:
                    self.screen_changer.switch_root_screen("Login")
            else:
                self.show_alert("Failed to register user. Please try again.")

    def on_ref_press(self, instance, ref): #function to move to login screen if already has account
        if ref == "login" and self.screen_changer:
            self.screen_changer.switch_root_screen("Login")
    
    def show_alert(self, text): #function sfor showing dialog box, potentially could make more pretty?
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
        text=text,
        buttons=[
            MDFlatButton(
                text="OK",
                on_release=lambda x: self.dialog.dismiss()
            ),
        ],
    )
        self.dialog.open()
