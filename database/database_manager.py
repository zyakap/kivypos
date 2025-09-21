import sqlite3
import hashlib
from datetime import datetime
import os
from .models import DatabaseModels

class DatabaseManager:
    """Database manager for handling all database operations"""
    
    def __init__(self, db_path="store_pos.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables"""
        conn = self.get_connection()
        DatabaseModels.create_tables(conn)
        DatabaseModels.create_default_data(conn)
        conn.close()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    # User management methods
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('''
            SELECT id, username, role, full_name FROM users 
            WHERE username = ? AND password_hash = ? AND is_active = 1
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'role': user[2],
                'full_name': user[3]
            }
        return None
    
    def create_user(self, username, password, role, full_name):
        """Create new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            cursor.execute('''
                INSERT INTO users (username, password_hash, role, full_name)
                VALUES (?, ?, ?, ?)
            ''', (username, password_hash, role, full_name))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    def get_all_users(self):
        """Get all active users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, role, full_name, created_at FROM users 
            WHERE is_active = 1 ORDER BY full_name
        ''')
        
        users = cursor.fetchall()
        conn.close()
        return users
    
    # Product management methods
    def add_product(self, barcode, name, description, category, price, cost_price, stock_quantity, min_stock_level=5):
        """Add new product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO products (barcode, name, description, category, price, cost_price, stock_quantity, min_stock_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (barcode, name, description, category, price, cost_price, stock_quantity, min_stock_level))
            conn.commit()
            product_id = cursor.lastrowid
            conn.close()
            return product_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    def get_product_by_barcode(self, barcode):
        """Get product by barcode"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, barcode, name, description, category, price, cost_price, stock_quantity, min_stock_level
            FROM products WHERE barcode = ? AND is_active = 1
        ''', (barcode,))
        
        product = cursor.fetchone()
        conn.close()
        return product
    
    def get_product_by_id(self, product_id):
        """Get product by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, barcode, name, description, category, price, cost_price, stock_quantity, min_stock_level
            FROM products WHERE id = ? AND is_active = 1
        ''', (product_id,))
        
        product = cursor.fetchone()
        conn.close()
        return product
    
    def search_products(self, search_term):
        """Search products by name or barcode"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, barcode, name, description, category, price, cost_price, stock_quantity, min_stock_level
            FROM products 
            WHERE (name LIKE ? OR barcode LIKE ?) AND is_active = 1
            ORDER BY name
        ''', (f'%{search_term}%', f'%{search_term}%'))
        
        products = cursor.fetchall()
        conn.close()
        return products
    
    def get_all_products(self):
        """Get all active products"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, barcode, name, description, category, price, cost_price, stock_quantity, min_stock_level
            FROM products WHERE is_active = 1 ORDER BY name
        ''')
        
        products = cursor.fetchall()
        conn.close()
        return products
    
    def update_product_stock(self, product_id, new_quantity, user_id, reason="Manual adjustment"):
        """Update product stock quantity"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get current stock
        cursor.execute('SELECT stock_quantity FROM products WHERE id = ?', (product_id,))
        current_stock = cursor.fetchone()[0]
        
        # Update stock
        cursor.execute('''
            UPDATE products SET stock_quantity = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (new_quantity, product_id))
        
        # Record inventory movement
        movement_type = "adjustment"
        quantity_change = new_quantity - current_stock
        
        cursor.execute('''
            INSERT INTO inventory_movements (product_id, movement_type, quantity, reason, user_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (product_id, movement_type, quantity_change, reason, user_id))
        
        conn.commit()
        conn.close()
    
    def get_low_stock_products(self):
        """Get products with stock below minimum level"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, barcode, name, stock_quantity, min_stock_level
            FROM products 
            WHERE stock_quantity <= min_stock_level AND is_active = 1
            ORDER BY stock_quantity
        ''')
        
        products = cursor.fetchall()
        conn.close()
        return products
    
    # Customer management methods
    def add_customer(self, name, phone="", email="", address=""):
        """Add new customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO customers (name, phone, email, address)
            VALUES (?, ?, ?, ?)
        ''', (name, phone, email, address))
        
        conn.commit()
        customer_id = cursor.lastrowid
        conn.close()
        return customer_id
    
    def search_customers(self, search_term):
        """Search customers by name or phone"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, phone, email, address
            FROM customers 
            WHERE (name LIKE ? OR phone LIKE ?) AND is_active = 1
            ORDER BY name
        ''', (f'%{search_term}%', f'%{search_term}%'))
        
        customers = cursor.fetchall()
        conn.close()
        return customers
    
    def get_all_customers(self):
        """Get all active customers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, phone, email, address, created_at
            FROM customers WHERE is_active = 1 ORDER BY name
        ''')
        
        customers = cursor.fetchall()
        conn.close()
        return customers
    
    # Sales management methods
    def create_sale(self, user_id, customer_id, total_amount, payment_method, cart_items, eftpos_receipt_path=None):
        """Create new sale transaction"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Generate sale number
        sale_number = f"SALE{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        try:
            # Insert sale record
            cursor.execute('''
                INSERT INTO sales (sale_number, user_id, customer_id, total_amount, payment_method, eftpos_receipt_path, is_dinau_settled)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (sale_number, user_id, customer_id, total_amount, payment_method, eftpos_receipt_path, 1 if payment_method != 'dinau' else 0))
            
            sale_id = cursor.lastrowid
            
            # If payment method is dinau, record the loan transaction
            if payment_method == 'dinau':
                cursor.execute('''
                    INSERT INTO dinau_transactions (customer_id, sale_id, transaction_type, amount, description, user_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (customer_id, sale_id, 'loan', total_amount, f"Goods on loan - Sale {sale_number}", user_id))
            
            # Insert sale items and update stock
            for item in cart_items:
                product_id = item['product_id']
                quantity = item['quantity']
                unit_price = item['unit_price']
                total_price = quantity * unit_price
                
                # Insert sale item
                cursor.execute('''
                    INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?)
                ''', (sale_id, product_id, quantity, unit_price, total_price))
                
                # Update product stock
                cursor.execute('''
                    UPDATE products SET stock_quantity = stock_quantity - ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (quantity, product_id))
                
                # Record inventory movement
                cursor.execute('''
                    INSERT INTO inventory_movements (product_id, movement_type, quantity, reason, user_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (product_id, "out", -quantity, f"Sale {sale_number}", user_id))
            
            conn.commit()
            conn.close()
            return sale_id, sale_number
            
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    # Dinau (loan) management methods
    def get_customer_dinau_balance(self, customer_id):
        """Get customer's current dinau (loan) balance"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                SUM(CASE WHEN transaction_type = 'loan' THEN amount ELSE -amount END) as balance
            FROM dinau_transactions 
            WHERE customer_id = ?
        ''', (customer_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result[0] else 0.0
    
    def get_customer_dinau_history(self, customer_id):
        """Get customer's dinau transaction history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT dt.transaction_type, dt.amount, dt.description, dt.created_at,
                   u.full_name as processed_by, s.sale_number
            FROM dinau_transactions dt
            LEFT JOIN users u ON dt.user_id = u.id
            LEFT JOIN sales s ON dt.sale_id = s.id
            WHERE dt.customer_id = ?
            ORDER BY dt.created_at DESC
        ''', (customer_id,))
        
        transactions = cursor.fetchall()
        conn.close()
        return transactions
    
    def get_all_dinau_customers(self):
        """Get all customers with outstanding dinau balances"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.id, c.name, c.phone, 
                   SUM(CASE WHEN dt.transaction_type = 'loan' THEN dt.amount ELSE -dt.amount END) as balance
            FROM customers c
            INNER JOIN dinau_transactions dt ON c.id = dt.customer_id
            WHERE c.is_active = 1
            GROUP BY c.id, c.name, c.phone
            HAVING balance > 0
            ORDER BY balance DESC
        ''', ())
        
        customers = cursor.fetchall()
        conn.close()
        return customers
    
    def process_dinau_payment(self, customer_id, payment_amount, user_id, description="Dinau payment"):
        """Process a dinau payment from customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Record the payment transaction
            cursor.execute('''
                INSERT INTO dinau_transactions (customer_id, transaction_type, amount, description, user_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (customer_id, 'payment', payment_amount, description, user_id))
            
            # Check if any sales are now fully settled
            current_balance = self.get_customer_dinau_balance(customer_id)
            
            if current_balance <= 0:
                # Mark all unsettled sales as settled
                cursor.execute('''
                    UPDATE sales 
                    SET is_dinau_settled = 1, dinau_settled_date = CURRENT_TIMESTAMP
                    WHERE customer_id = ? AND payment_method = 'dinau' AND is_dinau_settled = 0
                ''', (customer_id,))
            
            conn.commit()
            transaction_id = cursor.lastrowid
            conn.close()
            return transaction_id
            
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    def get_unsettled_dinau_sales(self):
        """Get all unsettled dinau sales"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.id, s.sale_number, s.total_amount, s.created_at,
                   c.name as customer_name, c.phone, u.full_name as cashier_name
            FROM sales s
            LEFT JOIN customers c ON s.customer_id = c.id
            LEFT JOIN users u ON s.user_id = u.id
            WHERE s.payment_method = 'dinau' AND s.is_dinau_settled = 0
            ORDER BY s.created_at DESC
        ''', ())
        
        sales = cursor.fetchall()
        conn.close()
        return sales
    
    def get_sales_report(self, start_date=None, end_date=None):
        """Get sales report for date range"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT s.id, s.sale_number, s.total_amount, s.payment_method, s.created_at,
                   u.full_name as cashier_name, c.name as customer_name
            FROM sales s
            LEFT JOIN users u ON s.user_id = u.id
            LEFT JOIN customers c ON s.customer_id = c.id
        '''
        
        params = []
        if start_date and end_date:
            query += ' WHERE DATE(s.created_at) BETWEEN ? AND ?'
            params = [start_date, end_date]
        
        query += ' ORDER BY s.created_at DESC'
        
        cursor.execute(query, params)
        sales = cursor.fetchall()
        conn.close()
        return sales
    
    def get_sale_details(self, sale_id):
        """Get detailed information about a sale"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get sale info
        cursor.execute('''
            SELECT s.sale_number, s.total_amount, s.payment_method, s.created_at,
                   u.full_name as cashier_name, c.name as customer_name
            FROM sales s
            LEFT JOIN users u ON s.user_id = u.id
            LEFT JOIN customers c ON s.customer_id = c.id
            WHERE s.id = ?
        ''', (sale_id,))
        
        sale_info = cursor.fetchone()
        
        # Get sale items
        cursor.execute('''
            SELECT p.name, si.quantity, si.unit_price, si.total_price
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            WHERE si.sale_id = ?
        ''', (sale_id,))
        
        sale_items = cursor.fetchall()
        conn.close()
        
        return sale_info, sale_items
