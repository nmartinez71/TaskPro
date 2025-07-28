from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivy.utils import get_color_from_hex


class UserLoginScreen(MDScreen):
    def __init__(self, screen_changer=None, **kwargs): #initialize screen, added screen_changer for callbacks
        super().__init__(**kwargs)
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

        screen_btn = MDRaisedButton(
            text="Continue without Login",
            pos_hint={"center_x": 0.5},
            md_bg_color=(0, 0.5, 1, 1),
            text_color=(1, 1, 1, 1)
        )
        screen_btn.bind(on_release=self.change_screen)
        card.add_widget(screen_btn)

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

    def login(self, *args): #logic for is username has admin privilage and password is passing 
                            #and true then screen changes to home. not sure how to check this againts the database?
        if self.username.text == "admin" and self.password.text == "pass":
            pass
            # if self.screen_changer:
            #     self.screen_changer.show_home()

    def change_screen(self, instance):
        self.screen_changer.switch_root_screen("Root Screen")
