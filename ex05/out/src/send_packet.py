import argparse
import array
import socket
import struct
from functools import reduce


def chksum(packet: bytes) -> int:
    """Calculates Internet Protocol checksum

    :param packet: packet to calculate checksum for
    :return: checksum value
    """
    if len(packet) % 2 != 0:
        packet += b'\0'  # padding

    res = sum(array.array("H", packet))
    res = (res >> 16) + (res & 0xffff)
    res += res >> 16
    res = ~res

    return res & 0xffff


class IPTCPPacket:
    def __init__(self,
                 src_host: str,
                 src_port: int,
                 dst_host: str,
                 dst_port: int,
                 data: str = '',
                 flags: list = None):
        if flags is None:
            flags = []

        self.src_host = src_host
        self.src_port = src_port
        self.dst_host = dst_host
        self.dst_port = dst_port
        self.data = bytes(data, encoding='utf-8')  # TODO: encoding
        self.flags = [
            1 if 'fin' in flags else 0,  # FIN
            1 if 'syn' in flags else 0,  # SYN
            1 if 'rst' in flags else 0,  # Reset
            1 if 'psh' in flags else 0,  # Push
            1 if 'ack' in flags else 0,  # Acknowledgement
            1 if 'urg' in flags else 0,  # Urgent
            1 if 'ecn' in flags else 0,  # ECN-Echo
            1 if 'cwr' in flags else 0,  # CWR
            1 if 'noc' in flags else 0,  # Nonce
            0,  # Reserved
        ]

        self.raw = self._compile()

    def _get_tcp_header(self) -> bytes:
        tcp_src = self.src_port
        tcp_dst = self.dst_port
        tcp_seq = 0
        tcp_ack = 0
        tcp_header = (5 << 4)  # Data offset
        tcp_flags = reduce(lambda a, b: a + b,
                           [self.flags[idx] << idx for idx in
                            range(len(self.flags))],
                           0)
        tcp_window = 8192
        tcp_checksum = 0  # Initial checksum
        tcp_urgent_ptr = 0

        return struct.pack(
            '!HHIIBBHHH',
            tcp_src,
            tcp_dst,
            tcp_seq,
            tcp_ack,
            tcp_header,
            tcp_flags,
            tcp_window,
            tcp_checksum,
            tcp_urgent_ptr
        )

    def _get_tcp_checksum(self, packet: bytes) -> int:
        pseudo = struct.pack(
            '!4s4sHH',
            socket.inet_aton(self.src_host),
            socket.inet_aton(self.dst_host),
            socket.IPPROTO_TCP,
            len(packet)
        )

        return chksum(pseudo + packet)

    def _compile(self) -> bytes:
        packet = bytes()
        packet += self._get_tcp_header()
        packet += self.data

        tcp_checksum = self._get_tcp_checksum(packet)
        packet = packet[:16] + struct.pack('H', tcp_checksum) + packet[18:]

        return packet


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('host',
                        help='IP address or domain name of the receiving host',
                        metavar='IP/DOMAIN')
    parser.add_argument('port',
                        help='TCP port of the receiving host',
                        type=int,
                        metavar='PORT')

    flag_group = parser.add_mutually_exclusive_group(required=True)
    flag_group.add_argument('--syn',
                            help='create TCP packet with only the SYN flag set',
                            action='store_true')
    flag_group.add_argument('--xmas',
                            help='create TCP packet with the FIN, URG and PSH flags set',
                            action='store_true')
    flag_group.add_argument('--fin',
                            help='create TCP packet with only the FIN flag set',
                            action='store_true')
    flag_group.add_argument('--null',
                            help='create TCP packet with no flags set',
                            action='store_true')

    args = parser.parse_args()

    use_flags = []

    if args.syn:
        use_flags.append('syn')
    elif args.xmas:
        use_flags.append('fin')
        use_flags.append('urg')
        use_flags.append('psh')
    elif args.fin:
        use_flags.append('fin')

    pak = IPTCPPacket(
        socket.gethostbyname(socket.gethostname()),
        20,
        socket.gethostbyname(args.host),
        args.port,
        '',
        use_flags
    )

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

    s.sendto(pak.raw, (args.host, 0))
