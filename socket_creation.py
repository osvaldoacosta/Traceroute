#!/usr/bin/env python

import platform
import socket

def create_icmp_receive_socket(port, timeout, device_name):
    if platform.system() == 'Windows':
        socket_rec_icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        socket_rec_icmp.settimeout(timeout)
        socket_rec_icmp.bind(('', port))
        return socket_rec_icmp
    else:
        socket_rec_icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)
        socket_rec_icmp.settimeout(timeout)
        s.bind((device_name, port))
        return socket_rec_icmp

def create_icmp_send_socket(ttl, timeout):
    ssnd = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    ssnd.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    ssnd.settimeout(timeout)
    return ssnd

def create_udp_send_socket(ttl):
    ssnd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ssnd.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    return ssnd

def create_tcp_send_socket(ttl):
    ssnd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssnd.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    ssnd.setblocking(False)
    return ssnd
