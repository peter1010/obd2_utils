#!/usr/bin/env python3

import os
import termios

BAUD_RATES = (
    0,          50,         75,         110,        134, 
    150,        200,        300,        600,        1200,
    1800,       2400,       4800,       9600,       19200,
    38400,      57600,      115200,     230400,     460800,
    500000,     576000,     921600,     1000000,    1152000, 
    1500000,    2000000,    2500000,    3000000,    3500000,
    4000000
)
 

def _flags2str(lookup, flags):
    """Convert the flag bits to a printable string"""
    items = []
    for bit_mask_name in lookup:
        try:
            bit_mask = getattr(termios, bit_mask_name)
            if (flags & bit_mask) == bit_mask:
                items.append(bit_mask_name)
                flags &= ~bit_mask
        except TypeError:
            mask_name, shift, enum_list = bit_mask_name
            mask = getattr(termios, mask_name)
            enum_val = flags & mask
            for enum_name in enum_list:
                if enum_val == getattr(termios, enum_name) << shift:
                    items.append(enum_name)
                    break
            else:
                assert False
            flags &= ~mask

    assert flags == 0
    return ",".join(items)


def _print_iflags(iflags):
    print("iflags =",
    _flags2str((
        "IGNBRK", "BRKINT", "IGNPAR", "PARMRK",
        "INPCK",  "ISTRIP", "INLCR",  "IGNCR",
        "ICRNL",  "IUCLC",  "IXON",   "IXANY",
        "IXOFF",  "IMAXBEL",
#        "IUTF8"
    ), iflags))


def _print_oflags(oflags):
    print("oflags =",
    _flags2str((
        "OPOST",
        "OLCUC",
        "ONLCR",
        "OCRNL",
        "ONOCR",
        "ONLRET",
        "OFILL",
        "OFDEL",
        ("NLDLY",  0, ("NL0", "NL1")),
        ("CRDLY",  0, ("CR0", "CR1", "CR2", "CR3")),
        ("TABDLY", 0, ("TAB0", "TAB1", "TAB2", "TAB3")),
        ("BSDLY",  0, ("BS0", "BS1")),
        ("VTDLY",  0, ("VT0", "VT1")),
        ("FFDLY",  0, ("FF0", "FF1"))
    ), oflags))


def _print_cflags(cflags):
    baud_rate_strs = ["B{}".format(speed) for speed in BAUD_RATES]
    print("cflags =",
    _flags2str((
        ("CBAUD", 0, baud_rate_strs),
        "CBAUDEX",
        ("CSIZE", 0, ("CS5", "CS6", "CS7", "CS8")),
        "CSTOPB",
        "CREAD",
        "PARENB",
        "PARODD",
        "HUPCL",
        "CLOCAL",
#        "LOBLK",
        ("CIBAUD", 5, baud_rate_strs),
#        "CMSPAR",
        "CRTSCTS"
    ), cflags))

def _print_lflags(lflags):
    print("lflags =",
    _flags2str((
        "ISIG",
        "ICANON",
        "XCASE",
        "ECHO",
        "ECHOE",
        "ECHOK",
        "ECHONL",
        "ECHOCTL",
        "ECHOPRT",
        "ECHOKE",
#        "DEFECHO",
        "FLUSHO",
        "NOFLSH",
        "TOSTOP",
        "PENDIN",
        "IEXTEN"
    ), lflags))

def _print_cc(cc):
    lookup = (
        "VDISCARD",
#        "VDSUSP",
        "VEOF",
        "VEOL",
        "VEOL2",
        "VERASE",
        "VINTR",
        "VKILL",
        "VLNEXT",
        "VMIN",
        "VQUIT",
        "VREPRINT",
        "VSTART",
#        "VSTATUS",
        "VSTOP",
        "VSUSP",
        "VSWTCH",
        "VTIME",
        "VWERASE"
    )
    for item in lookup:
        val = getattr(termios, item)
        print(item, "=", cc[val])


def _print_speed(speed_enum_val):
    for speed in BAUD_RATES:
        candiate_enum_val = getattr(termios, "B{}".format(speed))
        if speed_enum_val == candiate_enum_val:
            print("BAUD_RATE =", speed )
            return

class SerialIo:

    def __init__(self, dev, baud = 38400):
        self._baud = baud
        self._in_buf = b""
        self._fd = None

        try:
#           self._fd = os.open(dev, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
            self._fd = os.open(dev, os.O_RDWR | os.O_NOCTTY)
        except PermissionError as err:
            print("Permission to open {} denied".format(dev))
            raise
#       fcntl.fcntl(self._fd, fcntl.F_SETFL, 0) # Clear O_NONBLOCK

        iflag, oflag, cflag, lflag, ispeed, ospeed, cc = termios.tcgetattr(self._fd)

        _print_iflags(iflag)
        _print_oflags(oflag)
        _print_cflags(cflag)
        _print_lflags(lflag)
        _print_speed(ispeed)
        _print_speed(ospeed)
        _print_cc(cc)

        iflag = self._update_input_mode_flags(iflag)
        oflag = self._update_output_mode_flags(oflag)
        cflag = self._update_ctrl_mode_flags(cflag)
        lflag = self._update_local_mode_flags(lflag)
        ispeed = self._update_speed(ispeed)
        ospeed = self._update_speed(ospeed)
        termios.tcsetattr(self._fd, termios.TCSANOW, [iflag, oflag, cflag, lflag, ispeed, ospeed, cc])
   
    def __del__(self):
        if self._fd is not None:
            os.close(self._fd)
            self._fd = None

    def _update_input_mode_flags(self, old_iflag):
        """Update the iflags (input flags) for the serial port
        
        Need to set the following:
            IGNBRK (Ignore break character)
        Need to clear the following
            ISTRIP (No to Strip eigth bit)
            IGNCR (No to ignore CR)
            INLCR (No to LF -> CR)
            ICRNL (No to CR -> LF)
            IXON (No XON flow control)
            IXOFF (No XOFF flow control)

            """
        clr_mask = termios.ISTRIP | termios.INLCR | termios.IGNCR | termios.ICRNL | termios.IXON | termios.IXOFF
        set_mask = termios.IGNBRK
        return (old_iflag & ~clr_mask) | set_mask


    def _update_output_mode_flags(self, old_oflag):
        """Update the oflags (output flags) for the serial port

        Need to clr the following:
            OPOST (no to impl define processing)
            ONLCR (No to map LF to CR/LF
            OCRNL (No to map CR -> LF
            ONOCR (No to CR at col 0)
            ONLRET (No to output CR)
        """
        clr_mask = termios.OPOST | termios.ONLCR | termios.OCRNL | termios.ONOCR | termios.ONOCR | termios.ONLRET
        return (old_oflag & ~clr_mask) 

    def _update_ctrl_mode_flags(self, old_cflag):
        """Update the cflags (ctrl flags) for the serial port
    
        Need to set the following:
            CLOCAL (ignore Modem control lines)
            CREAD (enable Receiver)
            CS8 (8 bit data bits)
        Need to clear the following
            CSTOPB (no to >1stop bit)
            PARENB (no to parity)
            PARODD (no to ODD parity)
            CRTSCTS (no RTS / CTS)
        """
        clr_mask = termios.CSIZE | termios.CSTOPB | termios.PARENB | termios.PARODD | termios.CRTSCTS
        set_mask = termios.CS8 | termios.CLOCAL | termios.CREAD

        return (old_cflag & ~clr_mask) | set_mask


    def _update_local_mode_flags(self, old_lflag):
        """Update the lflags (local flags) for the serial port

        Need to clear the following
            ISIG (no to generate signals)
            ICANON (no to canonical mode)
            ECHO (no to echo)
            IEXTEN (no to special input processing)
        """
        clr_mask = termios.ECHO | termios.ICANON | termios.ISIG | termios.IEXTEN
        return (old_lflag & ~clr_mask)

    def _update_speed(self, old_speed):
        """Update the speed parameter"""
        for idx, val in enumerate(BAUD_RATES):
            if val > self._baud:
                return getattr(termios, "B{}".format(BAUD_RATES[idx-1]))

    def readline(self):
        while True:
            idx = self._in_buf.find(b"\r")
            if idx == 0:
                self._in_buf = self._in_buf[1:]
                continue
            if idx > 0:
                result = self._in_buf[:idx]
                self._in_buf = self._in_buf[idx+1:]
                break

            self._in_buf += os.read(self._fd, 1000)
        return result

    def write(self, cmd):
        os.write(self._fd, cmd + b"\r")


if __name__ == "__main__":
    app = SerialIo("/dev/ttyUSB0")
    app.write(b"ATZ")
    print(app.readline())
    print(app.readline())
    print(app.readline())
