# INSTALACIÓN Y USO RÁPIDO - OAKY DESKTOP

## 📋 Instalación en 3 pasos:

### 1️⃣ Crear entorno virtual (recomendado)

```bash
cd oaky-desktop
python -m venv venv
```

### 2️⃣ Activar el entorno virtual

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3️⃣ Instalar dependencias y ejecutar

```bash
pip install -r requirements.txt
python main.py
```

¡Listo! La aplicación se abrirá automáticamente.

---

## 🚀 Ejecución rápida (después de la primera vez)

```bash
cd oaky-desktop
source venv/bin/activate  # Linux/Mac
python main.py
```

---

## 📥 Importar productos del CSV existente

Si quieres cargar los productos del archivo `products.csv` de la carpeta raíz:

1. Abre la aplicación
2. Ve a la pestaña **"📁 Importar/Exportar"**
3. Haz click en **"📁 Seleccionar Archivo CSV"**
4. Navega hasta `/home/milena/Documents/projects/oaky/products.csv`
5. Selecciona el archivo
6. ¡Verás un reporte de cuántos productos se importaron!

---

## ✨ Funcionalidades Principales

### 🔍 Búsqueda de Productos
- **Ubicación**: Pestaña "Búsqueda y Productos"
- Escribe en la barra de búsqueda
- Busca por código de barras o nombre
- Resultados instantáneos

### ➕ Crear Producto Individual
- **Botón**: "➕ Nuevo Producto"
- Completa: Código de barras, Nombre, Precio, Stock
- El código de barras debe ser único

### ✏️ Editar Producto
- Haz click en "✏️ Editar" en cualquier producto
- Modifica los campos (excepto código de barras)
- Guarda los cambios

### 🗑️ Eliminar Producto
- Haz click en el botón 🗑️ de cualquier producto
- Confirma la eliminación

### 💰 Actualización Masiva de Precios
- **Ubicación**: Pestaña "Actualización Masiva"
- Click en "📊 Abrir Actualización Masiva"
- Ingresa un porcentaje:
  - Positivo: aumenta precios (ej: 10 = +10%)
  - Negativo: reduce precios (ej: -10 = -10%)
- Opcionalmente selecciona productos específicos
- Aplica cambios

### 📁 Importar CSV
- **Ubicación**: Pestaña "Importar/Exportar"
- Formato requerido: `barcode,name,price,stock`
- Los productos existentes se actualizan
- Los nuevos se agregan

### 📤 Exportar CSV
- **Ubicación**: Pestaña "Importar/Exportar"
- Exporta todos los productos a CSV
- Ideal para backups

---

## 📊 Estadísticas

En la parte superior verás en tiempo real:
- Total de productos
- Valor total del inventario
- Unidades en stock
- Productos con stock bajo (< 5 unidades)

---

## 🎨 Indicadores de Stock

- 🟢 **Verde (En Stock)**: 5 o más unidades
- 🟡 **Amarillo (Stock Bajo)**: 1-4 unidades
- 🔴 **Rojo (Sin Stock)**: 0 unidades

---

## ⚠️ Notas Importantes

1. **Códigos de barras únicos**: No puede haber dos productos con el mismo código
2. **Backups**: Exporta regularmente a CSV para tener copias de seguridad
3. **Base de datos**: Se crea automáticamente como `oaky.db` en la misma carpeta
4. **Entorno virtual**: Recuerda activarlo cada vez que uses la aplicación

---

## 🐛 Solución Rápida de Problemas

### Si algo no funciona:
```bash
# Desactiva y reactiva el entorno virtual
deactivate
source venv/bin/activate

# Reinstala las dependencias
pip install --force-reinstall -r requirements.txt

# Ejecuta
python main.py
```

### Si la base de datos da error:
```bash
# Exporta tus productos primero (desde la app)
# Luego elimina la base de datos
rm oaky.db

# Reinicia la aplicación
python main.py

# Importa de nuevo tus productos desde el CSV
```

---

**¡Disfruta usando Oaky Desktop! 🛍️**
