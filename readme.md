# Lector de Presentaciones PDF Dual

**Lector de Presentaciones PDF Dual** es una herramienta diseñada específicamente a oradores, académicos y conferencistas. Permite utilizar archivos convencionales en `.pdf` como robustas presentaciones de diapositivas interactivas en un diseño de ventanas duales. 

Mientras tu audiencia ve tu presentación sin distracciones en pantalla completa, tú, como presentador, visualizas un panel de control avanzado que potencia tu oratoria disminuyendo drásticamente tus tiempos muertos.

## Funcionalidades Destacadas

- **Diseño de Interfaz Dual Inteligente:** Abre en automático la presentación en pantalla completa en una segunda pantalla si es conectada.
- **Pre-Visualización de Diapositivas:** Panel nativo con la visualización de la diapositiva en curso gigante para ti, y anticipación/renderizado pre-visualizado de la diapositiva que sigue en un marco más chico.
- **Reloj Integrado para el orador:** Incluye un enorme cronómetro de visibilidad masiva ideal para controlar tu gestión de tiempos al discursar.

## Uso Activo del Lector (Controles de Teclado)
Una vez en ejecución, el Lector provee los atajos de teclado ideales utilizados comúnmente en herramientas pasapáginas:

| Acción a realizar | Teclas Compatibles |
| :------- | :-------- |
| **Avanzar una diapositiva** | `Flecha Derecha`, `Flecha Abajo`, `Avance de Página` |
| **Retroceder una diapositiva** | `Flecha Izquierda`, `Flecha Arriba`, `Retroceso de Página` |
| **Pausar/Reanudar cronómetro** | `Barra Espaciadora`, `P` |
| **Reiniciar tiempo del cronómetro** | `R` (Resetea de golpe a 00:00:00) |
| **Reiniciar demostración total** | `Inicio / Home` |

> *Importante*: Al presionar el botón de **Cerrar (X)** en cualquier de las dos ventanas, se desactivará toda presentación para facilidad del usuario.


## Descarga, Ejecución y Requerimientos

### 1. Requerimientos
Debes poseer en tu ordenador [Python 3](https://www.python.org/downloads/) al igual que `pip` instalados.
No es necesario disponer de las ramas complejas localmente como `PyQt6` ya que el script automatizado puede crearte y descargar un Entorno Virtual puro a tu medida.

### 2. Uso Estándar Autogestionado
La forma más sencilla de iniciar rápidamente este sistema desde su código fuente. Abre tu Terminal en esta carpeta y ejecuta:

```bash
./run_presentation.sh
```
> ***Nota del Script Automático:*** A diferencia del incómodo estándar de invocar los entornos Python a mano, este script verificará si posees los módulos `PyQt6` y `PyMuPDF` empaquetados. Si no los tienes, creará un sub-receptáculo aislado con todas las versiones clonadas para su reproducción intacta garantizada.

Puedes directamente lanzar un archivo particular por defecto sin clics manuales, invocando por terminal o creando un atajo gráfico: 
`./run_presentation.sh "Mi_charla.pdf"` (o `python main.py "Mi_charla.pdf"`)


## Empaquetado Automático del Binario (.exe / Nativo)

Pensando en la comodidad y evitando depender de scripts en la terminal durante las sesiones críticas de demostración, disponemos un script avanzado para convertirlo a una App monolítica.

```bash
# Compilar como ejecutable Nativo en tu propio sistema (Linux)
./build_executable.sh 
```
Posterior al proceso verás la herramienta lista como una `App` tradicional en la carpeta `/dist`.

**Compilación cruzada hacia `.exe` en Windows:**
Puedes construir de todo tu escritorio este programa directo a sus bases binarias de Windows de requerirlo:
```bash
./build_executable.sh -exe
```
*(Para utilizar esta modalidad, asegúrate de mantener Docker instalado y disponible para poder crear este puente).*
