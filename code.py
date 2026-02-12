from machine import Pin
from time import sleep_ms, sleep
import network
import sys  # for exit

# LED 
LED = Pin(2, Pin.OUT)

# Target SSID
TARGET_SSID = b'x'   # your Wi-Fi name

#Wi-Fi setup 
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

#  Motor Pins (TB6612FNG) 
AIN1 = Pin(25, Pin.OUT)
AIN2 = Pin(33, Pin.OUT)
BIN1 = Pin(27, Pin.OUT)
BIN2 = Pin(14, Pin.OUT)
PWMA = Pin(32, Pin.OUT)
PWMB = Pin(12, Pin.OUT)
STBY = Pin(26, Pin.OUT)

# PWM / Motor enable
PWMA.on()
PWMB.on()
STBY.on()

# Motor control functions
def forward():
    AIN1.on();  AIN2.off()
    BIN1.on();  BIN2.off()

def back():
    AIN1.off(); AIN2.on()
    BIN1.off(); BIN2.on()

def right():
    AIN1.on();  AIN2.off()
    BIN1.off(); BIN2.on()

def left():
    AIN1.off(); AIN2.on()
    BIN1.on();  BIN2.off()

def stop():
    AIN1.off(); AIN2.off()
    BIN1.off(); BIN2.off()

# Get RSSI for target SSID
def get_target_rssi():
    nets = wifi.scan()
    for net in nets:
        ssid, bssid, channel, rssi, authmode, hidden = net
        if ssid == TARGET_SSID:
            return rssi
    return None

print("Scanning for Wi-Fi networks...")

RSSI = []

while True:
    rssi = get_target_rssi()

    if rssi is not None:
        LED.on()
        RSSI.append(rssi)
        print("Target found! Current RSSI:", rssi)

        # Keep last 10 RSSI readings
        if len(RSSI) > 10:
            RSSI.pop(0)

        # Compare current vs previous RSSI
        if len(RSSI) > 1:
            print("Previous RSSI:", RSSI[-2], "Current:", RSSI[-1])

        
        if RSSI[-1] >= -15:  # Very close
            stop()
            print("Very close — stopping & blinking LED")
            for _ in range(3):
                LED.off(); sleep_ms(200)
                LED.on(); sleep_ms(200)
            print("Target reached. Exiting program.")
            stop()
            LED.off()
            sys.exit()  # exit the loop and stop program completely

        elif len(RSSI) > 1 and RSSI[-1] >= RSSI[-2]:
            print("Signal improving — moving forward")
            forward()
            sleep(1)

        else:
            print("Signal weakening — moving back and turning")
            back()
            sleep(1)
            right()
            sleep(0.5)
            forward()
            sleep(1)

    else:
        print("Target not found — stopping motors and LED off")
        stop()
        LED.off()
        sleep(3)

