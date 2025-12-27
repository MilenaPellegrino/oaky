"""
Módulo de base de datos para Oaky Desktop
Maneja todas las operaciones con SQLite
"""

import sqlite3
import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class Database:
    """Clase para manejar la base de datos de productos"""
    
    def __init__(self, db_path: str = "oaky.db"):
        """
        Inicializa la conexión a la base de datos
        
        Args:
            db_path: Ruta al archivo de base de datos
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establece la conexión a la base de datos"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
        self.cursor = self.conn.cursor()
    
    def _create_tables(self):
        """Crea las tablas necesarias si no existen"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear índices para mejorar búsquedas
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_barcode ON products(barcode)
        """)
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_name ON products(name)
        """)
        
        self.conn.commit()
    
    def search_products(self, search_term: str = "") -> List[Dict]:
        """
        Busca productos por código de barras o nombre
        
        Args:
            search_term: Término de búsqueda
            
        Returns:
            Lista de productos encontrados
        """
        if not search_term.strip():
            # Si no hay término de búsqueda, devolver todos
            self.cursor.execute("""
                SELECT * FROM products ORDER BY name
            """)
        else:
            self.cursor.execute("""
                SELECT * FROM products 
                WHERE barcode LIKE ? OR LOWER(name) LIKE LOWER(?)
                ORDER BY name
            """, (f"%{search_term}%", f"%{search_term}%"))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_all_products(self) -> List[Dict]:
        """
        Obtiene todos los productos
        
        Returns:
            Lista de todos los productos
        """
        self.cursor.execute("SELECT * FROM products ORDER BY name")
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """
        Obtiene un producto por su ID
        
        Args:
            product_id: ID del producto
            
        Returns:
            Diccionario con datos del producto o None
        """
        self.cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_product_by_barcode(self, barcode: str) -> Optional[Dict]:
        """
        Obtiene un producto por su código de barras
        
        Args:
            barcode: Código de barras
            
        Returns:
            Diccionario con datos del producto o None
        """
        self.cursor.execute("SELECT * FROM products WHERE barcode = ?", (barcode,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def create_product(self, barcode: str, name: str, price: float, stock: int = 0) -> Tuple[bool, str, int]:
        """
        Crea un nuevo producto
        
        Args:
            barcode: Código de barras único
            name: Nombre del producto
            price: Precio
            stock: Cantidad en stock
            
        Returns:
            Tupla (éxito, mensaje, id del producto)
        """
        try:
            self.cursor.execute("""
                INSERT INTO products (barcode, name, price, stock)
                VALUES (?, ?, ?, ?)
            """, (barcode, name, price, stock))
            self.conn.commit()
            return True, "Producto creado exitosamente", self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return False, "Ya existe un producto con ese código de barras", -1
        except Exception as e:
            return False, f"Error: {str(e)}", -1

    # --- Compatibilidad con API usada en la GUI (main.py) ---
    def add_product(self, barcode: str, name: str, price: float, stock: int = 0) -> bool:
        """
        Wrapper que crea un producto y devuelve True/False (compatibilidad con main.py).
        """
        success, _msg, _id = self.create_product(barcode, name, price, stock)
        return success

    def get_product(self, barcode: str) -> Optional[Dict]:
        """
        Wrapper para obtener producto por código de barras (compatibilidad con main.py).
        """
        return self.get_product_by_barcode(barcode)

    
    def update_product(self, *args) -> Tuple[bool, str]:
        """
        Actualiza un producto existente.

        Soporta dos firmas para compatibilidad:
        - update_product(product_id: int, barcode: str, name: str, price: float, stock: int)
        - update_product(barcode: str, name: str, price: float, stock: int)  # actualiza por barcode

        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            # Caso: llamada con product_id primero
            if len(args) == 5 and isinstance(args[0], int):
                product_id, barcode, name, price, stock = args
                self.cursor.execute("""
                    UPDATE products 
                    SET barcode = ?, name = ?, price = ?, stock = ?, 
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (barcode, name, price, stock, product_id))
                self.conn.commit()
                return True, "Producto actualizado exitosamente"

            # Caso: llamada por barcode
            if len(args) == 4 and isinstance(args[0], str):
                barcode, name, price, stock = args
                self.cursor.execute("""
                    UPDATE products 
                    SET name = ?, price = ?, stock = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE barcode = ?
                """, (name, price, stock, barcode))
                self.conn.commit()
                return True, "Producto actualizado exitosamente"

            return False, "Parámetros inválidos para update_product"
        except sqlite3.IntegrityError:
            return False, "Ya existe un producto con ese código de barras"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def delete_product(self, identifier) -> Tuple[bool, str]:
        """
        Elimina un producto por ID o por código de barras.

        Args:
            identifier: ID (int) o barcode (str)

        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            # Si recibe barcode, convertir a id
            if isinstance(identifier, str):
                self.cursor.execute("SELECT id FROM products WHERE barcode = ?", (identifier,))
                row = self.cursor.fetchone()
                if not row:
                    return False, "Producto no encontrado"
                product_id = row[0]
            else:
                product_id = identifier

            self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            self.conn.commit()
            return True, "Producto eliminado exitosamente"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def update_prices_bulk(self, percentage: float, product_ids: List[int] = None) -> Tuple[bool, str]:
        """
        Actualiza precios de forma masiva
        
        Args:
            percentage: Porcentaje de cambio (positivo o negativo)
            product_ids: Lista de IDs de productos (None = todos)
            
        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            multiplier = 1 + (percentage / 100)
            
            if product_ids:
                # Actualizar solo productos específicos
                placeholders = ','.join('?' * len(product_ids))
                self.cursor.execute(f"""
                    UPDATE products 
                    SET price = ROUND(price * ?, 2), 
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id IN ({placeholders})
                """, [multiplier] + product_ids)
            else:
                # Actualizar todos los productos
                self.cursor.execute("""
                    UPDATE products 
                    SET price = ROUND(price * ?, 2),
                        updated_at = CURRENT_TIMESTAMP
                """, (multiplier,))
            
            self.conn.commit()
            affected = self.cursor.rowcount
            return True, f"{affected} producto(s) actualizado(s)"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def import_from_csv_data(self, products_data: List[Dict]) -> Dict:
        """
        Importa productos desde datos CSV
        
        Args:
            products_data: Lista de diccionarios con datos de productos
            
        Returns:
            Diccionario con estadísticas de importación
        """
        imported = 0
        updated = 0
        errors = []
        
        for data in products_data:
            try:
                barcode = data.get('barcode', '').strip()
                name = data.get('name', '').strip()
                price = float(data.get('price', 0))
                stock = int(data.get('stock', 0))
                
                if not barcode or not name or price <= 0:
                    errors.append(f"Datos inválidos: {barcode}")
                    continue
                
                # Verificar si existe
                existing = self.get_product_by_barcode(barcode)
                
                if existing:
                    # Actualizar
                    self.cursor.execute("""
                        UPDATE products 
                        SET name = ?, price = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE barcode = ?
                    """, (name, price, barcode))
                    updated += 1
                else:
                    # Crear nuevo
                    self.cursor.execute("""
                        INSERT INTO products (barcode, name, price, stock)
                        VALUES (?, ?, ?, ?)
                    """, (barcode, name, price, stock))
                    imported += 1
                
            except Exception as e:
                errors.append(f"Error en {data.get('barcode', 'desconocido')}: {str(e)}")
        
        self.conn.commit()
        
        return {
            'imported': imported,
            'updated': updated,
            'errors': errors,
            'total': len(products_data)
        }
    
    def get_stats(self) -> Dict:
        """
        Obtiene estadísticas del inventario
        
        Returns:
            Diccionario con estadísticas
        """
        # Total de productos
        self.cursor.execute("SELECT COUNT(*) FROM products")
        total_products = self.cursor.fetchone()[0]
        
        # Valor total del inventario
        self.cursor.execute("SELECT SUM(price * stock) FROM products")
        total_value = self.cursor.fetchone()[0] or 0
        
        # Total de unidades en stock
        self.cursor.execute("SELECT SUM(stock) FROM products")
        total_stock = self.cursor.fetchone()[0] or 0
        
        # Productos con stock bajo (< 5)
        self.cursor.execute("SELECT COUNT(*) FROM products WHERE stock < 5")
        low_stock = self.cursor.fetchone()[0]
        
        return {
            'total_products': total_products,
            'total_value': round(total_value, 2),
            'total_stock': total_stock,
            'low_stock': low_stock
        }
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if self.conn:
            self.conn.close()
