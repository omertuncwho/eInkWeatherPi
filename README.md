# eInkWeatherPi

**Minimalist e-ink weather display powered by Raspberry Pi Zero 2W**

**eInkWeatherPi** is a compact, low-power, always-on weather station designed for minimalist setups and IoT enthusiasts. It utilizes a Waveshare 2.13" V4 e-Ink display to show real-time weather data, air quality, UV index, and more — all without a glowing screen.

---

## 📦 Requirements

### Hardware
- Raspberry Pi Zero 2 W  
- Waveshare 2.13" e-Paper Display HAT (V4)  
- microSD card (8GB or larger recommended)  
- USB power supply  
- WiFi connection  
- (Optional) 3D printed enclosure  

### Software
- Raspberry Pi OS Lite (32-bit)  
- Python 3  
- OpenWeatherMap API key  

---

## 🛠️ Installation

### 1. Flash Raspberry Pi OS

1. Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)  
2. Choose **Raspberry Pi OS Lite (32-bit)**  
3. Click ⚙️ (settings) to configure:
   - Enable SSH  
   - Set WiFi SSID & Password  
   - Set Locale to `Europe/Istanbul`  
4. Flash the image to a microSD card and insert it into your Raspberry Pi

---

### 2. Enable SPI Interface

Boot your Raspberry Pi and run:

```bash
sudo raspi-config
```
Navigate to:
Interface Options → SPI → Enable

Then reboot your Pi.

---

### 3. Connect the e-Ink Display
Connect your Waveshare 2.13" V4 e-Ink display to the Raspberry Pi GPIO pins as shown below:

| e-Ink Pin | GPIO Pin | Description  |
| --------- | -------- | ------------ |
| VCC       | 3.3V     | Power        |
| GND       | GND      | Ground       |
| DIN       | GPIO 10  | MOSI         |
| CLK       | GPIO 11  | Clock (SCLK) |
| CS        | GPIO 8   | Chip Select  |
| DC        | GPIO 25  | Data/Command |
| RST       | GPIO 17  | Reset        |
| BUSY      | GPIO 24  | Busy Status  |

---

### 4. Clone the Repository
```bash
git clone https://github.com/yourusername/eInkWeatherPi.git
cd eInkWeatherPi
```

---

### 5. Install Python Dependencies
```bash
pip3 install requests pillow
```
If you're using Python < 3.9:
```bash
pip3 install backports.zoneinfo
```

---

### 6. Configure OpenWeatherMap API Key
Get your free API key from [OpenWeatherMap](https://openweathermap.org/api)

Open the script file and replace the placeholder:
```bash
API_KEY = "your_actual_api_key_here"
```

---

### 7. Run the Script
```bash
python3 eInkWeatherPi.py
```

---

### 8. (Optional) Run on Boot with crontab
To automatically run the script on every boot:
```bash
crontab -e
```
Add this line at the end of the file:
```bash
@reboot python3 /home/pi/eInkWeatherPi/eInkWeatherPi.py &
```
Then save and exit.

---

### ⚙️ Troubleshooting
SPI not enabled → Run sudo raspi-config, enable SPI, reboot

API key not working → Double-check the API key and your internet connection

WiFi not connected → Make sure WiFi credentials are correct

GPIO errors → Try rebooting the Pi to release pins

Display not updating → Check pin wiring and display model compatibility

---

### 🤝 Contributions
Feel free to fork this repo, improve it, and submit pull requests.

---

## Thanks for using eInkWeatherPi! 🌤️
