import psutil

def get_active_devices():
    active_devices = []
    io_counters = psutil.net_io_counters(pernic=True)
    for interface, addrs in psutil.net_if_addrs().items():
        if interface in io_counters:
            if io_counters[interface].bytes_sent > 0 or io_counters[interface].bytes_recv > 0:
                for addr in addrs:
                    if addr.family == psutil.AF_LINK:  # Checa se é um MAC address
                        if(addr.address == "00:00:00:00:00:00"): #Ignora os mac inválidos
                            continue;
                        active_devices.append((interface, addr.address))
    return active_devices

