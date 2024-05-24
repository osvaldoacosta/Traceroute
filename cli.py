
import traceroute as tr  
import detectDevice

if __name__ == "__main__":
    destino = ""

    devices = detectDevice.get_active_devices()  # PEga os dispositivos de ethernet da maquina 
    #que estao trafegando pacotes e possuem um MAC válido

    if not devices:
        print("Nenhum dispositivo ativo encontrado.")
        exit(1)

    print("Selecione um dispositivo:")
    for idx, device in enumerate(devices):
        print(f"{idx}: {device}")

    try:
        device_index = int(input("Digite o número do dispositivo desejado: "))
        if device_index < 0 or device_index >= len(devices):
            raise IndexError("Número de dispositivo inválido.")
        selected_device = devices[device_index]
        print(f"Dispositivo selecionado: {selected_device}")

        tr.DEVICE_NAME = selected_device[0];
        destino = input("Digite o endereço de destino (ip ou url): ")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")
        exit(1)
    except IndexError as e:
        print(e)
        exit(1)
    except Exception as e:
        raise e

    tr.start(destino)

