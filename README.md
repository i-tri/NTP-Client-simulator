# NTP Client Simulator

This Python application simulates multiple NTP (Network Time Protocol) clients interacting with a specified NTP server. It provides a graphical user interface (GUI) to configure the simulation parameters and visualize the results in real-time.

## Features

- **Simulate Multiple Sensors:** 
  The application can simulate multiple sensors (NTP clients) sending requests to a specified NTP server.
- **Real-Time Graphing:**
  Visualize NTP response times, the number of responses per sensor, and the average response time per sensor.
- **User Configurable Parameters:**
  Easily configure:
  -NTP server IP,
  -number of sensors,
  -request rate (requests per second), and
  -simulation duration via the GUI.


## Requirements

- Python 3.x
- Required Python libraries:
  - `ntplib`
  - `tkinter`
  - `matplotlib`
  - `numpy`
  - `threading`
  - `collections`

To install the required Python libraries, run:

```bash
pip install ntplib matplotlib numpy
