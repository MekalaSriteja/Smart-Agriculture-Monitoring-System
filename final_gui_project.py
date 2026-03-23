import tkinter as tk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import datetime
import requests

# Data
soil_data = []
temp_data = []
hum_data = []

# Graph
def update_graph():
    ax.clear()
    ax.plot(soil_data, label="Soil")
    ax.plot(temp_data, label="Temp")
    ax.plot(hum_data, label="Humidity")
    ax.legend()
    canvas.draw()

# Update function
def update_data():
    soil = random.randint(10, 100)
    temp = random.randint(20, 40)
    hum = random.randint(30, 90)

    soil_data.append(soil)
    temp_data.append(temp)
    hum_data.append(hum)

    # ✅ CLOUD (ThingSpeak)
    url = "https://api.thingspeak.com/update"
    api_key = "D7MRC3CXCBMERQO2"   # keep in quotes

    requests.get(url, params={
        "api_key": api_key,
        "field1": soil,
        "field2": temp,
        "field3": hum
    })

    # ✅ DATA LOGGING
    with open("data_log.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([soil, temp, hum])

    # Limit data points
    if len(soil_data) > 10:
        soil_data.pop(0)
        temp_data.pop(0)
        hum_data.pop(0)

    # Update labels
    soil_label.config(text=f"Soil Moisture: {soil}")
    temp_label.config(text=f"Temperature: {temp}")
    hum_label.config(text=f"Humidity: {hum}")

    # Motor logic
    if soil < 30 and temp > 25:
        motor_label.config(text="Motor ON 🌱", bg="#4CAF50")
    else:
        motor_label.config(text="Motor OFF", bg="#f44336")

    # Alert
    if soil < 20:
        alert_label.config(text="⚠️ ALERT: Soil too dry!", fg="red")
    else:
        alert_label.config(text="System Normal", fg="green")

    # Time
    now = datetime.datetime.now().strftime("%H:%M:%S")
    time_label.config(text=f"Time: {now}")

    # Suggestion
    if soil < 30 and temp > 30:
        suggestion = "Irrigation needed immediately"
    elif soil < 30:
        suggestion = "Water the crops soon"
    elif hum < 40:
        suggestion = "Low humidity - consider irrigation"
    else:
        suggestion = "Conditions are optimal"

    suggestion_label.config(text=f"Suggestion: {suggestion}")

    # Update graph
    update_graph()

    root.after(15000, update_data)

# Window
root = tk.Tk()
root.title("Smart Agriculture Monitoring System")
root.geometry("800x550")
root.configure(bg="#e8f5e9")

# Title
title = tk.Label(root, text="🌱 Smart Agriculture Dashboard",
                 font=("Arial", 18, "bold"), bg="#2e7d32", fg="white")
title.pack(fill="x", pady=10)

# Frame
frame = tk.Frame(root, bg="#e8f5e9")
frame.pack(pady=10)

soil_label = tk.Label(frame, text="Soil Moisture:", font=("Arial", 14), bg="#e8f5e9")
soil_label.grid(row=0, column=0, padx=20, pady=5)

temp_label = tk.Label(frame, text="Temperature:", font=("Arial", 14), bg="#e8f5e9")
temp_label.grid(row=1, column=0, padx=20, pady=5)

hum_label = tk.Label(frame, text="Humidity:", font=("Arial", 14), bg="#e8f5e9")
hum_label.grid(row=2, column=0, padx=20, pady=5)

# Motor
motor_label = tk.Label(root, text="Motor Status", font=("Arial", 16, "bold"),
                       width=20, bg="gray", fg="white")
motor_label.pack(pady=10)

# Alert + Time + Suggestion
alert_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
alert_label.pack()

time_label = tk.Label(root, text="", font=("Arial", 12))
time_label.pack()

suggestion_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
suggestion_label.pack(pady=5)

# Graph
fig, ax = plt.subplots(figsize=(5,3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

# Start
update_data()
root.mainloop()
