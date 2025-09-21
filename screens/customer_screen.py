from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, ThreeLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.datatables import MDDataTable
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.app import App

class CustomerScreen(MDScreen):
    """Customer management screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.selected_customer = None
        self.data_table = None
        self.build_ui()
    
    def build_ui(self):
        """Build the customer screen UI"""
        # Main layout
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=0
        )
        
        # Top app bar
        toolbar = MDTopAppBar(
            title="Customer Management",
            left_action_items=[
                ["arrow-left", lambda x: self.go_back()]
            ],
            right_action_items=[
                ["plus", lambda x: self.add_customer()],
                ["refresh", lambda x: self.refresh_customers()]
            ],
            elevation=2
        )
        
        # Content layout
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10)
        )
        
        # Search section
        search_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            size_hint=(1, None),
            height=dp(120),
            elevation=2
        )
        
        search_title = MDLabel(
            text="Search Customers",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )
        
        search_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(56)
        )
        
        self.search_field = MDTextField(
            hint_text="Search by name or phone number",
            size_hint_x=0.8,
            on_text=self.on_search_text
        )
        
        search_button = MDIconButton(
            icon="magnify",
            on_release=self.search_customers
        )
        
        search_layout.add_widget(self.search_field)
        search_layout.add_widget(search_button)
        
        search_card.add_widget(search_title)
        search_card.add_widget(search_layout)
        
        # Customer table
        customers_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            elevation=2
        )
        
        customers_title = MDLabel(
            text="Customer List",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )
        
        # Create data table
        self.create_data_table()
        
        customers_card.add_widget(customers_title)
        customers_card.add_widget(self.data_table)
        
        # Add widgets to content layout
        content_layout.add_widget(search_card)
        content_layout.add_widget(customers_card)
        
        # Add to main layout
        main_layout.add_widget(toolbar)
        main_layout.add_widget(content_layout)
        
        self.add_widget(main_layout)
    
    def create_data_table(self):
        """Create the customer data table"""
        self.data_table = MDDataTable(
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("Name", dp(35)),
                ("Phone", dp(25)),
                ("Email", dp(35)),
                ("Address", dp(40)),
                ("Joined", dp(25)),
                ("Actions", dp(25))
            ],
            row_data=[],
            elevation=0
        )
        
        self.data_table.bind(on_row_press=self.on_row_press)
    
    def on_enter(self):
        """Called when screen is entered"""
        self.load_customers()
    
    def load_customers(self):
        """Load customer data"""
        app = App.get_running_app()
        db_manager = app.get_db_manager()
        
        try:
            customers = db_manager.get_all_customers()
            self.display_customers(customers)
        except Exception as e:
            print(f"Error loading customers: {e}")
    
    def display_customers(self, customers):
        """Display customers in the table"""
        row_data = []
        
        for customer in customers:
            customer_id, name, phone, email, address, created_at = customer
            
            # Format date
            try:
                from datetime import datetime
                date_obj = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                formatted_date = date_obj.strftime('%Y-%m-%d')
            except:
                formatted_date = created_at[:10] if created_at else "N/A"
            
            row_data.append([
                name[:30] + "..." if len(name) > 30 else name,
                phone or "N/A",
                email[:30] + "..." if email and len(email) > 30 else (email or "N/A"),
                address[:35] + "..." if address and len(address) > 35 else (address or "N/A"),
                formatted_date,
                "Edit | Delete"
            ])
        
        self.data_table.row_data = row_data
    
    def on_search_text(self, instance, text):
        """Handle search text change"""
        if len(text) >= 2:
            self.search_customers()
        elif len(text) == 0:
            self.load_customers()
    
    def search_customers(self, *args):
        """Search customers"""
        search_term = self.search_field.text.strip()
        
        if not search_term:
            self.load_customers()
            return
        
        app = App.get_running_app()
        db_manager = app.get_db_manager()
        
        try:
            customers = db_manager.search_customers(search_term)
            # Convert search results to full customer format
            full_customers = []
            for customer in customers:
                customer_id, name, phone, email, address = customer
                # Add created_at field (we'll need to modify the search method to include this)
                full_customers.append((customer_id, name, phone, email, address, "N/A"))
            
            self.display_customers(full_customers)
        except Exception as e:
            print(f"Error searching customers: {e}")
    
    def on_row_press(self, instance_table, instance_row):
        """Handle row press in data table"""
        # Get the selected customer based on row index
        row_index = instance_row.index
        
        app = App.get_running_app()
        db_manager = app.get_db_manager()
        
        try:
            # Get all customers to find the selected one
            customers = db_manager.get_all_customers()
            if row_index < len(customers):
                self.selected_customer = customers[row_index]
                self.show_customer_actions()
        except Exception as e:
            print(f"Error selecting customer: {e}")
    
    def show_customer_actions(self):
        """Show customer action dialog"""
        if not self.selected_customer:
            return
        
        customer_id, name, phone, email, address, created_at = self.selected_customer
        
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            size_hint_y=None,
            height=dp(200)
        )
        
        customer_info = MDLabel(
            text=f"Customer: {name}\nPhone: {phone or 'N/A'}\nEmail: {email or 'N/A'}",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_y=None,
            height=dp(80)
        )
        
        edit_button = MDRaisedButton(
            text="EDIT CUSTOMER",
            size_hint=(1, None),
            height=dp(40),
            on_release=lambda x: self.edit_customer()
        )
        
        history_button = MDRaisedButton(
            text="PURCHASE HISTORY",
            size_hint=(1, None),
            height=dp(40),
            on_release=lambda x: self.show_purchase_history()
        )
        
        delete_button = MDRaisedButton(
            text="DELETE CUSTOMER",
            size_hint=(1, None),
            height=dp(40),
            md_bg_color="Red",
            on_release=lambda x: self.delete_customer()
        )
        
        content.add_widget(customer_info)
        content.add_widget(edit_button)
        content.add_widget(history_button)
        content.add_widget(delete_button)
        
        self.dialog = MDDialog(
            title="Customer Actions",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.close_dialog
                )
            ]
        )
        
        self.dialog.open()
    
    def add_customer(self, *args):
        """Add new customer"""
        self.show_customer_form()
    
    def edit_customer(self, *args):
        """Edit selected customer"""
        self.close_dialog()
        self.show_customer_form(edit_mode=True)
    
    def show_customer_form(self, edit_mode=False):
        """Show customer add/edit form"""
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(300)
        )
        
        # Form fields
        self.name_field = MDTextField(
            hint_text="Customer Name *",
            size_hint_y=None,
            height=dp(56)
        )
        
        self.phone_field = MDTextField(
            hint_text="Phone Number",
            input_filter="int",
            size_hint_y=None,
            height=dp(56)
        )
        
        self.email_field = MDTextField(
            hint_text="Email Address",
            size_hint_y=None,
            height=dp(56)
        )
        
        self.address_field = MDTextField(
            hint_text="Address",
            multiline=True,
            size_hint_y=None,
            height=dp(100)
        )
        
        # If editing, populate fields
        if edit_mode and self.selected_customer:
            customer_id, name, phone, email, address, created_at = self.selected_customer
            self.name_field.text = name
            self.phone_field.text = phone or ""
            self.email_field.text = email or ""
            self.address_field.text = address or ""
        
        # Add fields to content
        content.add_widget(self.name_field)
        content.add_widget(self.phone_field)
        content.add_widget(self.email_field)
        content.add_widget(self.address_field)
        
        # Dialog buttons
        save_button = MDFlatButton(
            text="SAVE",
            on_release=lambda x: self.save_customer(edit_mode)
        )
        
        cancel_button = MDFlatButton(
            text="CANCEL",
            on_release=self.close_dialog
        )
        
        title = "Edit Customer" if edit_mode else "Add New Customer"
        
        self.dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=content,
            buttons=[cancel_button, save_button]
        )
        
        self.dialog.open()
    
    def save_customer(self, edit_mode):
        """Save customer data"""
        # Validate required fields
        if not self.name_field.text.strip():
            self.show_error_dialog("Customer name is required!")
            return
        
        try:
            # Get form data
            name = self.name_field.text.strip()
            phone = self.phone_field.text.strip()
            email = self.email_field.text.strip()
            address = self.address_field.text.strip()
            
            app = App.get_running_app()
            db_manager = app.get_db_manager()
            
            if edit_mode and self.selected_customer:
                # Update existing customer (this would require an update method in database_manager)
                self.show_error_dialog("Customer update functionality not yet implemented!")
            else:
                # Add new customer
                customer_id = db_manager.add_customer(name, phone, email, address)
                
                if customer_id:
                    self.close_dialog()
                    self.load_customers()
                    self.show_success_dialog("Customer added successfully!")
                else:
                    self.show_error_dialog("Failed to add customer!")
        
        except Exception as e:
            self.show_error_dialog(f"Error saving customer: {str(e)}")
    
    def show_purchase_history(self, *args):
        """Show customer purchase history"""
        if not self.selected_customer:
            return
        
        self.close_dialog()
        
        customer_id, name, phone, email, address, created_at = self.selected_customer
        
        # Get purchase history from database
        app = App.get_running_app()
        db_manager = app.get_db_manager()
        
        try:
            # This would require a method to get customer purchase history
            # For now, show a placeholder
            content = MDBoxLayout(
                orientation="vertical",
                spacing=dp(10),
                size_hint_y=None,
                height=dp(200)
            )
            
            history_label = MDLabel(
                text=f"Purchase history for {name}\n\nThis feature will show:\n- Recent purchases\n- Total spent\n- Favorite products\n- Purchase frequency",
                theme_text_color="Primary",
                font_style="Body1",
                text_size=(dp(300), None),
                size_hint_y=None,
                height=dp(150)
            )
            
            content.add_widget(history_label)
            
            self.dialog = MDDialog(
                title="Purchase History",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="CLOSE",
                        on_release=self.close_dialog
                    )
                ]
            )
            
            self.dialog.open()
            
        except Exception as e:
            self.show_error_dialog(f"Error loading purchase history: {str(e)}")
    
    def delete_customer(self, *args):
        """Delete customer (mark as inactive)"""
        # This would require implementing a soft delete in the database
        self.close_dialog()
        self.show_error_dialog("Customer deletion functionality not yet implemented!")
    
    def show_success_dialog(self, message):
        """Show success dialog"""
        self.dialog = MDDialog(
            title="Success",
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.close_dialog
                )
            ]
        )
        self.dialog.open()
    
    def show_error_dialog(self, message):
        """Show error dialog"""
        self.dialog = MDDialog(
            title="Error",
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.close_dialog
                )
            ]
        )
        self.dialog.open()
    
    def close_dialog(self, *args):
        """Close dialog"""
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
    
    def refresh_customers(self, *args):
        """Refresh customer data"""
        self.load_customers()
    
    def go_back(self, *args):
        """Go back to main menu"""
        app = App.get_running_app()
        app.switch_screen("main_menu")
