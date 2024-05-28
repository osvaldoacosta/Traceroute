#!/usr/bin/env python
import struct

def create_icmp_package(ttl):
    pass

def create_udp_package(port):
    udp_header = struct.pack('!HHHH', port, port, 8, 0)
    udp_packet = udp_header + b'0'
    return udp_header + udp_packet


