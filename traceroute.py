#!/usr/bin/env python

import socket
from show_routes import address_info, show_routes_print
import socket_creation
import time
global DEVICE_NAME




def tracer(srec, ssend, port, ttl, destination_address, timeout, update_output):
    busca = ""
    hasEnded = False

    ping_time: float = 0.0
    for cont in range(3):
        try:

            start_time = time.time()
            info, (addr, _) = srec.recvfrom(2000)
            end_time = time.time()

            if addr != "*":
                busca += addr
                ping_time = (end_time - start_time) * 1000
                hasEnded = True
                break

        except socket.error:
            busca += "* "
        finally:
            srec.close()
            ssend.close()

            if not hasEnded:
                resend_msg(destination_address, port, ttl, timeout)

    return busca, define_addr(busca),ping_time


def resend_msg(alvo, port, ttl, timeout):
    socket_recv = socket_creation.create_icmp_receive_socket(port,timeout,DEVICE_NAME)
    socket_sender = socket_creation.create_udp_send_socket(ttl)
    socket_sender.sendto(b'Tapioca!', (alvo, port))

    return socket_recv, socket_sender


def define_addr(busca):
    busca = busca.strip("* ")

    addr = "*" if busca == "" else busca

    return addr


    
def show_routes(addresses, update_output, add_router):
    for address in addresses:
        if address != "*":
            update_output(f"Connected to: {address}")
            add_router(address)
        else:
            update_output(f"Timeout or unreachable: {address}")


def traceroute(destination_address, max_hops=60, timeout=3, max_rejections=15, update_output=None, add_router=None, with_location=False):
    ttl = 1
    rejections = 0
    addresses = []
    port = 33434

    total_time:float= 0.0

    while ttl < max_hops:
        srec = socket_creation.create_icmp_receive_socket(port, timeout, DEVICE_NAME)
        ssnd = socket_creation.create_udp_send_socket(ttl)

        ssnd.sendto(b'Tapioca', (destination_address, port))

        if update_output:
            update_output(f"\nTTL: {ttl}")

        tries, addr,ping_time= tracer(srec, ssnd, port, ttl, destination_address, timeout, update_output)

        total_time = total_time + ping_time

        addr_w_ping = f"{addr}\n({ping_time:.2f} ms)" if ping_time else addr
        
        if with_location:
            addr_info = address_info(addr)
            addr_description = f"{addr_w_ping}\n{addr_info}"
        else:
            addr_description = addr_w_ping

        if update_output:
            update_output(f"Tentativa no endereço: {tries}")

        if addr == "*":
            rejections += 1
        else:
            rejections = 0
      
        if add_router:
            add_router(addr_description)

        addresses.append(addr)

        if rejections >= max_rejections or addr == destination_address:
            break

        ttl += 1

    if update_output:
        update_output(f"Rota concluída: {addresses}")

    try:
        show_routes(addresses)
    except Exception as error:
        if update_output:
            update_output(f"Houve um erro ao tentar rastrear a rota: {error}")

def start(website_address, ttl=60, timeout=3, max_rejections=15, update_output=None, add_router=None, with_geoinfo=False):
    website, website_address = socket_creation.get_website(website_address)

    if update_output:
        update_output(f"Destino: {website} ({website_address})")

    traceroute(website_address, max_hops=ttl, timeout=timeout, max_rejections=max_rejections,
               update_output=update_output, add_router=add_router, with_location=with_geoinfo)
