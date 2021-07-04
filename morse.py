import numpy as np
import wavio
import os
from datetime import datetime

frequency = 440  # Our played note will be 440 Hz
fs = 44100  # 44100 samples per second
dit_duration = int(44100 / 10 * 3)
dit_silence = np.zeros(dit_duration)
char_silence = np.zeros(dit_duration * 3)
word_silence = np.zeros(dit_duration * 7)


def make_morse(message):
    output_audio = []

    directory = "./static"

    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(".wav")]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)

    for i in range(len(message)):

        if message[i] == 2:
            audio = char_silence
        elif message[i] == 3:
            audio = word_silence
        else:
            if message[i] == 1:  # dot
                t = 0.1  # Note duration of dot in seconds
            else:  # dash
                t = 0.3  # Note duration of dash in seconds

            # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
            time_array = np.linspace(0, t, int(t * fs), False)

            # Generate a 440 Hz sine wave
            note = np.sin(frequency * time_array * 2 * np.pi)

            # Ensure that highest value is in 16-bit range
            audio = note * (2**15 - 1) / np.max(np.abs(note))

            # add silence after each signal
            if i < (len(message) - 1) and message[i + 1] in (1, 0):
                audio = np.append(audio, dit_silence)

        # Add to main array
        output_audio = np.append(output_audio, audio)

    # Convert to 16-bit data
    output_audio = output_audio.astype(np.int16)

    timestamp = str(datetime.now()).replace(":", "") .replace(" ", "").replace(".", "")
    filename = f"static/morse{timestamp}.wav"

    wavio.write(filename, output_audio, fs, sampwidth=2)

    return filename
