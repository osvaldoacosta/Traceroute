#!/usr/bin/env python

import socket
from packet_creation import create_icmp_packet, create_udp_packet, create_udp_packet
from show_routes import address_info
import socket_creation
import time
from util import get_website
import select
import struct
DEVICE_NAME:str


def tracer(srec,ssend,  port, ttl, destination_address, timeout,isIPV6,send_function):
    busca = ""
    hasEnded = False

    ping_time: float = 0.0
    for cont in range(3):
        try:

            start_time = time.time()
            info, (addr, _) = srec.recvfrom(1024)
            end_time = time.time()

            if addr != "*":
                busca += addr
                ping_time = (end_time - start_time) * 1000
                hasEnded = True
                break

        except socket.error:
            busca += "* "
        if not hasEnded:
            srec,ssend= resend_msg(destination_address, port, ttl, timeout,isIPV6,send_function)
        
        
        srec.close()
        ssend.close()


    return busca,ping_time


def resend_msg(destination_address, port, ttl, timeout,isIPV6,send_function):
    socket_recv = socket_creation.create_icmp_receive_socket(port,timeout,DEVICE_NAME,isIPV6)
    socket_sender = send_function(ttl,port,destination_address,timeout,isIPV6)
    
    return socket_recv, socket_sender


def send_udp(ttl, port, destination_address,timeout,isIPV6):
    ssnd = socket_creation.create_udp_send_socket(ttl,timeout,isIPV6)
    udp_packet = create_udp_packet(port)
    ssnd.sendto(udp_packet, (destination_address, port))
    return ssnd

def send_icmp(ttl, port, destination_address, timeout,isIPV6):
    icmp = socket.getprotobyname("icmp")
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))
    my_socket.settimeout(timeout)
    icmp_packet = create_icmp_packet(ttl,isIPV6)
    my_socket.sendto(icmp_packet, (destination_address, 0))
    return my_socket

def send_tcp(ttl, port, destination_address, timeout,isIPV6):
    ssnd = socket_creation.create_tcp_send_socket(ttl,timeout,isIPV6)
    try:
        if ssnd:
            ssnd.connect((destination_address, port))
        print("TCP connected to: ",destination_address)
    except socket.error as e:
        if e.errno == 115 or e.errno == 10035:  # errno 115(linux) e 10035(windows) é o erro 'Operation now in progress'
            '''
            Segundo a documentação:
            "The socket is nonblocking and the connection cannot be completed 
            immediately."
            '''
            # isso é normal para um socket não bloqueante, e já que isso não influencia no funcionamento do traceroute,
            # pois ele completa quando estiver disponivel para escrita Deixaremos dessa forma,
            # ignorando esse erro. Poderiamos usar o pool ou o select, porém aumentaria a complexidade do código
            pass
        #Pega todos os outros erros
        else: print(f"TCP connection error with TTL {ttl}: {e}")
    
    return ssnd

def traceroute(destination_address, max_hops=60, timeout=3, max_rejections=15, update_output=None, add_router=None, with_location=False, protocol="UDP", isIPV6=False):
    ttl = 1
    rejections = 0
    addresses = []

    port = 33434

    total_time:float= 0.0

    send_function = None

    if protocol == "UDP":
        send_function = send_udp
    elif protocol == "ICMP":
        send_function = send_icmp
    else :
        send_function = send_tcp

    if not send_function:
        return
    
    while ttl < max_hops:
        srec = socket_creation.create_icmp_receive_socket(port, timeout, DEVICE_NAME, isIPV6=isIPV6)
        ssend = send_function(ttl,port, destination_address, timeout,isIPV6)

        addr_info = ""

        if update_output:
            update_output(f"\nTTL: {ttl}")

        addr,ping_time= tracer(srec, ssend, port, ttl, destination_address, timeout,isIPV6, send_function)

        total_time = total_time + ping_time

        
        if with_location:
            addr_info = address_info(addr)
        

        if update_output:
            update_output(f"Tentativa no endereço: {addr}")

        if "*" in addr:
            total_time += timeout*1000
            if update_output:
                update_output(f"Timeout excedido ou roteador inalcançável")
            rejections += 1
        else:
            rejections = 0
      
        if add_router:
            ping_time_str = f"{ping_time:.2f}ms"
            address_with_info = f"{addr}\n{addr_info}"
            add_router(address_with_info,ping_time_str,protocol)

        addresses.append(addr)

        if rejections >= max_rejections or addr == destination_address:
            break

        ttl += 1

    if update_output:
        print("Tempo total para o protocolo ",protocol,": ",total_time/1000,"s")
        update_output(f"Rota concluída: {addresses}")
        update_output(f"Tempo total para o protocolo {protocol} : {total_time/1000:.2f} s")


def start(website_address, ttl=60, timeout=3, max_rejections=15, update_output=None, add_router=None, with_geoinfo=False, protocol="UDP", isIPV6=False):
    website, website_address = get_website(website_address, isIPV6)

    if update_output:
        update_output(f"Destino: {website} ({website_address})")

    print(website_address)
    print(ttl)
    print(timeout)
    print(max_rejections)
    print(with_geoinfo)
    print(protocol)
    traceroute(website_address, max_hops=ttl, timeout=timeout, max_rejections=max_rejections,
               update_output=update_output, add_router=add_router, with_location=with_geoinfo, protocol=protocol, isIPV6=isIPV6)

