import serial
import elm327
import pids

class ObdRecorder:

    def __init__(self):
        #io = serial.SerialIo("/dev/ttyUSB0")
        io = serial.SerialIo("/dev/pts/1")
        adapter = elm327.Elm327(io)
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
        _pids = set([0])
        while True:
            _pids.remove(cnt-1)
            response_octets = self.app.request_pid(1, cnt-1)
            for octet in response_octets:
                for bit in range(8):
                    if octet & (1 << (7-bit)) != 0:
                        _pids.add(cnt)
                    cnt += 1
            if cnt-1 not in _pids:
                break
        print(_pids)
        self.pids = _pids

    def do_mode0_scan(self):
        for pid in sorted(self.pids):
            details = pids.PIDS[pid]
            print(details[0])
            response_octets = self.app.request_pid(1, pid)
            details[1](response_octets)

if __name__ == "__main__":
    app = ObdRecorder()


#
