import serial
import rtmidi
import statistics
from utils.functions import scale_and_send, normalise_value, update_rolling_min_max, parse_serial_data

ser = serial.Serial('/dev/cu.wchusbserial2110', 115200)

# Initialize rolling minimum and maximum values for each sensor
rolling_mins = {1: float('inf'), 2: float('inf'), 3: float('inf'), 4: float('inf'), 5: float('inf'), 6: float('inf'), 7: float('inf'), 8: float('inf')}
rolling_maxs = {1: float('-inf'), 2: float('-inf'), 3: float('-inf'), 4: float('-inf'), 5: float('-inf'), 6: float('-inf'), 7: float('-inf'), 8: float('-inf')}

# Map sensor numbers to MIDI CC numbers
sensor_to_cc = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8}

recent_values = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}

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
            parsed_data = parse_serial_data(data, rolling_mins, rolling_maxs, recent_values, sensor_to_cc)

            # Check if parsing was successful before unpacking
            if parsed_data:
                pm1p0, pm2p5, pm4p0, pm10p0, humidity, temperature, voc_index, nox_index = parsed_data

                # Check if MIDI mappings are already done
                if not mapping_done:
                    # MAP MIDI CC messages for each sensor
                    input("Mapping MIDI CC for pm1p0. Press Enter to continue...")
                    scale_and_send(pm1p0, rolling_mins[1], rolling_maxs[1], 1)
                    input("Mapping MIDI CC for pm2p5. Press Enter to continue...")
                    scale_and_send(pm2p5, rolling_mins[2], rolling_maxs[2], 2)
                    input("Mapping MIDI CC for pm4p0. Press Enter to continue...")
                    scale_and_send(pm4p0, rolling_mins[3], rolling_maxs[3], 3)
                    input("Mapping MIDI CC for pm10p0. Press Enter to continue...")
                    scale_and_send(pm10p0, rolling_mins[4], rolling_maxs[4], 4)
                    input("Mapping MIDI CC for humidity. Press Enter to continue...")
                    scale_and_send(humidity, rolling_mins[5], rolling_maxs[5], 5)
                    input("Mapping MIDI CC for temperature. Press Enter to continue...")
                    scale_and_send(temperature, rolling_mins[6], rolling_maxs[6], 6)
                    input("Mapping MIDI CC for voc_index. Press Enter to continue...")
                    scale_and_send(voc_index, rolling_mins[7], rolling_maxs[7], 7)
                    input("Mapping MIDI CC for nox_index. Press Enter to continue...")
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

                print(rolling_maxs)
                print(rolling_mins)
                
except KeyboardInterrupt:
    ser.close()
    out.close_port()
    print("\nSerial port closed.")