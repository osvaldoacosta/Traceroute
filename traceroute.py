#!/usr/bin/env python

import socket
from show_routes import exibir_rota
import socket_creation
DEVICE_NAME = None;


def get_website(site_addr=""):
    site = site_addr
    try:
        site_addr = socket.gethostbyname(site_addr)
        print(site, site_addr)
    except socket.error:
        return [site_addr,None]

    return [site, site_addr]


def tracer(srec, ssend, port, ttl, destination_address, timeout):
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


def show_routes(addresses):
    exibir_rota(addresses)


def traceroute(destination_address, max_hops=60, timeout=3,max_rejections=15):
    ttl = 1
    rejections = 0
    addresses = []
    port = 33434

    while ttl < max_hops:
        #Socket icmp recebimento
        srec = socket_creation.create_icmp_receive_socket(port,timeout, DEVICE_NAME)
        #Socket udp envio
        ssnd = socket_creation.create_udp_send_socket(ttl)

       
        ssnd.sendto(b'Tapioca', (destination_address,port))
        print(f"\nTTL: {ttl}")

        tries, addr = tracer(srec, ssnd, port, ttl, destination_address, timeout)

        print(f"Tentativa no endereço: {tries}")
        if addr == "*":
            rejections += 1
        else:
            rejections = 0

        addresses.append(addr)

        if rejections >= max_rejections:
            break

        if addr == destination_address:
            break

        ttl +=1
    try:
        show_routes(addresses)
    except Exception as error:
        print(f"Houve um erro ao tentar rastrear a rota: {error}")



def start(website_address, ttl=60, timeout=3, max_rejections=15):
    website, website_address = get_website(website_address)

    
    print(f"Destino: {website} ({website_address})")
    traceroute(website_address,max_hops=ttl, timeout=timeout, max_rejections=max_rejections)



