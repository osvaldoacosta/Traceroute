## Traceroute

Para rodar o cli rode com privilegios de administrador

```
sudo python cli.py
```

Para rodar com interface grafica rode com privilegios de administrador

```
sudo python graphical_interface.py
```

### Metas:

- [x] Adicionar uma interface gráfica completa com:
  - [x] Fornecer opções avançadas para o usuário definir o ttl e o timeout
  - [x] Adaptar codigo do traceroute cli para gui
  - [x] Representação dos roteadores de maneira grafica
  - [x] Adicionar os roteadores on the go, ao realizar os hops
- [x] Fazer com que os botoes dos protocolos do gui funcionem
- [x] Tentar integrar o ping com traceroute
- [x] Usar mais de uma thread
- [ ] Realizar envio de pacotes:
  - [x] UDP
  - [x] ICMP
  - [ ] TCP
- [ ] Adicionar suporte ao ipv6 e ipv4

### Dependencias:

- pyqt
