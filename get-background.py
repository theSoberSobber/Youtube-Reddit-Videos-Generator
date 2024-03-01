import os
import json
import random
import subprocess
from pytube import YouTube
from moviepy.editor import VideoFileClip
from datetime import datetime
import math

def load_consolidated_json(file_path):
    # Load the consolidated JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def download_video(url, output_path):
    # Check if the video has already been downloaded
    filename = os.path.join(output_path, YouTube(url).streams.filter(file_extension='mp4').first().default_filename)
    if os.path.exists(filename):
        print("Video already downloaded. Skipping download.")
        return filename
    # Download the video from the given URL
    yt = YouTube(url)
    video = yt.streams.filter(file_extension='mp4').first()
    video.download(output_path=output_path)
    return os.path.join(output_path, video.default_filename)  # Return the full output path

def parse_duration(duration_str):
    # Parse the stringified datetime object and convert it to an integer representing the duration in seconds
    dt = datetime.strptime(duration_str, '%H:%M:%S,%f')
    duration_seconds = dt.hour * 3600 + dt.minute * 60 + dt.second + dt.microsecond / 1e6
    return int(duration_seconds)

def choose_segment_length(consolidated_data, offset):
    # Choose the segment length based on the last entry in the consolidated data plus offset
    last_entry_duration = parse_duration(consolidated_data[-1][2])
    segment_length = last_entry_duration + offset
    return segment_length

def choose_random_start_time(video_duration, segment_length):
    # Choose a random start time within the valid range
    max_start_time = video_duration - segment_length
    start_time = random.uniform(0, max_start_time)
    return start_time

def chop_video(input_path, output_path, start_time, segment_length):
    # Use ffmpeg to resize the video to the desired aspect ratio (9:16 for vertical)
    command = [
        "ffmpeg",
        "-i", f"{input_path}",
        "-ss", str(math.floor(start_time)),  # Start time
        "-t", str(math.ceil(segment_length)),  # Duration
        "-vf", f"crop=ih*(1080/1920):ih",
        "-c:v", "h264", 
        "-b:v", "20M",
        "-b:a", "192k", 
        "-an", f"{output_path}"
    ]
    print(command)
    subprocess.run(command, capture_output=False, text=True)

if __name__ == "__main__":
    # Read the URL of the YouTube video from a file
    with open('video-link.txt', 'r') as file:
        url = file.readline().strip()  # Read the first line from the file

    output_path = "./output/segment.mp4"  # Output path for the segment
    consolidated_json_path = "consolidated.json"  # Path to the consolidated JSON file
    offset = 3  # Offset for segment length in seconds
    
    # Load consolidated JSON data
    consolidated_data = load_consolidated_json(consolidated_json_path)
    
    # Choose segment length
    segment_length = choose_segment_length(consolidated_data, offset)
    
    # Download the video
    print("Downloading video...")
    filename = download_video(url, "./output")
    print("Video downloaded successfully!")
    
    # Open the downloaded video to get its duration
    video_clip = VideoFileClip(f"{filename}")
    video_duration = video_clip.duration
    
    # Choose a random start time within the valid range
    start_time = choose_random_start_time(video_duration, segment_length)
    
    # Chop the video into the specified segment with the desired aspect ratio
    print("Chopping video into segment...")
    chop_video(f"{filename}", output_path, start_time, segment_length)
    print("Video segment chopped successfully!")
