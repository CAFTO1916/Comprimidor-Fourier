
Este proyecto es una herramienta académica diseñada para demostrar cómo funciona la compresión de imágenes utilizando la Transformada Rápida de Fourier (FFT). El programa permite visualizar la pérdida de información y calcular métricas de calidad como MSE y PSNR.

----------🚀Características----------

. Transformada de Fourier 2D: Conversión de la imagen del dominio del espacio al dominio de la frecuencia.

. Compresión por Magnitud: Selección de los coeficientes más importantes (top-p%) para reconstruir la imagen.

. Métricas de Calidad: Cálculo automático de Error Cuadrático Medio (MSE) y Relación Señal a Ruido Pico (PSNR).

. Generación de Informes: Creación automática de gráficas comparativas en la carpeta /grafica.

----------🛠️Instalación y Requisitos----------

Ya puedes usar el programa! Encontrarás el ejecutable dentro de la carpeta 'dist', aunque también dejamos un acceso directo en la carpeta principal para que solo tengas que hacer doble clic y listo. :D

Si deseas ejecutar el código fuente desde Python, asegúrate de tener instaladas las siguientes librerías:
pip install opencv-python numpy matplotlib pillow

Ejecución

1.Activa el entorno virtual (opcional):
.\env\Scripts\Activate.ps1

2.Ejecuta el script:
python comprimir_imagen_fourier.py

----------📂Estructura del Proyecto----------

. /dist: Contiene el ejecutable .exe final.

. /grafica: Carpeta donde se guardan automáticamente los informes PSNR (fuera de la carpeta del ejecutable).

. /img: Carpeta destinada a guardar las imágenes procesadas.

. /env: Entorno virtual con las dependencias.

----------🧠 Explicación Técnica----------

El proceso de compresión sigue estos pasos matemáticos:

. FFT2: Se obtiene la representación en frecuencia de la imagen.

. Shift: Se centran las bajas frecuencias para facilitar el filtrado.

. Truncamiento: Se eliminan (convierten a cero) los coeficientes cuya magnitud sea menor al umbral del porcentaje seleccionado.

. IFFT2: Se aplica la transformada inversa para recuperar la imagen comprimida.

----------Notas del Desarrollador----------

. Esta versión está diseñada exclusivamente para Windows. Si intenta ejecutarla en un entorno Linux, el programa presentará errores de compatibilidad.

. ¿Por qué PSNR?: Es una medida de la fidelidad de la reconstrucción. A mayor PSNR, mejor calidad de imagen.

. El programa está programado para detectar si se ejecuta como script o como .exe, asegurando que las gráficas se guarden siempre en la raíz del proyecto Comprimidor Fourier/grafica.

. Tengo hambre :(

