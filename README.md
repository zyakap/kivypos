# Store POS & Inventory Management System

A comprehensive Point of Sale and Inventory Management system built with Kivy/KivyMD for cross-platform deployment, including Android.

## 🚀 Features

- **Point of Sale (POS)**: Complete transaction processing
- **Inventory Management**: Track products and stock levels
- **Customer Management**: Maintain customer database
- **Sales Reports**: Generate detailed sales analytics
- **Multi-user Support**: Admin and cashier roles
- **Cross-platform**: Runs on Windows, Linux, macOS, and Android

## 📱 Android APK

This repository automatically builds Android APK files using GitHub Actions. 

### Download APK
1. Go to the [Actions](../../actions) tab
2. Click on the latest successful build
3. Download the `store-pos-android-apk` artifact
4. Extract and install the APK on your Android device

### Build Status
![Build Android APK](../../workflows/Build%20Android%20APK/badge.svg)

## 🛠️ Installation

### Desktop (Windows/Linux/macOS)
```bash
# Clone the repository
git clone <your-repo-url>
cd stoapp

# Install dependencies
pip install -r requirements.txt

# Run the application
python launch_app.py
```

### Android
See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) for detailed Android installation instructions.

## 🔧 Development

### Requirements
- Python 3.8+
- Kivy 2.2.0
- KivyMD 1.1.1
- See `requirements.txt` for full list

### Project Structure
```
stoapp/
├── main.py                 # Main application entry point
├── launch_app.py          # Application launcher with dependency checks
├── screens/               # UI screens
│   ├── login_screen.py
│   ├── main_menu_screen.py
│   ├── cashier_screen.py
│   ├── inventory_screen.py
│   ├── customer_screen.py
│   └── reports_screen.py
├── database/              # Database management
│   ├── database_manager.py
│   └── models.py
├── assets/                # Static assets
│   ├── images/
│   └── receipts/
├── widgets/               # Custom widgets
├── utils/                 # Utility functions
└── buildozer.spec        # Android build configuration
```

### Default Login Credentials
- **Admin**: admin / admin123
- **Cashier**: cashier / cashier123

## 📦 Building for Android

### Automatic Build (GitHub Actions)
Push your changes to GitHub and the APK will be built automatically.

### Manual Build Options
See [ANDROID_PACKAGING_GUIDE.md](ANDROID_PACKAGING_GUIDE.md) for detailed build instructions including:
- WSL setup for Windows
- Docker build
- Manual buildozer setup

## 📋 Usage

1. **Login**: Use default credentials or create new users
2. **Main Menu**: Navigate to different modules
3. **Cashier**: Process sales transactions
4. **Inventory**: Manage products and stock
5. **Customers**: Maintain customer information
6. **Reports**: View sales and inventory analytics

## 🔒 Security

- Local SQLite database storage
- User authentication system
- Role-based access control (Admin/Cashier)
- Secure transaction processing

## 📊 Database

The application uses SQLite for local data storage with the following main tables:
- Users (authentication and roles)
- Products (inventory items)
- Customers (customer information)
- Sales (transaction records)
- Sale Items (transaction line items)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- Check [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) for installation help
- Review [ANDROID_PACKAGING_GUIDE.md](ANDROID_PACKAGING_GUIDE.md) for build issues
- Open an issue for bugs or feature requests

## 🔄 Version History

- **v1.0**: Initial release with core POS and inventory features
- Android support with automatic APK building
- Multi-user authentication system
- Comprehensive reporting features

---

**Note**: This application is designed for local business use. For multi-location or cloud-based features, additional development may be required.