"""
Diálogos para Oaky Desktop
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QSpinBox,
                             QDoubleSpinBox, QFormLayout, QTextEdit, QProgressBar,
                             QCheckBox, QScrollArea, QWidget)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class ProductDialog(QDialog):
    """Diálogo para crear o editar productos"""
    
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.product = product
        self.is_edit = product is not None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Editar Producto" if self.is_edit else "Nuevo Producto")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # Formulario
        form_layout = QFormLayout()
        
        # Código de barras
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Ej: 1K437610-12M")
        if self.is_edit:
            self.barcode_input.setText(self.product['barcode'])
            self.barcode_input.setEnabled(False)  # No editable en modo edición
        form_layout.addRow("Código de Barras *:", self.barcode_input)
        
        # Nombre
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ej: PACK 2 SHORTS")
        if self.is_edit:
            self.name_input.setText(self.product['name'])
        form_layout.addRow("Nombre del Producto *:", self.name_input)
        
        # Precio
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 999999999)
        self.price_input.setDecimals(2)
        self.price_input.setPrefix("$ ")
        if self.is_edit:
            self.price_input.setValue(self.product['price'])
        form_layout.addRow("Precio (ARS) *:", self.price_input)
        
        # Stock
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 999999)
        if self.is_edit:
            self.stock_input.setValue(self.product['stock'])
        form_layout.addRow("Stock *:", self.stock_input)
        
        layout.addLayout(form_layout)
        
        # Nota
        note_label = QLabel("* Campos obligatorios")
        note_label.setStyleSheet("color: #ef4444; font-size: 11px;")
        layout.addWidget(note_label)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #64748b;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #475569;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Actualizar" if self.is_edit else "Crear")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        save_btn.clicked.connect(self.accept)
        
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(save_btn)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def get_data(self):
        """Obtiene los datos del formulario"""
        return {
            'barcode': self.barcode_input.text().strip(),
            'name': self.name_input.text().strip(),
            'price': self.price_input.value(),
            'stock': self.stock_input.value()
        }
    
    def validate(self):
        """Valida los datos del formulario"""
        data = self.get_data()
        
        if not data['barcode']:
            QMessageBox.warning(self, "Error", "El código de barras es obligatorio")
            return False
        
        if not data['name']:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return False
        
        if data['price'] <= 0:
            QMessageBox.warning(self, "Error", "El precio debe ser mayor a 0")
            return False
        
        if data['stock'] < 0:
            QMessageBox.warning(self, "Error", "El stock no puede ser negativo")
            return False
        
        return True
    
    def accept(self):
        """Sobrescribe accept para validar antes de cerrar"""
        if self.validate():
            super().accept()


class BulkPriceDialog(QDialog):
    """Diálogo para actualización masiva de precios"""
    
    def __init__(self, parent=None, products=None):
        super().__init__(parent)
        self.products = products or []
        self.selected_ids = []
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Actualización Masiva de Precios")
        self.setMinimumWidth(700)
        self.setMinimumHeight(600)
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("💰 Actualización Masiva de Precios")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Porcentaje
        percentage_layout = QFormLayout()
        self.percentage_input = QDoubleSpinBox()
        self.percentage_input.setRange(-100, 1000)
        self.percentage_input.setDecimals(2)
        self.percentage_input.setSuffix(" %")
        self.percentage_input.setValue(0)
        self.percentage_input.valueChanged.connect(self.update_preview)
        percentage_layout.addRow("Porcentaje de Cambio:", self.percentage_input)
        
        help_label = QLabel("Valores positivos aumentan el precio, negativos lo reducen")
        help_label.setStyleSheet("color: #64748b; font-size: 11px;")
        percentage_layout.addRow("", help_label)
        
        layout.addLayout(percentage_layout)
        
        # Vista previa
        self.preview_label = QLabel("Vista previa: Un producto de $1000 pasaría a $1000.00")
        self.preview_label.setStyleSheet("""
            background-color: #f0f9ff;
            border-left: 4px solid #2563eb;
            padding: 10px;
            border-radius: 4px;
        """)
        layout.addWidget(self.preview_label)
        
        # Selección de productos
        selection_label = QLabel("Seleccionar Productos (opcional)")
        selection_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(selection_label)
        
        note_label = QLabel("Si no seleccionas productos, el cambio se aplicará a todos")
        note_label.setStyleSheet("color: #64748b; font-size: 11px;")
        layout.addWidget(note_label)
        
        # Seleccionar todos
        self.select_all_checkbox = QCheckBox("Seleccionar todos")
        self.select_all_checkbox.stateChanged.connect(self.toggle_select_all)
        layout.addWidget(self.select_all_checkbox)
        
        # Lista de productos con checkboxes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(300)
        
        products_widget = QWidget()
        products_layout = QVBoxLayout()
        products_widget.setLayout(products_layout)
        
        self.product_checkboxes = []
        
        for product in self.products:
            checkbox = QCheckBox(
                f"{product['barcode']} - {product['name']} - ${product['price']:,.2f}"
            )
            checkbox.setProperty('product_id', product['id'])
            checkbox.setProperty('price', product['price'])
            checkbox.stateChanged.connect(self.on_checkbox_changed)
            self.product_checkboxes.append(checkbox)
            products_layout.addWidget(checkbox)
        
        products_layout.addStretch()
        scroll.setWidget(products_widget)
        layout.addWidget(scroll)
        
        # Contador de seleccionados
        self.selection_count_label = QLabel("0 producto(s) seleccionado(s)")
        self.selection_count_label.setStyleSheet("color: #2563eb; font-weight: bold;")
        layout.addWidget(self.selection_count_label)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #64748b;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #475569;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        apply_btn = QPushButton("Aplicar Cambios")
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        apply_btn.clicked.connect(self.accept)
        
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(apply_btn)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        self.update_selection_count()
    
    def toggle_select_all(self, state):
        """Selecciona o deselecciona todos los productos"""
        checked = state == Qt.CheckState.Checked.value
        for checkbox in self.product_checkboxes:
            checkbox.setChecked(checked)
    
    def on_checkbox_changed(self):
        """Actualiza el contador cuando cambia una selección"""
        self.update_selection_count()
    
    def update_selection_count(self):
        """Actualiza el contador de productos seleccionados"""
        count = sum(1 for cb in self.product_checkboxes if cb.isChecked())
        self.selection_count_label.setText(f"{count} producto(s) seleccionado(s)")
        
        # Actualizar selected_ids
        self.selected_ids = [
            cb.property('product_id') 
            for cb in self.product_checkboxes 
            if cb.isChecked()
        ]
    
    def update_preview(self):
        """Actualiza la vista previa del cambio de precio"""
        percentage = self.percentage_input.value()
        multiplier = 1 + (percentage / 100)
        new_price = 1000 * multiplier
        self.preview_label.setText(
            f"Vista previa: Un producto de $1000 pasaría a ${new_price:,.2f}"
        )
    
    def get_data(self):
        """Obtiene los datos del diálogo"""
        return {
            'percentage': self.percentage_input.value(),
            'product_ids': self.selected_ids if self.selected_ids else None
        }
    
    def accept(self):
        """Valida y acepta"""
        percentage = self.percentage_input.value()
        
        if percentage == 0:
            QMessageBox.warning(self, "Error", "El porcentaje no puede ser 0")
            return
        
        # Confirmar
        count = len(self.selected_ids) if self.selected_ids else len(self.products)
        action = "aumentar" if percentage > 0 else "reducir"
        
        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Estás seguro de {action} el precio de {count} producto(s) en {abs(percentage)}%?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            super().accept()


class ImportResultDialog(QDialog):
    """Diálogo para mostrar resultados de importación"""
    
    def __init__(self, parent=None, result=None):
        super().__init__(parent)
        self.result = result or {}
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Resultado de Importación")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("✅ Importación Completada")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #10b981;")
        layout.addWidget(title)
        
        # Estadísticas
        stats_layout = QHBoxLayout()
        
        imported_label = QLabel(
            f"<div style='text-align: center;'>"
            f"<div style='font-size: 24px; font-weight: bold; color: #10b981;'>"
            f"{self.result.get('imported', 0)}</div>"
            f"<div>Nuevos Productos</div>"
            f"</div>"
        )
        imported_label.setStyleSheet("""
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        """)
        stats_layout.addWidget(imported_label)
        
        updated_label = QLabel(
            f"<div style='text-align: center;'>"
            f"<div style='font-size: 24px; font-weight: bold; color: #2563eb;'>"
            f"{self.result.get('updated', 0)}</div>"
            f"<div>Productos Actualizados</div>"
            f"</div>"
        )
        updated_label.setStyleSheet("""
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        """)
        stats_layout.addWidget(updated_label)
        
        total_label = QLabel(
            f"<div style='text-align: center;'>"
            f"<div style='font-size: 24px; font-weight: bold; color: #64748b;'>"
            f"{self.result.get('total', 0)}</div>"
            f"<div>Total Procesados</div>"
            f"</div>"
        )
        total_label.setStyleSheet("""
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        """)
        stats_layout.addWidget(total_label)
        
        layout.addLayout(stats_layout)
        
        # Errores si los hay
        errors = self.result.get('errors', [])
        if errors:
            errors_label = QLabel(f"⚠️ Errores encontrados ({len(errors)}):")
            errors_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            errors_label.setStyleSheet("color: #f59e0b;")
            layout.addWidget(errors_label)
            
            errors_text = QTextEdit()
            errors_text.setReadOnly(True)
            errors_text.setMaximumHeight(150)
            errors_text.setPlainText("\n".join(errors[:20]))
            if len(errors) > 20:
                errors_text.append(f"\n... y {len(errors) - 20} errores más")
            layout.addWidget(errors_text)
        
        # Botón cerrar
        close_btn = QPushButton("Cerrar")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.setLayout(layout)
