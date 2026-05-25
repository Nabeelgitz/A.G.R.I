// #include <TinyGPSPlus.h>
// #include <WiFi.h>
// #include <WebServer.h>
// #include <HTTPClient.h>

// // ======================
// // WIFI
// // ======================

// const char* ssid = "";
// const char* password = "";

// String djangoServer =
// "http://:8000/api/data/";

// // ======================
// // PINS
// // ======================

// #define MOISTURE_PIN 34
// #define PH_PIN 35
// #define TDS_PIN 32

// #define GPS_RX 16
// #define GPS_TX 17

// // ======================
// // FALLBACK LOCATION
// // BHOPAL
// // ======================

// const double FALLBACK_LAT = 23.2599;
// const double FALLBACK_LON = 77.4126;

// // ======================
// // OBJECTS
// // ======================

// WebServer server(80);

// TinyGPSPlus gps;
// HardwareSerial gpsSerial(2);

// // ======================
// // MOISTURE SENSOR
// // ======================

// int readMoisture() {

//   int rawValue =
//   analogRead(MOISTURE_PIN);

//   int moisture =
//   map(rawValue,
//       4095,
//       1500,
//       0,
//       100);

//   moisture =
//   constrain(
//     moisture,
//     0,
//     100
//   );

//   return moisture;
// }

// // ======================
// // PH SENSOR
// // ======================

// float readPH() {

//   int rawValue =
//   analogRead(PH_PIN);

//   float voltage =
//   rawValue *
//   (3.3 / 4095.0);

//   float pH =
//   7 +
//   (
//     (2.5 - voltage)
//     / 0.18
//   );

//   pH =
//   constrain(
//     pH,
//     0,
//     14
//   );

//   return pH;
// }

// // ======================
// // TDS SENSOR
// // ======================

// int readTDS() {

//   int rawValue =
//   analogRead(TDS_PIN);

//   float voltage =
//   rawValue *
//   (3.3 / 4095.0);

//   int tds =
//   (
//     133.42 *
//     voltage *
//     voltage *
//     voltage
//     -
//     255.86 *
//     voltage *
//     voltage
//     +
//     857.39 *
//     voltage
//   ) * 0.5;

//   if (tds < 0) {
//     tds = 0;
//   }

//   return tds;
// }

// // ======================
// // GPS FUNCTION
// // ======================

// bool getGPSData(
//   double &latitude,
//   double &longitude
// ) {

//   unsigned long startTime =
//   millis();

//   Serial.println(
//     "Searching GPS..."
//   );

//   while (
//     millis() - startTime
//     < 10000
//   ) {

//     while (
//       gpsSerial.available()
//     ) {

//       gps.encode(
//         gpsSerial.read()
//       );

//       if (
//         gps.location.isValid()
//       ) {

//         latitude =
//         gps.location.lat();

//         longitude =
//         gps.location.lng();

//         Serial.println(
//           "GPS FIX FOUND"
//         );

//         return true;
//       }
//     }
//   }

//   return false;
// }

// // ======================
// // SEND SENSOR DATA
// // ======================

// void sendSensorData() {

//   int moisture =
//   readMoisture();

//   float pH =
//   readPH();

//   int tds =
//   readTDS();

//   double latitude = 0;
//   double longitude = 0;

//   bool gpsStatus =
//   getGPSData(
//     latitude,
//     longitude
//   );

//   // ==================
//   // GPS FALLBACK
//   // ==================

//   if (
//     !gpsStatus ||
//     latitude == 0.0 ||
//     longitude == 0.0
//   ) {

//     Serial.println(
//       "GPS Failed!"
//     );

//     Serial.println(
//       "Using Bhopal Coordinates"
//     );

//     latitude =
//     FALLBACK_LAT;

//     longitude =
//     FALLBACK_LON;
//   }

//   // ==================
//   // CREATE JSON
//   // ==================

//   String jsonData = "{";

//   jsonData +=
//   "\"moisture\":"
//   + String(moisture)
//   + ",";

//   jsonData +=
//   "\"pH\":"
//   + String(pH, 2)
//   + ",";

//   jsonData +=
//   "\"tds\":"
//   + String(tds)
//   + ",";

//   jsonData +=
//   "\"latitude\":"
//   + String(latitude, 6)
//   + ",";

//   jsonData +=
//   "\"longitude\":"
//   + String(longitude, 6);

//   jsonData += "}";

//   Serial.println(
//     "\nCollected Data:"
//   );

//   Serial.println(
//     jsonData
//   );

//   // ==================
//   // SEND TO DJANGO
//   // ==================

//   HTTPClient http;

//   http.begin(
//     djangoServer
//   );

//   http.addHeader(
//     "Content-Type",
//     "application/json"
//   );

//   int responseCode =
//   http.POST(
//     jsonData
//   );

//   Serial.print(
//     "Response Code: "
//   );

//   Serial.println(
//     responseCode
//   );

//   http.end();
// }

// // ======================
// // HANDLE DJANGO REQUEST
// // ======================

// void handleCollect() {

//   Serial.println(
//     "\nCollection Triggered!"
//   );

//   sendSensorData();

//   server.send(
//     200,
//     "text/plain",
//     "Data Sent"
//   );
// }

// // ======================
// // SETUP
// // ======================

// void setup() {

//   Serial.begin(115200);

//   analogReadResolution(12);

//   gpsSerial.begin(
//     9600,
//     SERIAL_8N1,
//     GPS_RX,
//     GPS_TX
//   );

//   WiFi.begin(
//     ssid,
//     password
//   );

//   Serial.print(
//     "Connecting WiFi"
//   );

//   while (
//     WiFi.status()
//     != WL_CONNECTED
//   ) {

//     delay(1000);
//     Serial.print(".");
//   }

//   Serial.println(
//     "\nWiFi Connected!"
//   );

//   Serial.print(
//     "ESP32 IP: "
//   );

//   Serial.println(
//     WiFi.localIP()
//   );

//   server.on(
//     "/collect",
//     handleCollect
//   );

//   server.begin();

//   Serial.println(
//     "ESP32 Server Started"
//   );
// }

// // ======================
// // LOOP
// // ======================

// void loop() {

//   server.handleClient();
// }