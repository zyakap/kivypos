from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.app import App
from datetime import datetime

class MainMenuScreen(MDScreen):
    """Main menu/dashboard screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_data = None
        self.build_ui()
    
    def build_ui(self):
        """Build the main menu UI"""
        # Main layout
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=0
        )
        
        # Top app bar
        self.toolbar = MDTopAppBar(
            title="Store POS - Main Menu",
            right_action_items=[
                ["logout", lambda x: self.logout()]
            ],
            elevation=2
        )
        
        # Content layout
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=dp(20)
        )
        
        # Welcome section
        self.welcome_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            size_hint=(1, None),
            height=dp(100),
            elevation=2
        )
        
        self.welcome_label = MDLabel(
            text="Welcome!",
            theme_text_color="Primary",
            font_style="H5",
            size_hint_y=None,
            height=dp(40)
        )
        
        self.user_info_label = MDLabel(
            text="",
            theme_text_color="Secondary",
            font_style="Body1",
            size_hint_y=None,
            height=dp(30)
        )
        
        self.welcome_card.add_widget(self.welcome_label)
        self.welcome_card.add_widget(self.user_info_label)
        
        # Menu buttons grid
        menu_grid = MDGridLayout(
            cols=2,
            spacing=dp(20),
            adaptive_height=True,
            size_hint_y=None
        )
        
        # Cashier button
        cashier_card = self.create_menu_card(
            "Cashier",
            "cash-register",
            "Process sales and transactions",
            self.open_cashier
        )
        
        # Inventory button
        inventory_card = self.create_menu_card(
            "Inventory",
            "package-variant",
            "Manage products and stock",
            self.open_inventory
        )
        
        # Customers button
        customers_card = self.create_menu_card(
            "Customers",
            "account-group",
            "Manage customer information",
            self.open_customers
        )
        
        # Reports button
        reports_card = self.create_menu_card(
            "Reports",
            "chart-line",
            "View sales and inventory reports",
            self.open_reports
        )
        
        menu_grid.add_widget(cashier_card)
        menu_grid.add_widget(inventory_card)
        menu_grid.add_widget(customers_card)
        menu_grid.add_widget(reports_card)
        
        # Quick stats section
        stats_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            size_hint=(1, None),
            height=dp(120),
            elevation=2
        )
        
        stats_title = MDLabel(
            text="Quick Stats",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )
        
        self.stats_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(20),
            adaptive_height=True
        )
        
        stats_card.add_widget(stats_title)
        stats_card.add_widget(self.stats_layout)
        
        # Add widgets to content layout
        content_layout.add_widget(self.welcome_card)
        content_layout.add_widget(menu_grid)
        content_layout.add_widget(stats_card)
        
        # Add to main layout
        main_layout.add_widget(self.toolbar)
        main_layout.add_widget(content_layout)
        
        self.add_widget(main_layout)
    
    def create_menu_card(self, title, icon, description, callback):
        """Create a menu card button"""
        card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(10),
            size_hint=(None, None),
            size=(dp(200), dp(150)),
            elevation=3,
            on_release=callback
        )
        
        # Icon
        icon_button = MDIconButton(
            icon=icon,
            theme_icon_color="Primary",
            font_size=dp(48),
            size_hint=(None, None),
            size=(dp(60), dp(60)),
            pos_hint={"center_x": 0.5}
        )
        
        # Title
        title_label = MDLabel(
            text=title,
            theme_text_color="Primary",
            font_style="H6",
            halign="center",
            size_hint_y=None,
            height=dp(30)
        )
        
        # Description
        desc_label = MDLabel(
            text=description,
            theme_text_color="Secondary",
            font_style="Caption",
            halign="center",
            text_size=(dp(160), None),
            size_hint_y=None,
            height=dp(40)
        )
        
        card.add_widget(icon_button)
        card.add_widget(title_label)
        card.add_widget(desc_label)
        
        return card
    
    def update_user_info(self, user_data):
        """Update user information display"""
        self.user_data = user_data
        self.welcome_label.text = f"Welcome, {user_data['full_name']}!"
        self.user_info_label.text = f"Role: {user_data['role'].title()} | {datetime.now().strftime('%B %d, %Y')}"
        
        # Update quick stats
        self.update_quick_stats()
    
    def update_quick_stats(self):
        """Update quick statistics"""
        app = App.get_running_app()
        db_manager = app.get_db_manager()
        
        # Clear existing stats
        self.stats_layout.clear_widgets()
        
        try:
            # Get total products
            products = db_manager.get_all_products()
            total_products = len(products)
            
            # Get low stock products
            low_stock = db_manager.get_low_stock_products()
            low_stock_count = len(low_stock)
            
            # Get today's sales
            today = datetime.now().strftime('%Y-%m-%d')
            today_sales = db_manager.get_sales_report(today, today)
            today_sales_count = len(today_sales)
            today_revenue = sum(sale[2] for sale in today_sales)
            
            # Create stat widgets
            stats = [
                ("Products", str(total_products), "package-variant"),
                ("Low Stock", str(low_stock_count), "alert-circle"),
                ("Today's Sales", str(today_sales_count), "cash-register"),
                ("Today's Revenue", f"${today_revenue:.2f}", "currency-usd")
            ]
            
            for title, value, icon in stats:
                stat_widget = self.create_stat_widget(title, value, icon)
                self.stats_layout.add_widget(stat_widget)
                
        except Exception as e:
            print(f"Error updating stats: {e}")
    
    def create_stat_widget(self, title, value, icon):
        """Create a statistics widget"""
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(5),
            size_hint_x=0.25
        )
        
        icon_widget = MDIconButton(
            icon=icon,
            theme_icon_color="Primary",
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            pos_hint={"center_x": 0.5}
        )
        
        value_label = MDLabel(
            text=value,
            theme_text_color="Primary",
            font_style="H6",
            halign="center",
            size_hint_y=None,
            height=dp(25)
        )
        
        title_label = MDLabel(
            text=title,
            theme_text_color="Secondary",
            font_style="Caption",
            halign="center",
            size_hint_y=None,
            height=dp(20)
        )
        
        layout.add_widget(icon_widget)
        layout.add_widget(value_label)
        layout.add_widget(title_label)
        
        return layout
    
    def open_cashier(self, *args):
        """Open cashier screen"""
        app = App.get_running_app()
        app.switch_screen("cashier")
    
    def open_inventory(self, *args):
        """Open inventory screen"""
        app = App.get_running_app()
        app.switch_screen("inventory")
    
    def open_customers(self, *args):
        """Open customers screen"""
        app = App.get_running_app()
        app.switch_screen("customers")
    
    def open_reports(self, *args):
        """Open reports screen"""
        app = App.get_running_app()
        app.switch_screen("reports")
    
    def logout(self, *args):
        """Handle logout"""
        app = App.get_running_app()
        app.logout_user()
    
    def on_enter(self):
        """Called when screen is entered"""
        if self.user_data:
            self.update_quick_stats()
