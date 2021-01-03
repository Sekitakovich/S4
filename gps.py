import serial
from functools import reduce
from operator import xor
from multiprocessing import Process, Queue, Event
from threading import Thread
from loguru import logger


class GPSreceiver(Process):
    def __init__(self, *, port: str, baud: int):
        super().__init__()
        self.daemon = True

        self.isReady = True

        try:
            self.sp = serial.Serial(port=port, baudrate=baud)
        except (serial.SerialException) as e:
            self.isReady = False
            logger.error(e)
        else:
            self.port = port
            self.baud = baud

            self.antenna = Queue()
            self.QuitEvent = Event()
            self.working = True

    def run(self) -> None:
        def stopper():
            self.QuitEvent.wait()
            self.QuitEvent.clear()
            self.working = False

        ss = Thread(target=stopper, daemon=True)
        ss.start()

        self.working = True
        while self.working:
            nmea = self.sp.readline()
            self.antenna.put(nmea)

        ss.join()


if __name__ == '__main__':
    def main():

        port = '/dev/ttyACM0'
        baud = 9600

        GPS = GPSreceiver(port=port, baud=baud)
        if GPS.isReady:
            GPS.start()

            for loop in range(1000):
                nmea: bytes = GPS.antenna.get()
                part = nmea.split(b'*')
                thisCsum = reduce(xor, part[0][1:], 0)
                thatCsum = int(part[1][0:0 + 2], 16)
                if thisCsum == thatCsum:
                    logger.info(nmea)

            # GPS.working = False
            GPS.QuitEvent.set()
            GPS.join()

        # with serial.Serial(port=port, baudrate=baud) as sp:
        #     while True:
        #         ooo = sp.readline()
        #         logger.info(ooo)


    main()
