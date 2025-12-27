#!/bin/bash

# Script para ejecutar Oaky Desktop

echo "🛍️  Iniciando Oaky Desktop..."

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ El entorno virtual no existe."
    echo "Por favor ejecuta primero: ./install.sh"
    exit 1
fi

# Activar entorno virtual
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error al activar el entorno virtual."
    exit 1
fi

# Ejecutar aplicación
python main.py
