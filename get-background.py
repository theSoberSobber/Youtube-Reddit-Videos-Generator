import os
import json
import random
import subprocess
from datetime import datetime
import math
import yt_dlp
from moviepy.editor import VideoFileClip

def load_consolidated_json(file_path):
    # Load the consolidated JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def download_video_yt_dlp(url, output_path):
    try:
        # yt-dlp options
        ydl_opts = {
            'format': 'best[ext=mp4]/best',  # Choose the best available mp4 format
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Save the video in the output directory
        }

        # Download video using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info_dict)

        return video_path  # Return the full path to the downloaded video

    except Exception as e:
        print(f"An error occurred with yt-dlp: {str(e)}")
        return None

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
    print("Running ffmpeg command:", " ".join(command))
    subprocess.run(command, capture_output=False, text=True)

if __name__ == "__main__":
    # Read the URL of the YouTube video from a file
    with open('video-link.txt', 'r') as file:
        url = file.readline().strip()  # Read the first line from the file

    output_dir = "./output"  # Output directory for video
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

    consolidated_json_path = "consolidated.json"  # Path to the consolidated JSON file
    offset = 3  # Offset for segment length in seconds
    output_path = os.path.join(output_dir, "segment.mp4")  # Output path for the chopped segment

    # Load consolidated JSON data
    consolidated_data = load_consolidated_json(consolidated_json_path)

    # Choose segment length
    segment_length = choose_segment_length(consolidated_data, offset)

    # Download the video using yt-dlp
    print("Downloading video...")
    filename = download_video_yt_dlp(url, output_dir)

    if filename:
        print(f"Video downloaded successfully! File saved at {filename}")

        # Open the downloaded video to get its duration
        video_clip = VideoFileClip(filename)
        video_duration = video_clip.duration

        # Choose a random start time within the valid range
        start_time = choose_random_start_time(video_duration, segment_length)

        # Chop the video into the specified segment with the desired aspect ratio
        print("Chopping video into segment...")
        chop_video(filename, output_path, start_time, segment_length)
        print(f"Video segment chopped successfully! Segment saved at {output_path}")

    else:
        print("Failed to download the video.")
