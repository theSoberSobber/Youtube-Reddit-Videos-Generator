#!/bin/bash

# Define colors for logging
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Echo function with color
cecho () {
    color=$1
    shift
    echo -e "${color}$@${NC}"
}

# Function to check if file exists before removing
safe_rm() {
    if [ -e "$1" ]; then
        rm "$1"
        cecho $GREEN "Removed $1"
    else
        cecho $RED "$1 not found, skipping removal"
    fi
}

# Check if arguments are provided for gtt-s.py
if [ $# -eq 0 ]; then
    cecho $RED "Usage: $0 <arguments for gtt-s.py>"
    exit 1
fi

# Main script
cecho $GREEN "Starting script..."

# Run gen_init.py with arguments
cecho $GREEN "Running gen_init.py (thumbnail + tts)..."
python gen_init.py $*
cecho $GREEN "Thumbnail + TTS completed."

ls

# Convert rec16.mp3 to rec16.wav
cecho $GREEN "Converting rec16.mp3 to rec16.wav..."
ffmpeg -i rec16.mp3 -ar 16000 rec16.wav
cecho $GREEN "Conversion complete."

ls

# Run main script with model and input file
cecho $GREEN "Running main script..."
./main -m models/ggml-large-v1.bin rec16.wav -ojf -sow
cecho $GREEN "Main script completed."

ls

# Run consolidator script
cecho $GREEN "Running consolidator script..."
python consolidator.py > /dev/null 2>&1
cecho $GREEN "Consolidator script completed."

ls

cecho $GREEN "Fetching and Chopping BG Video..."
python get-background.py
cecho $GREEN "BG Video Processed"

ls

cecho $GREEN "Layering Captions on Segment.mp4..."
python captions.py
cecho $GREEN "Captions Layered Successfully"

ls

cecho $GREEN "Merging Audio with Captioned Video..."
python merge-audio.py
cecho $GREEN "Merged Audio Successfully"

ls

cecho $RED "Cleaning Up"
safe_rm "rec16.wav"
safe_rm "rec16.mp3"
safe_rm "rec16.wav.json"
safe_rm "consolidated.json"
safe_rm "./output/segment.mp4"
safe_rm "output_with_captions.mp4"

ls

cecho $GREEN "Script finished."
