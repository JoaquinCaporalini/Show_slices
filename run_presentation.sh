#!/bin/bash

# Moverse al directorio donde está el script para evitar problemas de rutas
cd "$(dirname "$0")"

# Comprobar si el entorno virtual existe; si no, crearlo e instalar dependencias
if [ ! -d "venv" ]; then
    echo "El entorno virtual (venv) no se detectó. Creando uno nuevo..."
    python3 -m venv venv
    echo "Instalando dependencias necesarias desde requirements.txt..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    # Activar el entorno virtual si ya existe
    source venv/bin/activate
fi

# Ejecutar la aplicación
python3 main.py
