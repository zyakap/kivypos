import sqlite3
from datetime import datetime
import hashlib

class DatabaseModels:
    """Database models and table creation for the POS system"""
    
    @staticmethod
    def create_tables(conn):
        """Create all necessary tables for the POS system"""
        cursor = conn.cursor()
        
        # Users table (cashiers and managers)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('cashier', 'manager')),
                full_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT UNIQUE,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                price DECIMAL(10,2) NOT NULL,
                cost_price DECIMAL(10,2),
                stock_quantity INTEGER DEFAULT 0,
                min_stock_level INTEGER DEFAULT 5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_number TEXT UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                customer_id INTEGER,
                total_amount DECIMAL(10,2) NOT NULL,
                payment_method TEXT NOT NULL CHECK (payment_method IN ('cash', 'eftpos', 'dinau')),
                eftpos_receipt_path TEXT,
                is_dinau_settled BOOLEAN DEFAULT 0,
                dinau_settled_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # Dinau (loan) transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dinau_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                sale_id INTEGER,
                transaction_type TEXT NOT NULL CHECK (transaction_type IN ('loan', 'payment')),
                amount DECIMAL(10,2) NOT NULL,
                description TEXT,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (sale_id) REFERENCES sales (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Sale items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                total_price DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (sale_id) REFERENCES sales (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # EFTPOS receipts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS eftpos_receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                receipt_path TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sale_id) REFERENCES sales (id)
            )
        ''')
        
        # Inventory movements table (for tracking stock changes)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                movement_type TEXT NOT NULL CHECK (movement_type IN ('in', 'out', 'adjustment')),
                quantity INTEGER NOT NULL,
                reason TEXT,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
    
    @staticmethod
    def create_default_data(conn):
        """Create default admin user and sample data"""
        cursor = conn.cursor()
        
        # Create default admin user
        admin_password = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password_hash, role, full_name)
            VALUES (?, ?, ?, ?)
        ''', ("admin", admin_password, "manager", "System Administrator"))
        
        # Create sample cashier user
        cashier_password = hashlib.sha256("cashier123".encode()).hexdigest()
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password_hash, role, full_name)
            VALUES (?, ?, ?, ?)
        ''', ("cashier", cashier_password, "cashier", "Sample Cashier"))
        
        # Create sample products
        sample_products = [
            ("1234567890123", "Coca Cola 500ml", "Soft drink", "Beverages", 2.50, 1.80, 50),
            ("2345678901234", "Bread Loaf", "White bread", "Bakery", 3.00, 2.20, 30),
            ("3456789012345", "Milk 1L", "Fresh milk", "Dairy", 4.50, 3.50, 25),
            ("4567890123456", "Bananas 1kg", "Fresh bananas", "Fruits", 5.00, 3.00, 40),
            ("5678901234567", "Rice 2kg", "Jasmine rice", "Grains", 8.00, 6.00, 20)
        ]
        
        for barcode, name, desc, category, price, cost, stock in sample_products:
            cursor.execute('''
                INSERT OR IGNORE INTO products (barcode, name, description, category, price, cost_price, stock_quantity)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (barcode, name, desc, category, price, cost, stock))
        
        # Create sample customer
        cursor.execute('''
            INSERT OR IGNORE INTO customers (name, phone, email)
            VALUES (?, ?, ?)
        ''', ("Walk-in Customer", "", ""))
        
        conn.commit()
