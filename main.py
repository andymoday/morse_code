from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from morse import make_morse
import time

app = Flask(__name__)
Bootstrap(app)

# set up dictionary of morse characters
morse_dict = {'a': '⚫➖',
              'b': '➖⚫⚫⚫',
              'c': '➖⚫➖⚫',
              'd': '➖⚫⚫',
              'e': '⚫',
              'f': '⚫⚫➖⚫',
              'g': '➖➖⚫',
              'h': '⚫⚫⚫⚫',
              'i': '⚫⚫',
              'j': '⚫➖➖➖',
              'k': '➖⚫➖',
              'l': '⚫➖⚫⚫',
              'm': '➖➖',
              'n': '➖⚫',
              'o': '➖➖➖',
              'p': '⚫➖➖⚫',
              'q': '➖➖⚫➖',
              'r': '⚫➖⚫',
              's': '⚫⚫⚫',
              't': '➖',
              'u': '⚫⚫➖',
              'v': '⚫⚫⚫➖',
              'w': '⚫➖➖',
              'x': '➖⚫⚫➖',
              'y': '➖⚫➖➖',
              'z': '➖➖⚫⚫',
              '.': '⚫➖⚫➖⚫➖',
              ',': '➖➖⚫⚫➖➖',
              '?': '⚫⚫➖➖⚫⚫',
              '\'': '⚫➖➖➖➖⚫',
              '!': '➖⚫➖⚫➖➖',
              '/': '➖⚫⚫➖⚫',
              '(': '➖⚫➖➖⚫',
              ')': '➖⚫➖➖⚫➖',
              '&': '⚫➖⚫⚫⚫',
              ':': '➖➖➖⚫⚫⚫',
              ';': '⚫➖⚫➖⚫➖',
              '=': '➖⚫⚫⚫➖',
              '+': '⚫➖⚫➖⚫',
              '-': '➖⚫⚫⚫⚫➖',
              '_': '⚫⚫➖➖⚫➖',
              '\"': '⚫➖⚫⚫➖⚫',
              '$': '⚫⚫⚫➖⚫⚫➖',
              '@': '⚫➖➖⚫➖⚫',
              '0': '➖➖➖➖➖',
              '1': '⚫➖➖➖➖',
              '2': '⚫⚫➖➖➖',
              '3': '⚫⚫⚫➖',
              '4': '⚫⚫⚫⚫➖',
              '5': '⚫⚫⚫⚫⚫',
              '6': '➖⚫⚫⚫⚫',
              '7': '➖➖⚫⚫⚫',
              '8': '➖➖➖⚫⚫',
              '9': '➖➖➖➖⚫'}


@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == "POST":
        # Get Input Text From User
        text_to_convert = request.form.get('input_text').replace("\r", "").replace("\n", " ")

        # Changing Case For Dictionary Lookup
        text = text_to_convert.lower()

        # Create Empty Translation String
        translation = ''
        morse_message_for_audio = []
        try:
            # Look up each letter in Morse Code Dictionary and add to Translation String
            for i in range(len(text)):
                letter = text[i]
                if letter == " ":
                    translation += '  /  '
                    morse_message_for_audio.append(3)
                else:
                    translation += f"[{morse_dict[letter]}]"
                    for j in range(len(morse_dict[letter])):
                        if morse_dict[letter][j] == '➖':
                            morse_message_for_audio.append(0)
                        elif morse_dict[letter][j] == '⚫':
                            morse_message_for_audio.append(1)
                        if i < (len(text) - 1) and j == (len(morse_dict[letter]) - 1) and text[i + 1] != " ":
                            morse_message_for_audio.append(2)

            wavfile = make_morse(morse_message_for_audio)

            # Return Morse Code Translation to User
            return render_template('index.html', msg=translation, text=text_to_convert, wav=wavfile)

        except KeyError:
            return render_template('index.html',
                                   msg='One or more letters are not translatable. '
                                       'Please enter A-Z, a-z, 0-9 [.,?\'!/()&:;=+-_\"$@]')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)