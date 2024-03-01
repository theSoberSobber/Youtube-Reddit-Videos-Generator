from gtts import gTTS
import sys

def text_to_speech():
    # Accept text input from command line arguments
    text = ' '.join(sys.argv[1:])

    # Initialize gTTS with the text to convert
    speech = gTTS(text)

    # Save the audio file to a temporary file
    speech_file = 'rec16.mp3'
    speech.save(speech_file)

    # Play the audio file
    # os.system('afplay ' + speech_file)

if __name__ == "__main__":
    text_to_speech()
