# visualization.py
import matplotlib.pyplot as plt

def plot_comparison(raw_df, processed_df, column=None):
    # choose column if not specified
    if column is None:
        numeric_cols = raw_df.select_dtypes(include=[float, int]).columns.tolist()
        if not numeric_cols:
            raise ValueError("no numeric columns available for plotting.")
        column = numeric_cols[0]

    # plot raw and filtered data
    plt.figure(figsize=(12, 6))
    plt.plot(raw_df[column], label='raw data', alpha=0.5)
    plt.plot(processed_df[column], label='filtered data', alpha=0.5)
    plt.title(f"comparison of raw and filtered data ({column})")
    plt.xlabel("sample index")
    plt.ylabel("value")
    plt.legend()
    plt.show()

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
