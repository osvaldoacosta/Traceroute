#!/usr/bin/env python

import socket
def create_icmp_receive_socket(port,timeout, DEVICE_NAME):
    socket_rec_icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)
    socket_rec_icmp.settimeout(timeout)
    s.bind((DEVICE_NAME, port))

    return socket_rec_icmp

def create_udp_send_socket(ttl):
    ssnd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ssnd.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    return ssnd
