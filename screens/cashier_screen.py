from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.app import App
from datetime import datetime
import os

class CashierScreen(MDScreen):
    """Cashier/POS screen for processing sales"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart_items = []
        self.selected_customer = None
        self.dialog = None
        self.build_ui()
    
    def build_ui(self):
        """Build the cashier screen UI"""
        # Main layout
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=0
        )
        
        # Top app bar
        toolbar = MDTopAppBar(
            title="Cashier - Point of Sale",
            left_action_items=[
                ["arrow-left", lambda x: self.go_back()]
            ],
            right_action_items=[
                ["refresh", lambda x: self.refresh_products()]
            ],
            elevation=2
        )
        
        # Content layout (horizontal split)
        content_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            padding=dp(10)
        )
        
        # Left panel - Product search and selection
        left_panel = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_x=0.6
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
            text="Product Search",
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
            hint_text="Search by name or scan barcode",
            size_hint_x=0.8,
            on_text=self.on_search_text
        )
        
        search_button = MDIconButton(
            icon="magnify",
            on_release=self.search_products
        )
        
        search_layout.add_widget(self.search_field)
        search_layout.add_widget(search_button)
        
        search_card.add_widget(search_title)
        search_card.add_widget(search_layout)
        
        # Products list
        products_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            elevation=2
        )
        
        products_title = MDLabel(
            text="Products",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )
        
        self.products_scroll = MDScrollView()
        self.products_list = MDList()
        self.products_scroll.add_widget(self.products_list)
        
        products_card.add_widget(products_title)
        products_card.add_widget(self.products_scroll)
        
        left_panel.add_widget(search_card)
        left_panel.add_widget(products_card)
        
        # Right panel - Cart and checkout
        right_panel = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_x=0.4
        )
        
        # Customer selection
        customer_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            size_hint=(1, None),
            height=dp(100),
            elevation=2
        )
        
        customer_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        self.customer_label = MDLabel(
            text="Customer: Walk-in",
            theme_text_color="Primary",
            font_style="Subtitle1"
        )
        
        select_customer_btn = MDIconButton(
            icon="account-search",
            on_release=self.select_customer
        )
        
        customer_layout.add_widget(self.customer_label)
        customer_layout.add_widget(select_customer_btn)
        customer_card.add_widget(customer_layout)
        
        # Shopping cart
        cart_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            elevation=2
        )
        
        cart_header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40)
        )
        
        cart_title = MDLabel(
            text="Shopping Cart",
            theme_text_color="Primary",
            font_style="H6"
        )
        
        clear_cart_btn = MDIconButton(
            icon="delete",
            on_release=self.clear_cart
        )
        
        cart_header.add_widget(cart_title)
        cart_header.add_widget(clear_cart_btn)
        
        self.cart_scroll = MDScrollView()
        self.cart_list = MDList()
        self.cart_scroll.add_widget(self.cart_list)
        
        # Total section
        total_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            size_hint=(1, None),
            height=dp(120),
            elevation=3
        )
        
        self.total_label = MDLabel(
            text="Total: $0.00",
            theme_text_color="Primary",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        
        checkout_button = MDRaisedButton(
            text="CHECKOUT",
            size_hint=(1, None),
            height=dp(48),
            on_release=self.checkout
        )
        
        total_card.add_widget(self.total_label)
        total_card.add_widget(checkout_button)
        
        cart_card.add_widget(cart_header)
        cart_card.add_widget(self.cart_scroll)
        
        right_panel.add_widget(customer_card)
        right_panel.add_widget(cart_card)
        right_panel.add_widget(total_card)
        
        # Add panels to content
        content_layout.add_widget(left_panel)
        content_layout.add_widget(right_panel)
        
        # Add to main layout
        main_layout.add_widget(toolbar)
        main_layout.add_widget(content_layout)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        """Called when screen is entered"""
        self.load_products()
        self.search_field.focus = True
    
    def load_products(self):
        """Load all products"""
        app = App.get_running_app()
        db_manager = app.get_db_manager()
        
        try:
            products = db_manager.get_all_products()
            self.display_products(products)
        except Exception as e:
            print(f"Error loading products: {e}")
    
    def display_products(self, products):
        """Display products in the list"""
        self.products_list.clear_widgets()
        
        for product in products:
            product_id, barcode, name, description, category, price, cost_price, stock, min_stock = product
            
            # Create product item
            item = ThreeLineListItem(
                text=name,
                secondary_text=f"Price: ${price:.2f} | Stock: {stock}",
                tertiary_text=f"Category: {category}" if category else "No category",
                on_release=lambda x, p=product: self.add_to_cart(p)
            )
            
            self.products_list.add_widget(item)
    
    def on_search_text(self, instance, text):
        """Handle search text change"""
        if len(text) >= 2:
            self.search_products()
    
    def search_products(self, *args):
        """Search products"""
        search_term = self.search_field.text.strip()
        
        if not search_term:
            self.load_products()
            return
        
        app = App.get_running_app()
        db_manager = app.get_db_manager()
        
        try:
            products = db_manager.search_products(search_term)
            self.display_products(products)
        except Exception as e:
            print(f"Error searching products: {e}")
    
    def add_to_cart(self, product):
        """Add product to cart"""
        product_id, barcode, name, description, category, price, cost_price, stock, min_stock = product
        
        if stock <= 0:
            self.show_dialog("Out of Stock", f"{name} is out of stock!")
            return
        
        # Check if product already in cart
        for item in self.cart_items:
            if item['product_id'] == product_id:
                if item['quantity'] < stock:
                    item['quantity'] += 1
                    item['total'] = item['quantity'] * item['unit_price']
                else:
                    self.show_dialog("Insufficient Stock", f"Only {stock} items available!")
                    return
                break
        else:
            # Add new item to cart
            cart_item = {
                'product_id': product_id,
                'name': name,
                'unit_price': price,
                'quantity': 1,
                'total': price
            }
            self.cart_items.append(cart_item)
        
        self.update_cart_display()
    
    def update_cart_display(self):
        """Update cart display"""
        self.cart_list.clear_widgets()
        total_amount = 0
        
        for i, item in enumerate(self.cart_items):
            cart_item_widget = self.create_cart_item_widget(item, i)
            self.cart_list.add_widget(cart_item_widget)
            total_amount += item['total']
        
        self.total_label.text = f"Total: ${total_amount:.2f}"
    
    def create_cart_item_widget(self, item, index):
        """Create cart item widget"""
        layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(60),
            padding=[dp(10), dp(5)]
        )
        
        # Item info
        info_layout = MDBoxLayout(
            orientation="vertical",
            size_hint_x=0.6
        )
        
        name_label = MDLabel(
            text=item['name'],
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_y=None,
            height=dp(25)
        )
        
        price_label = MDLabel(
            text=f"${item['unit_price']:.2f} x {item['quantity']} = ${item['total']:.2f}",
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_y=None,
            height=dp(20)
        )
        
        info_layout.add_widget(name_label)
        info_layout.add_widget(price_label)
        
        # Quantity controls
        qty_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(5),
            size_hint_x=0.3,
            adaptive_width=True
        )
        
        minus_btn = MDIconButton(
            icon="minus",
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            on_release=lambda x: self.decrease_quantity(index)
        )
        
        qty_label = MDLabel(
            text=str(item['quantity']),
            theme_text_color="Primary",
            halign="center",
            size_hint=(None, None),
            size=(dp(30), dp(30))
        )
        
        plus_btn = MDIconButton(
            icon="plus",
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            on_release=lambda x: self.increase_quantity(index)
        )
        
        remove_btn = MDIconButton(
            icon="delete",
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            on_release=lambda x: self.remove_from_cart(index)
        )
        
        qty_layout.add_widget(minus_btn)
        qty_layout.add_widget(qty_label)
        qty_layout.add_widget(plus_btn)
        qty_layout.add_widget(remove_btn)
        
        layout.add_widget(info_layout)
        layout.add_widget(qty_layout)
        
        return layout
    
    def increase_quantity(self, index):
        """Increase item quantity"""
        if index < len(self.cart_items):
            item = self.cart_items[index]
            
            # Check stock availability
            app = App.get_running_app()
            db_manager = app.get_db_manager()
            product = db_manager.get_product_by_id(item['product_id'])
            
            if product and item['quantity'] < product[7]:  # stock_quantity is at index 7
                item['quantity'] += 1
                item['total'] = item['quantity'] * item['unit_price']
                self.update_cart_display()
            else:
                self.show_dialog("Insufficient Stock", "Cannot add more items!")
    
    def decrease_quantity(self, index):
        """Decrease item quantity"""
        if index < len(self.cart_items):
            item = self.cart_items[index]
            if item['quantity'] > 1:
                item['quantity'] -= 1
                item['total'] = item['quantity'] * item['unit_price']
                self.update_cart_display()
    
    def remove_from_cart(self, index):
        """Remove item from cart"""
        if index < len(self.cart_items):
            self.cart_items.pop(index)
            self.update_cart_display()
    
    def clear_cart(self, *args):
        """Clear all items from cart"""
        self.cart_items.clear()
        self.update_cart_display()
    
    def select_customer(self, *args):
        """Select customer for the sale"""
        # This would open a customer selection dialog
        # For now, we'll use a simple implementation
        pass
    
    def checkout(self, *args):
        """Process checkout"""
        if not self.cart_items:
            self.show_dialog("Empty Cart", "Please add items to cart before checkout!")
            return
        
        # Calculate total
        total_amount = sum(item['total'] for item in self.cart_items)
        
        # Show payment dialog
        self.show_payment_dialog(total_amount)
    
    def show_payment_dialog(self, total_amount):
        """Show payment method selection dialog"""
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            size_hint_y=None,
            height=dp(280)
        )
        
        total_label = MDLabel(
            text=f"Total Amount: ${total_amount:.2f}",
            theme_text_color="Primary",
            font_style="H6",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        
        cash_button = MDRaisedButton(
            text="CASH PAYMENT",
            size_hint=(1, None),
            height=dp(48),
            on_release=lambda x: self.process_payment("cash", total_amount)
        )
        
        eftpos_button = MDRaisedButton(
            text="EFTPOS PAYMENT",
            size_hint=(1, None),
            height=dp(48),
            on_release=lambda x: self.process_eftpos_payment(total_amount)
        )
        
        dinau_button = MDRaisedButton(
            text="DINAU PAYMENT",
            size_hint=(1, None),
            height=dp(48),
            md_bg_color=(0.2, 0.8, 0.2, 1),  # Green color in RGBA format
            on_release=lambda x: self.process_payment("dinau", total_amount)
        )
        
        content.add_widget(total_label)
        content.add_widget(cash_button)
        content.add_widget(eftpos_button)
        content.add_widget(dinau_button)
        
        self.dialog = MDDialog(
            title="Select Payment Method",
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
    
    def process_payment(self, payment_method, total_amount):
        """Process the payment"""
        app = App.get_running_app()
        db_manager = app.get_db_manager()
        current_user = app.get_current_user()
        
        try:
            # Create sale
            customer_id = 1 if not self.selected_customer else self.selected_customer['id']  # Default walk-in customer
            
            sale_id, sale_number = db_manager.create_sale(
                user_id=current_user['id'],
                customer_id=customer_id,
                total_amount=total_amount,
                payment_method=payment_method,
                cart_items=self.cart_items
            )
            
            # Generate receipt
            self.generate_receipt(sale_id, sale_number, total_amount, payment_method)
            
            # Clear cart
            self.cart_items.clear()
            self.update_cart_display()
            
            # Close dialog
            self.close_dialog()
            
            # Show success message
            self.show_dialog("Sale Complete", f"Sale {sale_number} completed successfully!\nReceipt saved to assets/receipts/")
            
        except Exception as e:
            self.show_dialog("Error", f"Failed to process sale: {str(e)}")
    
    def process_eftpos_payment(self, total_amount):
        """Process EFTPOS payment with receipt upload"""
        # This would open a file picker for EFTPOS receipt
        # For now, process as regular EFTPOS payment
        self.process_payment("eftpos", total_amount)
    
    def generate_receipt(self, sale_id, sale_number, total_amount, payment_method):
        """Generate receipt file"""
        try:
            receipt_content = f"""
STORE POS SYSTEM
================

Sale Number: {sale_number}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Cashier: {App.get_running_app().get_current_user()['full_name']}

Items:
------
"""
            
            for item in self.cart_items:
                receipt_content += f"{item['name']}\n"
                receipt_content += f"  ${item['unit_price']:.2f} x {item['quantity']} = ${item['total']:.2f}\n"
            
            receipt_content += f"""
------
Total: ${total_amount:.2f}
Payment: {payment_method.upper()}

Thank you for your business!
"""
            
            # Save receipt
            receipt_filename = f"receipt_{sale_number}.txt"
            receipt_path = os.path.join("assets", "receipts", receipt_filename)
            
            with open(receipt_path, 'w') as f:
                f.write(receipt_content)
                
        except Exception as e:
            print(f"Error generating receipt: {e}")
    
    def show_dialog(self, title, message):
        """Show information dialog"""
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=title,
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
    
    def refresh_products(self, *args):
        """Refresh products list"""
        self.load_products()
    
    def go_back(self, *args):
        """Go back to main menu"""
        app = App.get_running_app()
        app.switch_screen("main_menu")
