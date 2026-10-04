import socket
import csv
import os
from datetime import datetime
import time

# --- Configuration ---
UDP_IP = "0.0.0.0"      
UDP_PORT = 5006        
DATA_DIR = "imu_data" 

COLLECTION_MINUTES = 5
COLLECTION_SECONDS = COLLECTION_MINUTES * 60
# --------------------

# Ensure the directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Prompt user for the activity name
activity = input("Enter activity label (e.g., sitting, standing, walking, brisk_walking, jogging, cycling, stair_up, stair_down, sit_stand_sit, phone_interaction, eating_with_spoon, pick_and_place): ")
filename = f"{activity}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
filepath = os.path.join(DATA_DIR, filename)

print(f"Data collection will start in 5 seconds...")
time.sleep(5)
print(f"Recording for activity '{activity}' for {COLLECTION_MINUTES} minutes.")
print(f"Saving data to: {filepath}")

# Create and open the CSV file for writing
with open(filepath, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header row matching the format sent by main.py plus activity label
    writer.writerow(["timestamp_ms", "ax", "ay", "az", "gx", "gy", "gz", "activity"])

    # Create UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((UDP_IP, UDP_PORT))
        print(f"Listening on UDP port {UDP_PORT}...")

        start_time = time.time()
        sample_count = 0

        try:
            while (time.time() - start_time) < COLLECTION_SECONDS:
                # Receive data packet (buffer size 1024 should be sufficient for the string)
                data, addr = sock.recvfrom(1024)
                
                # Decode the received bytes into a string
                decoded_data = data.decode().strip()

                # Split the string by commas to get individual values
                row_values = decoded_data.split(",")

                # Verify the number of values matches expected (7: ts, ax, ay, az, gx, gy, gz)
                if len(row_values) == 7:
                    # Convert timestamp to integer and floats for sensor values
                    try:
                        timestamp_ms = int(row_values[0])
                        ax = float(row_values[1])
                        ay = float(row_values[2])
                        az = float(row_values[3])
                        gx = float(row_values[4])
                        gy = float(row_values[5])
                        gz = float(row_values[6])
                        
                        # Append the activity label to the row
                        full_row = [timestamp_ms, ax, ay, az, gx, gy, gz, activity]
                        
                        # Write the row to the CSV file
                        writer.writerow(full_row)
                        
                        sample_count += 1
                        
                        if sample_count % 1000 == 0: 
                             print(f"Received and wrote {sample_count} samples...")
                        
                    except ValueError as e:
                        print(f"Warning: Could not convert data row to numbers: {row_values}, Error: {e}")
                        continue
                else:
                    print(f"Warning: Incorrect data format received, expected 7 values, got {len(row_values)}: {decoded_data}")
                    continue

        except KeyboardInterrupt:
            print("\nRecording stopped manually by user.")

        print(f"\nRecording finished for activity '{activity}'.")
        print(f"Total samples collected: {sample_count}")
        print(f"Data saved to: {filepath}")

print("Script finished.")