import time
import socket
from functools import reduce
from operator import xor
from threading import Thread
from queue import Queue as ThreadQueue
from multiprocessing import Process, Queue as ProcessQueue
from contextlib import closing
from dataclasses import dataclass
from enum import IntEnum
from loguru import logger


class DataStructure(IntEnum):
    RawNMEA = 0
    Type450 = 1


@dataclass()
class Report(object):
    channel: str
    raw: bytes

@dataclass()
class Entry(object):
    # channel: str
    nmea: bytes
    item: list
    sfi: str = ''
    seq: int = 0


class Antenna(Thread):
    def __init__(self, *, channel: int, qp: ThreadQueue, ds: IntEnum):
        super().__init__()
        self.daemon = True
        self.name = f'CH[{channel:02d}]'

        self.mg = f'239.192.0.{channel}'  # Multicast Group address
        self.port = 60000 + channel
        self.qp = qp
        self.ds = ds

        self.bufferSize = 4096
        self.watch = True

    def run(self) -> None:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            logger.debug(f'{self.name} on {self.mg}:{self.port} is ready to go')

            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(self.mg) + socket.inet_aton('0.0.0.0'))
            sock.bind(('', self.port))

            while self.watch:
                try:
                    stream, sender = sock.recvfrom(self.bufferSize)
                except (socket.error) as e:
                    logger.error(e)
                    break
                else:
                    self.qp.put(Report(channel=self.name, raw=stream))


class Receiver(Process):
    def __init__(self):
        super().__init__()
        self.daemon = True

        self.UdPbC = b'UdPbC\x00'
        self.inputQueue = ThreadQueue()
        self.outputQueue = ProcessQueue()

    def route450(self, *, stream: bytes):
        part = stream.split(b'\\')
        if part[0] == self.UdPbC:
            head = part[1]
            nmea = part[2]

            ooo = head.split(b'*')
            thisCsum = reduce(xor, ooo[0], 0)
            thatCsum = int(ooo[1], 16)
            if thisCsum == thatCsum:
                sfi = ''
                seqnum = 0
                for ppp in ooo[0].split(b','):
                    qqq = ppp.split(b':')
                    if qqq[0] == b's':
                        sfi = qqq[1].decode()
                    elif qqq[0] == b'n':
                        seqnum = int(qqq[1])

                np = nmea.split(b'*')
                if reduce(xor, np[0][1:], 0) == int(np[1][0: 0+2], 16):
                    body = np[0].decode()
                    item = body.split(',')
                    entry = Entry(sfi=sfi, seq=seqnum, nmea=nmea, item=item)
                    self.outputQueue.put(entry)
                else:
                    logger.error(f'Checksum Error')
            else:
                logger.error(f'Checksum Error')
        else:
            logger.error(f'450 Symbol Error')

    def run(self) -> None:
        member = {}
        for channel in range(1, 1+16):
            A = Antenna(channel=channel, qp=self.inputQueue, ds=DataStructure.Type450)
            A.start()
            member[channel] = A

        while True:
            ooo: Report = self.inputQueue.get()
            self.route450(stream=ooo.raw)
            # logger.info(f'{ooo.channel} {ooo.stream}')


if __name__ == '__main__':
    def main():

        R = Receiver()
        R.start()

        while True:
            ooo: Entry = R.outputQueue.get()
            symbol = ooo.item[0]
            logger.info(f'[{ooo.sfi}:{symbol}] {ooo.item[1:]}')

    main()
