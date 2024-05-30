## Traceroute

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
- [ ] Mostrar na mesma tela os diferentes hops dos roteadores de diferentes protocolos
- [x] Fazer com que os botoes dos protocolos do gui funcionem
- [x] Tentar integrar o ping com traceroute
- [x] Usar mais de uma thread
- [x] Realizar envio de pacotes:
  - [x] UDP
  - [x] ICMP
  - [x] TCP
- [ ] Adicionar suporte ao ipv6
- [x] Adicionar suporte ao windows

### Dependencias:

- pyqt
