import rtmidi
import statistics

out = rtmidi.MidiOut()
out.open_port(0)

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

def update_rolling_min_max(sensor_number, value, rolling_mins, rolling_maxs, recent_values, sensor_to_cc):
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

def parse_serial_data(serial_data, rolling_mins, rolling_maxs, recent_values, sensor_to_cc):
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
        update_rolling_min_max(1, pm1p0, rolling_mins, rolling_maxs, recent_values, sensor_to_cc)
        update_rolling_min_max(2, pm2p5, rolling_mins, rolling_maxs, recent_values, sensor_to_cc)
        update_rolling_min_max(3, pm4p0, rolling_mins, rolling_maxs, recent_values, sensor_to_cc)
        update_rolling_min_max(4, pm10p0, rolling_mins, rolling_maxs, recent_values, sensor_to_cc)
        update_rolling_min_max(5, humidity, rolling_mins, rolling_maxs, recent_values, sensor_to_cc)
        update_rolling_min_max(6, temperature, rolling_mins, rolling_maxs, recent_values, sensor_to_cc)
        update_rolling_min_max(7, voc_index, rolling_mins, rolling_maxs, recent_values, sensor_to_cc)
        update_rolling_min_max(8, nox_index, rolling_mins, rolling_maxs, recent_values, sensor_to_cc)

        return pm1p0, pm2p5, pm4p0, pm10p0, humidity, temperature, voc_index, nox_index
    else:
        print("Invalid data format: not enough values")
        return None
