class Elm327:

    def __init__(self, inp):
        self._inp = inp
        self._echo_mode = True


    def send_cmd(self, cmd):
        """Send a command to the ELM327 device"""
        self._inp.write(cmd)
        if self._echo_mode:
            for i in range(3):
                result = self._inp.readline()
                if result.startswith(b">"):
                    result = result[1:]
                if cmd != result:
                    print(cmd, "!=", result)
                    continue
                return self._inp.readline()
            raise RuntimeError
        else:
            result = self._inp.readline()
            if result.startswith(b">"):
                result = result[1:]
        return result

    def send_set_cmd(self, cmd):
        result = self.send_cmd(cmd)
        assert result == b"OK"

    def send_get_cmd(self, cmd):
        return self.send_cmd(cmd)


    def reset_all(self):
        version = self.send_get_cmd(b"ATZ")
        self._echo_mode = True
        print(version)

    def set_echo_mode(self, mode):
        if mode:
            self.send_set_cmd(b"ATE1")
            self._echo_mode = True
        else:
            self.send_set_cmd(b"ATE0")
            self._echo_mode = False

    def query_ignition_state(self):
        result = self.send_get_cmd(b"ATIGN")
        if result == b'ON':
            return True
        elif result == b'OFF':
            return False
        else:
            print(result)
            raise RuntimeError

    def read_voltage(self):
        """Send command to read voltage on pin 2 (battery volts)"""
        result = self.send_get_cmd(b"ATRV")
        assert result[-1:] == b'V'
        return float(result[:-1])

    def set_protocol(self, num):
        """Set the protocol"""
        for i in range(5):
            result = self.send_get_cmd(b"ATDPN")
            current_proto = int(result)
            print("proto=", current_proto)
            if current_proto == num:
                break
            cmd = "ATTP{}".format(num).encode("ASCII")
            print(cmd)
            self.send_set_cmd(cmd)
        result = self.send_get_cmd(b"ATDP")
        print(result)

    def request_pid(self, mode, pid):
        """Send mode and pid command"""
        self.send_get_cmd("{:02X}{:02X}".format(mode,pid).encode("ascii"))
if __name__ == "__main__":
    import serial
    io = serial.SerialIo("/dev/ttyUSB0")
    app = Elm327(io)
    app.reset_all()
    app.query_ignition_state()
    print(app.read_voltage())
    app.set_echo_mode(False)
    print(app.read_voltage())
#    app.set_protocol(3)
