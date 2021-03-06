from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from morse import make_morse

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
                    # add space to translation to be displayed
                    translation += '  /  '
                    # add word space to the array being passed into the morse_maker function
                    # (0 is dah, 1 is dit, 2 is character spacing, 3 is word spacing)
                    morse_message_for_audio.append(3)
                else:
                    # add characters to translation string
                    translation += f"[{morse_dict[letter]}]"

                    # add numbers to morse maker array
                    for j in range(len(morse_dict[letter])):
                        if morse_dict[letter][j] == '➖':
                            morse_message_for_audio.append(0)
                        elif morse_dict[letter][j] == '⚫':
                            morse_message_for_audio.append(1)
                        # stops space after last character and before spaces but adds it between individual dits and dahs
                        if i < (len(text) - 1) and j == (len(morse_dict[letter]) - 1) and text[i + 1] != " ":
                            morse_message_for_audio.append(2)

            # wavfile name passed to html audio src attribute
            wavfile = make_morse(morse_message_for_audio)

            # Return Morse Code Translation to User
            return render_template('index.html', msg=translation, text=text_to_convert, wav=wavfile)

        except KeyError:
            return render_template('index.html',
                                   err='One or more letters are not translatable. '
                                       'Please enter A-Z, a-z, 0-9 [.,?\'!/()&:;=+-_\"$@]')
        except AttributeError:
            return render_template('index.html',
                                   err='Please enter some text')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)