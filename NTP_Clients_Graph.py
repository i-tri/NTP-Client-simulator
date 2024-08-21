import ntplib
from time import ctime, sleep
import threading
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from collections import defaultdict
import numpy as np

# Global variables
stop_flag = False
sensor_data = defaultdict(list)
response_counts = defaultdict(int)
last_width, last_height = 0, 0  # Track last window size to minimize unnecessary redraws


def ntp_client(server, sensor_id, requests_per_second, duration):
    global stop_flag
    global sensor_data
    global response_counts
    try:
        ntp = ntplib.NTPClient()
        interval = 1 / requests_per_second
        total_requests = int(requests_per_second * duration)

        if sensor_id not in sensor_data:
            sensor_data[sensor_id] = []
            response_counts[sensor_id] = 0

        for _ in range(total_requests):
            if stop_flag:
                print(f"Sensor {sensor_id}: Simulation stopped.")
                break
            response = ntp.request(server, version=4)
            sensor_data[sensor_id].append(response.tx_time)
            response_counts[sensor_id] += 1
            print(f"Sensor {sensor_id}: Time from server: {ctime(response.tx_time)}")
            sleep(interval)
    except Exception as e:
        print(f"Sensor {sensor_id}: Could not connect to NTP server. Error: {e}")


def simulate_clients(server, num_sensors, requests_per_second, duration):
    global stop_flag
    global sensor_data
    global response_counts
    stop_flag = False
    sensor_data = defaultdict(list)
    response_counts = defaultdict(int)
    threads = []
    for i in range(1, num_sensors + 1):
        thread = threading.Thread(target=ntp_client, args=(server, i, requests_per_second, duration))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def update_graphs():
    if sensor_data:
        ax1.clear()
        ax2.clear()
        ax3.clear()

        colors = cm.get_cmap('tab10', len(sensor_data))
        for sensor_id, times in sensor_data.items():
            ax1.plot(times, marker='o', linestyle='-', color=colors(sensor_id - 1), label=f'Sensor {sensor_id}')

        ax1.set_title('NTP Response Times')
        ax1.set_xlabel('Request Number')
        ax1.set_ylabel('Response Time (Unix Timestamp)')
        #ax1.legend(loc='upper right')

        response_counts_times = [response_counts[i] for i in range(1, len(sensor_data) + 1)]
        ax2.bar(range(1, len(sensor_data) + 1), response_counts_times, color='c')

        ax2.set_title('Number of Responses per Sensor')
        ax2.set_xlabel('Sensors')
        ax2.set_ylabel('Number of Responses')
        ax2.set_xticks([])  # Remove individual labels

        avg_response_times = [np.mean(sensor_data[i]) if len(sensor_data[i]) > 0 else 0 for i in range(1, len(sensor_data) + 1)]
        ax3.bar(range(1, len(sensor_data) + 1), avg_response_times, color='m')

        ax3.set_title('Average Response Time per Sensor')
        ax3.set_xlabel('Sensors')
        ax3.set_ylabel('Average Response Time (Unix Timestamp)')
        ax3.set_xticks([])  # Remove individual labels

        canvas.draw()

    if not stop_flag:
        root.after(100, update_graphs)


def start_simulation():
    ntp_server = entry_server.get()
    try:
        num_sensors = int(entry_sensors.get())
        requests_per_second = int(entry_requests.get())
        duration = int(entry_duration.get())
    except ValueError:
        messagebox.showerror("Input Error",
                             "Please enter valid numbers for sensors, requests per second, and duration.")
        return

    simulation_thread = threading.Thread(target=simulate_clients,
                                         args=(ntp_server, num_sensors, requests_per_second, duration))
    simulation_thread.start()
    update_graphs()


def stop_simulation():
    global stop_flag
    stop_flag = True
    print("Simulation stopping...")


def on_resize(event):
    global last_width, last_height

    # Only redraw if the size has changed significantly
    if abs(event.width - last_width) > 10 or abs(event.height - last_height) > 10:
        last_width, last_height = event.width, event.height
        fig.set_size_inches(event.width / 100, event.height / 100)
        canvas.draw()


# GUI Setup
root = tk.Tk()
root.title("NTP Client Simulator")

tk.Label(root, text="NTP Server IP:").grid(row=0, column=0, padx=10, pady=10)
entry_server = tk.Entry(root)
entry_server.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Number of Sensors (NTP Clients):").grid(row=1, column=0, padx=10, pady=10)
entry_sensors = tk.Entry(root)
entry_sensors.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Requests per Second:").grid(row=2, column=0, padx=10, pady=10)
entry_requests = tk.Entry(root)
entry_requests.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Simulation Time (seconds):").grid(row=3, column=0, padx=10, pady=10)
entry_duration = tk.Entry(root)
entry_duration.grid(row=3, column=1, padx=10, pady=10)

start_button = tk.Button(root, text="Start Simulation", command=start_simulation)
start_button.grid(row=4, columnspan=2, pady=10)

stop_button = tk.Button(root, text="Stop Simulation", command=stop_simulation)
stop_button.grid(row=5, columnspan=2, pady=10)

# Frame for the Matplotlib figure
frame = tk.Frame(root)
frame.grid(row=6, columnspan=2, padx=10, pady=10, sticky="nsew")

# Create matplotlib figure and axes
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 18), dpi=100)
ax1.set_title('NTP Response Times')
ax1.set_xlabel('Request Number')
ax1.set_ylabel('Response Time (Unix Timestamp)')

ax2.set_title('Number of Responses per Sensor')
ax2.set_xlabel('Sensor ID')
ax2.set_ylabel('Number of Responses')

ax3.set_title('Average Response Time per Sensor')
ax3.set_xlabel('Sensor ID')
ax3.set_ylabel('Average Response Time (Unix Timestamp)')

# Create canvas to display the figures in tkinter
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.draw()
canvas.get_tk_widget().pack(fill="both", expand=True)

# Bind resize event to on_resize function
root.bind("<Configure>", on_resize)

# Configure the grid to expand the frame with window resizing
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
