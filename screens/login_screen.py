from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.app import App

class LoginScreen(MDScreen):
    """Login screen for user authentication"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.build_ui()
    
    def build_ui(self):
        """Build the login screen UI"""
        # Main layout
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            adaptive_height=True,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.8, None)
        )
        
        # Title
        title = MDLabel(
            text="Store POS System",
            theme_text_color="Primary",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height=dp(60)
        )
        
        # Login card
        login_card = MDCard(
            orientation="vertical",
            spacing=dp(20),
            padding=dp(30),
            size_hint=(None, None),
            size=(dp(400), dp(350)),
            pos_hint={"center_x": 0.5},
            elevation=3
        )
        
        # Card content
        card_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            adaptive_height=True
        )
        
        # Login form title
        form_title = MDLabel(
            text="Login",
            theme_text_color="Primary",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        
        # Username field
        self.username_field = MDTextField(
            hint_text="Username",
            icon_right="account",
            size_hint_y=None,
            height=dp(56)
        )
        
        # Password field
        self.password_field = MDTextField(
            hint_text="Password",
            icon_right="eye-off",
            password=True,
            size_hint_y=None,
            height=dp(56)
        )
        
        # Login button
        login_button = MDRaisedButton(
            text="LOGIN",
            size_hint=(1, None),
            height=dp(48),
            on_release=self.login
        )
        
        # Default credentials info
        info_label = MDLabel(
            text="Default: admin/admin123 or cashier/cashier123",
            theme_text_color="Hint",
            font_style="Caption",
            halign="center",
            size_hint_y=None,
            height=dp(30)
        )
        
        # Add widgets to card layout
        card_layout.add_widget(form_title)
        card_layout.add_widget(Widget(size_hint_y=None, height=dp(10)))
        card_layout.add_widget(self.username_field)
        card_layout.add_widget(self.password_field)
        card_layout.add_widget(Widget(size_hint_y=None, height=dp(10)))
        card_layout.add_widget(login_button)
        card_layout.add_widget(info_label)
        
        login_card.add_widget(card_layout)
        
        # Add widgets to main layout
        main_layout.add_widget(title)
        main_layout.add_widget(login_card)
        
        self.add_widget(main_layout)
    
    def login(self, *args):
        """Handle login attempt"""
        username = self.username_field.text.strip()
        password = self.password_field.text.strip()
        
        if not username or not password:
            self.show_error_dialog("Please enter both username and password")
            return
        
        # Get app instance and database manager
        app = App.get_running_app()
        db_manager = app.get_db_manager()
        
        # Authenticate user
        user_data = db_manager.authenticate_user(username, password)
        
        if user_data:
            # Login successful
            app.login_user(user_data)
        else:
            # Login failed
            self.show_error_dialog("Invalid username or password")
    
    def show_error_dialog(self, message):
        """Show error dialog"""
        if not self.dialog:
            self.dialog = MDDialog(
                title="Login Error",
                text=message,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=self.close_dialog
                    )
                ]
            )
        else:
            self.dialog.text = message
        
        self.dialog.open()
    
    def close_dialog(self, *args):
        """Close error dialog"""
        if self.dialog:
            self.dialog.dismiss()
    
    def clear_form(self):
        """Clear login form fields"""
        self.username_field.text = ""
        self.password_field.text = ""
        if self.dialog:
            self.dialog.dismiss()
    
    def on_enter(self):
        """Called when screen is entered"""
        # Focus on username field
        self.username_field.focus = True
