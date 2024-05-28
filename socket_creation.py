#!/usr/bin/env python

import socket


def get_website(site_addr=""):
    site = site_addr
    try:
        site_addr = socket.gethostbyname(site_addr)
        print(site, site_addr)
    except socket.error:
        return [site_addr,None]

    return [site, site_addr]

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


