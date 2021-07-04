import numpy as np
import wavio
import os
from datetime import datetime

frequency = 440  # Morse sounds will be at 440 Hz
fs = 44100  # 44100 samples per second

base_duration = 0.1  # Note duration of dit in seconds
dit_duration = int(44100 * base_duration)  # Note duration of dit in kHz

# these silence arrays are added between the characters
dit_silence = np.zeros(dit_duration)  # should be the same duration as dit
char_silence = np.zeros(dit_duration * 3)  # standard reference multiplier between characters
word_silence = np.zeros(dit_duration * 7)  # standard reference multipliers between words


def make_morse(message):

    # set up array for full audio to be outputted to wav file
    output_audio = []

    # remove previous wav file from directory
    directory = "./static"
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(".wav")]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)

    # converts each character in the input array
    for i in range(len(message)):

        # (0 is dah, 1 is dit, 2 is character spacing, 3 is word spacing)
        # dealing with silences
        if message[i] == 2:
            audio = char_silence
        elif message[i] == 3:
            audio = word_silence
        else:
            # adding sounds for characters
            if message[i] == 1:  # dit
                t = base_duration  # Note duration of dit in seconds
            else:  # dah
                t = base_duration * 3  # Note duration of dah in seconds

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

    # generate specific filename for browser refresh in audio player
    timestamp = str(datetime.now()).replace(":", "") .replace(" ", "").replace(".", "")
    filename = f"static/morse{timestamp}.wav"

    # write the output wav file
    wavio.write(filename, output_audio, fs, sampwidth=2)

    # filename is passed through to html audio player as src
    return filename
