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
