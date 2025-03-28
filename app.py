from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout

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
        self.button_checked = True

        self.button = QPushButton("Press")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.button_clicked)
        # self.button.released.connect(self.button_released)
        # button.clicked.connect(self.button_toggled)

        widget = QLabel("Hello")
        font = widget.font()
        font.setPointSize(30)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        #layout
        layout = QVBoxLayout()
        layout.addWidget(widget)
        layout.addWidget(self.button)

        #container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def button_clicked(self):
        self.button.setText("You already clicked me.")
        self.button.setEnabled(False) # Disables button
        # Also change the window title.
        self.setWindowTitle("My Oneshot App")


    # def button_toggled(self, checked):
    #     self.checked = checked
    #     print("Checked?", self.checked)
    # def button_released(self):
    #     self.button_checked = self.button.isChecked()
    #     print("checked?", self.button_checked)

#window
app = QApplication(sys.argv)
window = MainWindow()
window.show() #show windows, hidden by default

app.exec_()
