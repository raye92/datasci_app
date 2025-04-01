# visualization.py
import matplotlib.pyplot as plt

def plot_comparison(raw_df, processed_df, column=None, time=None):
    if column is None:
        print("no column specified for plotting")
        return

    plt.figure(figsize=(12, 6))

    # filter by time if given
    if time is not None:
        raw_df = raw_df[raw_df.index <= time]
        processed_df = processed_df[processed_df.index <= time]

    # plot raw data
    for activity in [0, 1]:
        data = raw_df[raw_df["activity"] == activity]
        plt.plot(data.index, data[column], label=f'raw activity {activity}', alpha=0.6)

    # plot processed data
    for activity in [0, 1]:
        data = processed_df[processed_df["activity"] == activity]
        plt.plot(data.index, data[column], label=f'processed activity {activity}', alpha=0.8)

    plt.title(f"raw vs. processed data: {column}")
    plt.xlabel("sample index" if time is None else "time (s)")
    plt.ylabel(column)
    plt.legend()
    plt.tight_layout()
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
