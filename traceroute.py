#!/usr/bin/env python

import socket
from packet_creation import create_icmp_packet, create_udp_packet, create_udp_packet
from show_routes import address_info
import socket_creation
import time
from util import get_website
import select

DEVICE_NAME:str


def tracer(srec,  port, ttl, destination_address, timeout, update_output):
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

            if not hasEnded:
                resend_msg(destination_address, port, ttl, timeout)

    return busca,ping_time


def resend_msg(destination_address, port, ttl, timeout):
    socket_recv = socket_creation.create_icmp_receive_socket(port,timeout,DEVICE_NAME)
    socket_sender = send_udp(ttl,port,destination_address)
    
    return socket_recv, socket_sender


def send_udp(ttl, port, destination_address,timeout=None):
    ssnd = socket_creation.create_udp_send_socket(ttl)
    udp_packet = create_udp_packet(port)
    ssnd.sendto(udp_packet, (destination_address, port))
    return ssnd

def send_icmp(ttl, port, destination_address, timeout):
    ssnd = socket_creation.create_icmp_send_socket(ttl,timeout)
    icmp_packet = create_icmp_packet(ttl)

    ssnd.sendto(icmp_packet, (destination_address,0))
     

def send_tcp(ttl, port, destination_address, timeout=None):
    ssnd = socket_creation.create_tcp_send_socket(ttl)
    try:
        if ssnd:
            ssnd.connect((destination_address, port))
        print("TCP connected to: ",destination_address)
    except socket.error as e:
        if e.errno == 115:  # errno 115 é o erro 'Operation now in progress'
            '''
            Segundo a documentação:
            "The socket is nonblocking and the connection cannot be completed 
            immediately."
            '''
            # isso é normal para um socket não bloqueante, e já que 
            # isso não influencia no funcionamento do traceroute, pois ele completa quando estiver disponivel para escrita
            # Deixaremos dessa forma, ignorando esse erro. Poderiamos usar o pool ou o select, porém aumentaria a complexidade do código
            pass
        #Pega todos os outros erros
        else: print(f"TCP connection error with TTL {ttl}: {e}")
    
    return ssnd

def traceroute(destination_address, max_hops=60, timeout=3, max_rejections=15, update_output=None, add_router=None, with_location=False, protocol=None):
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
        srec = socket_creation.create_icmp_receive_socket(port, timeout, DEVICE_NAME)


        ssend = send_function(ttl,port, destination_address, timeout)


        if update_output:
            update_output(f"\nTTL: {ttl}")

        addr,ping_time= tracer(srec, port, ttl, destination_address, timeout, update_output)

        if ssend:
            ssend.close()
        total_time = total_time + ping_time

        addr_w_ping = f"{addr}\n({ping_time:.2f} ms)" if ping_time else addr
        
        if with_location:
            addr_info = address_info(addr)
            addr_description = f"{addr_w_ping}\n{addr_info}"
        else:
            addr_description = addr_w_ping

        if update_output:
            update_output(f"Tentativa no endereço: {addr}")

        if "*" in addr:
            if update_output:
                update_output(f"Timeout excedido ou roteador inalcançável")
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


def start(website_address, ttl=60, timeout=3, max_rejections=15, update_output=None, add_router=None, with_geoinfo=False, protocols=[]):
    website, website_address = get_website(website_address)

    if update_output:
        update_output(f"Destino: {website} ({website_address})")

    for prot in protocols:
        traceroute(website_address, max_hops=ttl, timeout=timeout, max_rejections=max_rejections,
               update_output=update_output, add_router=add_router, with_location=with_geoinfo, protocol=prot)

