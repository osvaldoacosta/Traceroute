#!/usr/bin/env python

import socket
import psutil

def get_active_devices():
    active_devices = []
    io_counters = psutil.net_io_counters(pernic=True)
    for interface, addrs in psutil.net_if_addrs().items():
        if interface in io_counters:
            if io_counters[interface].bytes_sent > 0 or io_counters[interface].bytes_recv > 0:
                for addr in addrs:
                    if addr.family == psutil.AF_LINK:  # Checa se é um MAC address
                        if(addr.address == "00:00:00:00:00:00"): #Ignora os mac address inválidos
                            continue;
                        active_devices.append((interface, addr.address))
    return active_devices


def get_website(isIPV6, site_addr="", ):
    site = site_addr
    if isIPV6:
        try:
        
            info = socket.getaddrinfo(site, None, socket.AF_INET6)
            if info:
                for result in info:
                    ipv6_address = result[4][0]
                    return [site, ipv6_address]
            
            return "No IPv6 address found."
        
        except socket.gaierror as e:
            return f"Failed to get IPv6 address: {e}"
    else:
        try:
            site_addr = socket.gethostbyname(site_addr)
            print(site, site_addr)
        except socket.error:
            return [site_addr,None]

        return [site, site_addr]
