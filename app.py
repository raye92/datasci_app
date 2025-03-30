from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout, QFileDialog
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import sys
import pandas as pd
# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([])
# works too.

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(500, 350))
        # self.setMaximumSize(QSize(1000, 700))

        #layout
        layout = QVBoxLayout()

        #get csv file path
        self.browse_button = QPushButton("Browse CSV")
        self.browse_button.clicked.connect(self.load_csv)
        layout.addWidget(self.browse_button)
        #show file path
        self.csv_path = QLabel("No file selected")
        layout.addWidget(self.csv_path)

        # self.classify_button = QPushButton("Classify")
        # self.classify_button.clicked.connect(self.classify_data)
        # layout.addWidget(self.classify_button)

        #matplotlib figure and canvas for visualization
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        #container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.csv_path.setText(file_path)
            df = pd.read_csv(file_path)
            #display on canvas
            self.plot_data(df)

    def plot_data(self, df):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.plot(df['Time (s)'], df['Linear Acceleration x (m/s^2)'], label='Accel X')
        ax.plot(df['Time (s)'], df['Linear Acceleration y (m/s^2)'], label='Accel Y')
        ax.plot(df['Time (s)'], df['Linear Acceleration z (m/s^2)'], label='Accel Z')

        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Acceleration (m/s²)")
        ax.set_title("Walking Accelerometer Data")
        ax.legend()
        ax.grid(True)


        self.canvas.draw()

#main method
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show() #show windows, hidden by default
    app.exec_()
