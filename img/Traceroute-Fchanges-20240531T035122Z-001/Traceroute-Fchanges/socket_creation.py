#!/usr/bin/env python

import platform
import socket

def create_icmp_receive_socket(port, timeout, device_name, isIPV6):
    if platform.system() == 'Windows':
        if isIPV6:
            socket_rec_icmp = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.IPPROTO_ICMPV6)
        else:
            socket_rec_icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        socket_rec_icmp.settimeout(timeout)
        socket_rec_icmp.bind(('', port))
    else:
        if isIPV6:
            socket_rec_icmp = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.IPPROTO_ICMPV6)
        else:
            socket_rec_icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)
            s.bind((device_name, port))
        socket_rec_icmp.settimeout(timeout)
        
    return socket_rec_icmp

def create_icmp_send_socket(ttl, timeout, isIPV6):
    if isIPV6:
        ssnd = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.IPPROTO_ICMPV6)
        ssnd.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_UNICAST_HOPS, ttl)
    else:
        ssnd = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        ssnd.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    ssnd.settimeout(timeout)
    return ssnd

def create_udp_send_socket(ttl, isIPV6):
    if isIPV6:
        ssnd = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        ssnd.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_UNICAST_HOPS, ttl)
    else:
        ssnd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        ssnd.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    return ssnd

def create_tcp_send_socket(ttl, isIPV6):
    if isIPV6:
        ssnd = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        ssnd.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_UNICAST_HOPS, ttl)
    else:
        ssnd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssnd.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    ssnd.setblocking(False)
    return ssnd
