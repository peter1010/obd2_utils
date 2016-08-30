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

PARITY_NONE = 0
PARITY_EVEN = 1
PARITY_ODD = 2

class SerialIo:

    def __init__(self, dev, baud = 38400, databits = 8, parity = PARITY_NONE, stopbits = 1):
        self._baud = baud
        self._data_bits = databits
        self._parity = parity
        self._stop_bits = stopbits

        self.fd = os.open(dev, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
        iflag, oflag, cflag, lflag, ispeed, ospeed, cc = termios.tcgetattr(self.fd)
        print(iflag, oflag, cflag, lflag, ispeed, ospeed, cc)
        _print_iflags(iflag)
        _print_oflags(oflag)
        _print_cflags(cflag)
        _print_lflags(lflag)
        _print_cc(cc)

        iflag = self._update_input_mode_flags(iflag)
        oflag = self._update_output_mode_flags(oflag)
        cflag = self._update_ctrl_mode_flags(cflag)
        lflag = self._update_local_mode_flags(lflag)
        termios.tcsetattr(self.fd, termios.TCSANOW, [iflag, oflag, cflag, lflag, ispeed, ospeed, cc])
        
    def _update_input_mode_flags(self, old_iflag):
        """Set IGNBRK"""
        clr_mask = termios.IGNBRK | termios.BRKINT | termios.PARMRK | termios.ISTRIP
        set_mask = termios.INLCR | termios.IGNCR | termios.ICRNL | termios.IXON
        return (old_iflag & ~clr_mask) | set_mask

    def _update_output_mode_flags(self, old_oflag):
        """"""
        clr_mask = termios.OPOST
        return (old_oflag & ~clr_mask) 

    def _update_ctrl_mode_flags(self, old_cflag):
        """"""
        enum_val = getattr(termios, "CS{}".format(self._data_bits))
        
        if self._stop_bits > 1:
            stopb_mask = termios.CSTOPB
        else:
            stopb_mask = 0

        if self._parity == PARITY_EVEN:
            parity_mask = termios.PARENB
        elif self._parity == PARITY_ODD:
            parity_mask = termios.PARENB | termios.PARODD
        else:
            parity_mask = 0

        clr_mask = termios.CSIZE | termios.CSTOPB | termios.PARENB | termios.PARODD
        return (old_cflag & ~clr_mask) \
                 | (enum_val | stopb_mask | parity_mask)

    def _update_local_mode_flags(self, old_lflag):
        clr_mask = termios.ECHO | termios.ECHONL | termios.ICANON | termios.ISIG | termios.IEXTEN
        return (old_lflag & ~clr_mask)

if __name__ == "__main__":
    app = SerialIo("/dev/ttyUSB0")
