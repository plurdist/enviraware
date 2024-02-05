import serial
import rtmidi
import statistics


def scale_and_send(sensor_value, rolling_min, rolling_max, cc_number):
    normalised_value = normalise_value(sensor_value, rolling_min, rolling_max)
    scaled_value = int(normalised_value * 127)
    cc_msg = [0xB4, cc_number, scaled_value]
    out.send_message(cc_msg)
    print(f"Sent CC message for sensor {cc_number}: {scaled_value}")

def normalise_value(value, in_min, in_max):
    # Check for zero denominator
    if in_max == in_min:
        return 0  # or any other default value you prefer
    normalised_value = (value - in_min) / (in_max - in_min)
    # Clip the normalized value to [0, 1]
    return max(0, min(normalised_value, 1))

ser = serial.Serial('/dev/cu.wchusbserial2110', 115200)

# Initialize rolling minimum and maximum values for each sensor
rolling_mins = {1: float('inf'), 2: float('inf'), 3: float('inf'), 4: float('inf'), 5: float('inf'), 6: float('inf'), 7: float('inf'), 8: float('inf')}
rolling_maxs = {1: float('-inf'), 2: float('-inf'), 3: float('-inf'), 4: float('-inf'), 5: float('-inf'), 6: float('-inf'), 7: float('-inf'), 8: float('-inf')}

# Map sensor numbers to MIDI CC numbers
sensor_to_cc = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8}

recent_values = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}

def update_rolling_min_max(sensor_number, value):
    global rolling_mins, rolling_maxs, recent_values
    recent_values[sensor_number].append(value)
    recent_values[sensor_number] = recent_values[sensor_number][-10:]
    if len(recent_values[sensor_number]) >= 2:
        mean_value = statistics.mean(recent_values[sensor_number])
        stdev_value = statistics.stdev(recent_values[sensor_number])
        threshold = 3.0
        # Z-Score filtering for outliers
        if mean_value - threshold * stdev_value <= value <= mean_value + threshold * stdev_value:
            rolling_mins[sensor_number] = min(rolling_mins[sensor_number], value)
            rolling_maxs[sensor_number] = max(rolling_maxs[sensor_number], value)
            scale_and_send(value, rolling_mins[sensor_number], rolling_maxs[sensor_number], sensor_to_cc[sensor_number])
        else:
            print(f"Outlier detected for sensor {sensor_number}: {value}. Ignoring...")
    else:
        print(f"Not enough data points for stdev calculation for sensor {sensor_number}.")

def parse_serial_data(serial_data):
    # Split the received data by tabs
    values = serial_data.split('\t')

    # Ensure there are enough elements in the list
    if len(values) >= 8:
        # Extract specific values based on their positions
        pm1p0 = float(values[0].split(':')[1])
        pm2p5 = float(values[1].split(':')[1])
        pm4p0 = float(values[2].split(':')[1])
        pm10p0 = float(values[3].split(':')[1])
        humidity = float(values[4].split(':')[1])
        temperature = float(values[5].split(':')[1])
        voc_index = float(values[6].split(':')[1])
        nox_index = float(values[7].split(':')[1])

        # Update rolling min and max values for each sensor
        update_rolling_min_max(1, pm1p0)
        update_rolling_min_max(2, pm2p5)
        update_rolling_min_max(3, pm4p0)
        update_rolling_min_max(4, pm10p0)
        update_rolling_min_max(5, humidity)
        update_rolling_min_max(6, temperature)
        update_rolling_min_max(7, voc_index)
        update_rolling_min_max(8, nox_index)

        return pm1p0, pm2p5, pm4p0, pm10p0, humidity, temperature, voc_index, nox_index
    else:
        print("Invalid data format: not enough values")
        return None

# MIDI setup
out = rtmidi.MidiOut()
out.open_port(0)

mapping_done = False

try:
    while True:
        try:
            data = ser.readline().decode('utf-8', 'replace').strip()
        except UnicodeDecodeError as e:
            print(f"Error decoding data: {e}")
            continue
        if data:
            # Parse the received data
            parsed_data = parse_serial_data(data)

            # Check if parsing was successful before unpacking
            if parsed_data:
                pm1p0, pm2p5, pm4p0, pm10p0, humidity, temperature, voc_index, nox_index = parsed_data

                # Check if MIDI mappings are already done
                if not mapping_done:
                    # MAP MIDI CC messages for each sensor
                    input("Press Enter to continue...")
                    scale_and_send(pm1p0, rolling_mins[1], rolling_maxs[1], 1)
                    input("Press Enter to continue...")
                    scale_and_send(pm2p5, rolling_mins[2], rolling_maxs[2], 2)
                    input("Press Enter to continue...")
                    scale_and_send(pm4p0, rolling_mins[3], rolling_maxs[3], 3)
                    input("Press Enter to continue...")
                    scale_and_send(pm10p0, rolling_mins[4], rolling_maxs[4], 4)
                    input("Press Enter to continue...")
                    scale_and_send(humidity, rolling_mins[5], rolling_maxs[5], 5)
                    input("Press Enter to continue...")
                    scale_and_send(temperature, rolling_mins[6], rolling_maxs[6], 6)
                    input("Press Enter to continue...")
                    scale_and_send(voc_index, rolling_mins[7], rolling_maxs[7], 7)
                    input("Press Enter to continue...")
                    scale_and_send(nox_index, rolling_mins[8], rolling_maxs[8], 8)

                    # Set the flag to True to indicate that MIDI mappings are done
                    mapping_done = True

                # Print or use the parsed values
                print(f"PM1.0: {pm1p0}, PM2.5: {pm2p5}, PM4.0: {pm4p0}, PM10.0: {pm10p0}, Humidity: {humidity}, Temperature: {temperature}, VOC Index: {voc_index}, NOx Index: {nox_index}")

                # Send MIDI CC messages for each sensor
                scale_and_send(pm1p0, rolling_mins[1], rolling_maxs[1], 1)
                scale_and_send(pm2p5, rolling_mins[2], rolling_maxs[2], 2)
                scale_and_send(pm4p0, rolling_mins[3], rolling_maxs[3], 3)
                scale_and_send(pm10p0, rolling_mins[4], rolling_maxs[4], 4)
                scale_and_send(humidity, rolling_mins[5], rolling_maxs[5], 5)
                scale_and_send(temperature, rolling_mins[6], rolling_maxs[6], 6)
                scale_and_send(voc_index, rolling_mins[7], rolling_maxs[7], 7)
                scale_and_send(nox_index, rolling_mins[8], rolling_maxs[8], 8)
except KeyboardInterrupt:
    ser.close()
    out.close_port()
    print("\nSerial port closed.")