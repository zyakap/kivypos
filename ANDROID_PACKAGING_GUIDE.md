# Android Packaging Guide for Store POS App

Your Kivy Store POS & Inventory Management app is ready to be packaged for Android! Since you're on Windows, here are the best options:

## Option 1: Using Windows Subsystem for Linux (WSL) - RECOMMENDED

### Step 1: Install WSL
```powershell
# Run as Administrator in PowerShell
wsl --install -d Ubuntu
```

### Step 2: Set up the environment in WSL
```bash
# Update Ubuntu
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install Java (required for Android development)
sudo apt install openjdk-17-jdk -y

# Install build tools
sudo apt install build-essential git unzip -y

# Install Buildozer
pip3 install buildozer
```

### Step 3: Copy your project to WSL
```bash
# Create a directory in WSL
mkdir -p ~/android-projects
cd ~/android-projects

# Copy your project files (you can use Windows Explorer to access \\wsl$\Ubuntu\home\yourusername\android-projects)
```

### Step 4: Build the APK
```bash
cd ~/android-projects/stoapp
buildozer android debug
```

## Option 2: Using Docker (Alternative)

### Step 1: Install Docker Desktop for Windows

### Step 2: Use Kivy Buildozer Docker Image
```powershell
# Pull the buildozer image
docker pull kivy/buildozer

# Run buildozer in container (from your project directory)
docker run --rm -v ${PWD}:/app kivy/buildozer android debug
```

## Option 3: Using GitHub Actions (Cloud Build)

Create a `.github/workflows/build-android.yml` file in your project:

```yaml
name: Build Android APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install buildozer
    
    - name: Build APK
      run: buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: store-pos-apk
        path: bin/*.apk
```

## Option 4: Manual Setup with Python-for-Android (Advanced)

If you prefer manual control:

```bash
# Install python-for-android
pip install python-for-android

# Create the APK
p4a apk --private . --package=com.storepos.app --name="Store POS" --version=1.0 --bootstrap=sdl2 --requirements=python3,kivy,kivymd,pillow,reportlab,pyzbar,plyer
```

## Current Project Configuration

Your `buildozer.spec` file has been configured with:
- **App Name**: Store POS & Inventory
- **Package**: com.storepos.storepos
- **Version**: 1.0
- **Requirements**: python3,kivy==2.2.0,kivymd==1.1.1,pillow==10.0.1,reportlab==4.0.4,pyzbar==0.1.9,plyer==2.1.0
- **Permissions**: INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, CAMERA, VIBRATE
- **Target API**: 33
- **Min API**: 21

## Installation Instructions

Once you have the APK file:

1. **Enable Unknown Sources** on your Android device:
   - Go to Settings > Security > Unknown Sources (or Install Unknown Apps)
   - Enable installation from unknown sources

2. **Transfer the APK** to your phone:
   - Copy the APK file to your phone via USB, email, or cloud storage
   - The APK will be in the `bin/` folder after building

3. **Install the APK**:
   - Open the APK file on your Android device
   - Follow the installation prompts
   - Grant necessary permissions when requested

## Troubleshooting

### Common Issues:
1. **Build fails**: Ensure all dependencies are installed
2. **App crashes**: Check that all Python packages are compatible with Android
3. **Permissions denied**: Make sure Android permissions are properly configured

### Debug Mode vs Release Mode:
- Use `buildozer android debug` for testing
- Use `buildozer android release` for production (requires signing)

## Next Steps

1. Choose one of the options above (WSL recommended)
2. Follow the setup instructions
3. Build your APK
4. Test on your Android device
5. Iterate and improve based on testing

The WSL option is recommended as it provides the most reliable build environment while staying on Windows.
