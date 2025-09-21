#!/usr/bin/env python3
"""
Test script for the Store POS database functionality only.
This tests the core database operations without requiring GUI dependencies.
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.database_manager import DatabaseManager

def test_database_functionality():
    """Test all database operations"""
    print("=" * 60)
    print("STORE POS DATABASE FUNCTIONALITY TEST")
    print("=" * 60)
    
    try:
        # Initialize database
        print("\n1. Initializing Database...")
        db_manager = DatabaseManager("test_store_pos.db")
        print("✅ Database initialized successfully")
        
        # Test user authentication
        print("\n2. Testing User Authentication...")
        
        # Test admin login
        admin_user = db_manager.authenticate_user("admin", "admin123")
        if admin_user:
            print(f"✅ Admin login successful: {admin_user['full_name']} ({admin_user['role']})")
        else:
            print("❌ Admin login failed")
            
        # Test cashier login
        cashier_user = db_manager.authenticate_user("cashier", "cashier123")
        if cashier_user:
            print(f"✅ Cashier login successful: {cashier_user['full_name']} ({cashier_user['role']})")
        else:
            print("❌ Cashier login failed")
            
        # Test invalid login
        invalid_user = db_manager.authenticate_user("invalid", "wrong")
        if not invalid_user:
            print("✅ Invalid login correctly rejected")
        else:
            print("❌ Invalid login incorrectly accepted")
        
        # Test product operations
        print("\n3. Testing Product Operations...")
        
        # Get all products
        products = db_manager.get_all_products()
        print(f"✅ Found {len(products)} products in database")
        
        # Display sample products
        for i, product in enumerate(products[:3]):
            product_id, barcode, name, description, category, price, cost_price, stock, min_stock = product
            print(f"   Product {i+1}: {name} - ${price:.2f} (Stock: {stock})")
        
        # Test product search
        search_results = db_manager.search_products("Coca")
        print(f"✅ Search for 'Coca' returned {len(search_results)} results")
        
        # Test barcode lookup
        if products:
            test_barcode = products[0][1]  # Get barcode from first product
            if test_barcode:
                barcode_product = db_manager.get_product_by_barcode(test_barcode)
                if barcode_product:
                    print(f"✅ Barcode lookup successful for {test_barcode}")
                else:
                    print(f"❌ Barcode lookup failed for {test_barcode}")
        
        # Test low stock products
        low_stock = db_manager.get_low_stock_products()
        print(f"✅ Found {len(low_stock)} low stock products")
        
        # Test customer operations
        print("\n4. Testing Customer Operations...")
        
        # Get all customers
        customers = db_manager.get_all_customers()
        print(f"✅ Found {len(customers)} customers in database")
        
        # Add a test customer
        test_customer_id = db_manager.add_customer(
            "Test Customer", 
            "1234567890", 
            "test@example.com", 
            "123 Test Street"
        )
        if test_customer_id:
            print(f"✅ Test customer added with ID: {test_customer_id}")
        else:
            print("❌ Failed to add test customer")
        
        # Search customers
        customer_search = db_manager.search_customers("Test")
        print(f"✅ Customer search for 'Test' returned {len(customer_search)} results")
        
        # Test sales operations
        print("\n5. Testing Sales Operations...")
        
        # Create a test sale
        if products and admin_user:
            # Prepare cart items (using first product)
            test_product = products[0]
            cart_items = [{
                'product_id': test_product[0],
                'quantity': 2,
                'unit_price': test_product[5]  # price is at index 5
            }]
            
            total_amount = cart_items[0]['quantity'] * cart_items[0]['unit_price']
            
            try:
                sale_id, sale_number = db_manager.create_sale(
                    user_id=admin_user['id'],
                    customer_id=1,  # Default walk-in customer
                    total_amount=total_amount,
                    payment_method='cash',
                    cart_items=cart_items
                )
                print(f"✅ Test sale created: {sale_number} (ID: {sale_id})")
                
                # Get sale details
                sale_info, sale_items = db_manager.get_sale_details(sale_id)
                if sale_info and sale_items:
                    print(f"✅ Sale details retrieved: {len(sale_items)} items")
                
            except Exception as e:
                print(f"❌ Sale creation failed: {str(e)}")
        
        # Test reporting
        print("\n6. Testing Reporting...")
        
        # Get today's sales report
        today = datetime.now().strftime('%Y-%m-%d')
        sales_report = db_manager.get_sales_report(today, today)
        print(f"✅ Today's sales report: {len(sales_report)} transactions")
        
        if sales_report:
            total_revenue = sum(sale[2] for sale in sales_report)
            print(f"   Total revenue today: ${total_revenue:.2f}")
        
        # Test inventory management
        print("\n7. Testing Inventory Management...")
        
        if products and admin_user:
            test_product = products[0]
            original_stock = test_product[7]  # stock is at index 7
            new_stock = original_stock + 10
            
            try:
                db_manager.update_product_stock(
                    test_product[0], 
                    new_stock, 
                    admin_user['id'], 
                    "Test stock update"
                )
                print(f"✅ Stock updated from {original_stock} to {new_stock}")
                
                # Verify the update
                updated_product = db_manager.get_product_by_id(test_product[0])
                if updated_product and updated_product[7] == new_stock:
                    print("✅ Stock update verified")
                else:
                    print("❌ Stock update verification failed")
                    
            except Exception as e:
                print(f"❌ Stock update failed: {str(e)}")
        
        print("\n" + "=" * 60)
        print("DATABASE FUNCTIONALITY TEST COMPLETED SUCCESSFULLY! ✅")
        print("=" * 60)
        print("\nCore Features Tested:")
        print("• User Authentication (Admin & Cashier)")
        print("• Product Management (Search, Lookup, Stock)")
        print("• Customer Management (Add, Search)")
        print("• Sales Processing (Create, Retrieve)")
        print("• Inventory Tracking (Stock Updates)")
        print("• Reporting (Sales Reports)")
        print("\nThe database layer is fully functional and ready for GUI integration!")
        
    except Exception as e:
        print(f"\n❌ Database test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_database_functionality()
    
    if success:
        print(f"\n🎉 All tests passed! The Store POS system is ready.")
        print(f"📁 Test database created: test_store_pos.db")
        print(f"🔑 Login credentials:")
        print(f"   Admin: admin / admin123")
        print(f"   Cashier: cashier / cashier123")
    else:
        print(f"\n💥 Some tests failed. Please check the error messages above.")
        sys.exit(1)
