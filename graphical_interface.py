from PyQt5 import QtWidgets, QtGui, QtCore, QtSvg
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import random
from util import get_active_devices
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

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Input form widget
        self.input_form_widget = QtWidgets.QWidget()
        self.stacked_widget.addWidget(self.input_form_widget)
        self.input_form_layout = QtWidgets.QVBoxLayout(self.input_form_widget)

        self.formGroupBox = QtWidgets.QGroupBox("Preencha os campos do traceroute: ")
        self.input_form_layout.addWidget(self.formGroupBox)

        self.address_entry = QtWidgets.QLineEdit()

        device_names = [device[0] for device in self.devices]
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItems(device_names)
        self.combo_box.setCurrentText("Escolha um dispositivo: ")

        self.ipv4_checkbox = QtWidgets.QCheckBox("IPv4")
        self.ipv6_checkbox = QtWidgets.QCheckBox("IPv6")
        self.ipv_layout = QtWidgets.QHBoxLayout()
        self.ipv4_checkbox.click()
        self.ipv_layout.addWidget(self.ipv4_checkbox)
        self.ipv_layout.addWidget(self.ipv6_checkbox)

        self.radio_layout = QtWidgets.QHBoxLayout()
         
        self.radio_sim = QtWidgets.QRadioButton('Sim')
        self.radio_nao = QtWidgets.QRadioButton('Não')
        self.radio_nao.click()
        self.radio_layout.addWidget(self.radio_sim)
        self.radio_layout.addWidget(self.radio_nao)

        self.udp_checkbox = QtWidgets.QCheckBox("UDP")
        self.tcp_checkbox = QtWidgets.QCheckBox("TCP")
        self.icmp_checkbox = QtWidgets.QCheckBox("ICMP")
        self.protocol_layout = QtWidgets.QHBoxLayout()
        self.udp_checkbox.click()
        self.protocol_layout.addWidget(self.udp_checkbox)
        self.protocol_layout.addWidget(self.tcp_checkbox)
        self.protocol_layout.addWidget(self.icmp_checkbox)

        
        self.create_init_form()
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button = QtWidgets.QPushButton("Buscar")
        self.button.clicked.connect(self.enviar_dados)
        self.button_layout.addWidget(self.button)
        self.advanced_options_button = QtWidgets.QPushButton("Opções Avançadas")
        self.advanced_options_button.clicked.connect(self.show_advanced_options)
        self.button_layout.addWidget(self.advanced_options_button)

        self.input_form_layout.addLayout(self.button_layout)

        self.advanced_options_frame = QtWidgets.QWidget()
        self.advanced_options_frame_layout = QtWidgets.QVBoxLayout(self.advanced_options_frame)
        self.advanced_options_frame.setVisible(False)
        self.input_form_layout.addWidget(self.advanced_options_frame)

        self.setup_advanced_options()

        # Visualization widget
        self.visualization_widget = ImageWindow()
        self.stacked_widget.addWidget(self.visualization_widget)

    def create_init_form(self):
        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Digite um dominio ou endereço ip válido:"), self.address_entry)
        layout.addRow(QtWidgets.QLabel("Escolha um dispositivo de rede: "), self.combo_box)
        layout.addRow(QtWidgets.QLabel("Escolha os protocolos que voce deseja enviar: "), self.protocol_layout)
        layout.addRow(QtWidgets.QLabel("Escolha os tipos de protocolo ip: "), self.ipv_layout)
       
        layout.addRow(QtWidgets.QLabel("Você deseja visualizar a posição geográfica dos roteadores? : "), self.radio_layout)

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

    
   
    def show_advanced_options(self):
        self.advanced_options_frame.setVisible(True)

    def hide_advanced_options(self):
        self.advanced_options_frame.setVisible(False)


    def start_traceroute(self, address, ttl, timeout, attempts, with_geoinfo, protocols):
        self.traceroute_thread = TracerouteThread(address, ttl, timeout, attempts, with_geoinfo, protocols)
        self.traceroute_thread.update_output_signal.connect(self.visualization_widget.update_output)
        self.traceroute_thread.add_router_signal.connect(self.visualization_widget.add_router)
        self.traceroute_thread.start()

    def enviar_dados(self):
        selected_item = ([device for device in self.devices if device[0] == self.combo_box.currentText()] or [""])[0]
        address = self.address_entry.text()
        ttl = self.ttl_entry.text()
        timeout = self.timeout_entry.text()
        attempts = self.attempts_entry.text()
        with_geoinfo = self.radio_sim.isChecked()
      
        isUDP = self.udp_checkbox.isChecked()
        isTCP = self.tcp_checkbox.isChecked()
        isICMP= self.icmp_checkbox.isChecked()
           
        protocols = []
        if isUDP:
            protocols.append("UDP")
        if isTCP:
            protocols.append("TCP")
        if isICMP:
            protocols.append("ICMP")
       
        print(protocols)
        tr.DEVICE_NAME = selected_item[0]
        self.start_traceroute(address, int(ttl), int(timeout), int(attempts),with_geoinfo, protocols)
        self.stacked_widget.setCurrentWidget(self.visualization_widget)
        self.visualization_widget.clear_scene()

class ImageWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Traceroute')
        self.setGeometry(200, 200, 1000, 700)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)

        self.graphics_view = QtWidgets.QGraphicsView()
        self.graphics_scene = QtWidgets.QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)

        self.scroll.setWidget(self.graphics_view)

        main_layout = QtWidgets.QVBoxLayout(self)

        # Zoom buttons layout
        zoom_layout = QtWidgets.QVBoxLayout()
        self.zoom_out_button = QtWidgets.QPushButton("-")
        self.zoom_out_button.setFixedSize(30, 30)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_in_button = QtWidgets.QPushButton("+")
        self.zoom_in_button.setFixedSize(30, 30)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        zoom_layout.addWidget(self.zoom_out_button)
        zoom_layout.addWidget(self.zoom_in_button)
        zoom_layout.addStretch()

        # Add the zoom layout and graphics view to a horizontal layout
        display_layout = QtWidgets.QHBoxLayout()
        display_layout.addLayout(zoom_layout)
        display_layout.addWidget(self.scroll)

        main_layout.addLayout(display_layout, stretch=2)

        self.output_text = QtWidgets.QTextEdit()
        self.output_text.setReadOnly(True)
        main_layout.addWidget(self.output_text, stretch=1)

        self.setLayout(main_layout)
        self.svg_items = []

        self.initial_zoom()

    def initial_zoom(self):
        self.graphics_view.scale(0.5, 0.5)

    def zoom_in(self):
        self.graphics_view.scale(1.2, 1.2)

    def zoom_out(self):
        self.graphics_view.scale(0.8, 0.8)

    def add_initial_router(self, description="Você"):
        center_x = self.graphics_view.width() // 2
        center_y = self.graphics_view.height() // 2
        initial_position = self.graphics_view.mapToScene(center_x, center_y)
        svg_item = self.place_router((initial_position.x(), initial_position.y()), description, src="./img/desktop.svg")
        self.svg_items.append(svg_item)
        self.center_on_item(svg_item)

    def place_router(self, position, description, unreachable=False, src="./img/router.svg"):
        if unreachable:
            src = './img/gray_router.svg'
        svg_item = QtSvg.QGraphicsSvgItem(src)
            
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

    def add_router(self, address, ping_time=None):
        description = f"{address} ({ping_time:.2f} ms)" if ping_time else address

        last_item = self.svg_items[-1] if self.svg_items else None
        last_position = last_item.pos() if last_item else QtCore.QPointF(0, 0)
        max_attempts = 100
        for _ in range(max_attempts):
            offset_x = random.randint(-200, 200)
            offset_y = random.randint(-200, 200)
            new_position = (last_position.x() + offset_x, last_position.y() + offset_y)
            if not self.check_collision(new_position):
                break
        else:
            self.update_output("Failed to place a new router without collision.")
            return

        unreachable = address == "*"
        new_svg_item = self.place_router(new_position, description, unreachable=unreachable)
        self.svg_items.append(new_svg_item)

        if last_item:
            line = QtWidgets.QGraphicsLineItem(
                last_item.boundingRect().center().x() + last_item.pos().x(),
                last_item.boundingRect().center().y() + last_item.pos().y(),
                new_svg_item.boundingRect().center().x() + new_svg_item.pos().x(),
                new_svg_item.boundingRect().center().y() + new_svg_item.pos().y())
            line.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.black, 2))
            self.graphics_scene.addItem(line)

    def update_router_info(self, address, addr_info):
        for item in self.svg_items:
            if address in item.description:  # Check if address is part of the description
                item.description += f"\n{addr_info}"
                break

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

    def start_traceroute(self):
        self.clear_scene()
        self.add_initial_router()


    def update_output(self, message):
        self.output_text.append(message)

    def clear_scene(self):
        self.output_text.clear()
        self.svg_items = []
        self.graphics_scene.clear()
        self.add_initial_router()

class TracerouteThread(QThread):
    update_output_signal = pyqtSignal(str)
    add_router_signal = pyqtSignal(str)

    def __init__(self, address, ttl, timeout, attempts, with_geoinfo, protocols):
        super().__init__()
        self.address = address
        self.ttl = ttl
        self.timeout = timeout
        self.attempts = attempts
        self.with_geoinfo = with_geoinfo
        self.protocols = protocols

    def run(self):
        tr.start(self.address, self.ttl, self.timeout, self.attempts,
                 update_output=self.update_output, add_router=self.add_router, with_geoinfo=self.with_geoinfo, protocols=self.protocols)

    def update_output(self, message):
        self.update_output_signal.emit(message)

    def add_router(self, description):
        self.add_router_signal.emit(description)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    traceroute_window = TracerouteUI()
    traceroute_window.show()
    sys.exit(app.exec_())
