#!/usr/bin/env python

import socket
from show_routes import show_routes_print
import socket_creation
global DEVICE_NAME


def get_website(site_addr=""):
    site = site_addr
    try:
        site_addr = socket.gethostbyname(site_addr)
        print(site, site_addr)
    except socket.error:
        return [site_addr,None]

    return [site, site_addr]


def tracer(srec, ssend, port, ttl, destination_address, timeout, update_output):
    busca = ""
    hasEnded = False

    for cont in range(3):
        try:
            info, (addr, _) = srec.recvfrom(2000)

            if addr != "*":
                busca += addr
                hasEnded = True
                break

        except socket.error:
            busca += "* "
        finally:
            srec.close()
            ssend.close()

            if not hasEnded:
                socket_recv, socket_sender = resend_msg(destination_address, port, ttl, timeout)

    return busca, define_addr(busca)


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


def traceroute(destination_address, max_hops=60, timeout=3, max_rejections=15, update_output=None, add_router=None):
    ttl = 1
    rejections = 0
    addresses = []
    port = 33434

    while ttl < max_hops:
        srec = socket_creation.create_icmp_receive_socket(port, timeout, DEVICE_NAME)
        ssnd = socket_creation.create_udp_send_socket(ttl)

        ssnd.sendto(b'Tapioca', (destination_address, port))

        if update_output:
            update_output(f"\nTTL: {ttl}")

        tries, addr = tracer(srec, ssnd, port, ttl, destination_address, timeout, update_output)

        if update_output:
            update_output(f"Tentativa no endereço: {tries}")

        if addr == "*":
            rejections += 1
        else:
            rejections = 0
        
        if add_router:
            add_router(addr)

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

def start(website_address, ttl=60, timeout=3, max_rejections=15, update_output=None, add_router=None):
    website, website_address = get_website(website_address)

    if update_output:
        update_output(f"Destino: {website} ({website_address})")

    traceroute(website_address, max_hops=ttl, timeout=timeout, max_rejections=max_rejections,
               update_output=update_output, add_router=add_router)
