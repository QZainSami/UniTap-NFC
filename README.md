# **💳🎓 UniTap: IoT Campus Wallet & PoS Terminal**

**UniTap** is an IoT-based Point of Sale (PoS) system and digital wallet designed for university campuses. It allows students to pay for canteen meals by tapping an RFID/NFC card on an ESP32-based terminal. The terminal communicates via Wi-Fi with a Python Flask backend to verify the card, check the balance, and authorize or decline the transaction in real-time.

## **🛠️ Technologies & Tools Used**

### **💻 Software Stack**

* **Arduino IDE (C++):** Used to write, compile, and flash the hardware firmware. C++ provides the low-level control needed for hardware communication (SPI, I2C, PWM) and memory management.  
* **Visual Studio Code (VS Code):** Used as the primary code editor for developing and running the Python backend API.  
* **Python 3 & Flask:** A lightweight Python web framework used to create the REST API. It acts as the "Bank Server," handling the mock database, processing transaction logic, and responding with JSON.  
* **JSON (JavaScript Object Notation):** The data format used for lightning-fast communication between the ESP32 hardware and the Python server.

### **📚 Key Libraries**

* 📦 **ArduinoJson**: Used on the ESP32 to serialize/deserialize JSON payloads sent to and received from the Python API.  
* 🎨 **Adafruit\_GFX & Adafruit\_SH110X**: Used to draw text, shapes, and custom UI animations on the OLED screen.  
* 📻 **MFRC522**: Handles the complex SPI communication required to read UID data from the RFID cards.  
* 🌐 **HTTPClient & WiFi**: Core ESP32 libraries used to manage the wireless network connection and execute HTTP POST/GET requests.

## **⚙️ Hardware Components: The "What" and "Why"**

**1\. 🧠 Microcontroller: ESP32-S3 Development Board**

* **Why:** The ESP32-S3 is a powerful, dual-core microcontroller with built-in Wi-Fi capabilities. Unlike basic Arduino boards, it can connect directly to the internet to make API calls, making it the perfect brain for an IoT PoS terminal.

**2\. 🏷️ RFID Module: RFID-RC522 (Red Board)**

* **Why:** Operating at 13.56MHz, this module is an industry standard for reading Mifare smart cards. It uses the high-speed **SPI protocol** to instantly read the unique identifier (UID) of a student's card the moment it is tapped.

**3\. 📺 Display: 1.3" SH1106 OLED Display**

* **Why:** OLEDs provide high contrast and do not require a backlight, making them very power-efficient and easy to read. It uses the **I2C protocol**, requiring only two data wires (SDA and SCL) to draw complex user interfaces, progress bars, and transaction results.

**4\. 🔊 Audio: Passive Buzzer**

* **Why:** A *passive* buzzer was chosen over an *active* one because it allows us to control the exact pitch/frequency using PWM (Pulse Width Modulation). This means we can create a high-pitched "Happy Beep" for a successful payment and a low-pitched "Angry Beep" for a declined card.

## **🔌 Wiring & Connections Guide**

The hardware is connected using standard Female-to-Female jumper wires. The system utilizes three different hardware protocols: **I2C** (for the screen), **SPI** (for the RFID), and **PWM** (for the buzzer).

### **📺 1\. OLED Display (I2C Protocol)**

| OLED Pin | ESP32-S3 Pin | Purpose |
| :---- | :---- | :---- |
| **VCC** | 3.3V | Power |
| **GND** | GND | Ground |
| **SDA** | Pin 21 | I2C Data Line |
| **SCL** | Pin 47 | I2C Clock Line |

### **📻 2\. RFID-RC522 Module (SPI Protocol)**

⚠️ **CRITICAL WARNING:** The RC522 *must* be powered by 3.3V. Connecting it to 5V will instantly damage the module\!

| RC522 Pin | ESP32-S3 Pin | Purpose |
| :---- | :---- | :---- |
| **VCC** | 3.3V | Power |
| **RST** | Pin 9 | Reset Pin |
| **GND** | GND | Ground |
| **MISO / MIOS** | Pin 13 | Master In Slave Out (Data to ESP) |
| **MOSI** | Pin 11 | Master Out Slave In (Data to NFC) |
| **SCK** | Pin 12 | Serial Clock |
| **NSS / SDA** | Pin 10 | Slave Select (Chip Select) |

### **🔊 3\. Passive Buzzer (PWM)**

| Buzzer Pin | ESP32-S3 Pin | Purpose |
| :---- | :---- | :---- |
| **VCC / \+** | Pin 4 | PWM Signal (Moves the speaker cone) |
| **GND / \-** | GND | Ground |

## **🚀 System Workflow (How It Works)**

1. **🔌 Boot & Handshake:** On startup, the ESP32 connects to the local Wi-Fi. It immediately sends a GET /check-status request to the Python Flask server to ensure the API is online.  
2. **⏳ Idle State:** The OLED draws an interactive "Ready to Tap" UI, and the RC522 module continuously polls for a nearby magnetic field.  
3. **💳 Card Tap (NFC Detection):** When a card is tapped, the RC522 reads its UID via SPI and passes it to the ESP32.  
4. **📡 API Request:** The ESP32 packages the UID into a JSON payload and sends an HTTP POST request to the Flask server (/payment).  
5. **🏦 Server Processing:** The Python backend receives the UID, checks the mock dictionary database for the student's name, account status (Active/Blocked), and wallet balance. It deducts the meal cost (Rs. 50\) and sends back a JSON response.  
6. **✅ Hardware Feedback:** The ESP32 parses the JSON response.  
   * *If successful:* It displays a checkmark and the remaining balance on the OLED, playing a 3000Hz success tone.  
   * *If failed:* (e.g., low balance), it inverts the screen colors, draws an 'X', and plays an 800Hz error tone.

## **💻 Software Setup Instructions**

### **🐍 Part 1: Python Backend (server.py)**

1. Ensure Python 3 is installed on your laptop.  
2. Open a terminal (or VS Code) and install Flask:  
   pip install flask

3. Run the server:  
   python server.py

4. The terminal will print your Laptop's Local IP address (e.g., 192.168.100.43). Leave this terminal open.

### **⚙️ Part 2: ESP32 Firmware (.ino file)**

1. Open the .ino file in the **Arduino IDE**.  
2. Go to **Sketch \> Include Library \> Manage Libraries** and install:  
   * Adafruit GFX Library  
   * Adafruit SH110X  
   * ArduinoJson  
   * MFRC522 (by GithubCommunity)  
3. Update the Wi-Fi and Server IP variables at the top of the C++ code:  
   const char\* ssid     \= "YOUR\_WIFI\_NAME";  
   const char\* password \= "YOUR\_WIFI\_PASSWORD";  
   String serverIp      \= "192.168.100.43"; // Replace with the IP from the Python terminal

4. Select your ESP32-S3 board, choose the correct COM port, and click **Upload**.

*🎓 Developed as a Software Engineering University Project.*
