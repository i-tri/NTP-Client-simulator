import ntplib
from time import ctime, sleep
import threading
import tkinter as tk
from tkinter import messagebox

# Global flag to stop the simulation
stop_flag = False

def ntp_client(server, client_id, requests_per_second, duration):
    global stop_flag
    try:
        ntp = ntplib.NTPClient()
        interval = 1 / requests_per_second
        total_requests = int(requests_per_second * duration)
        for _ in range(total_requests):
            if stop_flag:
                print(f"Client {client_id}: Simulation stopped.")
                break
            response = ntp.request(server, version=4)
            print(f"Client {client_id}: Time from server: {ctime(response.tx_time)}")
            sleep(interval)
    except Exception as e:
        print(f"Client {client_id}: Could not connect to NTP server. Error: {e}")

def simulate_clients(server, num_clients, requests_per_second, duration):
    global stop_flag
    stop_flag = False
    threads = []
    for i in range(num_clients):
        thread = threading.Thread(target=ntp_client, args=(server, i + 1, requests_per_second, duration))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def start_simulation():
    ntp_server = entry_server.get()
    try:
        num_clients = int(entry_clients.get())
        requests_per_second = int(entry_requests.get())
        duration = int(entry_duration.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for clients, requests per second, and duration.")
        return

    # Run the simulation in a separate thread to keep the GUI responsive
    simulation_thread = threading.Thread(target=simulate_clients, args=(ntp_server, num_clients, requests_per_second, duration))
    simulation_thread.start()

def stop_simulation():
    global stop_flag
    stop_flag = True
    print("Simulation stopping...")

# GUI Setup
root = tk.Tk()
root.title("NTP Client Simulator")

tk.Label(root, text="NTP Server IP:").grid(row=0, column=0, padx=10, pady=10)
entry_server = tk.Entry(root)
entry_server.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Number of Clients:").grid(row=1, column=0, padx=10, pady=10)
entry_clients = tk.Entry(root)
entry_clients.grid(row=1, column=1, padx=10, pady=10)

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

root.mainloop()
