import os
import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

# Import screens
from screens.login_screen import LoginScreen
from screens.main_menu_screen import MainMenuScreen
from screens.cashier_screen import CashierScreen
from screens.inventory_screen import InventoryScreen
from screens.customer_screen import CustomerScreen
from screens.reports_screen import ReportsScreen

# Import database manager
from database.database_manager import DatabaseManager

class StorePOSApp(MDApp):
    """Main application class for Store POS system"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Store POS & Inventory Management"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # Initialize database
        self.db_manager = DatabaseManager()
        
        # Current user session
        self.current_user = None
        
        # Create assets directory if it doesn't exist
        os.makedirs("assets/images", exist_ok=True)
        os.makedirs("assets/receipts", exist_ok=True)
    
    def build(self):
        """Build the application UI"""
        # Create screen manager
        self.screen_manager = MDScreenManager()
        
        # Add screens
        self.screen_manager.add_widget(LoginScreen(name="login"))
        self.screen_manager.add_widget(MainMenuScreen(name="main_menu"))
        self.screen_manager.add_widget(CashierScreen(name="cashier"))
        self.screen_manager.add_widget(InventoryScreen(name="inventory"))
        self.screen_manager.add_widget(CustomerScreen(name="customers"))
        self.screen_manager.add_widget(ReportsScreen(name="reports"))
        
        return self.screen_manager
    
    def login_user(self, user_data):
        """Handle user login"""
        self.current_user = user_data
        self.screen_manager.current = "main_menu"
        
        # Update main menu with user info
        main_menu_screen = self.screen_manager.get_screen("main_menu")
        main_menu_screen.update_user_info(user_data)
    
    def logout_user(self):
        """Handle user logout"""
        self.current_user = None
        self.screen_manager.current = "login"
        
        # Clear login form
        login_screen = self.screen_manager.get_screen("login")
        login_screen.clear_form()
    
    def switch_screen(self, screen_name):
        """Switch to specified screen"""
        self.screen_manager.current = screen_name
    
    def get_current_user(self):
        """Get current logged in user"""
        return self.current_user
    
    def get_db_manager(self):
        """Get database manager instance"""
        return self.db_manager

if __name__ == "__main__":
    StorePOSApp().run()
