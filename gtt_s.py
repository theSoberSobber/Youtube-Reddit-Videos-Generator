import subprocess
import os
from gtts import gTTS

def text_to_speech(text, speed=1.3):
    # Initialize gTTS with the text to convert
    speech = gTTS(text)

    # Save the audio file to a temporary file
    temp_audio_file = 'temp_audio.mp3'
    speech.save(temp_audio_file)

    # Use ffmpeg to adjust the speed of the audio and save it as rec16.mp3
    output_audio_file = "rec16.mp3"
    ffmpeg_command = ["ffmpeg", "-y", "-i", temp_audio_file, "-filter:a", f"atempo={speed}", output_audio_file]
    subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Remove the temporary audio file
    os.remove(temp_audio_file)

if __name__ == "__main__":
    text_to_speech("meow")