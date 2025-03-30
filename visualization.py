# visualization.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)

def plot_acceleration_on_canvas(canvas, data, title="Accelerometer Data"):
    # Clear previous plots
    canvas.ax.clear()
    # Plot the data (assuming 'data' is a DataFrame with columns 'time', 'x', 'y', and 'z')
    canvas.ax.plot(data['time'], data['x'], label='X-axis')
    canvas.ax.plot(data['time'], data['y'], label='Y-axis')
    canvas.ax.plot(data['time'], data['z'], label='Z-axis')
    canvas.ax.set_title(title)
    canvas.ax.set_xlabel("Time (s)")
    canvas.ax.set_ylabel("Acceleration")
    canvas.ax.legend()
    # Refresh the canvas
    canvas.draw()
