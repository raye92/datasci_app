from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

import sys
# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([])
# works too.


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(500, 350))
        self.setMaximumSize(QSize(1000, 700))

        button = QPushButton("Press")
        self.setCentralWidget(button)


#window
app = QApplication(sys.argv)
window = MainWindow()
window.show() #show windows, hidden by default

app.exec_()
