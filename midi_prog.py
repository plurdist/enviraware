import time
import rtmidi

out = rtmidi.MidiOut()

out.open_port(0)

with out:
    note_on = [0x94, 48, 112]
    note_off = [0x84, 48, 0]

    # Set the filter to 0
    cc_msg = [0xB4, 3, 0]
    out.send_message(cc_msg)
    time.sleep(0.1)

    # Set note on
    out.send_message(note_on)
    time.sleep (1)

    # Start ramping filter
    for cc in range (127):
    # OxB_ is controller change
        cc_msg = [0xB4, 3, cc]
        out.send_message(cc_msg)
        time.sleep(0.1)
    out.send_message(note_off)
    time.sleep(0.1)




# notes = [60, 62, 64, 65, 67, 69, 71, 72]



# for _ in range(2):
#     for note in notes:
#         out.open_port(0)
#         with out:
#             note_on = [0x94, note, 100]
#             note_off = [0x84, note, 0]
#             out.send_message(note_on)
#             time.sleep(0.02)
#             out.send_message(note_off)
#             time.sleep(0.1)


# Making a dictionary so I can refer to the device by name

# ports_dict = {k: v for (v, k) in enumerate(out.get_ports())}
# out.open_port(ports_dict["0P-Z 1"])