#!/bin/bash

# Default to non-verbose mode
VERBOSE=false

# Check if script is running as root
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Function to print green message
print_green() {
    echo -e "${GREEN}$1${NC}"
}

# Function to print red message
print_red() {
    echo -e "${RED}$1${NC}"
}

# Function to print verbose output
verbose_print() {
    if [ "$VERBOSE" = true ]; then
        echo "$1"
    fi
}

# Print message about verbose mode
print_verbose_message() {
    echo "You can enable verbose mode using the --verbose or -v flag."
}

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -v|--verbose) VERBOSE=true;;
        *) echo "Unknown parameter passed: $1"; exit 1;;
    esac
    shift
done

# Print message about enabling verbose mode
print_verbose_message

# Update package lists and install essential packages
print_green "Updating package lists and installing essential packages..."
apt-get update
apt-get install -y build-essential cmake make g++ ffmpeg imagemagick libmagick++-dev
verbose_print "Essential packages installed successfully."

# Change directory to whisper submodule and build it
print_green "Building whisper submodule..."
cd lib/whisper
cmake -B build && cmake --build build && print_green "Whisper submodule built successfully." || { print_red "Error building whisper submodule."; exit 1; }
cd ../../  # Navigate back to the repository's root directory

# Move the main binary to the root of the project
print_green "Moving main binary to the root of the project..."
mv ./lib/whisper/build/bin/main . && print_green "Main binary moved successfully." || { print_red "Error moving main binary."; exit 1; }

# Run model downloader script
print_green "Running model downloader script..."
./models/downloader.sh large-v1 && print_green "Model downloader script completed successfully." || { print_red "Error running model downloader script."; exit 1; }

# Backup existing policy.xml
if [ -f /etc/ImageMagick-6/policy.xml ]; then
    print_green "Backing up existing policy.xml..."
    cp /etc/ImageMagick-6/policy.xml /etc/ImageMagick-6/policy.xml.backup
    verbose_print "Existing policy.xml backed up to /etc/ImageMagick-6/policy.xml.backup"
fi

# Replace policy.xml
print_green "Replacing policy.xml..."
mv policy.xml /etc/ImageMagick-6/policy.xml && print_green "policy.xml replaced successfully." || { print_red "Error replacing policy.xml."; exit 1; }

# Install Python dependencies
print_green "Installing Python dependencies..."
python -m pip install --upgrade pip
python -m pip install moviepy pytube gtts -r lib/generator/requirements.txt && print_green "Python dependencies installed successfully." || { print_red "Error installing Python dependencies."; exit 1; }

# Make the generate-with-extra-logging.sh and generate.sh scripts executable
print_green "Making scripts executable..."
chmod +x generate-with-extra-logging.sh && print_green "generate-with-extra-logging.sh made executable." || { print_red "Error making generate-with-extra-logging.sh executable."; exit 1; }
chmod +x generate.sh && print_green "generate.sh made executable." || { print_red "Error making generate.sh executable."; exit 1; }

print_green "Setup completed successfully."
