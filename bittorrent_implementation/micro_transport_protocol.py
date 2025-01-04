# Check BEP:29 https://www.bittorrent.org/beps/bep_0029.html

####
# Note: window size is not properly adjusted
# header extension 'SELECTIVE ACK' not supported
# rtt calculation is dubious at best --BarbedMach
####

from enum import IntEnum
from dataclasses import dataclass
import asyncio, struct, random, time

class PacketType(IntEnum):
    ST_DATA = 0
    ST_FIN = 1
    ST_STATE = 2
    ST_RESET = 3
    ST_SYN = 4

@dataclass
class Header:
    type: PacketType
    ver: int
    extension: int
    connection_id: int
    timestamp_microseconds: int
    timestamp_difference_microseconds: int
    wnd_size: int
    seq_nr: int
    ack_nr: int

class ConnectionState(IntEnum):
    CS_UNKNOWN = 1
    CS_SYN_SENT = 2
    CS_SYN_RECV = 3
    CS_CONNECTED = 4
    CS_DISCONNECTED = 5

def get_ms():
    return int(time.time_ns() / 1_000_000)

DEFAULT_WND_SIZE = 0xf000
HEADER_FORMAT = "!BBHLLLHH"

def make_packet(header: Header, data: bytes):

    type_and_ver = header.type.value << 4 | header.ver

    packed_header = struct.pack(HEADER_FORMAT,
                                type_and_ver,
                                header.extension,
                                header.connection_id,
                                header.timestamp_microseconds,
                                header.timestamp_difference_microseconds,
                                header.wnd_size,
                                header.seq_nr,
                                header.ack_nr
                                )

    return packed_header + data

def decode_packet(byte_stream: bytes):
    header_size = struct.calcsize(HEADER_FORMAT)
    header_bytes = byte_stream[:header_size]

    type_and_ver, extension, connection_id, \
        timestamp_microseconds, timestamp_difference_microseconds, \
        wnd_size, seq_nr, ack_nr = struct.unpack("!BBHLLLHH", header_bytes)

    version = type_and_ver & 0x0F
    packet_type = PacketType(type_and_ver >> 4)

    header = Header(
        type=packet_type,
        ver=version,
        extension=extension,
        connection_id=connection_id,
        timestamp_microseconds=timestamp_microseconds,
        timestamp_difference_microseconds=timestamp_difference_microseconds,
        wnd_size=wnd_size,
        seq_nr=seq_nr,
        ack_nr=ack_nr
    )

    data = byte_stream[header_size:]

    return header, data

class UTPSocket(asyncio.DatagramProtocol):
    def __init__(self, user_protocol):
        self.user_protocol = user_protocol
        self.transport = None
        self.state = ConnectionState.CS_UNKNOWN
        self.seq_nr = 1
        self.ack_nr = 0
        self.connection_id_recv = random.randint(0, 65535)
        self.connection_id_send = self.connection_id_recv + 1
        self.last_packet_sent_ms = 0
        self.last_packet_received_ms = 0

    def get_time_diff(self):
        diff = self.last_packet_received_ms - self.last_packet_sent_ms
        return min(0, diff)

    def connection_made(self, transport):
        self.transport = transport

        header = Header(
            type=PacketType.ST_SYN,
            ver=1,
            connection_id=self.connection_id_recv,
            timestamp_microseconds=get_ms(),
            timestamp_difference_microseconds=0,
            wnd_size=DEFAULT_WND_SIZE,
            seq_nr=self.seq_nr,
            ack_nr=0,
            extension=0
        )

        data = b''

        self.last_packet_sent_ms = header.timestamp_microseconds
        self.transport.sendto(make_packet(header, data))
        self.seq_nr += 1
        self.state = ConnectionState.CS_SYN_SENT

    def write(self, data):
        header = Header(
            type=PacketType.ST_DATA,
            ver=1,
            extension=0,
            connection_id=self.connection_id_send,
            timestamp_microseconds=get_ms(),
            timestamp_difference_microseconds=self.get_time_diff(),
            wnd_size=DEFAULT_WND_SIZE,
            seq_nr=self.seq_nr,
            ack_nr=self.ack_nr,
        )

        self.last_packet_sent_ms = header.timestamp_microseconds
        self.seq_nr += 1
        self.transport.sendto(make_packet(header, data))

    def datagram_received(self, data, addr):
        header, _data = decode_packet(data)
        self.ack_nr = header.seq_nr
        self.last_packet_received_ms = header.timestamp_microseconds

        if header.type == PacketType.ST_DATA:
            response_header = Header(
                type=PacketType.ST_STATE,
                ver=1,
                extension=0,
                connection_id=self.connection_id_send,
                timestamp_microseconds=get_ms(),
                timestamp_difference_microseconds=self.get_time_diff(),
                wnd_size=DEFAULT_WND_SIZE,
                seq_nr=self.seq_nr,
                ack_nr=self.ack_nr,
            )

            self.transport.sendto(make_packet(response_header, b''))
            self.last_packet_sent_ms = response_header.timestamp_microseconds

            if self.state == ConnectionState.CS_SYN_RECV:
                self.state = ConnectionState.CS_CONNECTED
                self.user_protocol.connection_made(self)

            self.user_protocol.data_received(_data)

        elif header.type == PacketType.ST_SYN:
            self.connection_id_send = header.connection_id
            self.connection_id_recv = header.connection_id + 1
            self.state = ConnectionState.CS_SYN_RECV

            response_header = Header(
                type=PacketType.ST_STATE,
                ver=1,
                extension=0,
                connection_id=self.connection_id_send,
                timestamp_microseconds=get_ms(),
                timestamp_difference_microseconds=self.get_time_diff(),
                wnd_size=DEFAULT_WND_SIZE,
                seq_nr=self.seq_nr,
                ack_nr=self.ack_nr,
            )

            self.seq_nr += 1
            self.transport.sendto(make_packet(response_header, b''))
            self.last_packet_sent_ms = response_header.timestamp_microseconds

        elif header.type == PacketType.ST_STATE:
            if self.state == ConnectionState.CS_SYN_SENT:
                self.state = ConnectionState.CS_CONNECTED
                self.user_protocol.connection_made(self)

        elif header.type == PacketType.ST_RESET:
            self.state = ConnectionState.CS_DISCONNECTED
            self.user_protocol.connection_lost(None)

        elif header.type == PacketType.ST_FIN:
            self.state = ConnectionState.CS_DISCONNECTED

            response_header = Header(
                type=PacketType.ST_FIN,
                ver=1,
                extension=0,
                connection_id=self.connection_id_send,
                timestamp_microseconds=get_ms(),
                timestamp_difference_microseconds=self.get_time_diff(),
                wnd_size=DEFAULT_WND_SIZE,
                seq_nr=self.seq_nr,
                ack_nr=self.ack_nr,
            )

            self.transport.sendto(make_packet(response_header, b''))
            self.user_protocol.connection_lost(None)

    def connection_lost(self, exc):
        self.user_protocol.connection_lost(exc)

    def close(self):
        if self.state == ConnectionState.CS_CONNECTED:
            self.state = ConnectionState.CS_DISCONNECTED

            response_header = Header(
                type=PacketType.ST_FIN,
                ver=1,
                extension=0,
                connection_id=self.connection_id_send,
                timestamp_microseconds=get_ms(),
                timestamp_difference_microseconds=self.get_time_diff(),
                wnd_size=DEFAULT_WND_SIZE,
                seq_nr=self.seq_nr,
                ack_nr=self.ack_nr,
            )

            self.transport.sendto(make_packet(response_header, b''))
            self.user_protocol.connection_lost(None)





        





