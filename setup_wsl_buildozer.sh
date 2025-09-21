#!/bin/bash

# Setup script for Buildozer in WSL
# Run this script in WSL Ubuntu after installing WSL

echo "🚀 Setting up Buildozer for Android development in WSL..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and development tools
echo "🐍 Installing Python and development tools..."
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y build-essential git unzip wget curl
sudo apt install -y libffi-dev libssl-dev
sudo apt install -y zlib1g-dev libjpeg-dev
sudo apt install -y libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev

# Install Java (required for Android development)
echo "☕ Installing Java JDK..."
sudo apt install -y openjdk-17-jdk

# Set JAVA_HOME
echo "🔧 Setting up Java environment..."
echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc
echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.bashrc
source ~/.bashrc

# Install Android SDK dependencies
echo "📱 Installing Android SDK dependencies..."
sudo apt install -y libc6:i386 libncurses5:i386 libstdc++6:i386 lib32z1 libbz2-1.0:i386

# Install Buildozer and Cython
echo "🔨 Installing Buildozer and dependencies..."
pip3 install --upgrade pip
pip3 install buildozer
pip3 install cython

# Create project directory
echo "📁 Creating project directory..."
mkdir -p ~/android-projects
cd ~/android-projects

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy your Store POS project to ~/android-projects/"
echo "2. Navigate to your project directory: cd ~/android-projects/stoapp"
echo "3. Build the APK: buildozer android debug"
echo ""
echo "📍 Your project should be copied to: $(pwd)"
echo "💡 You can access this from Windows at: \\\\wsl\$\\Ubuntu\\home\\$(whoami)\\android-projects"
