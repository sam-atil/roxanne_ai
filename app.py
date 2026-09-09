from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PySide6.QtCore import QSize, Qt

import sys

#SubClass for QMainWindow, customizes application main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Storing Instance variables


        self.setWindowTitle("Roxanne")
        self.button = QPushButton("Press me")

        #Connecting button to custom python function
        self.button.clicked.connect(self.button_clicked)

        self.setCentralWidget(self.button)


    def button_clicked(self):
        self.button.setText("You already clicked me")
        self.button.setEnabled(False)

        self.setWindowTitle("Roxanne.AI")


#Allowing Command Line Arguments
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

