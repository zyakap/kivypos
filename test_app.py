#!/usr/bin/env python3
"""
Comprehensive test script for the Store POS & Inventory Management System.
This tests both database functionality and GUI components (when Kivy is available).
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_layer():
    """Test database functionality"""
    print("\n" + "="*50)
    print("TESTING DATABASE LAYER")
    print("="*50)
    
    try:
        from database.database_manager import DatabaseManager
        
        # Initialize database
        print("✅ Database imports successful")
        db_manager = DatabaseManager("test_full_app.db")
        print("✅ Database initialized")
        
        # Test authentication
        admin = db_manager.authenticate_user("admin", "admin123")
        cashier = db_manager.authenticate_user("cashier", "cashier123")
        
        if admin and cashier:
            print("✅ User authentication working")
            return True, db_manager
        else:
            print("❌ User authentication failed")
            return False, None
            
    except Exception as e:
        print(f"❌ Database layer failed: {e}")
        return False, None

def test_gui_imports():
    """Test GUI framework imports"""
    print("\n" + "="*50)
    print("TESTING GUI IMPORTS")
    print("="*50)
    
    try:
        import kivy
        print(f"✅ Kivy {kivy.__version__} imported successfully")
        
        import kivymd
        print(f"✅ KivyMD imported successfully")
        
        # Test core Kivy components
        from kivy.app import App
        from kivy.uix.screenmanager import ScreenManager
        print("✅ Core Kivy components imported")
        
        # Test KivyMD components
        from kivymd.app import MDApp
        from kivymd.uix.screen import MDScreen
        print("✅ KivyMD components imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ GUI import failed: {e}")
        print("   Kivy/KivyMD may not be installed yet")
        return False
    except Exception as e:
        print(f"❌ GUI import error: {e}")
        return False

def test_screen_imports():
    """Test screen imports"""
    print("\n" + "="*50)
    print("TESTING SCREEN IMPORTS")
    print("="*50)
    
    try:
        from screens.login_screen import LoginScreen
        print("✅ LoginScreen imported")
        
        from screens.main_menu_screen import MainMenuScreen
        print("✅ MainMenuScreen imported")
        
        from screens.cashier_screen import CashierScreen
        print("✅ CashierScreen imported")
        
        from screens.inventory_screen import InventoryScreen
        print("✅ InventoryScreen imported")
        
        from screens.customer_screen import CustomerScreen
        print("✅ CustomerScreen imported")
        
        from screens.reports_screen import ReportsScreen
        print("✅ ReportsScreen imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Screen import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Screen import error: {e}")
        return False

def test_main_app_import():
    """Test main application import"""
    print("\n" + "="*50)
    print("TESTING MAIN APP")
    print("="*50)
    
    try:
        # Import main app (but don't run it)
        import main
        print("✅ Main application imported successfully")
        
        # Check if StorePOSApp class exists
        if hasattr(main, 'StorePOSApp'):
            print("✅ StorePOSApp class found")
            return True
        else:
            print("❌ StorePOSApp class not found")
            return False
            
    except ImportError as e:
        print(f"❌ Main app import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Main app error: {e}")
        return False

def test_file_structure():
    """Test project file structure"""
    print("\n" + "="*50)
    print("TESTING FILE STRUCTURE")
    print("="*50)
    
    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "TODO.md",
        "database/__init__.py",
        "database/models.py",
        "database/database_manager.py",
        "screens/__init__.py",
        "screens/login_screen.py",
        "screens/main_menu_screen.py",
        "screens/cashier_screen.py",
        "screens/inventory_screen.py",
        "screens/customer_screen.py",
        "screens/reports_screen.py",
        "widgets/__init__.py",
        "utils/__init__.py"
    ]
    
    required_dirs = [
        "assets",
        "assets/images",
        "assets/receipts"
    ]
    
    missing_files = []
    missing_dirs = []
    
    # Check files
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    # Check directories
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    if not missing_files and not missing_dirs:
        print(f"✅ All {len(required_files)} required files present")
        print(f"✅ All {len(required_dirs)} required directories present")
        return True
    else:
        if missing_files:
            print(f"❌ Missing files: {missing_files}")
        if missing_dirs:
            print(f"❌ Missing directories: {missing_dirs}")
        return False

def run_comprehensive_test():
    """Run comprehensive application test"""
    print("="*60)
    print("STORE POS COMPREHENSIVE APPLICATION TEST")
    print("="*60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_results = {}
    
    # Test 1: File Structure
    test_results['file_structure'] = test_file_structure()
    
    # Test 2: Database Layer
    db_success, db_manager = test_database_layer()
    test_results['database'] = db_success
    
    # Test 3: GUI Imports
    test_results['gui_imports'] = test_gui_imports()
    
    # Test 4: Screen Imports (only if GUI imports work)
    if test_results['gui_imports']:
        test_results['screen_imports'] = test_screen_imports()
        
        # Test 5: Main App (only if screens work)
        if test_results['screen_imports']:
            test_results['main_app'] = test_main_app_import()
        else:
            test_results['main_app'] = False
    else:
        test_results['screen_imports'] = False
        test_results['main_app'] = False
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results.values() if result)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title():<20} {status}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    # Determine readiness
    if test_results['database'] and test_results['file_structure']:
        if test_results['gui_imports'] and test_results['screen_imports'] and test_results['main_app']:
            print("\n🎉 APPLICATION FULLY READY!")
            print("   All components tested successfully.")
            print("   You can run: python main.py")
        else:
            print("\n⚠️  APPLICATION PARTIALLY READY")
            print("   Database layer is functional.")
            print("   GUI components need Kivy installation to complete.")
            print("   Wait for Kivy installation to finish, then run this test again.")
    else:
        print("\n❌ APPLICATION NOT READY")
        print("   Critical components are missing or broken.")
    
    # Provide next steps
    print(f"\n📋 NEXT STEPS:")
    if not test_results['gui_imports']:
        print("   1. Wait for Kivy installation to complete")
        print("   2. Run this test again: python test_app.py")
    elif not test_results['screen_imports'] or not test_results['main_app']:
        print("   1. Check for import errors in screen files")
        print("   2. Verify all dependencies are installed")
    else:
        print("   1. Launch the application: python main.py")
        print("   2. Test login with admin/admin123 or cashier/cashier123")
        print("   3. Explore all features: POS, Inventory, Customers, Reports")
    
    print(f"\n📊 SYSTEM INFO:")
    print(f"   Python Version: {sys.version}")
    print(f"   Working Directory: {os.getcwd()}")
    print(f"   Test Database: test_full_app.db")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    try:
        success = run_comprehensive_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
