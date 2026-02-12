# Phone-Finder-Bot
The purpose of this project is to design and implement an autonomous phone finder robot that can locate a target smartphone indoors by detecting and analyzing the Wi-Fi signal strength (RSSI) of the phone’s hotspot. 
**How It Works: **
1. The phone sends the MAC address of the phone. 
2. The bot takes the MAC address as the input. 
3. The ESP32 runs in Wi-Fi sniffer mode and scans nearby packets. The ESP32 runs code that listens to all nearby Wi-Fi traffic, like a scanner. It checks every packet and looks for your phone's MAC address. 
4. If it detects the phone, it reads the RSSI (Received Signal Strength Indicator) value.  
5. The RSSI value to estimate how close the phone is. RSSI values are usually negative, the closer the device, the stronger (less negative) the signal. 
• If RSSI increases (becomes less negative): continue in the same direction 
• If RSSI decreases: turn or scan in other direction 
6. Once the phone is found it stops and alerts.
