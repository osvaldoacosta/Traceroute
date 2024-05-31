#!/usr/bin/env python
from os import getpid
import struct
import struct

FLAG = "TAPIOCA!"

def create_icmp_packet(ttl, isIPV6):
    if isIPV6:
        icmp_type = 128  # Echo Request para ICMPv6
    else:
        icmp_type = 8  # Echo Request para ICMP

    icmp_code = 0
    calc_checksum = 0
    icmp_identifier = getpid() & 0xFFFF
    icmp_sequence = 1

    # Construir o cabeçalho base
    base_header = struct.pack("!BBHHH", icmp_type, icmp_code, calc_checksum, icmp_identifier, icmp_sequence)
    data_str = f'{FLAG}{ttl}'
    data_str_len = len(data_str)
    data = struct.pack(f'{data_str_len}s', data_str.encode())

    # Calcular o checksum
    calc_checksum = icmp_checksum(base_header + data)

    # Atualizar o cabeçalho com o checksum calculado
    header = struct.pack("!BBHHH", icmp_type, icmp_code, calc_checksum, icmp_identifier, icmp_sequence)

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


