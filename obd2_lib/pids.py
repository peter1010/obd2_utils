def get_bit(byte, pos):
    if byte & (1 << pos) != 0:
        return True
    return False

def extract_dtc_status(octets):
    A, B, C, D = octets
    mil = get_bit(A, 7)
    dtc_cnt = A & 0x7F
    status = []
    if get_bit(B, 0):
        if get_bit(B, 4):
            status.append("Misfire Test complete")
        else:
            status.append("Misfire Test incomplete")

    if get_bit(B, 1):
        if get_bit(B, 5):
            status.append("Fuel System Test complete")
        else:
            status.append("Fuel System Test incomplete")

    if get_bit(B, 2):
        if get_bit(B, 6):
            status.append("Components Test complete")
        else:
            status.append("Components Test incomplete")

    is_diesel = get_bit(B, 3)
    if get_bit(C, 0):
        if get_bit(D, 0):
            status.append("Catalyst Test complete")
        else:
            status.append("Catalyst Test incomplete")

    if get_bit(C, 1):
        if is_diesel:
            if get_bit(D, 1):
                status.append("NOx Monitor Test complete")
            else:
                status.append("NOx Monitor Test incomplete")
        else:
            if get_bit(D, 1):
                status.append("Heated CAT Test complete")
            else:
                status.append("Heated CAT Test incomplete")

    if get_bit(C, 2) and not is_diesel:
        if get_bit(D, 2):
            status.append("Evaporative System Test complete")
        else:
            status.append("Evaporative System Test incomplete")

    if get_bit(C, 3):
        if is_diesel:
            if get_bit(D, 3):
                status.append("Boost pressure Test complete")
            else:
                status.append("Boost pressure Test incomplete")
        else:
            if get_bit(D, 3):
                status.append("Secondary air Test complete")
            else:
                status.append("Secondary air Test incomplete")

    if get_bit(C, 4) and not is_diesel:
        if get_bit(D, 4):
            status.append("A/C Refrigerant Test complete")
        else:
            status.append("A/C Refrigerant Test incomplete")

    if get_bit(C, 5):
        if is_diesel:
            if get_bit(D, 5):
                status.append("Exhaust Gas sensor Test complete")
            else:
                status.append("Exhaust Gas sensor Test incomplete")
        else:
            if get_bit(D, 5):
                status.append("Oxygen sensor Test complete")
            else:
                status.append("Oxygen sensor Test incomplete")

    if get_bit(C, 6):
        if is_diesel:
            if get_bit(D, 6):
                status.append("PM filter mon Test complete")
            else:
                status.append("PM filter mon Test incomplete")
        else:
            if get_bit(D, 6):
                status.append("Oxygen Sensor heater Test complete")
            else:
                status.append("Oxygen Sensor heater Test incomplete")

    if get_bit(C, 7):
        if get_bit(D, 7):
            status.append("EGR System Test complete")
        else:
            status.append("EGR System Test incomplete")
    print("MIL =", mil)
    print("DTC CNT =", dtc_cnt)
    print("TEST STATUS=", ",".join(status))


FUEL_SYSTEM_STATUS = {
    1: "Open loop due to insufficient engine temperature",
    2: "Closed lopp, using oxygen sensor to determine fuel mix",
    4: "Open loop due engine load or fuel cut due to deceleration",
    8: "Open loop due to system failure",
    16: "Open loop due to fault in feedback loop"
}

def extract_fuel_system_status(octets):
    for octet in octets:
        try:
            status  = FUEL_SYSTEM_STATUS[octet]
        except KeyError:
            status = "Invalid fuel system status"

        print("FUEL SYSTEM STATUS=", ",".join(status))
        
def extract_percentage(octets):
    percent = (100 * octets[0]) / 255
    print("{}%",format(percent))

def extract_temperature(octets):
    temp = octets[0] - 40
    print("{} ^C".format(temp))

def extract_trim(octets):
    """-100 = Too rich, +99.2 = Too Lean"""
    trim = (100 * octets[0])/128 - 100
    print("trim {}%".format(trim))

def extract_fuel_pressure(octets):
    pressure = 3 * octets[0]
    print("{} KPa".format(pressure))

def extract_manifold_pressure(octets):
    pressure = octets[0]
    print("{} KPa".format(pressure))

def extract_rpm(octets):
    rpm = (256 * octets[0] + octets[1])/4
    print("{} rpm".format(rpm))

def extract_speed(octets):
    speed = octets[0]
    print ("{} km/h".format(speed))

def extract_advance(octets):
    advance = octets[0]/2.0 - 64
    print("{} ^TDC".format(advance))

def extract_flow(octets):
    flow = (octets[0] * 256 + octets[1])/100.0
    print("{} grams/sec".format(flow))

    
AIR_STATUS = {
    1: "Upstream",
    2: "Downstream of catalytic convertor",
    4: "From the outside atmosphere or off",
    8: "Pump commanded on for diagnostics"
}
 
def extract_air_status(octets):
    A = octets[0]
    try:
        status = AIR_STATUS[A]
    except KeyError:
        status = "Invalid status ({})".format(A)
    print("AIR STATUS={}".format(status))


def extract_oxygen_sensors_present(octets):
    A = octets[0]
    sensors = []
    if get_bit(A, 0):
        sensors.append("1-1")
    if get_bit(A, 1):
        sensors.append("1-2")
    if get_bit(A, 2):
        sensors.append("1-3")
    if get_bit(A, 3):
        sensors.append("1-4")
    if get_bit(A, 4):
        sensors.append("2-1")
    if get_bit(A, 5):
        sensors.append("2-2")
    if get_bit(A, 6):
        sensors.append("2-3")
    if get_bit(A, 7):
        sensors.append("2-4")
    print("O2 SENSORS = {}".format(",".join(sensors)))


def extract_oxygen_sensors_present2(octets):
    A = octets[0]
    sensors = []
    if get_bit(A, 0):
        sensors.append("1-1")
    if get_bit(A, 1):
        sensors.append("1-2")
    if get_bit(A, 2):
        sensors.append("2-1")
    if get_bit(A, 3):
        sensors.append("2-2")
    if get_bit(A, 4):
        sensors.append("3-1")
    if get_bit(A, 5):
        sensors.append("3-2")
    if get_bit(A, 6):
        sensors.append("4-1")
    if get_bit(A, 7):
        sensors.append("4-2")
    print("O2 SENSORS = {}".format(",".join(sensors)))


def extract_oxygen_sensor(octets):
    A, B = octets[:2]
    volts = A / 200.0
    if B == 0xff:
        trim = "N/A"
    else:
        trim = (100 * B)/128 - 100
    print("{} volts -- {}%".format(volts, trim))


OBD_STANDARDS = {
    1: "OBD-II as defined by the CARB",
    2: "OBD as defined by the EPA",
    3: "OBD and OBD-II",
    4: "OBD-I",
    5: "Not OBD Compliant",
    6: "EOBD (Europe)",
    7: "EOBD and OBD-II",
    8: "EOBD and OBD",
    9: "EOBD, OBD and OBD-II",
    10: "JOBD  (Japan)",
    11: "JOBD and OBD-II",
    12: "JOBD and EOBD",
    13: "JOBD, EOBD and OBD-II",
    17: "Engine Manufacturer Diagnostics (EMD)",
    18: "Engine Manufacturer Diagnostics Enhanced (EMD+)",
    19: "Heavy Duty On-Board Diagnostics (Child/Partial) (HD OBD-C)",
    20: "Heavy Duty On-Board Diagnostics (HD OBD)",
    21: "World Wide Harmonized OBD (WWH OBD)",
    23: "Heavy Duty Euro OBD Stage 1 without NOx (H EOBD-I)",
    24: "Heavy Duty Euro OBD Stage I with NOx control (HD EOBD-I N)",
    25: "Heavy Duty Euro OBD Stage II without NOx control (HD EOBD-II)",
    26: "Heavy Duty Euro OBD Stage II with NOx control (HD EOBD-II N)",
    28: "Brazil OBD Phase 1 (OBDBr-1)",
    29: "Brazil OBD Phase 2 (OBDBr-2)",
    30: "Korean OBD (KOBD)",
    31: "India OBD I (IOBD I)",
    32: "India OBD II (IOBD II)",
    33: "Heavy Duty Euro OBD Stage VI (HD EOBD-IV)"
}

def extract_obd_standard(octets):
    A = octets[0]
    try:
        standard = OBD_STANDARDS[A]
    except KeyError:
        standard = "Invalid standard ({})".format(A)
    print(standard)

def extract_pto(octets):
    if get_bit(octets[0], 0):
        status = "Power Take off active"
    else:
        status = "N/A"
    print(status)

def extract_runtime(octets):
    A, B = octets[:2]
    time = 256* A + B
    print("{} secs".format(time))

def extract_distance(octets):
    A, B = octets[:2]
    distance = 256* A + B
    print("{} km".format(distance))


PIDS  = {
    1: ("DTC Status", extract_dtc_status),
    2: ("Freeze DTC", None),
    3: ("Fuel System Status", extract_fuel_system_status),
    4: ("Calculated engine load", extract_percentage),
    5: ("Engine Coolant temperaure", extract_temperature),
    6: ("Short term fuel trim - Bank 1", extract_trim),
    7: ("Long term fuel trim - Bank 1", extract_trim),
    8: ("Short term fuel trim - Bank 2", extract_trim),
    9: ("Long term fuel trim - Bank 2", extract_trim),
    10: ("Fuel pressure", extract_fuel_pressure),
    11: ("Intake Manifold pressure", extract_manifold_pressure),
    12: ("Engine RPM", extract_rpm),
    13: ("Vehicle speed", extract_speed),
    14: ("Timing Advance", extract_advance),
    15: ("Intake air temperature", extract_temperature),
    16: ("MAF air flow rate", extract_flow),
    17: ("Throttle position", extract_percentage),
    18: ("Commanded Secondary Air Status", extract_air_status),
    19: ("Oxygen Sensors present", extract_oxygen_sensors_present),
    20: ("Oxygen Sensor 1", extract_oxygen_sensor),
    21: ("Oxygen Sensor 2", extract_oxygen_sensor),
    22: ("Oxygen Sensor 3", extract_oxygen_sensor),
    23: ("Oxygen Sensor 4", extract_oxygen_sensor),
    24: ("Oxygen Sensor 5", extract_oxygen_sensor),
    25: ("Oxygen Sensor 6", extract_oxygen_sensor),
    26: ("Oxygen Sensor 7", extract_oxygen_sensor),
    27: ("Oxygen Sensor 8", extract_oxygen_sensor),
    28: ("OBD Standard", extract_obd_standard),
    29: ("Oxygen Sensors present", extract_oxygen_sensors_present2),
    30: ("Auxiliary input status", extract_pto),
    31: ("Run time since engine start", extract_runtime),
    33: ("Distance traveled since MIL", extract_distance),
}
