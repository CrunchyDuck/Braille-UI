# MIT licence and all that in licence.txt

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
#from os import system
#system("venv\\Scripts\\pyuic5.exe braillebs.ui -o ui_backend.py")  # Update UI file.
import ui_backend
import json


class BrailleConverter(ui_backend.Ui_MainWindow):
    braille_dictionary = json.load(open("dictionary.json"))

    def __init__(self, window):
        self.setupUi(window)
        self.binaryButton.clicked.connect(self.get_binary_braille)
        self.boxButton.clicked.connect(self.get_box_braille)

    def get_binary_braille(self):
        binary_string = self.textEdit.toPlainText()[:8]  # Stores a string like "11001100"
        binary_string = self.make_input_incorrect_for_mouse(binary_string)
        self.display_braille(binary_string)

    def make_input_incorrect_for_mouse(self, string):
        """he wanted to make the braille dictionary go from top to bottom, left to right
        instead of the far more logical left to right, top to bottom
        this converts to the wrong format for him."""
        new_string = ""
        for i in range(0, len(string), 2):
            new_string += string[i]
        for i in range(1, len(string), 2):
            new_string += string[i]
        return new_string

    def get_box_braille(self):
        checkboxes = [self.checkBox_1, self.checkBox_2, self.checkBox_3,self.checkBox_4,
                      self.checkBox_5, self.checkBox_6, self.checkBox_7, self.checkBox_8]
        binary_string = ""
        for checkbox in checkboxes:
            binary_string += str(int(checkbox.isChecked()))
        self.display_braille(self.make_input_incorrect_for_mouse(binary_string))

    def display_braille(self, value):
        try:
            braille_character = self.braille_dictionary[value]  # Get the braille character
        except KeyError:
            self.brailleOutput.setText(f"Unknown key: {value}")
            return
        self.brailleOutput.setText(braille_character)  # Display the character in the braille box.


def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


if __name__ == "__main__":
    #with open("dictionary.json", "w") as f:
    #    f.write(json.dumps(BrailleConverter.braille_dictionary, indent=4, sort_keys=True))

    # Don't mind this. It just makes PyQt actually display errors when it crashes instead of silently dying.
    sys._excepthook = sys.excepthook
    sys.excepthook = exception_hook

    app = QApplication([])
    window = QMainWindow()
    UI = BrailleConverter(window)

    window.show()
    try:
        app.exec()
    except Exception as e:
        raise e
