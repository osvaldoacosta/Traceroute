from time import sleep
from PyQt5 import QtWidgets, QtGui, QtCore, QtSvg
from PyQt5.QtCore import QPointF, QThread, Qt, pyqtSignal
import sys
import random
from util import get_active_devices
import traceroute as tr
import math


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

        self.ipv4_radio= QtWidgets.QRadioButton("IPv4")
        self.ipv6_radio= QtWidgets.QRadioButton("IPv6")
        self.ipv_layout = QtWidgets.QHBoxLayout()
        self.ipv_layout.addWidget(self.ipv4_radio)
        self.ipv_layout.addWidget(self.ipv6_radio)
        self.ipv_button_group = QtWidgets.QButtonGroup()
        self.ipv4_radio.click()
        self.ipv_button_group.addButton(self.ipv4_radio)
        self.ipv_button_group.addButton(self.ipv6_radio)

        self.radio_button_group = QtWidgets.QButtonGroup()
         
        self.radio_layout = QtWidgets.QHBoxLayout()
        self.radio_sim = QtWidgets.QRadioButton('Sim')
        self.radio_nao = QtWidgets.QRadioButton('Não')
        self.radio_nao.click()
        self.radio_button_group.addButton(self.radio_sim)
        self.radio_button_group.addButton(self.radio_nao)
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
        layout.addRow(QtWidgets.QLabel("Escolha um tipo de protocolo ip: "), self.ipv_layout)
       
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


    def start_traceroute(self, address, ttl, timeout, attempts, with_geoinfo, protocols,isIPV6):
        self.traceroute_thread = TracerouteThread(address, ttl, timeout, attempts, with_geoinfo, protocols, isIPV6)
        self.traceroute_thread.update_output_signal.connect(self.visualization_widget.update_output)
        self.traceroute_thread.add_router_signal.connect(self.visualization_widget.add_router)
        self.traceroute_thread.protocol_start_signal.connect(self.visualization_widget.on_protocol_start)
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
      
        isIPV6 = self.ipv6_radio.isChecked()
        tr.DEVICE_NAME = selected_item[0]
        self.start_traceroute(address, int(ttl), int(timeout), int(attempts),with_geoinfo, protocols, isIPV6)
        self.stacked_widget.setCurrentWidget(self.visualization_widget)
        self.visualization_widget.clear_scene()

class ImageWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.router_positions = {} # Ele usa o endereço do roteador como chave e o valor seria a posição na tela
        self.hasAlreadyStarted = False
        self.arrowColors = {
                "TCP": QtCore.Qt.GlobalColor.blue,
                "UDP": QtCore.Qt.GlobalColor.red,
                "ICMP": QtCore.Qt.GlobalColor.green,
        } 

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

    def add_initial_router(self, description="EU"):
        center_x = self.graphics_view.width() // 2
        center_y = self.graphics_view.height() // 2
        initial_position = self.graphics_view.mapToScene(center_x, center_y)
        svg_item = self.place_router((initial_position.x(), initial_position.y()), description, src="./img/desktop.svg")
        self.svg_items.append(svg_item)
        self.center_on_item(svg_item)

    def on_protocol_start(self):
        if self.svg_items:
            self.svg_items.append(self.svg_items[0])
       
        self.hasAlreadyStarted = True


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

    
    def add_router(self, address_info,ping_time,protocol):
        last_item = self.svg_items[-1] if self.svg_items else None

        if address_info in self.router_positions and "*" not in address_info:
            new_position = self.router_positions[address_info]
        else:
            last_position = last_item.pos() if last_item else QtCore.QPointF(0, 0)
            max_attempts = 100
            for _ in range(max_attempts):
                offset_x = random.randint(-500, 500)
                offset_y = random.randint(-500, 500)
                new_position = (last_position.x() + offset_x, last_position.y() + offset_y)
                if not self.check_collision(new_position):
                    break
            else:
                self.update_output("Failed to place a new router without collision.")
                return

            self.router_positions[address_info] = new_position

        unreachable = "*" in address_info
        new_svg_item = self.place_router(new_position, address_info, unreachable=unreachable)
        self.svg_items.append(new_svg_item)

        if last_item:
            self.draw_curved_line_with_arrow(last_item, new_svg_item, ping_time,protocol)

    def draw_curved_line_with_arrow(self, start_item, end_item, ping_time,protocol):
        start_pos = start_item.boundingRect().center() + start_item.pos()
        end_pos = end_item.boundingRect().center() + end_item.pos()

        path = QtGui.QPainterPath()
        path.moveTo(start_pos)

        # Offset for multiple arrows to the same position
        offset_x = random.randint(-100, 100)
        offset_y = random.randint(-100, 100)
        control_point = QPointF((start_pos.x() + end_pos.x()) / 2 + offset_x, (start_pos.y() + end_pos.y()) / 2 + offset_y)
        path.quadTo(control_point, end_pos)

        path_item = QtWidgets.QGraphicsPathItem(path)
        path_item.setPen(QtGui.QPen(self.arrowColors[protocol], 2))
        self.graphics_scene.addItem(path_item)

        self.add_arrowhead(path,protocol)
        if ping_time is not None:
            self.add_ping_time_text(path, ping_time,protocol)

    def add_arrowhead(self, path,protocol):
        # Calculate position for the arrowhead
        end_point = path.pointAtPercent(1.0)
        tangent = path.angleAtPercent(1.0)
        angle_rad = math.radians(tangent)

        arrow_size = 10
        p1 = end_point + QPointF(math.sin(angle_rad - math.pi / 3) * arrow_size,
                                 math.cos(angle_rad - math.pi / 3) * arrow_size)
        p2 = end_point + QPointF(math.sin(angle_rad - math.pi + math.pi / 3) * arrow_size,
                                 math.cos(angle_rad - math.pi + math.pi / 3) * arrow_size)

        arrow_head = QtGui.QPolygonF([end_point, p1, p2])
        arrow_item = QtWidgets.QGraphicsPolygonItem(arrow_head)
        arrow_item.setBrush(self.arrowColors[protocol])
        self.graphics_scene.addItem(arrow_item)

    def add_ping_time_text(self, path, ping_time,protocol):
        midpoint = path.pointAtPercent(0.5)
        text_item = QtWidgets.QGraphicsTextItem(ping_time)
        text_item.setDefaultTextColor(self.arrowColors[protocol])
        text_item.setPos(midpoint)
        font = text_item.font()
        font.setPointSize(10)
        font.setBold(True)
        text_item.setFont(font)
        self.graphics_scene.addItem(text_item)

    def update_router_info(self, address, addr_info):
        for item in self.svg_items:
            if address in item.description:  # Check if address is part of the description
                item.description += f"\n{addr_info}"
                break

    def check_collision(self, position, margin=100):
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
        if not self.hasAlreadyStarted:
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
    add_router_signal = pyqtSignal(str,str,str)
    protocol_start_signal = pyqtSignal()


    def __init__(self, address, ttl, timeout, attempts, with_geoinfo, protocols,isIPV6):
        super().__init__()
        self.address = address
        self.ttl = ttl
        self.timeout = timeout
        self.attempts = attempts
        self.with_geoinfo = with_geoinfo
        self.protocols = protocols
        self.isIPV6 = isIPV6
    def run(self):
        #Deixa de forma sequencial para melhor entendimento
        for protocol in self.protocols:
            tr.start(self.address, self.ttl, self.timeout, self.attempts,
                    update_output=self.update_output, add_router=self.add_router, with_geoinfo=self.with_geoinfo,
                    protocol=protocol,isIPV6=self.isIPV6)

            sleep(3) #TODO: DESCOBRIR O PQ DISSO FUNCIONAR
            self.protocol_start_signal.emit()

    def update_output(self, message):
        self.update_output_signal.emit(message)

    def add_router(self, description,ping_time,protocol):
        self.add_router_signal.emit(description,ping_time,protocol)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    traceroute_window = TracerouteUI()
    traceroute_window.show()
    sys.exit(app.exec_())
