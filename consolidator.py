import json
import re
from datetime import datetime, timedelta

threshold = timedelta(seconds=2)

def subtract_timestamps(timestamp1_str, timestamp2_str):
    # Convert timestamp strings to datetime objects
    timestamp_format = "%H:%M:%S,%f"
    timestamp1 = datetime.strptime(timestamp1_str, timestamp_format)
    timestamp2 = datetime.strptime(timestamp2_str, timestamp_format)

    # Calculate the time difference
    time_difference = timestamp2 - timestamp1

    return time_difference < threshold

consolidated = []

def process_json_file(file_path, output_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

        # Check if the 'transcription' key exists
        if 'transcription' in data and isinstance(data['transcription'], list):
            # Iterate over the list of transcriptions
            for transcription_obj in data['transcription']:
                # Check if the 'tokens' key exists in the transcription object
                if 'tokens' in transcription_obj and isinstance(transcription_obj['tokens'], list):
                    # Iterate over the list of tokens
                    for token_obj in transcription_obj['tokens']:
                        # Check if the text of the token is not [_BEG_] or matches the pattern [_TT_<someNumberHere>]
                        if 'text' in token_obj and token_obj['text'] not in ['[_BEG_]'] \
                                and not re.match(r'\[_TT_\d+\]', token_obj['text']):
                            if len(consolidated)==0:
                                consolidated.append([token_obj['text'], token_obj['timestamps']['from'], token_obj['timestamps']['to']])
                                continue
                            if subtract_timestamps(consolidated[-1][1], token_obj['timestamps']['to']):
                                tmp = consolidated[-1]
                                consolidated.pop()
                                consolidated.append([tmp[0]+token_obj['text'], tmp[1], token_obj['timestamps']['to']])
                            else:
                                consolidated.append([token_obj['text'], token_obj['timestamps']['from'], token_obj['timestamps']['to']])
                else:
                    print("No 'tokens' key found in transcription object or it's not a list.")
        else:
            print("No 'transcription' key found in the JSON or it's not a list.")

        # Write the consolidated object to the output file
        with open(output_path, 'w') as output_file:
            json.dump(consolidated, output_file, indent=4)

# Example usage
input_file_path = 'rec16.wav.json'  # Replace 'rec16.wav.json' with the actual path to your JSON file
output_file_path = 'consolidated.json'  # Replace 'consolidated.json' with the desired output file path
process_json_file(input_file_path, output_file_path)
