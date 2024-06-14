import os
import ffmpeg


def convert_to_wav(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        input_file = os.path.join(input_folder, filename)

        if filename.lower().endswith(('.mp3', '.m4a', '.flac', '.aac', '.ogg', '.wav')):
            output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + '.wav')

            # convert the audio file to WAV format
            ffmpeg.input(input_file).output(output_file, format='wav').run()
            print(f"Converted {input_file} to {output_file}")

input_folder = "songs"
output_folder = "songs_wav"
convert_to_wav(input_folder, output_folder)
