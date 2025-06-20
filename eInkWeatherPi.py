import os
import time
import socket
import requests
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13b_V4

API_KEY = "YOUR API KEY"

LOCATIONS = [
    {"name": "Izmir", "lat": 38.4192, "lon": 27.1287},
    {"name": "Ayrancilar", "lat": 38.2036, "lon": 27.0641},
    {"name": "Cesme", "lat": 38.3232, "lon": 26.3057},
   {"name": "Cinardibi", "lat": 38.1543, "lon": 28.1290}
]


def get_weather_and_aqi(lat, lon):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=en"
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

    weather_data = requests.get(weather_url).json()
    aqi_data = requests.get(aqi_url).json()

    desc = weather_data['weather'][0]['description'].capitalize()
    icon = weather_data['weather'][0]['icon']
    temp = round(weather_data['main']['temp'], 1)
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']
    wind_deg = weather_data['wind'].get('deg', 0)
    pollen_level = "Moderate"
    aqi_value = aqi_data['list'][0]['main']['aqi']

    aqi_text = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }.get(aqi_value, "Unknown")

    return desc, icon, temp, humidity, pressure, wind_speed, wind_deg, pollen_level, aqi_text

def deg_to_direction(deg):
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    ix = int((deg + 22.5) // 45) % 8
    return dirs[ix]

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except:
        ip = "0.0.0.0"
    return ip

def is_wifi_connected():
    try:
        output = os.popen("iwgetid").read()
        return "Connected" if output else "Not Connected"
    except:
        return "Unknown"

def draw_display(name, desc, icon, temp, humidity, pressure, wind_speed, wind_dir, pollen, aqi):
    epd = epd2in13b_V4.EPD()
    epd.init()
    epd.Clear()

    font_path_bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    font_path_regular = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

    font_loc = ImageFont.truetype(font_path_bold, 18)
    font_bold = ImageFont.truetype(font_path_bold, 12)
    font_regular = ImageFont.truetype(font_path_regular, 12)
    font_small = ImageFont.truetype(font_path_regular, 10)
    font_ip = ImageFont.truetype(font_path_regular, 8)

    blackimage = Image.new('1', (epd.height, epd.width), 255)
    redimage = Image.new('1', (epd.height, epd.width), 255)
    draw_black = ImageDraw.Draw(blackimage)
    draw_red = ImageDraw.Draw(redimage)

    now_istanbul = datetime.now(ZoneInfo("Europe/Istanbul")).strftime("%d.%m.%Y %H:%M:%S")
    now_utc = datetime.now(timezone.utc).strftime("%d.%m.%Y %H:%M:%S")
    ip = get_ip_address()
    wifi_status = is_wifi_connected()

    x = 5
    y = 0
    line_spacing = 14

    draw_black.text((x, y), name, font=font_loc, fill=0)
    y += 20

    draw_black.text((x, y), "Temp: ", font=font_bold, fill=0)
    temp_text = f"{temp}°C"
    draw_black.text((x + 65, y), temp_text, font=font_regular, fill=0)

    draw_black.text((x + 115, y), "Weather: ", font=font_bold, fill=0)
    draw_black.text((x + 180, y), desc, font=font_regular, fill=0)
    y += line_spacing

    draw_black.text((x, y), "Humidity: ", font=font_bold, fill=0)
    draw_black.text((x + 65, y), f"%{humidity}", font=font_regular, fill=0)

    humidity_text = f"%{humidity}"
    humidity_width = draw_black.textlength(humidity_text, font=font_regular)
    base_x = x + 65 + humidity_width + draw_black.textlength("  ", font=font_regular)

    draw_black.text((base_x, y), "Pressure: ", font=font_bold, fill=0)
    draw_black.text((base_x + 70, y), f"{pressure} hPa", font=font_regular, fill=0)
    y += line_spacing

    draw_red.text((x, y), "Pollen: ", font=font_bold, fill=0)
    draw_red.text((x + 60, y), pollen, font=font_regular, fill=0)

    draw_red.text((x + 120, y), "UV: ", font=font_bold, fill=0)
    draw_red.text((x + 150, y), "N/A", font=font_regular, fill=0)
    y += line_spacing

    draw_black.text((x, y), "Wind: ", font=font_bold, fill=0)
    draw_black.text((x + 45, y), f"{wind_speed} m/s {wind_dir}", font=font_regular, fill=0)
    draw_black.text((x + 135, y), "AQI: ", font=font_bold, fill=0)
    draw_black.text((x + 170, y), aqi, font=font_regular, fill=0)
    y += line_spacing

    draw_black.text((x, y), "Local Time: ", font=font_bold, fill=0)
    draw_black.text((x + 90, y), now_istanbul, font=font_small, fill=0)
    y += line_spacing - 2

    draw_black.text((x, y), "UTC Time: ", font=font_bold, fill=0)
    draw_black.text((x + 90, y), now_utc, font=font_small, fill=0)
    y += line_spacing - 2

    draw_red.text((x, y), "IP: ", font=font_bold, fill=0)
    draw_black.text((x + 30, y), ip, font=font_ip, fill=0)
    draw_red.text((x + 150, y), f"WiFi: {wifi_status}", font=font_ip, fill=0)

    blackimage = blackimage.rotate(180)
    redimage = redimage.rotate(180)
    epd.display(epd.getbuffer(blackimage), epd.getbuffer(redimage))
    epd.sleep()

if __name__ == "__main__":
    i = 0
    while True:
        try:
            loc = LOCATIONS[i % len(LOCATIONS)]
            desc, icon, temp, humidity, pressure, wind_speed, wind_deg, pollen, aqi = get_weather_and_aqi(loc["lat"], loc["lon"])
            wind_dir = deg_to_direction(wind_deg)
            draw_display(loc["name"], desc, icon, temp, humidity, pressure, wind_speed, wind_dir, pollen, aqi)
            print(f"[LOG] Displayed: {loc['name']} - {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            print("Error:", e)
        i += 1
        time.sleep(60)
