from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

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
              '9': '➖➖➖➖⚫',
              ' ': '  /  '}


@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == "POST":
        # Get Input Text From User
        # text_to_convert = input("Please Enter The Text You Wish To Convert: ")
        text_to_convert = request.form.get('input_text')

        # Validate Input
        # Changing Case For Dictionary Lookup
        text = text_to_convert.lower()

        # Create Empty Translation String
        translation = ''

        try:
            # Look up each letter in Morse Code Dictionary and add to Translation String
            for letter in text:
                translation += f"{morse_dict[letter]}  "

            # Return Morse Code Translation to User
            return render_template('index.html', msg=translation, text=text_to_convert)
            # print(translation)

        except KeyError:
            return render_template('index.html',
                                   msg='One or more letters are not translatable. '
                                       'Please enter A-Z, a-z, 0-9 [.,?\'!/()&:;=+-_\"$@]')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)