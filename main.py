import serial
import time
import rtmidi

def scale_value(value, in_min, in_max, out_min, out_max):
    scaled_value = int((value - in_min) / (in_max - in_min) * (out_max - out_min) + out_min)
    # Clip the value to the valid MIDI CC range (0-127)
    return max(min(scaled_value, 127), 0)

ser = serial.Serial('/dev/cu.wchusbserial2110', 115200)

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

        # Scale the temperature value
        scaled_temperature = scale_value(temperature, 20, 40, 0, 127)

        return pm1p0, pm2p5, pm4p0, pm10p0, humidity, temperature, voc_index, nox_index, scaled_temperature
    else:
        print("Invalid data format: not enough values")
        return None

# MIDI setup
out = rtmidi.MidiOut()
out.open_port(0)

try:
    while True:
        data = ser.readline().decode('utf-8').strip()
        if data:
            # Parse the received data
            parsed_data = parse_serial_data(data)

            # Check if parsing was successful before unpacking
            if parsed_data:
                pm1p0, pm2p5, pm4p0, pm10p0, humidity, temperature, voc_index, nox_index, scaled_temperature = parsed_data

                # Print or use the parsed values
                print(f"PM1.0: {pm1p0}, PM2.5: {pm2p5}, PM4.0: {pm4p0}, PM10.0: {pm10p0}, Humidity: {humidity}, Temperature: {temperature}, VOC Index: {voc_index}, NOx Index: {nox_index}")

                # Send MIDI CC messages with scaled temperature
                cc_msg = [0xB4, 3, scaled_temperature]
                out.send_message(cc_msg)

except KeyboardInterrupt:
    ser.close()
    out.close_port()
    print("\nSerial port closed.")
