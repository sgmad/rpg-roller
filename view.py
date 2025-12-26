from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QSpinBox, QLineEdit, 
                             QScrollArea, QFrame, QTextEdit, QLayout)
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QPolygon, QBrush

class RowWidget(QWidget):
    # Base class for rows with a shared layout and delete button
    delete_clicked = pyqtSignal()
    def setup_base(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 2, 0, 2)
        self.layout.setSpacing(6)
        self.del_btn = QPushButton("×")
        self.del_btn.setObjectName("DeleteBtn")
        self.del_btn.setFixedSize(24, 24)
        self.del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.del_btn.clicked.connect(self.delete_clicked.emit)

class StatRow(RowWidget):
    # Entry for custom character stats
    use_clicked = pyqtSignal(str, int)
    def __init__(self, name="", value=10):
        super().__init__()
        self.setup_base()
        self.name_inp = QLineEdit(name)
        self.name_inp.setPlaceholderText("Stat")
        self.name_inp.setFixedWidth(100)
        
        self.val_inp = QSpinBox()
        self.val_inp.setRange(-999, 999)
        self.val_inp.setValue(value)
        self.val_inp.setFixedWidth(80)
        self.val_inp.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.use_btn = QPushButton("➜")
        self.use_btn.setObjectName("UseBtn")
        self.use_btn.setFixedSize(28, 24)
        self.use_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.use_btn.clicked.connect(lambda: self.use_clicked.emit(self.name_inp.text(), self.val_inp.value()))
        
        self.layout.addWidget(self.name_inp)
        self.layout.addWidget(self.val_inp)
        self.layout.addWidget(self.use_btn)
        self.layout.addWidget(self.del_btn)

    def get_data(self):
        return {"name": self.name_inp.text(), "value": self.val_inp.value()}

class DiceRow(RowWidget):
    # Entry for die quantity and faces
    def __init__(self):
        super().__init__()
        self.setup_base()
        self.count_inp = QSpinBox()
        self.count_inp.setSuffix(" d")
        self.count_inp.setFixedWidth(90)
        self.count_inp.setMinimum(1)
        self.count_inp.setValue(1)
        self.count_inp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.face_inp = QSpinBox()
        self.face_inp.setValue(20)
        self.face_inp.setFixedWidth(90)
        self.face_inp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.layout.addWidget(self.count_inp)
        self.layout.addWidget(self.face_inp)
        self.layout.addWidget(self.del_btn)

    def get_values(self):
        return self.count_inp.value(), self.face_inp.value()

class ModRow(RowWidget):
    # Entry for numeric modifiers
    def __init__(self, name="", value=0):
        super().__init__()
        self.setup_base()
        self.name_inp = QLineEdit(name)
        self.name_inp.setPlaceholderText("Reason")
        self.name_inp.setFixedWidth(135)
        
        self.val_inp = QSpinBox()
        self.val_inp.setRange(-999, 999)
        self.val_inp.setValue(value)
        self.val_inp.setFixedWidth(80)
        self.val_inp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.layout.addWidget(self.name_inp)
        self.layout.addWidget(self.val_inp)
        self.layout.addWidget(self.del_btn)

    def get_values(self):
        return self.name_inp.text(), self.val_inp.value()

class RollerView(QMainWindow):
    # Main interface manager handling layout, containers, and size constraints.
    roll_requested = pyqtSignal()
    clear_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPG Roller")
        self.set_icon()
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(6)
        
        # Enforce strict window sizing based on active widgets.
        self.main_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        
        h = QHBoxLayout()
        self.toggle_btn = QPushButton("▼")
        self.toggle_btn.setObjectName("ToggleBtn")
        self.toggle_btn.setFixedSize(24, 24)
        h.addWidget(self.toggle_btn)
        h.addWidget(QLabel("STATS"))
        self.add_stat_btn = QPushButton("+")
        self.add_stat_btn.setFixedSize(36, 36)
        h.addWidget(self.add_stat_btn)
        h.addStretch()
        self.main_layout.addLayout(h)
        
        self.stats_container = QWidget()
        self.stats_layout = QVBoxLayout(self.stats_container)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        self.stats_layout.setSpacing(2)
        
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.stats_container)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(110)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.main_layout.addWidget(self.scroll)

        self.toggle_btn.clicked.connect(self.toggle_stats_panel)

        self.dice_container = QWidget()
        self.dice_layout = QVBoxLayout(self.dice_container)
        self.dice_layout.setContentsMargins(0, 0, 0, 0)
        self.dice_layout.setSpacing(2)
        self.main_layout.addWidget(self.dice_container)

        self.mod_container = QWidget()
        self.mod_layout = QVBoxLayout(self.mod_container)
        self.mod_layout.setContentsMargins(0, 0, 0, 0)
        self.mod_layout.setSpacing(2)
        self.main_layout.addWidget(self.mod_container)

        ctrl = QHBoxLayout()
        self.add_dice_btn = QPushButton("+ Dice")
        self.add_mod_btn = QPushButton("+ Modifier")
        self.clear_btn = QPushButton("Clear")
        ctrl.addWidget(self.add_dice_btn)
        ctrl.addWidget(self.add_mod_btn)
        ctrl.addWidget(self.clear_btn)
        self.main_layout.addLayout(ctrl)

        self.clear_btn.clicked.connect(self.clear_requested.emit)

        self.roll_btn = QPushButton("ROLL")
        self.roll_btn.setObjectName("RollButton")
        self.roll_btn.setFixedHeight(40)
        self.main_layout.addWidget(self.roll_btn)
        self.roll_btn.clicked.connect(self.roll_requested.emit)

        self.log = QTextEdit()
        self.log.setFixedHeight(100)
        self.log.setReadOnly(True)
        self.main_layout.addWidget(self.log)

    def update_window_size(self):
        # Forces the window frame to snap precisely to current content dimensions
        self.main_layout.activate()
        self.setFixedSize(self.main_layout.sizeHint())

    def toggle_stats_panel(self):
        # Toggles stats visibility and triggers an immediate resize update
        is_visible = self.scroll.isVisible()
        self.scroll.setVisible(not is_visible)
        self.toggle_btn.setText("▶" if is_visible else "▼")
        self.update_window_size()

    def set_icon(self):
        # Renders the application icon with correct PyQt6 render hint path
        pixmap = QPixmap(64, 64)
        pixmap.fill(QColor(0, 0, 0, 0))
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor("#a00000")))
        painter.setPen(Qt.PenStyle.NoPen)
        poly = QPolygon([
            QPoint(32, 0), QPoint(62, 16), QPoint(62, 48),
            QPoint(32, 64), QPoint(2, 48), QPoint(2, 16)
        ])
        painter.drawPolygon(poly)
        painter.end()
        self.setWindowIcon(QIcon(pixmap))

    def add_stat_row(self, row): self.stats_layout.addWidget(row)
    def add_dice_row(self, row): self.dice_layout.addWidget(row)
    def add_mod_row(self, row): self.mod_layout.addWidget(row)
