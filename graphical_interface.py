import tkinter as tk
from tkinter.font import BOLD

import traceroute as tr  

from detectDevice import get_active_devices
import customtkinter

def enviar_dados():
    selected_item= ([device for device in devices if device[0] == combo_box.get()] or [""])[0]
    address = address_entry.get()

    print("Selected Item:", selected_item[0])
    print("Address:", address)

    print(f"Destino: {address} ")
    tr.DEVICE_NAME = selected_item[0]
    tr.start(address)
    

def on_click(event):
    address_entry.configure(state=tk.NORMAL)
    address_entry.delete(0, tk.END)

    #make the callback only work once
    address_entry.unbind('<Button-1>', on_click_id)

root = customtkinter.CTk()
root.geometry("800x600")

# Combobox for selecting items
devices = get_active_devices(); # PEga os dispositivos de ethernet que estao trafegando pacotes e possuem um MAC válido

print(devices)


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

label2 = customtkinter.CTkLabel(root, text="TRACEROUTE - POLI UPE",font=('Helvetica', 25, BOLD))
label2.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

device_names = [device[0] for device in devices]

label = customtkinter.CTkLabel(root, text="Escolha um dispositivo de rede disponivel: ",font=('Helvetica', 15, BOLD))
label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
selected_item = tk.StringVar()
combo_box = customtkinter.CTkComboBox(master=root, values=device_names, width=200)
combo_box.set("Escolha um dispositivo: ")
combo_box.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

# Entry widget for inputting address
label1 = customtkinter.CTkLabel(root, text="Digite o nome do website(ou ip) de destino: ", font=('Helvetica', 15, BOLD))
label1.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
address_entry = customtkinter.CTkEntry(master=root,width=200)
address_entry.insert(0,"Digite o nome do website(ou ip) de destino: ")
address_entry.place(relx=0.5, rely=0.25, anchor=tk.CENTER)



on_click_id = address_entry.bind('<Button-1>', on_click)

# Button to trigger enviar_dados function
button = customtkinter.CTkButton(master=root, text="Buscar", command=enviar_dados, width=8)
button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

root.mainloop()

