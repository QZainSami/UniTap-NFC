UniTap: IoT Campus Wallet & PoS Terminal 💳🎓

UniTap is an IoT-based Point of Sale (PoS) system and digital wallet designed for university campuses. It allows students to pay for canteen meals by tapping an RFID/NFC card on an ESP32-based terminal. The terminal communicates via WiFi with a Python Flask backend to verify the card, check the balance, and authorize or decline the transaction.

✨ Features

NFC/RFID Scanning: Fast and reliable card reading using the RC522 module.

Real-Time API Communication: ESP32 communicates with a Python backend using HTTP POST/GET requests over WiFi.

Interactive UI: 1.3" OLED display shows connection status, processing animations, and transaction results (Success/Declined).

Audio Feedback: A passive buzzer provides distinct tones for successful payments and errors.

Mock Database: Python server handles user verification, balance deduction, and blocked card flagging.

🛠️ Hardware Requirements

Microcontroller: ESP32-S3 Development Board

RFID Module: RFID-RC522 (Red or Blue Board)

Display: 1.3" SH1106 OLED Display (I2C)

Audio: Passive Buzzer

Misc: Breadboard, Jumper Wires (Female-to-Female, Male-to-Female)

🔌 Wiring Guide

1. OLED Display (I2C)
| OLED Pin | ESP32-S3 Pin |
| :--- | :--- |
| VCC | 3.3V |
| GND | GND |
| SDA | Pin 21 |
| SCL | Pin 47 |

2. RFID-RC522 Module (SPI)
⚠️ CRITICAL: The RC522 must be powered by 3.3V. 5V will damage the module!
| RC522 Pin | ESP32-S3 Pin |
| :--- | :--- |
| VCC | 3.3V |
| RST | Pin 9 |
| GND | GND |
| MISO / MIOS | Pin 13 |
| MOSI | Pin 11 |
| SCK | Pin 12 |
| NSS / SDA | Pin 10 |

3. Passive Buzzer
| Buzzer Pin | ESP32-S3 Pin |
| :--- | :--- |
| VCC / + | Pin 4 (Note: Moved from Pin 12 to avoid conflict with SCK) |
| GND / - | GND |

💻 Software Setup

1. Python Backend (server.py)

Ensure you have Python installed on your laptop.

Install the Flask library:

pip install flask


Run the server:

python server.py


The terminal will print your Laptop's Local IP address (e.g., 192.168.100.43). Keep the server running.

2. ESP32 Firmware (.ino file)

Open the .ino file in the Arduino IDE.

Install the required libraries via the Library Manager:

Adafruit GFX Library

Adafruit SH110X (for the OLED)

ArduinoJson (for parsing API responses)

MFRC522 by GithubCommunity (for the RFID reader)

Update the configuration variables at the top of the code:

const char* ssid     = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
String serverIp      = "192.168.100.43"; // Replace with the IP from Python


Compile and upload the code to your ESP32-S3.

🚀 How It Works

Boot Up: The ESP32 connects to the local WiFi network.

Handshake: It sends a GET request to /check-status to ensure the Python server is online.

Idle State: The OLED displays "Ready to Tap".

Transaction: When an RFID card is tapped, the ESP32 reads the UID and sends a JSON POST request to the /payment endpoint.

Processing: The Python server checks the mock database for the UID. If the user exists and has a sufficient balance (>= Rs. 50), it deducts the amount and returns a SUCCESS JSON response.

Result: The ESP32 parses the response, updates the OLED (Success Checkmark or Error X), and plays the corresponding buzzer tone.

📡 API Endpoints

GET /check-status

Used by the ESP32 on boot to verify the server is reachable.

Response: {"status": "ONLINE", "msg": "Server Ready"}

POST /payment

Processes a transaction for a given card UID.

Payload: {"uid": "A1B2C3D4"}

Success Response (200 OK): {"status": "SUCCESS", "name": "Sami", "msg": "Paid Rs.50", "balance": 450.0}

Error Responses (403/404): {"status": "FAILED", "name": "Hamza", "msg": "Low Balance"}
{"status": "BLOCKED", "name": "User", "msg": "Card Frozen"}

Developed as a Software Engineering University Project.
