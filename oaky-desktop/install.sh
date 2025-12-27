#!/bin/bash

# Script de instalación para Oaky Desktop (Python)
# Este script configura el entorno e instala las dependencias

echo "🛍️  Instalando Oaky Desktop (Python)..."
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python no está instalado."
        echo "Por favor instala Python 3.8 o superior desde https://www.python.org/"
        exit 1
    fi
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

echo "✅ Python detectado: $($PYTHON_CMD --version)"
echo ""

# Verificar pip
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "❌ pip no está instalado."
    echo "Por favor instala pip"
    exit 1
fi

echo "✅ pip detectado"
echo ""

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
$PYTHON_CMD -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Error al crear el entorno virtual."
    exit 1
fi

echo "✅ Entorno virtual creado"
echo ""

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error al activar el entorno virtual."
    exit 1
fi

echo "✅ Entorno virtual activado"
echo ""

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ¡Instalación completada exitosamente!"
    echo ""
    echo "🚀 Para iniciar la aplicación, ejecuta:"
    echo "   source venv/bin/activate"
    echo "   python main.py"
    echo ""
    echo "O simplemente ejecuta:"
    echo "   ./run.sh"
    echo ""
    echo "📚 Para más información, consulta README.md"
else
    echo ""
    echo "❌ Error durante la instalación de dependencias."
    echo "Por favor verifica los errores y vuelve a intentar."
    exit 1
fi
