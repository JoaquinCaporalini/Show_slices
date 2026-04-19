#!/bin/bash

echo "Iniciando proceso de empaquetado del programa..."

# Asegurarse de estar en el directorio correcto
cd "$(dirname "$0")"

if [ "$1" == "-exe" ]; then
    echo "¡Detectada la bandera -exe! Preparando compilación cruzada hacia Windows (.exe) usando Docker..."
    if ! command -v docker &> /dev/null; then
        echo "Error: Docker no está instalado o no se encuentra en el PATH. Es necesario para generar ejecutables de Windows desde Linux."
        exit 1
    fi
    echo "Obteniendo el emulador Docker. Esto descargará la imagen y construirá las versiones .whl de Windows (tardará unos minutos la primera vez)..."
    docker run --rm -v "$(pwd):/src" tobix/pyinstaller-windows:python3.11 "pip install -r requirements.txt && pyinstaller --onefile --windowed --name LectorPDF --icon=lambdito.ico --add-data \"lambdito.png;.\" --add-data \"lambdito.ico;.\" main.py"
    echo "Proceso finalizado. Puedes encontrar tu ejecutable LectorPDF.exe en la carpeta 'dist/'."
else
    # Comprobar si el venv existe
    if [ ! -d "venv" ]; then
        echo "El entorno virtual no existe. Ejecuta run_presentation.sh o instálalo manualmente primero."
        exit 1
    fi

    echo "Activando el entorno virtual de forma nativa para Linux..."
    source venv/bin/activate

    echo "Asegurando que PyInstaller esté instalado..."
    pip install pyinstaller

    echo "Generando ejecutable autónomo nativo..."
    pyinstaller --onefile --windowed --name "LectorPDF" --icon="lambdito.ico" --add-data "lambdito.png:." --add-data "lambdito.ico:." main.py

    echo "Proceso finalizado. Puedes encontrar tu programa listo en la carpeta 'dist/'."
    echo "Para moverlo al nivel actual, ejecutando:"
    echo "cp dist/LectorPDF ."
fi
