"""
Oaky Desktop - Sistema de Gestión de Precios y Stock
Aplicación de escritorio para tienda de ropa usando Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from database import Database


class OakyDesktopApp:
    """Aplicación principal"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🛍️ Oaky Desktop - Gestión de Precios y Stock")
        self.root.geometry("1400x900")
        
        # Base de datos
        self.db = Database()
        
        # Variables
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search)
        
        # Crear interfaz
        self.create_widgets()
        
        # Cargar productos
        self.load_products()
        self.update_stats()
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Header
        header_frame = tk.Frame(self.root, bg='#2563eb', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🛍️ Oaky Desktop",
            font=('Arial', 24, 'bold'),
            bg='#2563eb',
            fg='white'
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Sistema de Gestión de Precios y Stock",
            font=('Arial', 12),
            bg='#2563eb',
            fg='white'
        )
        subtitle_label.pack()
        
        # Panel de estadísticas
        self.create_stats_panel()
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestañas
        self.create_search_tab()
        self.create_bulk_tab()
        self.create_import_tab()
    
    def create_stats_panel(self):
        """Crea el panel de estadísticas"""
        stats_frame = tk.Frame(self.root, bg='#f8fafc', height=120)
        stats_frame.pack(fill='x', padx=10, pady=10)
        stats_frame.pack_propagate(False)
        
        # Variables de estadísticas
        self.stat_products = tk.StringVar(value="0")
        self.stat_value = tk.StringVar(value="$0.00")
        self.stat_stock = tk.StringVar(value="0")
        self.stat_low = tk.StringVar(value="0")
        
        # Crear tarjetas
        self.create_stat_card(stats_frame, "📦", "Total Productos", self.stat_products, '#667eea', 0)
        self.create_stat_card(stats_frame, "💰", "Valor Inventario", self.stat_value, '#f093fb', 1)
        self.create_stat_card(stats_frame, "📊", "Unidades Stock", self.stat_stock, '#4facfe', 2)
        self.create_stat_card(stats_frame, "⚠️", "Stock Bajo", self.stat_low, '#fa8231', 3)
    
    def create_stat_card(self, parent, icon, label, var, color, col):
        """Crea una tarjeta de estadística"""
        card = tk.Frame(parent, bg=color, relief='raised', bd=2)
        card.grid(row=0, column=col, padx=10, pady=10, sticky='nsew')
        parent.grid_columnconfigure(col, weight=1)
        
        icon_label = tk.Label(card, text=icon, font=('Arial', 32), bg=color, fg='white')
        icon_label.pack(side='left', padx=20)
        
        info_frame = tk.Frame(card, bg=color)
        info_frame.pack(side='left', fill='both', expand=True)
        
        value_label = tk.Label(
            info_frame,
            textvariable=var,
            font=('Arial', 18, 'bold'),
            bg=color,
            fg='white'
        )
        value_label.pack(anchor='w')
        
        desc_label = tk.Label(
            info_frame,
            text=label,
            font=('Arial', 10),
            bg=color,
            fg='white'
        )
        desc_label.pack(anchor='w')
    
    def create_search_tab(self):
        """Crea la pestaña de búsqueda"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔍 Búsqueda y Productos")
        
        # Barra de búsqueda
        search_frame = tk.Frame(tab)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Arial', 12),
            width=50
        )
        search_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        search_entry.insert(0, "🔍 Buscar por código de barras o nombre...")
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, 'end') if search_entry.get().startswith('🔍') else None)
        
        new_btn = tk.Button(
            search_frame,
            text="➕ Nuevo Producto",
            command=self.create_product,
            bg='#2563eb',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        new_btn.pack(side='left')
        
        # Tabla de productos
        table_frame = tk.Frame(tab)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame)
        y_scroll.pack(side='right', fill='y')
        
        x_scroll = ttk.Scrollbar(table_frame, orient='horizontal')
        x_scroll.pack(side='bottom', fill='x')
        
        # Treeview (tabla)
        self.tree = ttk.Treeview(
            table_frame,
            columns=('Código', 'Nombre', 'Precio', 'Stock', 'Estado'),
            show='headings',
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )
        
        y_scroll.config(command=self.tree.yview)
        x_scroll.config(command=self.tree.xview)
        
        # Configurar columnas
        self.tree.heading('Código', text='Código de Barras')
        self.tree.heading('Nombre', text='Nombre del Producto')
        self.tree.heading('Precio', text='Precio')
        self.tree.heading('Stock', text='Stock')
        self.tree.heading('Estado', text='Estado')
        
        self.tree.column('Código', width=150)
        self.tree.column('Nombre', width=400)
        self.tree.column('Precio', width=120)
        self.tree.column('Stock', width=80)
        self.tree.column('Estado', width=120)
        
        self.tree.pack(fill='both', expand=True)
        
        # Menú contextual
        self.tree.bind('<Double-Button-1>', self.edit_product_from_tree)
        self.tree.bind('<Button-3>', self.show_context_menu)
    
    def create_bulk_tab(self):
        """Crea la pestaña de actualización masiva"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💰 Actualización Masiva")
        
        # Frame principal
        main_frame = tk.Frame(tab)
        main_frame.pack(fill='both', expand=True, padx=50, pady=50)
        
        # Título
        title = tk.Label(
            main_frame,
            text="💰 Actualización Masiva de Precios",
            font=('Arial', 18, 'bold')
        )
        title.pack(pady=20)
        
        # Info
        info = tk.Label(
            main_frame,
            text="Aplica un porcentaje de aumento o descuento a los precios.\n"
                 "Valores positivos aumentan, valores negativos reducen.",
            font=('Arial', 11),
            fg='#64748b'
        )
        info.pack(pady=10)
        
        # Entrada de porcentaje
        input_frame = tk.Frame(main_frame)
        input_frame.pack(pady=20)
        
        tk.Label(
            input_frame,
            text="Porcentaje:",
            font=('Arial', 12)
        ).pack(side='left', padx=10)
        
        self.percentage_var = tk.StringVar()
        percentage_entry = tk.Entry(
            input_frame,
            textvariable=self.percentage_var,
            font=('Arial', 14),
            width=15
        )
        percentage_entry.pack(side='left')
        
        tk.Label(
            input_frame,
            text="%",
            font=('Arial', 14)
        ).pack(side='left', padx=5)
        
        # Botón aplicar
        apply_btn = tk.Button(
            main_frame,
            text="📊 Aplicar Cambios a TODOS los Productos",
            command=self.apply_bulk_price_update,
            bg='#10b981',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=30,
            pady=15,
            relief='flat',
            cursor='hand2'
        )
        apply_btn.pack(pady=30)
        
        # Ejemplo
        example = tk.Label(
            main_frame,
            text="Ejemplos:\n"
                 "• Ingresa 10 para aumentar precios 10%\n"
                 "• Ingresa -15 para reducir precios 15%",
            font=('Arial', 10),
            fg='#64748b',
            justify='left'
        )
        example.pack(pady=10)
    
    def create_import_tab(self):
        """Crea la pestaña de importar/exportar"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📁 Importar/Exportar")
        
        main_frame = tk.Frame(tab)
        main_frame.pack(fill='both', expand=True, padx=50, pady=30)
        
        # Sección Importar
        import_label = tk.Label(
            main_frame,
            text="📥 Importar Productos desde CSV",
            font=('Arial', 16, 'bold')
        )
        import_label.pack(anchor='w', pady=(0, 10))
        
        import_info = tk.Label(
            main_frame,
            text="Importa productos desde un archivo CSV.\n"
                 "El archivo debe tener las columnas: barcode,name,price,stock",
            font=('Arial', 10),
            fg='#64748b',
            justify='left'
        )
        import_info.pack(anchor='w', pady=(0, 10))
        
        import_btn = tk.Button(
            main_frame,
            text="📁 Seleccionar Archivo CSV",
            command=self.import_csv,
            bg='#2563eb',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2'
        )
        import_btn.pack(anchor='w', pady=(0, 30))
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=20)
        
        # Sección Exportar
        export_label = tk.Label(
            main_frame,
            text="📤 Exportar Productos a CSV",
            font=('Arial', 16, 'bold')
        )
        export_label.pack(anchor='w', pady=(0, 10))
        
        export_info = tk.Label(
            main_frame,
            text="Exporta todos tus productos a un archivo CSV.\n"
                 "Ideal para hacer copias de seguridad.",
            font=('Arial', 10),
            fg='#64748b',
            justify='left'
        )
        export_info.pack(anchor='w', pady=(0, 10))
        
        export_btn = tk.Button(
            main_frame,
            text="💾 Exportar a CSV",
            command=self.export_csv,
            bg='#10b981',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2'
        )
        export_btn.pack(anchor='w', pady=(0, 30))
        
        # Ejemplo CSV
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=20)
        
        example_label = tk.Label(
            main_frame,
            text="📋 Ejemplo de Archivo CSV",
            font=('Arial', 16, 'bold')
        )
        example_label.pack(anchor='w', pady=(0, 10))
        
        example_text = tk.Text(
            main_frame,
            height=5,
            font=('Courier', 10),
            bg='#f8fafc',
            relief='solid',
            bd=1
        )
        example_text.pack(fill='x', pady=(0, 10))
        example_text.insert('1.0',
            'barcode,name,price,stock\n'
            '1K437610-12M,"PACK 2 SHORTS LUNARES",28608,15\n'
            '1K480410-6M,"SET 4 PIEZAS REMERA",35592,8\n'
            '1N616510-3M,"BODY MUSCULOSA Y SHORT",22907,20'
        )
        example_text.config(state='disabled')
    
    def load_products(self, search_term=""):
        """Carga productos en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener productos
        products = self.db.search_products(search_term)
        
        # Agregar a tabla
        for product in products:
            stock = product['stock']
            
            # Determinar estado
            if stock == 0:
                estado = "🔴 Sin Stock"
                tag = 'red'
            elif stock < 5:
                estado = "🟡 Stock Bajo"
                tag = 'yellow'
            else:
                estado = "🟢 En Stock"
                tag = 'green'
            
            self.tree.insert(
                '',
                'end',
                values=(
                    product['barcode'],
                    product['name'],
                    f"${product['price']:,.2f}",
                    stock,
                    estado
                ),
                tags=(tag,)
            )
        
        # Configurar colores
        self.tree.tag_configure('red', background='#fee2e2')
        self.tree.tag_configure('yellow', background='#fef3c7')
        self.tree.tag_configure('green', background='#d1fae5')
    
    def update_stats(self):
        """Actualiza las estadísticas"""
        stats = self.db.get_stats()
        self.stat_products.set(f"{stats['total_products']:,}")
        self.stat_value.set(f"${stats['total_value']:,.2f}")
        self.stat_stock.set(f"{stats['total_stock']:,}")
        self.stat_low.set(f"{stats['low_stock']:,}")
    
    def on_search(self, *args):
        """Maneja la búsqueda"""
        search_text = self.search_var.get()
        if not search_text.startswith('🔍'):
            self.load_products(search_text)
    
    def create_product(self):
        """Abre ventana para crear producto"""
        ProductDialog(self.root, self.db, self.refresh_data)
    
    def edit_product_from_tree(self, event):
        """Edita el producto seleccionado"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        barcode = item['values'][0]
        
        product = self.db.get_product(barcode)
        if product:
            ProductDialog(self.root, self.db, self.refresh_data, product)
    
    def show_context_menu(self, event):
        """Muestra menú contextual"""
        selection = self.tree.selection()
        if not selection:
            return
        
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="✏️ Editar", command=lambda: self.edit_product_from_tree(event))
        menu.add_command(label="🗑️ Eliminar", command=self.delete_selected_product)
        
        menu.post(event.x_root, event.y_root)
    
    def delete_selected_product(self):
        """Elimina el producto seleccionado"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        barcode = item['values'][0]
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este producto?"):
            if self.db.delete_product(barcode):
                messagebox.showinfo("Éxito", "Producto eliminado exitosamente")
                self.refresh_data()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto")
    
    def apply_bulk_price_update(self):
        """Aplica actualización masiva de precios"""
        try:
            percentage = float(self.percentage_var.get())
        except ValueError:
            messagebox.showerror("Error", "Ingresa un porcentaje válido")
            return
        
        if percentage == 0:
            messagebox.showerror("Error", "El porcentaje no puede ser 0")
            return
        
        action = "aumentar" if percentage > 0 else "reducir"
        products = self.db.get_all_products()
        
        if messagebox.askyesno(
            "Confirmar",
            f"¿Estás seguro de {action} el precio de {len(products)} productos en {abs(percentage)}%?"
        ):
            if self.db.update_prices_bulk(percentage):
                messagebox.showinfo("Éxito", "Precios actualizados exitosamente")
                self.refresh_data()
            else:
                messagebox.showerror("Error", "No se pudieron actualizar los precios")
    
    def import_csv(self):
        """Importa productos desde CSV"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                products_data = []
                
                for row in reader:
                    if 'price' in row:
                        row['price'] = row['price'].strip().replace(' ', '')
                    products_data.append(row)
            
            result = self.db.import_from_csv_data(products_data)
            
            msg = f"Importación completada:\n\n"
            msg += f"✅ Nuevos productos: {result['imported']}\n"
            msg += f"🔄 Productos actualizados: {result['updated']}\n"
            msg += f"📊 Total procesados: {result['total']}\n"
            
            if result['errors']:
                msg += f"\n⚠️ Errores: {len(result['errors'])}"
            
            messagebox.showinfo("Importación Completada", msg)
            self.refresh_data()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar archivo:\n{str(e)}")
    
    def export_csv(self):
        """Exporta productos a CSV"""
        file_path = filedialog.asksaveasfilename(
            title="Guardar archivo CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="productos-oaky.csv"
        )
        
        if not file_path:
            return
        
        try:
            products = self.db.get_all_products()
            
            with open(file_path, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=['barcode', 'name', 'price', 'stock']
                )
                writer.writeheader()
                
                for product in products:
                    writer.writerow({
                        'barcode': product['barcode'],
                        'name': product['name'],
                        'price': product['price'],
                        'stock': product['stock']
                    })
            
            messagebox.showinfo(
                "Éxito",
                f"Productos exportados exitosamente a:\n{file_path}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar:\n{str(e)}")
    
    def refresh_data(self):
        """Refresca todos los datos"""
        self.load_products()
        self.update_stats()


class ProductDialog:
    """Diálogo para crear/editar producto"""
    
    def __init__(self, parent, db, callback, product=None):
        self.db = db
        self.callback = callback
        self.product = product
        
        # Crear ventana
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Producto" if product else "Nuevo Producto")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Crea los widgets del diálogo"""
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title = tk.Label(
            main_frame,
            text="✏️ Editar Producto" if self.product else "➕ Nuevo Producto",
            font=('Arial', 16, 'bold')
        )
        title.pack(pady=(0, 20))
        
        # Formulario
        form_frame = tk.Frame(main_frame)
        form_frame.pack(fill='both', expand=True)
        
        # Código de barras
        tk.Label(form_frame, text="Código de Barras *:", font=('Arial', 10)).grid(
            row=0, column=0, sticky='w', pady=10
        )
        self.barcode_var = tk.StringVar(value=self.product['barcode'] if self.product else "")
        barcode_entry = tk.Entry(form_frame, textvariable=self.barcode_var, font=('Arial', 11), width=30)
        barcode_entry.grid(row=0, column=1, pady=10, sticky='ew')
        if self.product:
            barcode_entry.config(state='disabled')  # No editable
        
        # Nombre
        tk.Label(form_frame, text="Nombre *:", font=('Arial', 10)).grid(
            row=1, column=0, sticky='w', pady=10
        )
        self.name_var = tk.StringVar(value=self.product['name'] if self.product else "")
        tk.Entry(form_frame, textvariable=self.name_var, font=('Arial', 11), width=30).grid(
            row=1, column=1, pady=10, sticky='ew'
        )
        
        # Precio
        tk.Label(form_frame, text="Precio (ARS) *:", font=('Arial', 10)).grid(
            row=2, column=0, sticky='w', pady=10
        )
        self.price_var = tk.StringVar(value=str(self.product['price']) if self.product else "0")
        tk.Entry(form_frame, textvariable=self.price_var, font=('Arial', 11), width=30).grid(
            row=2, column=1, pady=10, sticky='ew'
        )
        
        # Stock
        tk.Label(form_frame, text="Stock *:", font=('Arial', 10)).grid(
            row=3, column=0, sticky='w', pady=10
        )
        self.stock_var = tk.StringVar(value=str(self.product['stock']) if self.product else "0")
        tk.Entry(form_frame, textvariable=self.stock_var, font=('Arial', 11), width=30).grid(
            row=3, column=1, pady=10, sticky='ew'
        )
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            command=self.dialog.destroy,
            bg='#64748b',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="Actualizar" if self.product else "Crear",
            command=self.save,
            bg='#2563eb',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=5)
    
    def save(self):
        """Guarda el producto"""
        barcode = self.barcode_var.get().strip()
        name = self.name_var.get().strip()
        
        try:
            price = float(self.price_var.get())
            stock = int(self.stock_var.get())
        except ValueError:
            messagebox.showerror("Error", "Precio y Stock deben ser números válidos")
            return
        
        # Validaciones
        if not barcode:
            messagebox.showerror("Error", "El código de barras es obligatorio")
            return
        
        if not name:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        
        if price <= 0:
            messagebox.showerror("Error", "El precio debe ser mayor a 0")
            return
        
        if stock < 0:
            messagebox.showerror("Error", "El stock no puede ser negativo")
            return
        
        # Guardar
        if self.product:
            # Actualizar
            if self.db.update_product(barcode, name, price, stock):
                messagebox.showinfo("Éxito", "Producto actualizado exitosamente")
                self.callback()
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el producto")
        else:
            # Crear
            if self.db.add_product(barcode, name, price, stock):
                messagebox.showinfo("Éxito", "Producto creado exitosamente")
                self.callback()
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", "Ya existe un producto con ese código de barras")


def main():
    """Función principal"""
    root = tk.Tk()
    app = OakyDesktopApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
