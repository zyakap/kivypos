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
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.app import App
from datetime import datetime, timedelta
import os

class ReportsScreen(MDScreen):
    """Reports and analytics screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.data_table = None
        self.current_report_type = "sales"
        self.build_ui()
    
    def build_ui(self):
        """Build the reports screen UI"""
        # Main layout
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=0
        )
        
        # Top app bar
        toolbar = MDTopAppBar(
            title="Reports & Analytics",
            left_action_items=[
                ["arrow-left", lambda x: self.go_back()]
            ],
            right_action_items=[
                ["download", lambda x: self.export_report()],
                ["refresh", lambda x: self.refresh_report()]
            ],
            elevation=2
        )
        
        # Content layout
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10)
        )
        
        # Report controls section
        controls_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            size_hint=(1, None),
            height=dp(180),
            elevation=2
        )
        
        controls_title = MDLabel(
            text="Report Controls",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )
        
        # Report type selection
        type_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        type_label = MDLabel(
            text="Report Type:",
            theme_text_color="Primary",
            font_style="Subtitle1",
            size_hint_x=0.3
        )
        
        sales_button = MDRaisedButton(
            text="SALES",
            size_hint_x=0.2,
            on_release=lambda x: self.set_report_type("sales")
        )
        
        inventory_button = MDRaisedButton(
            text="INVENTORY",
            size_hint_x=0.2,
            on_release=lambda x: self.set_report_type("inventory")
        )
        
        customer_button = MDRaisedButton(
            text="CUSTOMERS",
            size_hint_x=0.2,
            on_release=lambda x: self.set_report_type("customers")
        )
        
        type_layout.add_widget(type_label)
        type_layout.add_widget(sales_button)
        type_layout.add_widget(inventory_button)
        type_layout.add_widget(customer_button)
        
        # Date range selection
        date_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(56)
        )
        
        self.start_date_field = MDTextField(
            hint_text="Start Date (YYYY-MM-DD)",
            text=datetime.now().strftime('%Y-%m-%d'),
            size_hint_x=0.3
        )
        
        self.end_date_field = MDTextField(
            hint_text="End Date (YYYY-MM-DD)",
            text=datetime.now().strftime('%Y-%m-%d'),
            size_hint_x=0.3
        )
        
        generate_button = MDRaisedButton(
            text="GENERATE REPORT",
            size_hint_x=0.4,
            on_release=self.generate_report
        )
        
        date_layout.add_widget(self.start_date_field)
        date_layout.add_widget(self.end_date_field)
        date_layout.add_widget(generate_button)
        
        # Quick date buttons
        quick_date_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        today_button = MDFlatButton(
            text="TODAY",
            on_release=lambda x: self.set_date_range("today")
        )
        
        week_button = MDFlatButton(
            text="THIS WEEK",
            on_release=lambda x: self.set_date_range("week")
        )
        
        month_button = MDFlatButton(
            text="THIS MONTH",
            on_release=lambda x: self.set_date_range("month")
        )
        
        quick_date_layout.add_widget(today_button)
        quick_date_layout.add_widget(week_button)
        quick_date_layout.add_widget(month_button)
        
        controls_card.add_widget(controls_title)
        controls_card.add_widget(type_layout)
        controls_card.add_widget(date_layout)
        controls_card.add_widget(quick_date_layout)
        
        # Summary cards section
        summary_layout = MDGridLayout(
            cols=4,
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(120)
        )
        
        self.summary_cards = []
        for i in range(4):
            card = self.create_summary_card("", "0", "")
            summary_layout.add_widget(card)
            self.summary_cards.append(card)
        
        # Report data section
        report_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            elevation=2
        )
        
        self.report_title = MDLabel(
            text="Sales Report",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )
        
        # Create data table
        self.create_data_table()
        
        report_card.add_widget(self.report_title)
        report_card.add_widget(self.data_table)
        
        # Add widgets to content layout
        content_layout.add_widget(controls_card)
        content_layout.add_widget(summary_layout)
        content_layout.add_widget(report_card)
        
        # Add to main layout
        main_layout.add_widget(toolbar)
        main_layout.add_widget(content_layout)
        
        self.add_widget(main_layout)
    
    def create_summary_card(self, title, value, icon):
        """Create a summary statistics card"""
        card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(5),
            elevation=2
        )
        
        icon_widget = MDIconButton(
            icon=icon or "chart-line",
            theme_icon_color="Primary",
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            pos_hint={"center_x": 0.5}
        )
        
        value_label = MDLabel(
            text=value,
            theme_text_color="Primary",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(30)
        )
        
        title_label = MDLabel(
            text=title,
            theme_text_color="Secondary",
            font_style="Caption",
            halign="center",
            size_hint_y=None,
            height=dp(20)
        )
        
        card.add_widget(icon_widget)
        card.add_widget(value_label)
        card.add_widget(title_label)
        
        return card
    
    def create_data_table(self):
        """Create the report data table"""
        self.data_table = MDDataTable(
            use_pagination=True,
            rows_num=15,
            column_data=[
                ("Date", dp(25)),
                ("Description", dp(40)),
                ("Amount", dp(20)),
                ("Details", dp(30))
            ],
            row_data=[],
            elevation=0
        )
    
    def on_enter(self):
        """Called when screen is entered"""
        self.generate_report()
    
    def set_report_type(self, report_type):
        """Set the current report type"""
        self.current_report_type = report_type
        
        # Update report title
        titles = {
            "sales": "Sales Report",
            "inventory": "Inventory Report", 
            "customers": "Customer Report"
        }
        self.report_title.text = titles.get(report_type, "Report")
        
        # Update data table columns based on report type
        if report_type == "sales":
            self.data_table.column_data = [
                ("Sale #", dp(20)),
                ("Date", dp(25)),
                ("Customer", dp(30)),
                ("Cashier", dp(25)),
                ("Amount", dp(20)),
                ("Payment", dp(20))
            ]
        elif report_type == "inventory":
            self.data_table.column_data = [
                ("Product", dp(35)),
                ("Category", dp(25)),
                ("Stock", dp(15)),
                ("Min Stock", dp(15)),
                ("Value", dp(20)),
                ("Status", dp(20))
            ]
        elif report_type == "customers":
            self.data_table.column_data = [
                ("Customer", dp(30)),
                ("Phone", dp(25)),
                ("Purchases", dp(20)),
                ("Total Spent", dp(25)),
                ("Last Purchase", dp(25))
            ]
    
    def set_date_range(self, period):
        """Set date range based on period"""
        today = datetime.now()
        
        if period == "today":
            start_date = today.strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
        elif period == "week":
            start_date = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
        elif period == "month":
            start_date = today.replace(day=1).strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
        
        self.start_date_field.text = start_date
        self.end_date_field.text = end_date
    
    def generate_report(self, *args):
        """Generate the selected report"""
        start_date = self.start_date_field.text.strip()
        end_date = self.end_date_field.text.strip()
        
        if not start_date or not end_date:
            self.show_error_dialog("Please enter valid start and end dates!")
            return
        
        try:
            # Validate date format
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            self.show_error_dialog("Please use YYYY-MM-DD date format!")
            return
        
        app = App.get_running_app()
        db_manager = app.get_db_manager()
        
        try:
            if self.current_report_type == "sales":
                self.generate_sales_report(db_manager, start_date, end_date)
            elif self.current_report_type == "inventory":
                self.generate_inventory_report(db_manager)
            elif self.current_report_type == "customers":
                self.generate_customer_report(db_manager)
                
        except Exception as e:
            self.show_error_dialog(f"Error generating report: {str(e)}")
    
    def generate_sales_report(self, db_manager, start_date, end_date):
        """Generate sales report"""
        sales = db_manager.get_sales_report(start_date, end_date)
        
        # Update summary cards
        total_sales = len(sales)
        total_revenue = sum(sale[2] for sale in sales)
        avg_sale = total_revenue / total_sales if total_sales > 0 else 0
        
        # Count payment methods
        cash_sales = len([s for s in sales if s[3] == 'cash'])
        
        self.update_summary_cards([
            ("Total Sales", str(total_sales), "cash-register"),
            ("Total Revenue", f"${total_revenue:.2f}", "currency-usd"),
            ("Average Sale", f"${avg_sale:.2f}", "chart-line"),
            ("Cash Sales", str(cash_sales), "cash")
        ])
        
        # Update data table
        row_data = []
        for sale in sales:
            sale_id, sale_number, total_amount, payment_method, created_at, cashier_name, customer_name = sale
            
            # Format date
            try:
                date_obj = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                formatted_date = date_obj.strftime('%m/%d %H:%M')
            except:
                formatted_date = created_at[:16] if created_at else "N/A"
            
            row_data.append([
                sale_number,
                formatted_date,
                customer_name or "Walk-in",
                cashier_name or "N/A",
                f"${total_amount:.2f}",
                payment_method.upper()
            ])
        
        self.data_table.row_data = row_data
    
    def generate_inventory_report(self, db_manager):
        """Generate inventory report"""
        products = db_manager.get_all_products()
        
        # Calculate summary statistics
        total_products = len(products)
        total_value = sum(product[4] * product[7] for product in products)  # price * stock
        low_stock_count = len([p for p in products if p[7] <= p[8]])  # stock <= min_stock
        out_of_stock = len([p for p in products if p[7] == 0])
        
        self.update_summary_cards([
            ("Total Products", str(total_products), "package-variant"),
            ("Inventory Value", f"${total_value:.2f}", "currency-usd"),
            ("Low Stock Items", str(low_stock_count), "alert-circle"),
            ("Out of Stock", str(out_of_stock), "close-circle")
        ])
        
        # Update data table
        row_data = []
        for product in products:
            product_id, barcode, name, description, category, price, cost_price, stock, min_stock = product
            
            # Calculate inventory value for this product
            product_value = price * stock
            
            # Determine status
            if stock <= 0:
                status = "Out of Stock"
            elif stock <= min_stock:
                status = "Low Stock"
            else:
                status = "In Stock"
            
            row_data.append([
                name[:30] + "..." if len(name) > 30 else name,
                category or "N/A",
                str(stock),
                str(min_stock),
                f"${product_value:.2f}",
                status
            ])
        
        self.data_table.row_data = row_data
    
    def generate_customer_report(self, db_manager):
        """Generate customer report"""
        customers = db_manager.get_all_customers()
        
        # For now, show basic customer info
        # In a full implementation, we'd calculate purchase statistics
        
        total_customers = len(customers)
        
        self.update_summary_cards([
            ("Total Customers", str(total_customers), "account-group"),
            ("Active Customers", str(total_customers), "account-check"),
            ("New This Month", "0", "account-plus"),
            ("Avg Purchases", "0", "chart-bar")
        ])
        
        # Update data table
        row_data = []
        for customer in customers:
            customer_id, name, phone, email, address, created_at = customer
            
            # Format date
            try:
                date_obj = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                formatted_date = date_obj.strftime('%Y-%m-%d')
            except:
                formatted_date = created_at[:10] if created_at else "N/A"
            
            row_data.append([
                name[:25] + "..." if len(name) > 25 else name,
                phone or "N/A",
                "0",  # Placeholder for purchase count
                "$0.00",  # Placeholder for total spent
                formatted_date
            ])
        
        self.data_table.row_data = row_data
    
    def update_summary_cards(self, card_data):
        """Update summary cards with new data"""
        for i, (title, value, icon) in enumerate(card_data):
            if i < len(self.summary_cards):
                card = self.summary_cards[i]
                # Update card content
                card.children[2].text = title  # title_label
                card.children[1].text = value  # value_label
                card.children[0].icon = icon   # icon_widget
    
    def export_report(self, *args):
        """Export current report to file"""
        try:
            # Generate report filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.current_report_type}_report_{timestamp}.txt"
            filepath = os.path.join("assets", "receipts", filename)
            
            # Generate report content
            content = f"{self.report_title.text}\n"
            content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            content += f"Date Range: {self.start_date_field.text} to {self.end_date_field.text}\n"
            content += "=" * 50 + "\n\n"
            
            # Add table data
            if self.data_table.row_data:
                # Add column headers
                headers = [col[0] for col in self.data_table.column_data]
                content += " | ".join(headers) + "\n"
                content += "-" * 50 + "\n"
                
                # Add rows
                for row in self.data_table.row_data:
                    content += " | ".join(str(cell) for cell in row) + "\n"
            
            # Save to file
            with open(filepath, 'w') as f:
                f.write(content)
            
            self.show_success_dialog(f"Report exported to {filename}")
            
        except Exception as e:
            self.show_error_dialog(f"Error exporting report: {str(e)}")
    
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
    
    def refresh_report(self, *args):
        """Refresh current report"""
        self.generate_report()
    
    def go_back(self, *args):
        """Go back to main menu"""
        app = App.get_running_app()
        app.switch_screen("main_menu")
