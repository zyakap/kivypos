#!/usr/bin/env python3
"""
Simple launcher script for the Store POS & Inventory Management System.
This script provides an easy way to launch the application with proper error handling.
"""

import sys
import os
from datetime import datetime

def check_dependencies():
    """Check if all required dependencies are available"""
    print("Checking dependencies...")
    
    missing_deps = []
    
    try:
        import kivy
        print(f"✅ Kivy {kivy.__version__}")
    except ImportError:
        missing_deps.append("kivy")
        print("❌ Kivy not found")
    
    try:
        import kivymd
        print("✅ KivyMD")
    except ImportError:
        missing_deps.append("kivymd")
        print("❌ KivyMD not found")
    
    try:
        import sqlite3
        print("✅ SQLite3")
    except ImportError:
        missing_deps.append("sqlite3")
        print("❌ SQLite3 not found")
    
    try:
        import pillow
        print("✅ Pillow")
    except ImportError:
        try:
            import PIL
            print("✅ PIL/Pillow")
        except ImportError:
            missing_deps.append("pillow")
            print("❌ Pillow not found")
    
    return missing_deps

def launch_application():
    """Launch the Store POS application"""
    print("="*60)
    print("STORE POS & INVENTORY MANAGEMENT SYSTEM")
    print("="*60)
    print(f"Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check dependencies
    missing_deps = check_dependencies()
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("\nPlease install missing dependencies:")
        print("   pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies available!")
    print("\nLaunching application...")
    print("\n" + "="*60)
    
    try:
        # Import and run the main application
        from main import StorePOSApp
        
        print("🚀 Starting Store POS Application...")
        print("\n📋 Default Login Credentials:")
        print("   Admin: admin / admin123")
        print("   Cashier: cashier / cashier123")
        print("\n" + "="*60)
        
        # Create and run the app
        app = StorePOSApp()
        app.run()
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\nThere may be an issue with the application files.")
        print("Please run the test script first: python test_app.py")
        return False
        
    except Exception as e:
        print(f"❌ Application Error: {e}")
        print("\nThe application encountered an error during startup.")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main launcher function"""
    try:
        success = launch_application()
        if success:
            print("\n👋 Application closed successfully.")
        else:
            print("\n💥 Application failed to start.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Application interrupted by user.")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
