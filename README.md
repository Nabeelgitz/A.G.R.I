# 🌱 Agricultural AI System

An AI-powered Smart Agricultural Soil Analysis and Crop Recommendation System using ESP32, IoT Sensors, Django, and Artificial Intelligence.

This project collects real-time soil data using sensors, combines it with climate intelligence and location analysis, predicts soil nutrient behavior, and generates a professional agricultural advisory report with crop recommendations, irrigation guidance, fertilizer suggestions, and risk analysis.

---

# 🚀 Features

- Real-time soil data collection using ESP32
- Soil Moisture Analysis
- Soil pH Detection
- TDS / Conductivity Measurement
- GPS-based Location Detection
- Climate Zone Identification
- NPK Prediction
- AI-based Agricultural Intelligence Report
- Crop Recommendation System
- Fertilizer Recommendation
- Irrigation Strategy
- Pest Risk Detection
- PDF Report Generation
- GPS Fallback System
- Web Dashboard (Django)

---

# 🧠 Project Overview

The system combines:

- IoT
- Artificial Intelligence
- Embedded Systems
- Climate Intelligence
- Precision Agriculture
- Web Technologies

to create an intelligent agricultural decision-support platform.

The goal is to help farmers understand soil conditions and make better agricultural decisions without depending on expensive laboratory soil testing.

---

# ⚙️ System Architecture

```text
                USER INPUT
                      │
                      ▼
         Manual Soil Information
        (Color, Texture, Depth)
                      │
                      ▼
                Django Server
                      │
                      ▼
             Trigger ESP32 API
                      │
                      ▼
              ESP32 + Sensors
     ┌──────────┬──────────┬──────────┐
     │ Moisture │   pH     │   TDS    │
     └──────────┴──────────┴──────────┘
                      │
                      ▼
                 GPS Module
                      │
                      ▼
          Sensor Data Collection
                      │
                      ▼
           JSON Sent to Django
                      │
                      ▼
           Climate Intelligence
                      │
                      ▼
              NPK Prediction
                      │
                      ▼
           AI Agricultural Analysis
                      │
                      ▼
            Professional PDF Report
```

---

# 🔌 Hardware Components

| Component | Purpose |
|-----------|---------|
| ESP32 | Main Microcontroller |
| Soil Moisture Sensor | Soil water measurement |
| pH Sensor | Soil acidity/alkalinity |
| TDS Sensor | Dissolved minerals detection |
| GPS NEO-6M | Location tracking |
| Jumper Wires | Connections |
| Breadboard | Prototyping |

---

# 🔧 ESP32 Pin Configuration

| GPIO Pin | Device |
|----------|--------|
| GPIO34 | Soil Moisture Sensor |
| GPIO35 | pH Sensor |
| GPIO32 | TDS Sensor |
| GPIO16 | GPS TX |
| GPIO17 | GPS RX |

Important:

GPIO34 and GPIO35 are input-only pins on ESP32 and are ideal for analog sensors.

---

# 🛰 Sensor Connections

## Soil Moisture Sensor

| Sensor | ESP32 |
|--------|-------|
| VCC | 3.3V |
| GND | GND |
| AO | GPIO34 |

---

## pH Sensor

| Sensor | ESP32 |
|--------|-------|
| V+ | 3.3V / 5V |
| G | GND |
| PO | GPIO35 |

---

## TDS Sensor

| Sensor | ESP32 |
|--------|-------|
| + | 3.3V |
| - | GND |
| A | GPIO32 |

---

## GPS Module (NEO-6M)

| GPS Module | ESP32 |
|------------|-------|
| VCC | 3.3V / 5V |
| GND | GND |
| TX | GPIO16 |
| RX | GPIO17 |

---

# 💻 Tech Stack

Frontend:
- HTML
- CSS
- JavaScript

Backend:
- Python
- Django

Embedded:
- ESP32
- Arduino Framework

Libraries:
- TinyGPS++
- WiFi.h
- HTTPClient.h
- WebServer.h
- ReportLab
- Requests

AI/ML:
- Custom Agricultural Analysis Engine
- NPK Prediction Logic

---

# 📂 Project Workflow

1. User enters:
   - Soil Color
   - Soil Texture
   - Soil Depth

2. Django triggers ESP32.

3. ESP32 collects:
   - Moisture
   - pH
   - TDS
   - GPS coordinates

4. Sensor data is sent to Django API.

5. Climate intelligence module calculates:
   - Location
   - Climate zone
   - Rainfall
   - Temperature range
   - Seasonal pattern

6. NPK values are predicted.

7. AI generates agricultural analysis.

8. User downloads professional PDF report.

---

# 📡 Example Sensor Data

```json
{
  "moisture": 68,
  "pH": 6.5,
  "tds": 430,
  "latitude": 23.2599,
  "longitude": 77.4126
}
```

---

# 📄 Generated Report Includes

- Soil Classification
- Fertility Analysis
- Nutrient Deficiency Detection
- Water Retention Analysis
- Kharif Crop Recommendation
- Rabi Crop Recommendation
- Zaid Crop Recommendation
- Unsuitable Crops
- Organic Fertilizer Guidance
- Chemical Fertilizer Recommendation
- Irrigation Strategy
- Pest Risk Detection
- Pest Prevention Methods
- Long-Term Soil Improvement

---

# 🌍 GPS Fallback System

If GPS fails or signal is unavailable:

Default fallback location is automatically used.

```text
Bhopal, Madhya Pradesh
Latitude: 23.2599
Longitude: 77.4126
```

This ensures climate intelligence always works.

---

# 🛠 Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/agricultural-ai-system.git
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Run Django Server

```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 4. Upload ESP32 Code

Open Arduino IDE:

- Select ESP32 Board
- Select COM Port
- Upload code

Update IP addresses if needed.

---

# 🌐 Network Configuration

Update Django Server IP inside ESP32:

```cpp
String djangoServer =
"http://YOUR_LOCAL_IP:8000/api/data/";
```

Update ESP32 IP inside Django:

```python
esp32_url =
"http://ESP32_IP/collect"
```

---

# ⚠️ Known Limitations

- Requires WiFi connection
- Sensor calibration needed
- GPS may fail indoors
- NPK prediction is estimated
- Not a replacement for certified soil labs

---

# 🔮 Future Improvements

- Cloud Deployment
- Database History
- Farmer Dashboard
- Mobile App
- Multi-language Support
- Live Weather API
- Disease Detection using Camera
- Fertilizer Optimization AI
- SMS Alerts

---

# 👨‍💻 Author

Nabeel

Major Project — AI + IoT Based Smart Agriculture System

---

# 📜 License

This project is developed for educational and research purposes.
