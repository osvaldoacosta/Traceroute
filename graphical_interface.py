from PyQt5 import QtWidgets, QtGui, QtCore, QtSvg
import sys
import random
from detectDevice import get_active_devices
import traceroute as tr

class TracerouteUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('TRACEROUTE - POLI UPE')
        self.setGeometry(100, 100, 800, 600)
        self.devices = get_active_devices()  # Get active devices

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        # Main frame
        self.main_frame = QtWidgets.QWidget()
        self.main_frame_layout = QtWidgets.QVBoxLayout()
        self.main_frame.setLayout(self.main_frame_layout)
        self.main_layout.addWidget(self.main_frame)

        # Advanced options frame
        self.advanced_options_frame = QtWidgets.QWidget()
        self.advanced_options_frame_layout = QtWidgets.QVBoxLayout()
        self.advanced_options_frame.setLayout(self.advanced_options_frame_layout)
        self.advanced_options_frame.setVisible(False)
        self.main_layout.addWidget(self.advanced_options_frame)

        # Address input
        self.formGroupBox = QtWidgets.QGroupBox("Preencha os campos do traceroute: ")
        self.address_entry = QtWidgets.QLineEdit()

        # Network device selection
        device_names = [device[0] for device in self.devices]
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItems(device_names)
        self.combo_box.setCurrentText("Escolha um dispositivo: ")

        # IPv4 and IPv6 checkboxes
        self.ipv4_checkbox = QtWidgets.QCheckBox("IPv4")
        self.ipv6_checkbox = QtWidgets.QCheckBox("IPv6")
        self.ipv_layout = QtWidgets.QHBoxLayout()
        self.ipv_layout.addWidget(self.ipv4_checkbox)
        self.ipv_layout.addWidget(self.ipv6_checkbox)

        # UDP, TCP, and ICMP checkboxes
        self.udp_checkbox = QtWidgets.QCheckBox("UDP")
        self.tcp_checkbox = QtWidgets.QCheckBox("TCP")
        self.icmp_checkbox = QtWidgets.QCheckBox("ICMP")
        self.protocol_layout = QtWidgets.QHBoxLayout()
        self.protocol_layout.addWidget(self.udp_checkbox)
        self.protocol_layout.addWidget(self.tcp_checkbox)
        self.protocol_layout.addWidget(self.icmp_checkbox)

        
        self.create_init_form()
        # Buttons
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button = QtWidgets.QPushButton("Buscar")
        self.button.clicked.connect(self.enviar_dados)
        self.button_layout.addWidget(self.button)
        self.advanced_options_button = QtWidgets.QPushButton("Opções Avançadas")
        self.advanced_options_button.clicked.connect(self.show_advanced_options)
        self.button_layout.addWidget(self.advanced_options_button)

        self.main_frame_layout.addLayout(self.button_layout)

        # Advanced options UI
        self.setup_advanced_options()

    def create_init_form(self):
        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Digite um dominio ou endereço ip válido:"), self.address_entry)
        layout.addRow(QtWidgets.QLabel("Escolha um dispositivo de rede: "), self.combo_box)
       
        layout.addRow(QtWidgets.QLabel("Escolha os protocolos que voce deseja enviar: "), self.protocol_layout)

        layout.addRow(QtWidgets.QLabel("Escolha os tipos de protocolo ip: "), self.ipv_layout)
        self.main_frame_layout.addWidget(self.formGroupBox)
        self.formGroupBox.setLayout(layout)

    def create_advanced_form(self):
        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Digite a quantidade maxima de TTL's:"), self.ttl_entry)
        layout.addRow(QtWidgets.QLabel("Digite o tempo de timeout:"), self.timeout_entry)
        layout.addRow(QtWidgets.QLabel("Digite a quantidade de tentativas em um endereço:"), self.attempts_entry)
        self.advanced_options_frame_layout.addLayout(layout)

    def setup_advanced_options(self):
        self.ttl_entry = QtWidgets.QLineEdit()
        self.ttl_entry.setText("30")
        self.advanced_options_frame_layout.addWidget(self.ttl_entry)

        self.timeout_entry = QtWidgets.QLineEdit()
        self.timeout_entry.setText("5")
        self.advanced_options_frame_layout.addWidget(self.timeout_entry)

        self.attempts_entry = QtWidgets.QLineEdit()
        self.attempts_entry.setText("3")
        self.advanced_options_frame_layout.addWidget(self.attempts_entry)

        self.create_advanced_form()
        self.close_button = QtWidgets.QPushButton("Voltar")
        self.close_button.clicked.connect(self.hide_advanced_options)
        self.advanced_options_frame_layout.addWidget(self.close_button)

    def enviar_dados(self):
        selected_item = ([device for device in self.devices if device[0] == self.combo_box.currentText()] or [""])[0]
        address = self.address_entry.text()
        ttl = self.ttl_entry.text()
        timeout = self.timeout_entry.text()
        attempts = self.attempts_entry.text()
        print("Selected Item:", selected_item)
        print("Address:", address)
        print("TTL:", ttl)
        print("Timeout:", timeout)
        print("Attempts:", attempts)
        tr.DEVICE_NAME = selected_item[0]
        # tr.start(address, int(ttl), int(timeout), int(attempts))
        self.close()

    def show_advanced_options(self):
        self.main_frame.setVisible(False)
        self.advanced_options_frame.setVisible(True)

    def hide_advanced_options(self):
        self.advanced_options_frame.setVisible(False)
        self.main_frame.setVisible(True)

class ImageWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Image Window')
        self.setGeometry(200, 200, 800, 600)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)

        self.graphics_view = QtWidgets.QGraphicsView()
        self.graphics_scene = QtWidgets.QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)

        self.scroll.setWidget(self.graphics_view)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.scroll)

        self.add_button = QtWidgets.QPushButton("Add Router")
        self.add_button.clicked.connect(self.add_router)
        main_layout.addWidget(self.add_button)

        self.setLayout(main_layout)

        self.svg_items = []
        self.add_initial_router()

    def add_initial_router(self):
        center_x = self.graphics_view.width() // 2
        center_y = self.graphics_view.height() // 2
        initial_position = self.graphics_view.mapToScene(center_x, center_y)
        svg_item = self.place_router((initial_position.x(), initial_position.y()), "Você")
        self.svg_items.append(svg_item)
        self.center_on_item(svg_item)

    def place_router(self, position, description):
        svg_item = QtSvg.QGraphicsSvgItem('router.svg')
        svg_item.setFlags(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable or 
                          QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        svg_item.setPos(position[0], position[1])
        self.graphics_scene.addItem(svg_item)

        label_x = position[0]
        label_y = position[1] + svg_item.boundingRect().height() + 5
        description_label = QtWidgets.QGraphicsTextItem(description)
        description_label.setDefaultTextColor(QtCore.Qt.GlobalColor.black)
        description_label.setPos(label_x, label_y)

        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(12)
        description_label.setFont(font)

        self.graphics_scene.addItem(description_label)

        return svg_item

    def add_router(self):
        max_attempts = 100
        for _ in range(max_attempts):
            last_item = self.svg_items[-1] if self.svg_items else None
            last_position = last_item.pos() if last_item else QtCore.QPointF(0, 0)
            offset_x = random.randint(-200, 200)
            offset_y = random.randint(-200, 200)
            new_position = (last_position.x() + offset_x, last_position.y() + offset_y)
            if not self.check_collision(new_position):
                break
        else:
            print("Failed to place a new router without collision.")
            return

        new_router_description = f"Router {len(self.svg_items) + 1}"
        new_svg_item = self.place_router(new_position, new_router_description)
        self.svg_items.append(new_svg_item)

        if last_item:
            line = QtWidgets.QGraphicsLineItem(
                last_item.boundingRect().center().x() + last_item.pos().x(),
                last_item.boundingRect().center().y() + last_item.pos().y(),
                new_svg_item.boundingRect().center().x() + new_svg_item.pos().x(),
                new_svg_item.boundingRect().center().y() + new_svg_item.pos().y())
            line.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.black, 2))
            self.graphics_scene.addItem(line)

    def check_collision(self, position, margin=50):
        for item in self.svg_items:
            item_rect = item.sceneBoundingRect()
            new_rect = QtCore.QRectF(position[0] - margin, position[1] - margin, 
                                     item_rect.width() + 2 * margin, 
                                     item_rect.height() + 2 * margin)
            if new_rect.intersects(item_rect):
                return True
        return False

    def center_on_item(self, item):
        self.graphics_view.centerOn(item)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    traceroute_window = TracerouteUI()
    traceroute_window.show()

    image_window = ImageWindow()

    traceroute_window.button.clicked.connect(image_window.show)
    sys.exit(app.exec_())
