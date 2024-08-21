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

## Screenshots

### GUI Interface
<img width="959" alt="Screenshot 1" src="https://github.com/user-attachments/assets/0373673f-6584-4450-9d05-e5d5297d3b4f">

### Required Fields 
<img width="266" alt="Screenshot 2" src="https://github.com/user-attachments/assets/d488c5d3-1845-4d13-89bc-9b85318a502c">

### NTP Response Times
<img width="255" alt="Screenshot 3" src="https://github.com/user-attachments/assets/22dd6429-f579-4e11-b224-1eb95c063d17">

### Number of Responses per Sensor
<img width="250" alt="Screenshot 4" src="https://github.com/user-attachments/assets/331a1ccd-c4f6-4049-be17-ade10a6f80c6">


### Average Response Time per Sensor
<img width="260" alt="Screenshot 5" src="https://github.com/user-attachments/assets/7ab4fbbe-341b-434f-a1a4-ebab1ed46a15">


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


