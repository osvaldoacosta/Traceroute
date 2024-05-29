#!/usr/bin/env python

import platform
import socket

from time import time





def create_icmp_receive_socket(port,timeout, DEVICE_NAME):
    socket_rec_icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)
    socket_rec_icmp.settimeout(timeout)
    s.bind((DEVICE_NAME, port))

    return socket_rec_icmp


def create_icmp_send_socket(ttl,timeout):


    ssnd = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    if platform == 'Windows':
        ssnd.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl) # Set TTL value
    else:
        ssnd.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl) # Set TTL value
    
    ssnd.settimeout(timeout)

    return ssnd




def create_udp_send_socket(ttl):
    ssnd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ssnd.setsockopt(socket.IPPROTO_HOPOPTS,socket.IP_TTL, ttl)
    return ssnd


def create_tcp_send_socket(ttl):
    ssnd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if platform == 'Windows':
        ssnd.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl) # Set TTL value
    else:
        ssnd.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl) # Set TTL value

    ssnd.setblocking(False) # Make the sending of packets more fast





