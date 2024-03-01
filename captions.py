from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import json

def time_to_seconds(time_str):
    # Split the time string into hours, minutes, seconds, and milliseconds
    hours, minutes, seconds_milliseconds = time_str.split(':')
    seconds, milliseconds = seconds_milliseconds.split(',')
    
    # Convert hours, minutes, seconds, and milliseconds to integers
    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)
    milliseconds = int(milliseconds)
    
    # Convert the time to seconds
    total_seconds = (hours * 3600) + (minutes * 60) + seconds + (milliseconds / 1000)
    return total_seconds

def layer_captions(background_video_path, captions_data, output_path):
    # Load the background video
    background_clip = VideoFileClip(background_video_path)
    
    # Initialize an empty list to hold the clips with captions
    caption_clips = []
    
    # Iterate through each entry in the consolidated JSON file
    for entry in captions_data:
        text, start_time_str, end_time_str = entry
        
        # Convert the stringified datetime objects to integers
        start_time = time_to_seconds(start_time_str)
        end_time = time_to_seconds(end_time_str)
        
        # Create a TextClip with the extracted text
        text_clip = TextClip(text, fontsize=15, font='font.ttf', color='white', align='center', method='caption', size=background_clip.size) 
        # Set the duration of the text clip
        text_clip = text_clip.set_duration(end_time - start_time)
        
        # Position the text clip vertically in the middle of the video
        text_clip = text_clip.set_position(('center', 'center'))
        
        # Add the text clip to the list
        caption_clips.append(text_clip.set_start(start_time))
    
    # Composite the text clips onto the background video
    final_clip = CompositeVideoClip([background_clip] + caption_clips)
    
    # Export the final video with the layered captions
    final_clip.write_videofile(output_path, codec='libx264', fps=24)
    
    # Close the background clip
    background_clip.close()

if __name__ == "__main__":
    # Path to the background video
    background_video_path = "./output/segment.mp4"
    
    # Path to the consolidated JSON file
    consolidated_json_path = "consolidated.json"
    
    # Output path for the final video with layered captions
    output_path = "output_with_captions.mp4"
    
    # Load captions data from the JSON file
    with open(consolidated_json_path, 'r') as file:
        captions_data = json.load(file)
    
    # Layer captions onto the background video
    layer_captions(background_video_path, captions_data, output_path)
