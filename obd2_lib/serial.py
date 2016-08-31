#!/usr/bin/env python3

import os
import termios

BAUD_RATES = (
'B0', 
'B50', 
'B75', 
'B110', 
'B134', 
'B150', 
'B200', 
'B300', 
'B600', 
'B1200', 
'B1800', 
'B2400', 
'B4800', 
'B9600', 
'B19200', 
'B38400', 
'B57600', 
'B115200', 
'B230400', 
'B460800', 
'B500000', 
'B576000', 
'B921600', 
'B1000000', 
'B1152000', 
'B1500000', 
'B2000000', 
'B2500000', 
'B3000000', 
'B3500000', 
'B4000000'
)

"""
'CDSUSP', 
'CEOF', 
'CEOL', 
'CEOT', 
'CERASE', 
'CFLUSH', 
'CINTR', 
'CKILL', 
'CLNEXT', 
'CQUIT', 
'CRPRNT', 
'CSTART', 
'CSTOP', 
'CSUSP', 
'CWERASE', 

'EXTA', 
'EXTB', 
'FIOASYNC', 
'FIOCLEX', 
'FIONBIO', 
'FIONCLEX', 
'FIONREAD', 
'IOCSIZE_MASK', 
'IOCSIZE_SHIFT', 
'NCC', 
'NCCS', 
'N_MOUSE', 
'N_PPP', 
'N_SLIP', 
'N_STRIP', 
'N_TTY', 
'TCFLSH', 
'TCGETA', 
'TCGETS', 
'TCIFLUSH', 
'TCIOFF', 
'TCIOFLUSH', 
'TCION', 
'TCOFLUSH', 
'TCOOFF', 
'TCOON', 

'TCSANOW', 
'TCSADRAIN', 
'TCSAFLUSH', 

'TCSBRK', 
'TCSBRKP', 
'TCSETA', 
'TCSETAF', 
'TCSETAW', 'TCSETS', 'TCSETSF', 'TCSETSW', 'TCXONC', 'TIOCCONS', 'TIOCEXCL', 'TIOCGETD', 'TIOCGICOUNT', 'TIOCGLCKTRMIOS', 'TIOCGPGRP', 'TIOCGSERIAL', 
'TIOCGSOFTCAR', 'TIOCGWINSZ', 'TIOCINQ', 'TIOCLINUX', 'TIOCMBIC', 'TIOCMBIS', 
'TIOCMGET', 'TIOCMIWAIT', 'TIOCMSET', 'TIOCM_CAR', 'TIOCM_CD', 'TIOCM_CTS', 
'TIOCM_DSR', 'TIOCM_DTR', 'TIOCM_LE', 'TIOCM_RI', 'TIOCM_RNG', 'TIOCM_RTS', 
'TIOCM_SR', 'TIOCM_ST', 'TIOCNOTTY', 'TIOCNXCL', 'TIOCOUTQ', 'TIOCPKT', 
'TIOCPKT_DATA', 'TIOCPKT_DOSTOP', 'TIOCPKT_FLUSHREAD', 'TIOCPKT_FLUSHWRITE', 
'TIOCPKT_NOSTOP', 'TIOCPKT_START', 'TIOCPKT_STOP', 'TIOCSCTTY', 
'TIOCSERCONFIG', 'TIOCSERGETLSR', 'TIOCSERGETMULTI', 'TIOCSERGSTRUCT', 
'TIOCSERGWILD', 'TIOCSERSETMULTI', 'TIOCSERSWILD', 'TIOCSER_TEMT', 'TIOCSETD', 
'TIOCSLCKTRMIOS', 'TIOCSPGRP', 'TIOCSSERIAL', 'TIOCSSOFTCAR', 'TIOCSTI', 
'TIOCSWINSZ', 
'__loader__', '__spec__', 'error', 'tcdrain', 'tcflow', 'tcflush', 'tcgetattr', 'tcsendbreak', 'tcsetattr'
"""

def _flags2str(lookup, flags):
    options = []
    for bit_mask_name in lookup:
        try:
            bit_mask = getattr(termios, bit_mask_name)
#            print(bit_mask_name, "=", bit_mask)
            if (flags & bit_mask) == bit_mask:
                options.append(bit_mask_name)
                flags &= ~bit_mask
        except TypeError:
            mask_name, shift, enum_list = bit_mask_name
            mask = getattr(termios, mask_name)
#            print(mask_name, "=", mask)
            enum = flags & mask
            for enum_name in enum_list:
                enum_val = getattr(termios, enum_name) << shift
#                print(enum_name, "=", enum_val)
                if enum == enum_val:
                    options.append(enum_name)
                    break
            else:
                assert False
            flags &= ~mask
                

    assert flags == 0
    return ",".join(options)

def _print_iflags(iflags):
    print("iflags =",
    _flags2str((
        "IGNBRK",
        "BRKINT",
        "IGNPAR",
        "PARMRK",
        "INPCK",
        "ISTRIP",
        "INLCR",
        "IGNCR",
        "ICRNL",
        "IUCLC",
        "IXON",
        "IXANY",
        "IXOFF",
        "IMAXBEL",
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
    print("cflags =",
    _flags2str((
        ("CBAUD", 0, BAUD_RATES),
        "CBAUDEX",
        ("CSIZE", 0, ("CS5", "CS6", "CS7", "CS8")),
        "CSTOPB",
        "CREAD",
        "PARENB",
        "PARODD",
        "HUPCL",
        "CLOCAL",
#        "LOBLK",
        ("CIBAUD", 5, BAUD_RATES),
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

def _print_speed(speed):
    for item in BAUD_RATES:
        val = getattr(termios, item)
        if speed == val:
            print(speed, "=", item)
            return

class SerialIo:

    def __init__(self, dev, baud = 38400):
        self._baud = baud
        self._in_buf = b""

        try:
#           self.fd = os.open(dev, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
            self.fd = os.open(dev, os.O_RDWR | os.O_NOCTTY)
        except PermissionError as err:
            print("Permission to open {} denied".format(dev))
            raise
#       fcntl.fcntl(self.fd, fcntl.F_SETFL, 0) # Clear O_NONBLOCK

        iflag, oflag, cflag, lflag, ispeed, ospeed, cc = termios.tcgetattr(self.fd)
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
        termios.tcsetattr(self.fd, termios.TCSANOW, [iflag, oflag, cflag, lflag, ispeed, ospeed, cc])
   
    def __del__(self):
        os.close(self.fd)

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
        ranges = (0,
                 50,      75,      110,     134, 
                150,     200,      300,     600, 
               1200,    1800,     2400,    4800, 
               9600,   19200,    38400,   57600, 
             115200,  230400,   460800,  500000, 
             576000,  921600,  1000000, 1152000, 
            1500000, 2000000,  2500000, 3000000, 
            3500000, 4000000
        )
        for idx, val in enumerate(ranges):
            if val > self._baud:
                return getattr(termios, "B{}".format(ranges[idx-1]))

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

            self._in_buf += os.read(self.fd, 1000)
        return result

    def write(self, cmd):
        os.write(self.fd, cmd + b"\r")


if __name__ == "__main__":
    app = SerialIo("/dev/ttyUSB0")
    app.write(b"ATZ")
    print(app.readline())
    print(app.readline())
    print(app.readline())
