from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
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

class InventoryScreen(MDScreen):
    """Inventory management screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.selected_product = None
        self.data_table = None
        self.build_ui()
    
    def build_ui(self):
        """Build the inventory screen UI"""
        # Main layout
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=0
        )
        
        # Top app bar
        toolbar = MDTopAppBar(
            title="Inventory Management",
            left_action_items=[
                ["arrow-left", lambda x: self.go_back()]
            ],
            right_action_items=[
                ["plus", lambda x: self.add_product()],
                ["refresh", lambda x: self.refresh_inventory()]
            ],
            elevation=2
        )
        
        # Content layout
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10)
        )
        
        # Search and filter section
        search_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            size_hint=(1, None),
            height=dp(120),
            elevation=2
        )
        
        search_title = MDLabel(
            text="Search & Filter",
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
            hint_text="Search products by name or barcode",
            size_hint_x=0.7,
            on_text=self.on_search_text
        )
        
        search_button = MDIconButton(
            icon="magnify",
            on_release=self.search_products
        )
        
        low_stock_button = MDRaisedButton(
            text="LOW STOCK",
            size_hint_x=0.2,
            on_release=self.show_low_stock
        )
        
        search_layout.add_widget(self.search_field)
        search_layout.add_widget(search_button)
        search_layout.add_widget(low_stock_button)
        
        search_card.add_widget(search_title)
        search_card.add_widget(search_layout)
        
        # Inventory table
        inventory_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            elevation=2
        )
        
        inventory_title = MDLabel(
            text="Products Inventory",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )
        
        # Create data table
        self.create_data_table()
        
        inventory_card.add_widget(inventory_title)
        inventory_card.add_widget(self.data_table)
        
        # Add widgets to content layout
        content_layout.add_widget(search_card)
        content_layout.add_widget(inventory_card)
        
        # Add to main layout
        main_layout.add_widget(toolbar)
        main_layout.add_widget(content_layout)
        
        self.add_widget(main_layout)
    
    def create_data_table(self):
        """Create the inventory data table"""
        self.data_table = MDDataTable(
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("Barcode", dp(30)),
                ("Name", dp(40)),
                ("Category", dp(25)),
                ("Price", dp(20)),
                ("Stock", dp(15)),
                ("Min Stock", dp(20)),
                ("Status", dp(20)),
                ("Actions", dp(25))
            ],
            row_data=[],
            elevation=0
        )
        
        self.data_table.bind(on_row_press=self.on_row_press)
    
    def on_enter(self):
        """Called when screen is entered"""
        self.load_inventory()
    
    def load_inventory(self):
        """Load inventory data"""
        app = App.get_running_app()
        db_manager = app.get_db_manager()
        
        try:
            products = db_manager.get_all_products()
            self.display_inventory(products)
        except Exception as e:
            print(f"Error loading inventory: {e}")
    
    def display_inventory(self, products):
        """Display inventory in the table"""
        row_data = []
        
        for product in products:
            product_id, barcode, name, description, category, price, cost_price, stock, min_stock = product
            
            # Determine stock status
            if stock <= 0:
                status = "Out of Stock"
            elif stock <= min_stock:
                status = "Low Stock"
            else:
                status = "In Stock"
            
            row_data.append([
                barcode or "N/A",
                name[:25] + "..." if len(name) > 25 else name,
                category or "N/A",
                f"${price:.2f}",
                str(stock),
                str(min_stock),
                status,
                "Edit | Delete"
            ])
        
        self.data_table.row_data = row_data
    
    def on_search_text(self, instance, text):
        """Handle search text change"""
        if len(text) >= 2:
            self.search_products()
        elif len(text) == 0:
            self.load_inventory()
    
    def search_products(self, *args):
        """Search products"""
        search_term = self.search_field.text.strip()
        
        if not search_term:
            self.load_inventory()
            return
        
        app = App.get_running_app()
        db_manager = app.get_db_manager()
        
        try:
            products = db_manager.search_products(search_term)
            self.display_inventory(products)
        except Exception as e:
            print(f"Error searching products: {e}")
    
    def show_low_stock(self, *args):
        """Show only low stock products"""
        app = App.get_running_app()
        db_manager = app.get_db_manager()
        
        try:
            low_stock_products = db_manager.get_low_stock_products()
            # Convert to full product format for display
            products = []
            for product in low_stock_products:
                product_id, barcode, name, stock, min_stock = product
                full_product = db_manager.get_product_by_id(product_id)
                if full_product:
                    products.append(full_product)
            
            self.display_inventory(products)
        except Exception as e:
            print(f"Error loading low stock products: {e}")
    
    def on_row_press(self, instance_table, instance_row):
        """Handle row press in data table"""
        # Get the selected product based on row index
        row_index = instance_row.index
        
        app = App.get_running_app()
        db_manager = app.get_db_manager()
        
        try:
            # Get all products to find the selected one
            products = db_manager.get_all_products()
            if row_index < len(products):
                self.selected_product = products[row_index]
                self.show_product_actions()
        except Exception as e:
            print(f"Error selecting product: {e}")
    
    def show_product_actions(self):
        """Show product action dialog"""
        if not self.selected_product:
            return
        
        product_id, barcode, name, description, category, price, cost_price, stock, min_stock = self.selected_product
        
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            size_hint_y=None,
            height=dp(200)
        )
        
        product_info = MDLabel(
            text=f"Product: {name}\nCurrent Stock: {stock}",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_y=None,
            height=dp(60)
        )
        
        edit_button = MDRaisedButton(
            text="EDIT PRODUCT",
            size_hint=(1, None),
            height=dp(40),
            on_release=lambda x: self.edit_product()
        )
        
        stock_button = MDRaisedButton(
            text="UPDATE STOCK",
            size_hint=(1, None),
            height=dp(40),
            on_release=lambda x: self.update_stock()
        )
        
        delete_button = MDRaisedButton(
            text="DELETE PRODUCT",
            size_hint=(1, None),
            height=dp(40),
            md_bg_color="Red",
            on_release=lambda x: self.delete_product()
        )
        
        content.add_widget(product_info)
        content.add_widget(edit_button)
        content.add_widget(stock_button)
        content.add_widget(delete_button)
        
        self.dialog = MDDialog(
            title="Product Actions",
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
    
    def add_product(self, *args):
        """Add new product"""
        self.show_product_form()
    
    def edit_product(self, *args):
        """Edit selected product"""
        self.close_dialog()
        self.show_product_form(edit_mode=True)
    
    def show_product_form(self, edit_mode=False):
        """Show product add/edit form"""
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(400)
        )
        
        # Form fields
        self.barcode_field = MDTextField(
            hint_text="Barcode (optional)",
            size_hint_y=None,
            height=dp(56)
        )
        
        self.name_field = MDTextField(
            hint_text="Product Name *",
            size_hint_y=None,
            height=dp(56)
        )
        
        self.description_field = MDTextField(
            hint_text="Description",
            size_hint_y=None,
            height=dp(56)
        )
        
        self.category_field = MDTextField(
            hint_text="Category",
            size_hint_y=None,
            height=dp(56)
        )
        
        self.price_field = MDTextField(
            hint_text="Selling Price *",
            input_filter="float",
            size_hint_y=None,
            height=dp(56)
        )
        
        self.cost_field = MDTextField(
            hint_text="Cost Price",
            input_filter="float",
            size_hint_y=None,
            height=dp(56)
        )
        
        self.stock_field = MDTextField(
            hint_text="Stock Quantity *",
            input_filter="int",
            size_hint_y=None,
            height=dp(56)
        )
        
        self.min_stock_field = MDTextField(
            hint_text="Minimum Stock Level",
            input_filter="int",
            text="5",
            size_hint_y=None,
            height=dp(56)
        )
        
        # If editing, populate fields
        if edit_mode and self.selected_product:
            product_id, barcode, name, description, category, price, cost_price, stock, min_stock = self.selected_product
            self.barcode_field.text = barcode or ""
            self.name_field.text = name
            self.description_field.text = description or ""
            self.category_field.text = category or ""
            self.price_field.text = str(price)
            self.cost_field.text = str(cost_price) if cost_price else ""
            self.stock_field.text = str(stock)
            self.min_stock_field.text = str(min_stock)
        
        # Add fields to content
        content.add_widget(self.barcode_field)
        content.add_widget(self.name_field)
        content.add_widget(self.description_field)
        content.add_widget(self.category_field)
        content.add_widget(self.price_field)
        content.add_widget(self.cost_field)
        content.add_widget(self.stock_field)
        content.add_widget(self.min_stock_field)
        
        # Dialog buttons
        save_button = MDFlatButton(
            text="SAVE",
            on_release=lambda x: self.save_product(edit_mode)
        )
        
        cancel_button = MDFlatButton(
            text="CANCEL",
            on_release=self.close_dialog
        )
        
        title = "Edit Product" if edit_mode else "Add New Product"
        
        self.dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=content,
            buttons=[cancel_button, save_button]
        )
        
        self.dialog.open()
    
    def save_product(self, edit_mode):
        """Save product data"""
        # Validate required fields
        if not self.name_field.text.strip():
            self.show_error_dialog("Product name is required!")
            return
        
        if not self.price_field.text.strip():
            self.show_error_dialog("Selling price is required!")
            return
        
        if not self.stock_field.text.strip():
            self.show_error_dialog("Stock quantity is required!")
            return
        
        try:
            # Get form data
            barcode = self.barcode_field.text.strip() or None
            name = self.name_field.text.strip()
            description = self.description_field.text.strip() or None
            category = self.category_field.text.strip() or None
            price = float(self.price_field.text)
            cost_price = float(self.cost_field.text) if self.cost_field.text.strip() else None
            stock = int(self.stock_field.text)
            min_stock = int(self.min_stock_field.text) if self.min_stock_field.text.strip() else 5
            
            app = App.get_running_app()
            db_manager = app.get_db_manager()
            
            if edit_mode and self.selected_product:
                # Update existing product (this would require an update method in database_manager)
                # For now, we'll show a message
                self.show_error_dialog("Product update functionality not yet implemented!")
            else:
                # Add new product
                product_id = db_manager.add_product(
                    barcode, name, description, category, price, cost_price, stock, min_stock
                )
                
                if product_id:
                    self.close_dialog()
                    self.load_inventory()
                    self.show_success_dialog("Product added successfully!")
                else:
                    self.show_error_dialog("Failed to add product. Barcode might already exist.")
        
        except ValueError:
            self.show_error_dialog("Please enter valid numeric values for price and stock!")
        except Exception as e:
            self.show_error_dialog(f"Error saving product: {str(e)}")
    
    def update_stock(self, *args):
        """Update product stock"""
        if not self.selected_product:
            return
        
        self.close_dialog()
        
        product_id, barcode, name, description, category, price, cost_price, current_stock, min_stock = self.selected_product
        
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            size_hint_y=None,
            height=dp(150)
        )
        
        current_label = MDLabel(
            text=f"Current Stock: {current_stock}",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_y=None,
            height=dp(30)
        )
        
        self.new_stock_field = MDTextField(
            hint_text="New Stock Quantity",
            input_filter="int",
            text=str(current_stock),
            size_hint_y=None,
            height=dp(56)
        )
        
        self.stock_reason_field = MDTextField(
            hint_text="Reason for change (optional)",
            size_hint_y=None,
            height=dp(56)
        )
        
        content.add_widget(current_label)
        content.add_widget(self.new_stock_field)
        content.add_widget(self.stock_reason_field)
        
        update_button = MDFlatButton(
            text="UPDATE",
            on_release=self.save_stock_update
        )
        
        cancel_button = MDFlatButton(
            text="CANCEL",
            on_release=self.close_dialog
        )
        
        self.dialog = MDDialog(
            title="Update Stock",
            type="custom",
            content_cls=content,
            buttons=[cancel_button, update_button]
        )
        
        self.dialog.open()
    
    def save_stock_update(self, *args):
        """Save stock update"""
        if not self.selected_product:
            return
        
        try:
            new_quantity = int(self.new_stock_field.text)
            reason = self.stock_reason_field.text.strip() or "Manual stock update"
            
            app = App.get_running_app()
            db_manager = app.get_db_manager()
            current_user = app.get_current_user()
            
            product_id = self.selected_product[0]
            
            db_manager.update_product_stock(product_id, new_quantity, current_user['id'], reason)
            
            self.close_dialog()
            self.load_inventory()
            self.show_success_dialog("Stock updated successfully!")
            
        except ValueError:
            self.show_error_dialog("Please enter a valid stock quantity!")
        except Exception as e:
            self.show_error_dialog(f"Error updating stock: {str(e)}")
    
    def delete_product(self, *args):
        """Delete product (mark as inactive)"""
        # This would require implementing a soft delete in the database
        self.close_dialog()
        self.show_error_dialog("Product deletion functionality not yet implemented!")
    
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
    
    def refresh_inventory(self, *args):
        """Refresh inventory data"""
        self.load_inventory()
    
    def go_back(self, *args):
        """Go back to main menu"""
        app = App.get_running_app()
        app.switch_screen("main_menu")
