# Store POS Android Installation Guide

## 📱 Installing Your Store POS App on Android

### Prerequisites
- Android device running Android 5.0 (API 21) or higher
- At least 100MB of free storage space
- Internet connection (for initial setup and syncing)

### Step 1: Enable Unknown Sources
1. Open **Settings** on your Android device
2. Navigate to **Security** or **Privacy & Security**
3. Find **Install unknown apps** or **Unknown sources**
4. Enable installation from the source you'll use (e.g., File Manager, Chrome, etc.)

### Step 2: Download the APK
Choose one of these methods to get your APK:

#### Method A: Direct Transfer
1. Connect your phone to your computer via USB
2. Copy the APK file from your computer's `bin/` folder to your phone's Downloads folder
3. Use a file manager app to locate and tap the APK file

#### Method B: Cloud Storage
1. Upload the APK to Google Drive, Dropbox, or similar
2. Download it on your phone
3. Tap the downloaded APK file

#### Method C: Email
1. Email the APK file to yourself
2. Open the email on your phone
3. Download and tap the APK attachment

### Step 3: Install the App
1. Tap the APK file
2. You'll see an installation screen
3. Tap **Install**
4. Wait for the installation to complete
5. Tap **Open** to launch the app

### Step 4: Grant Permissions
When you first open the app, it may request permissions:

- **Storage**: To save receipts and database files
- **Camera**: For barcode scanning (if implemented)
- **Internet**: For potential online features
- **Vibrate**: For haptic feedback

Grant these permissions for full functionality.

## 🚀 First Time Setup

### Default Login Credentials
- **Admin**: 
  - Username: `admin`
  - Password: `admin123`
- **Cashier**: 
  - Username: `cashier`
  - Password: `cashier123`

### Initial Configuration
1. Launch the app
2. Log in with admin credentials
3. Set up your store information
4. Add initial inventory items
5. Create additional user accounts if needed

## 📋 App Features

### Main Features
- **Point of Sale (POS)**: Process sales transactions
- **Inventory Management**: Track stock levels and products
- **Customer Management**: Maintain customer database
- **Reports**: Generate sales and inventory reports
- **Multi-user Support**: Admin and cashier roles

### Screens Available
- **Login Screen**: Secure user authentication
- **Main Menu**: Navigate to different modules
- **Cashier Screen**: Process sales and transactions
- **Inventory Screen**: Manage products and stock
- **Customer Screen**: Customer information management
- **Reports Screen**: View sales and inventory reports

## 🔧 Troubleshooting

### App Won't Install
- **Error**: "App not installed"
  - **Solution**: Enable "Unknown sources" in Settings
  - **Solution**: Clear space on your device (need at least 100MB)
  - **Solution**: Try redownloading the APK file

### App Crashes on Startup
- **Solution**: Restart your device
- **Solution**: Clear app data: Settings > Apps > Store POS > Storage > Clear Data
- **Solution**: Reinstall the app

### Login Issues
- **Problem**: Can't log in with default credentials
  - **Solution**: Ensure you're using the correct credentials:
    - Admin: admin / admin123
    - Cashier: cashier / cashier123
  - **Solution**: Check if caps lock is on

### Performance Issues
- **Problem**: App runs slowly
  - **Solution**: Close other apps running in background
  - **Solution**: Restart the app
  - **Solution**: Restart your device

### Database Issues
- **Problem**: Data not saving
  - **Solution**: Grant storage permissions to the app
  - **Solution**: Ensure device has sufficient storage space

## 📊 Data Management

### Backup Your Data
The app stores data locally on your device. To backup:
1. Navigate to your device's internal storage
2. Look for the app's data folder
3. Copy database files to a safe location

### Receipts
- Receipts are saved in the `assets/receipts/` folder
- They are stored as text files with transaction details

## 🔄 Updates

### Installing Updates
1. Download the new APK file
2. Install it over the existing app
3. Your data will be preserved

### Version Information
- Current Version: 1.0
- Package Name: com.storepos.storepos
- Minimum Android Version: 5.0 (API 21)
- Target Android Version: 13 (API 33)

## 📞 Support

### Common Issues and Solutions
1. **App not responding**: Force close and restart
2. **Data lost**: Check if you have backup files
3. **Can't scan barcodes**: Ensure camera permission is granted
4. **Sync issues**: Check internet connection

### Getting Help
If you encounter issues not covered here:
1. Check the app logs (if accessible)
2. Try reinstalling the app
3. Contact your system administrator

## 🔒 Security Notes

### Data Security
- All data is stored locally on your device
- Use strong passwords for user accounts
- Regularly backup your data
- Keep the app updated

### Permissions Explained
- **Storage**: Required to save transaction data and receipts
- **Camera**: Optional, for barcode scanning features
- **Internet**: Optional, for online features and updates
- **Vibrate**: Optional, for haptic feedback during transactions

## 📱 Device Compatibility

### Supported Devices
- Android 5.0+ (API 21 and above)
- ARM64 and ARMv7 processors
- Minimum 2GB RAM recommended
- 100MB+ free storage space

### Tested On
- Android 5.0 to Android 13
- Various screen sizes (phones and tablets)
- Different hardware configurations

---

**Note**: This app is designed for local use. For multi-device synchronization or cloud features, additional setup may be required.
