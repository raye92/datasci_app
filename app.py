# app.py
import sys
import pandas as pd
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Plotter")
        self.setMinimumSize(QSize(500, 350))
        layout = QVBoxLayout()

        # button to load csv file
        self.upload_button = QPushButton("Upload CSV")
        self.upload_button.clicked.connect(self.load_csv)
        layout.addWidget(self.upload_button)

        # label to display selected csv file path
        self.csv_path = QLabel("No file selected")
        layout.addWidget(self.csv_path)

        # matplotlib figure and canvas for visualization
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.csv_path.setText(file_path)

            from process_data import load_and_label
            df = load_and_label(file_path)

            # segment data
            from storage import segment_signal #jack
            segments = pd.concat(segment_signal(df))
            print("CSV loaded:\n", segments)

            # extract features from segments #vikran
            from feature_extraction import extract_features, clf, scaler, feature_cols
            features = extract_features(segments)

            # drop 'activity' if present before scaling
            if 'activity' in features.columns:
                features = features.drop(columns=['activity'])

            # scale the features using the training scaler
            features[feature_cols] = scaler.transform(features[feature_cols])

            # predict activity using the classifier
            predicted_activity = clf.predict(features[feature_cols])
            features['predicted_activity'] = predicted_activity

            # merge predictions back into segments on 'segment' key
            segments = segments.merge(features[['segment', 'predicted_activity']], on='segment', how='left')

            print("Segments with predicted activity:\n", segments)
            self.plot_data(pd.read_csv("test.csv"))

    def plot_data(self, df):
        self.figure.clear()
        ax1 = self.figure.add_subplot(311)
        ax2 = self.figure.add_subplot(312, sharex=ax1)
        ax3 = self.figure.add_subplot(313, sharex=ax1)

        x = df['segment']

        def plot_segmented_line(ax, x, y, pred):
            if len(x) == 0:
                return

            start_idx = 0
            current_pred = pred.iloc[0]
            color = 'red' if current_pred == 1 else 'blue'

            for i in range(1, len(x)):
                # if activity changes, plot segment including the transition point
                if pred.iloc[i] != current_pred:
                    ax.plot(x.iloc[start_idx:i+1], y.iloc[start_idx:i+1], color=color)
                    start_idx = i
                    current_pred = pred.iloc[i]
                    color = 'red' if current_pred == 1 else 'blue'

            # plot the final segment
            ax.plot(x.iloc[start_idx:], y.iloc[start_idx:], color=color)

        # plot accel_x_mean on ax1
        plot_segmented_line(ax1, x, df['accel_x_mean'], df['predicted_activity'])
        ax1.set_ylabel("Accel X Mean")
        ax1.set_title("Accel X Mean")

        # plot accel_z_mean on ax2
        plot_segmented_line(ax2, x, df['accel_z_mean'], df['predicted_activity'])
        ax2.set_ylabel("Accel Z Mean")
        ax2.set_title("Accel Z Mean")

        # plot abs_accel_mean on ax3
        plot_segmented_line(ax3, x, df['abs_accel_mean'], df['predicted_activity'])
        ax3.set_ylabel("Abs Accel Mean")
        ax3.set_xlabel("Segment")
        ax3.set_title("Abs Accel Mean")

        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
