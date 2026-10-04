import network
import socket
import time
from machine import Pin, SPI, LED
from lsm6dsox import LSM6DSOX

# --- Configuration ---
# Wi-Fi credentials and the PC's address live in wifi_secrets.py (gitignored);
# see wifi_secrets_example.py
from wifi_secrets import SSID, KEY, PC_IP
PORT = 5006
SAMPLE_RATE_HZ = 60
INTERVAL_US = int(1_000_000 / SAMPLE_RATE_HZ)
# ---------------------

# --- Initialize LEDs ---
red_led = LED("LED_RED")
green_led = LED("LED_GREEN")

# --- Initialize SPI and IMU ---
spi = SPI(5)
cs = Pin("PF6", Pin.OUT_PP, Pin.PULL_UP)
imu = LSM6DSOX(spi, cs)
print("LSM6DSOX IMU initialized successfully.")

# --- Setup WiFi connection ---
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, KEY)

# Wait for connection with timeout and LED feedback
timeout = 10
while not wifi.isconnected() and timeout > 0:
    print('Trying to connect to "{:s}"...'.format(SSID))
    time.sleep_ms(1000)
    timeout -= 1
    red_led.toggle()
    time.sleep_ms(100)
    red_led.toggle()

if not wifi.isconnected():
    print('Failed to connect to Wi-Fi after timeout.')
    red_led.on()
    green_led.off()
    while True:
        time.sleep_ms(1000)
else:
    # We should have a valid IP now via DHCP
    print("WiFi Connected ", wifi.ifconfig())
    green_led.on()
    red_led.off()
    time.sleep(1)

# Create UDP socket for sending data
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Print header for the data stream
print("Now collecting the IMU data at ~{} Hz".format(SAMPLE_RATE_HZ))
print("Timestamp_ms,Ax,Ay,Az,Gx,Gy,Gz") # Header for readability

# Main data collection loop
start_time_us = time.ticks_us()
sample_count = 0

try:
    while True:
        loop_start_us = time.ticks_us()

        # Read raw IMU data (Accelerometer & Gyroscope)
        ax, ay, az = imu.accel()
        gx, gy, gz = imu.gyro()

        # Get timestamp (milliseconds since boot)
        ts_ms = time.ticks_ms()

        # Format data for transmission
        data_string = "{:d}, {:f}, {:f}, {:f}, {:f}, {:f}, {:f}".format(
            ts_ms, ax, ay, az, gx, gy, gz
        )

        # Print the data to the console
        print(data_string)

        # Send data packet(as string) to PC
        sock.sendto(data_string.encode(), (PC_IP, PORT))

        sample_count += 1

        # Maintain sampling rate using ticks_us for microsecond precision
        loop_end_us = time.ticks_us()
        elapsed_us = time.ticks_diff(loop_end_us, loop_start_us)
        sleep_us = INTERVAL_US - elapsed_us

        # Only sleep if there's remaining time in the interval
        if sleep_us > 0:
            time.sleep_us(sleep_us)

except KeyboardInterrupt:
    print("\nData collection stopped by user.")
    print(f"Total samples sent: {sample_count}")

finally:
    sock.close()
    print("Socket closed.")
    red_led.off()
    green_led.off() # Turn off LED when stopping
