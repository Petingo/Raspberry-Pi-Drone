import sys
import socket, struct, time
import thread
from modules.utils import *

#import pygame

try:
    import tty, termios
except ImportError:
    # Probably Windows.
    try:
        import msvcrt
    except ImportError:
        # FIXME what to do on other platforms?
        # Just give up here.
        raise ImportError('getch not available')
    else:
        getch = msvcrt.getch
else:
    def getch():
        """getch() -> key character

        Read a single keypress from stdin and return the resulting character. 
        Nothing is echoed to the console. This call will block if a keypress 
        is not already available, but will not wait for Enter to be pressed. 

        If the pressed key was a modifier key, nothing will be detected; if
        it were a special function key, it may return the first character of
        of an escape sequence, leaving additional characters in the buffer.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# Main configuration
#UDP_IP = "127.0.0.1" # Localhost (for testing)
UDP_IP = "192.168.10.1" # Vehicle IP address
UDP_PORT = 51001 # This port match the ones using on other scripts

update_rate = 0.01 # 100 hz loop cycle
# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

raw_roll = 0
raw_pitch = 0
raw_yaw = 0
raw_throttle = 0
    
def Thread(*args):
    while(True):
        current = time.time()
        elapsed = 0
    
        # Joystick reading
        roll     = float(mapping(raw_roll,-10,10,1000,2000))
        pitch    = float(mapping(raw_pitch,10,-10,1000,2000))
        yaw      = float(mapping(raw_yaw,-10,10,1000,2000))
        throttle = float(mapping(raw_throttle,10,-10,1000,2000))

        # Be sure to always send the data as floats
        # The extra zeros on the message are there in order for the other scripts to do not complain about missing information
        message = [roll, pitch, yaw, throttle, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        '''buf = struct.pack('>' + 'd' * len(message), *message)
        sock.sendto(buf, (UDP_IP, UDP_PORT))'''
    
        print (message[0:4])
        time.sleep(0.5)
        # Make this loop work at update_rate

if __name__ == "__main__":
    thread.start_new_thread(Thread, ())
    while True:
        key = getch()
        if key == 'f' and raw_roll < 10:
            raw_roll = raw_roll + 1
        elif key == 's' and raw_roll > -10:
            raw_roll = raw_roll - 1
        elif key == 'e' and raw_pitch < 10:
            raw_pitch = raw_pitch + 1
        elif key == 'd' and raw_pitch > -10:
            raw_pitch = raw_pitch - 1
        elif key == 'j' and raw_yaw < 10:
            raw_yaw = raw_yaw + 1
        elif key == 'l' and raw_yaw > -10:
            raw_yaw = raw_yaw - 1
        elif key == 'i' and raw_throttle < 10:
            raw_throttle = raw_throttle + 1
        elif key == 'k' and raw_throttle > -10:
            raw_throttle = raw_throttle - 1
        elif key == 'n':
            raw_roll = 0
            raw_pitch = 0
            raw_yaw = 0
            raw_throttle = 0