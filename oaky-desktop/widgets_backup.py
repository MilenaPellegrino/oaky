"""
Widgets personalizados para Oaky Desktop
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFrame, QGridLayout, QCheckBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor


class StatsCard(QFrame):
    """Tarjeta de estadística individual"""
    
    def __init__(self, title: str, value: str, icon: str, color: str):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}, stop:1 #764ba2);
                border-radius: 10px;
                padding: 15px;
            }}
            QLabel {{
                color: white;
                background: transparent;
            }}
        """)
        
        layout = QHBoxLayout()
        
        # Icono
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 36))
        layout.addWidget(icon_label)
        
        # Contenido
        content_layout = QVBoxLayout()
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        content_layout.addWidget(value_label)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10))
        content_layout.addWidget(title_label)
        
        layout.addLayout(content_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        self.setMinimumHeight(100)
        
        # Guardar referencias para actualizar
        self.value_label = value_label
        self.title_label = title_label
    
    def update_value(self, value: str):
        """Actualiza el valor mostrado"""
        self.value_label.setText(value)


class StatsPanel(QWidget):
    """Panel de estadísticas del inventario"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(15)
        
        # Crear tarjetas de estadísticas
        self.total_products_card = StatsCard(
            "Total Productos", "0", "📦", "#667eea"
        )
        self.total_value_card = StatsCard(
            "Valor Total Inventario", "$0", "💰", "#f093fb"
        )
        self.total_stock_card = StatsCard(
            "Unidades en Stock", "0", "📊", "#4facfe"
        )
        self.low_stock_card = StatsCard(
            "Stock Bajo", "0", "⚠️", "#fa8231"
        )
        
        # Agregar al layout en grid
        layout.addWidget(self.total_products_card, 0, 0)
        layout.addWidget(self.total_value_card, 0, 1)
        layout.addWidget(self.total_stock_card, 0, 2)
        layout.addWidget(self.low_stock_card, 0, 3)
        
        self.setLayout(layout)
    
    def update_stats(self, stats: dict):
        """
        Actualiza las estadísticas mostradas
        
        Args:
            stats: Diccionario con las estadísticas
        """
        self.total_products_card.update_value(f"{stats['total_products']:,}")
        self.total_value_card.update_value(f"${stats['total_value']:,.2f}")
        self.total_stock_card.update_value(f"{stats['total_stock']:,}")
        self.low_stock_card.update_value(f"{stats['low_stock']:,}")


class ProductTable(QTableWidget):
    """Tabla personalizada para mostrar productos"""
    
    edit_requested = pyqtSignal(dict)  # Señal cuando se quiere editar
    delete_requested = pyqtSignal(int)  # Señal cuando se quiere eliminar
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.products_data = []
    
    def init_ui(self):
        # Configurar columnas
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels([
            "Código de Barras", "Nombre", "Precio", "Stock", "Estado", "Acciones"
        ])
        
        # Configurar comportamiento
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)
        
        # Ajustar anchos de columnas
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(5, 150)
        
        # Estilos
        self.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
                gridline-color: #e2e8f0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #e0e7ff;
                color: #1e293b;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                font-weight: bold;
                color: #64748b;
            }
        """)
    
    def load_products(self, products: list):
        """
        Carga productos en la tabla
        
        Args:
            products: Lista de productos
        """
        self.products_data = products
        self.setRowCount(len(products))
        
        for row, product in enumerate(products):
            # Código de barras
            barcode_item = QTableWidgetItem(product['barcode'])
            barcode_item.setFont(QFont("Courier New", 10))
            self.setItem(row, 0, barcode_item)
            
            # Nombre
            name_item = QTableWidgetItem(product['name'])
            self.setItem(row, 1, name_item)
            
            # Precio
            price_item = QTableWidgetItem(f"${product['price']:,.2f}")
            price_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            price_item.setForeground(QColor("#10b981"))
            self.setItem(row, 2, price_item)
            
            # Stock
            stock_item = QTableWidgetItem(str(product['stock']))
            stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 3, stock_item)
            
            # Estado de stock
            stock = product['stock']
            if stock == 0:
                status = "Sin Stock"
                color = QColor("#fee2e2")
                text_color = QColor("#991b1b")
            elif stock < 5:
                status = "Stock Bajo"
                color = QColor("#fef3c7")
                text_color = QColor("#92400e")
            else:
                status = "En Stock"
                color = QColor("#d1fae5")
                text_color = QColor("#065f46")
            
            status_item = QTableWidgetItem(status)
            status_item.setBackground(color)
            status_item.setForeground(text_color)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setFont(QFont("Arial", 9, QFont.Weight.Bold))
            self.setItem(row, 4, status_item)
            
            # Botones de acción
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_layout.setSpacing(5)
            
            edit_btn = QPushButton("✏️ Editar")
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #1d4ed8;
                }
            """)
            edit_btn.clicked.connect(lambda checked, p=product: self.edit_requested.emit(p))
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ef4444;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #dc2626;
                }
            """)
            delete_btn.clicked.connect(lambda checked, pid=product['id']: self.delete_requested.emit(pid))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_widget.setLayout(actions_layout)
            
            self.setCellWidget(row, 5, actions_widget)
