import subprocess
import time
from pathlib import Path


class Control(object):
    def __init__(self, **kwargs):
        self.rx = kwargs.get('rx')
        self.tx = kwargs.get('tx')
        self.current = None
        self.root_dir = Path(__file__).resolve().parents[1]

    def kill(self, proc=None):
        """Stop the active flowgraph and reset the HackRF connection."""
        target = proc or self.current
        time.sleep(.3)

        if target is not None:
            try:
                target.hide()
                target.stop()
                target.wait()
            except Exception as E:
                print(E)

        if target is self.current or proc is None:
            self.current = None

        self.reset_hackrf()

    def reset_hackrf(self):
        try:
            lsusb = subprocess.run(
                ['lsusb'],
                check=False,
                capture_output=True,
                text=True,
            )
        except OSError as E:
            print(E)
            return

        hackrf_line = next(
            (line for line in lsusb.stdout.splitlines() if 'OpenMoko' in line),
            None,
        )
        if not hackrf_line:
            print('HackRF not found in lsusb output')
            return

        parts = hackrf_line.split()
        try:
            bus = parts[1]
            dev = parts[3].rstrip(':')
        except IndexError:
            print(f'Unable to parse HackRF lsusb line: {hackrf_line}')
            return

        hackrf = f'/dev/bus/usb/{bus}/{dev}'
        reset_tool = self.root_dir / 'usbreset'
        bind_script = self.root_dir / 'bind.sh'

        if reset_tool.exists():
            subprocess.run([str(reset_tool), hackrf], check=False)
        elif bind_script.exists():
            subprocess.run(['bash', str(bind_script), hackrf], check=False)
        else:
            print('No usbreset tool or bind.sh script found')

    def startTX(self):
        """Launch tx capabilities."""
        action = self.tx.fmTX(self)
        action.start()
        action.show()
        self.current = action
        return action

    def startRX(self):
        """Launch rx capabilities."""
        action = self.rx.fmRX(self)
        action.start()
        action.show()
        self.current = action
        return action

    def switch_to_tx(self, proc=None):
        self.kill(proc)
        return self.startTX()

    def switch_to_rx(self, proc=None):
        self.kill(proc)
        return self.startRX()
