import numpy as np
import wavio

frequency = 440  # Our played note will be 440 Hz
fs = 44100  # 44100 samples per second
dit_duration = int(44100 / 10 * 3)
dit_silence = np.zeros(dit_duration)
char_silence = np.zeros(dit_duration * 3)
word_silence = np.zeros(dit_duration * 7)
output_audio = []

# message = [1, 1, 1, 2, 0, 0, 0, 2, 1, 1, 1, 3, 1, 1, 1, 2, 0, 0, 0, 2, 1, 1, 1]


def make_morse(message):
    global output_audio
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

    wavio.write("morse.wav", output_audio, fs, sampwidth=2)
