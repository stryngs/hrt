from shlex import split
import fcntl, subprocess, time

class Control(object):
    
    def __init__(self, **kwargs):
        self.rx = kwargs.get('rx')
        self.tx = kwargs.get('tx')
        

    def kill(self, proc):
        """Reset the hackRF connection"""
        time.sleep(.3)
        try:
            proc.hide()
            proc.stop()
        except:
            pass
        s1 = subprocess.Popen(split('lsusb'), stdout = subprocess.PIPE)
        s2 = subprocess.Popen(split('grep OpenMoko'), stdin = s1.stdout, stdout = subprocess.PIPE)
        oPut = s2.communicate()[0].split()
        bus = oPut[1]
        dev = oPut[3].split(':')[0]
        hackRF = '/dev/bus/usb/{0}/{1}'.format(bus, dev)
        USBDEVFS_RESET = ord('U') << (4*2) | 20
        with open(hackRF, 'w') as kOption:
            fcntl.ioctl(kOption, USBDEVFS_RESET, 0)


    def startTX(self):
        """Launch tx capabilities"""
        action = self.tx.fmTX(self)
        action.start()
        action.show()
        return action


    def startRX(self):
        """Launch rx capabilities"""
        action = self.rx.fmRX(self)
        action.start()
        action.show()
        return action