from kivymd.uix.bottomsheet import (
    MDBottomSheet,
    MDBottomSheetDragHandle,
    MDBottomSheetDragHandleTitle,
    MDBottomSheetDragHandleButton,
    MDBottomSheetContent,
)
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp


class BottomMenu(MDBottomSheet):
    def __init__(self, screen_changer=None, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_changer
        self.type = "modal"
        self.size_hint_y = None
        self.height = dp(315) # Adjusted for better content fit
        self.bg_color = (1, 1, 1, 1)

        # === Handle Section ===
        handle = MDBottomSheetDragHandle()
        title = MDBottomSheetDragHandleTitle(text="Task Options", adaptive_height=True)
        close_button = MDBottomSheetDragHandleButton(icon="close", on_release=self.dismiss)

        handle.add_widget(title)
        handle.add_widget(close_button)
        self.ids.drag_handle_container.add_widget(handle)

        # === Main Content ===
        content = MDBottomSheetContent(orientation="vertical", padding=dp(16))

        # Scrollable row of FABs with labels
        scroll = MDScrollView(size_hint_y=None, height=dp(200))
        icon_row = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(24),
            adaptive_height=True,
            padding=(dp(10), 0),
            size_hint_x=None,
        )
        icon_row.width = dp(500)  # Enough to allow horizontal scrolling

        # Add FAB + label groups
        for icon_name, label_text, callback in [
            ("plus", "Add Task", self.add_task),
            ("calendar-today", "Daily", lambda: print("Daily clicked")),
            ("calendar-week", "Weekly", lambda: print("Weekly clicked")),
            ("calendar-month", "Monthly", lambda: print("Monthly clicked")),
        ]:
            fab_column = MDBoxLayout(
                orientation="vertical",
                spacing=dp(8),
                size_hint=(None, None),
                size=(dp(72), dp(100)),
                padding=(0, dp(10)),
            )

            fab = MDFloatingActionButton(
                icon=icon_name,
                on_release=callback,
                md_bg_color=self.theme_cls.primary_color,
                size_hint=(None, None),
                size=(dp(56), dp(56)),
            )

            label = MDLabel(
                text=label_text,
                halign="center",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(20),
                font_style="Caption",
            )

            fab_column.add_widget(fab)
            fab_column.add_widget(label)

            icon_row.add_widget(fab_column)

        scroll.add_widget(icon_row)
        content.add_widget(scroll)

        # Add to bottom sheet
        self.ids.container.add_widget(content)

    def add_task(self, *args):
        print("Add Task clicked")
