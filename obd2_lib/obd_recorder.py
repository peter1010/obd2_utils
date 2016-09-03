import serial

class ObdRecorder:

    def __init__(self):
        io = serial.SerialIo("/dev/ttyUSB0")
        adapter = Elm327(io)
        adapter.reset_all()
        ign_state = adapter.query_ignition_state()
        print("Ignition state =", ign_state)
        voltage = adapter.read_voltage()
        print("Voltage =", voltage)
        self.app = adapter
        self.get_mode0_pids()
        self.do_mode0_scan()
    
    def get_mode0_pids(self):
        cnt = 1
        _pids = set()
        while True:
            response_octets = self.app.request_pid(self, 1, cnt-1)
            for octet in octets:
                for bit in range(8):
                    if octet & (1 << (7-i)) != 0:
                        _pids.add(cnt)
                    cnt += 1
            if cnt-1 not in _pids:
                break
        print(_pids)
        self.pids = _pids

    def do_mode0_scan(self):
        for pid in self.pids.sorted():
            details = pids.PIDS[pid]
            response_octets = self.app.request_pid(self, 1, pid)
            details[1](response_octets)

if __name__ == "__main__":
    app = ObdRecorder()


#
