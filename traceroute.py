#!/usr/bin/env python

import socket
from show_routes import exibir_rota

import psutil

DEVICE_NAME = None;



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

#TODO: mudar para deixar o dispositivo modular
def create_icmp_receive_socket(port,timeout):
    socket_rec_icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)
    socket_rec_icmp.settimeout(timeout)
    s.bind((DEVICE_NAME, port))

    return socket_rec_icmp

def create_udp_send_socket(ttl):
    ssnd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ssnd.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    return ssnd

#TODO: CLI

# def input_website():
#
#     site = site_addr = ""
#     while site_addr == "":
#         try:
#             site = input("Digite o nome do website(ou ip) de destino: ")
#             site_addr = socket.gethostbyname(site)
#         except socket.error:
#             print("Destinatario fora de alcance!")
#
#     return [site, site_addr]

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
    socket_recv = create_icmp_receive_socket(port,timeout)
    socket_sender = create_udp_send_socket(ttl)
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
        srec = create_icmp_receive_socket(port,timeout)
        #Socket udp envio
        ssnd = create_udp_send_socket(ttl)

       
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



def start(website_address):
    website, website_address = get_website(website_address)

    
    print(f"Destino: {website} ({website_address})")
    traceroute(website_address)


