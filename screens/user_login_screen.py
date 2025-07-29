from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivy.utils import get_color_from_hex

from utils.encryption import derive_key, decode_salt

from firestore_api import FirestoreAPI
import bcrypt


class UserLoginScreen(MDScreen):
    def __init__(self, screen_changer=None, **kwargs): #initialize screen, added screen_changer for callbacks
        super().__init__(**kwargs)
        self.api = FirestoreAPI(project_id="teamf-ae838", collection="users")
        self.screen_changer = screen_changer 
        self.password_visible = False #Starts password as not visible

        # Set background color
        self.md_bg_color = get_color_from_hex("#2196F3")  # Material Blue

        # Centered layout
        layout = MDAnchorLayout(anchor_x="center", anchor_y="center")

        # Adding Card look to center of screen with shadowed box
        card = MDCard(
            orientation="vertical",
            padding=30,
            size_hint=(0.85, None),
            height="460dp",
            spacing=20,
            elevation=10,
        )
        card.md_bg_color = [1, 1, 1, 1]  # Makes Card White

        # Title
        card.add_widget(MDLabel(
            text="Welcome To Task Tracking", #First text on card, could be changed to title of app or a diff message
            halign="center",
            font_style="H5",
            theme_text_color="Primary"
        ))

        # Username input
        self.username = MDTextField(
            hint_text="Username", #Default text in box to be overwritten
            mode="rectangle",
            size_hint_x=0.92
        )
        card.add_widget(self.username)

        # Password input with toggle button
        password_box = MDBoxLayout(orientation="horizontal", size_hint_x=1, height="48dp", spacing=5)
        self.password = MDTextField(
            hint_text="Password",
            password=True,
            mode="rectangle",
            size_hint_x=0.92
        )
        #logic for password to toggle on or off using the icon
        self.toggle_button = MDIconButton(
            icon="eye-off",
            on_release=self.toggle_password_visibility
        )
        password_box.add_widget(self.password)
        password_box.add_widget(self.toggle_button)
        card.add_widget(password_box)

        # Login button
        login_btn = MDRaisedButton(
            text="Login",
            pos_hint={"center_x": 0.5},
            md_bg_color=(0, 0.5, 1, 1),
            text_color=(1, 1, 1, 1)
        )
        login_btn.bind(on_release=self.login) #when clicked calls the "login" function
        card.add_widget(login_btn)

        # screen_btn = MDRaisedButton(
        #     text="Continue without Login",
        #     pos_hint={"center_x": 0.5},
        #     md_bg_color=(0, 0.5, 1, 1),
        #     text_color=(1, 1, 1, 1)
        # )
        # screen_btn.bind(on_release=self.change_screen)
        # card.add_widget(screen_btn)

        # Sign up button
        signup_label = MDLabel(
            text='Don\'t have an account? [ref=signup][color=#1565C0]Sign Up[/color][/ref]', #Makes the "sign Up" text blue and clickable
            markup=True,
            halign = "center"
        )
        signup_label.bind(on_ref_press=self.on_ref_press)
        card.add_widget(signup_label)

        #adds widgets and card to screen
        layout.add_widget(card)
        self.add_widget(layout)

    def toggle_password_visibility(self, instance): #Function for switching eye on or off
        self.password.password = not self.password.password
        self.toggle_button.icon = "eye" if not self.password.password else "eye-off"
        
    def on_ref_press(self, instance, ref): # add functionality to redirect to signup screen not yet created
        if ref == "signup":
            self.screen_changer.switch_root_screen("Sign Up")

    def login(self, *args):
        username_input = self.username.text.strip()
        password_input = self.password.text.strip()

        if not username_input or not password_input:
            print("Username and password required.")
            return

        user = self.api.get_user_by_username(username_input)
        if user:
            hashed_pw = user.get("password")
            salt_b64 = user.get("salt")  # Base64-encoded salt stored in Firestore

            if not hashed_pw or not salt_b64:
                print("User record is incomplete.")
                return

            if bcrypt.checkpw(password_input.encode(), hashed_pw.encode()):
                try:
                    salt = decode_salt(salt_b64)  # decode base64 to bytes
                    key = derive_key(password_input, salt)

                    # Store globally
                    from utils import globals
                    globals.encryption_key = key
                    globals.current_user_id = user.get("doc_id")

                    print("Login successful.")

                    app = MDApp.get_running_app()
                    print(f"Current user ID: {globals.current_user_id}")
                    app.init_user_screens()
                    self.screen_changer.switch_root_screen("Root Screen")


                except Exception as e:
                    print(f"Encryption key derivation failed: {e}")
            else:
                print("Incorrect password.")
        else:
            print("User not found.")
