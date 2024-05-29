#!/usr/bin/env python
from os import getpid
import struct
import struct

FLAG = "TAPIOCA!"

def create_icmp_packet(ttl):
    # Header: Code (8) - Type (0) - Checksum (using checksum function) - ID (unique so take process ID) - Sequence (1)
    base_header = struct.pack("bbHHh", 8, 0, 0, getpid() & 0xFFFF, 1)
    data_str = f'{FLAG}{ttl}'
    data_str_len = len(data_str)
    data = struct.pack(f'{data_str_len}s', data_str.encode()) # Data is flag + TTL value (needed for receiver to map response to TTL)
    calc_checksum = icmp_checksum(base_header + data) # Checksum value base header and data for header packing
    header = struct.pack("bbHHh", 8, 0, calc_checksum, getpid() & 0xFFFF, 1) # Header packing with checksum

    icmp_packet = header + data
    return icmp_packet



def icmp_checksum(data):
    '''
    Checksum calculator for ICMP header from https://gist.github.com/pyos/10980172
        
            Parameters:
                data (str): data to derive checksum from
            Returns:
                checksum (int): calculated checksum
    '''    
    x = sum(x << 8 if i % 2 else x for i, x in enumerate(data)) & 0xFFFFFFFF
    x = (x >> 16) + (x & 0xFFFF)
    x = (x >> 16) + (x & 0xFFFF)
    checksum = ~x & 0xFFFF

    return checksum


def create_udp_packet(port):
    udp_header = struct.pack('!HHHH', port, port, 8, 0)
    udp_packet = udp_header + FLAG.encode()
    return udp_header + udp_packet


