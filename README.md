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

- [ ] Adicionar uma interface gráfica completa com:
  - [x] Fornecer opções avançadas para o usuário definir o ttl e o timeout
  - [ ] Adaptar codigo do traceroute cli para gui
  - [x] Representação dos roteadores de maneira grafica
  - [ ] Adicionar os roteadores on the go, ao realizar os hops
- [ ] Tentar integrar o ping com traceroute
- [ ] Usar mais de uma thread
- [ ] Realizar envio de pacotes UDP, ICMP e TCP
- [ ] Adicionar suporte ao ipv6 e ipv4

### Dependencias:

- pyqt
