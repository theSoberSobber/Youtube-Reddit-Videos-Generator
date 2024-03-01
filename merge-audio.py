from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def merge_audio_with_video(video_path, audio_path, output_path):
    # Load the video clip
    video_clip = VideoFileClip(video_path)
    
    # Load the audio clip
    audio_clip = AudioFileClip(audio_path)
    
    # Calculate the duration of the shorter audio clip
    audio_duration = min(video_clip.duration, audio_clip.duration)
    
    # Set the audio clip duration to match the duration of the video clip
    audio_clip = audio_clip.set_duration(audio_duration)
    
    # Set the audio clip to start at the beginning of the video clip
    audio_clip = audio_clip.set_start(0)
    
    # Merge the audio clip with the video clip
    final_clip = video_clip.set_audio(audio_clip)
    
    # Write the final video with merged audio to the output path
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
    # Close the video and audio clips
    video_clip.close()
    audio_clip.close()

if __name__ == "__main__":
    # Path to the video file with layered captions
    video_path = "output_with_captions.mp4"
    
    # Path to the audio file to be merged
    audio_path = "rec16.wav"
    
    # Output path for the final video with merged audio
    output_path = "final_video_with_audio.mp4"
    
    # Merge audio with video
    merge_audio_with_video(video_path, audio_path, output_path)
