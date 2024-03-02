from gtt_s import text_to_speech
import sys

sys.path.append('lib/generator')

from generate_tweet_image import generate


# Get input text from command line arguments
input_text = ' '.join(sys.argv[1:])

# Extract the title between <<< and >>>
start_index = input_text.find("<<<")
end_index = input_text.find(">>>")

if start_index != -1 and end_index != -1:
    title = input_text[start_index + 3: end_index].strip()
    # Remove angle brackets from the title
    title = title.strip("<>").strip()
else:
    title = ""

generate(title)

# Remove asterisks from the text
processed_text = input_text.replace("*", "").replace("<", "").replace(">", "")

# Pass the processed text to the text_to_speech function
text_to_speech(processed_text)