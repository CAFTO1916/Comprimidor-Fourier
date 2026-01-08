import cv2 # Librería para procesamiento de imágenes (Lectura/Escritura)
import numpy as np # Librería fundamental para cálculo numérico y manejo de matrices
import tkinter as tk # Librería estándar para crear interfaces gráficas (GUI)
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt # Librería para generación de gráficas científicas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import os  # Librería para manejar rutas de archivos y creación de directorios

class AppCompresion:

    """
    Clase principal que gestiona la lógica de compresión por Fourier y la Interfaz.
    Cumple con el requerimiento del proyecto escolar.
    """

    def __init__(self, root):

        self.root = root
        self.root.title("Compresor de Imágenes por Fourier - Proyecto Escolar")

        # Variables de estado para almacenar las matrices de la imagen
        self.img_original = None
        self.img_procesada = None
        
        # --- CONFIGURACIÓN DE LA INTERFAZ (GUI) ---

        # --- Panel Lateral de Controles ---
        control_frame = tk.Frame(root, width=200, padx=10, pady=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)


        # Botones de gestión de archivos
        tk.Button(control_frame, text="Cargar Imagen", command=self.cargar_imagen, bg="#e1e1e1").pack(fill=tk.X, pady=2)
        tk.Button(control_frame, text="Quitar Imagen", command=self.quitar_imagen, bg="#ffcccb").pack(fill=tk.X, pady=2)
        

        # Selector de niveles de compresión (Requerimiento de 4 niveles: 5, 10, 20, 40%)
        tk.Label(control_frame, text="\nCoeficientes a mantener (%):", font=('Arial', 9, 'bold')).pack()
        self.opciones_niveles = ["5", "10", "20", "40"]
        self.seleccion_p = tk.StringVar(root)
        self.seleccion_p.set(self.opciones_niveles[1]) # Inicia en 10% por defecto (se puede cambiar el parametro modficando en la linea de codigo "[1]"" )
        
        self.menu_desplegable = tk.OptionMenu(control_frame, self.seleccion_p, *self.opciones_niveles)
        self.menu_desplegable.pack(pady=5, fill=tk.X)

        # Botón principal de procesamiento
        tk.Button(control_frame, text="Comprimir y Calcular", command=self.procesar, bg="lightblue", font=('Arial', 10, 'bold')).pack(fill=tk.X, pady=20)

        # Botones para exportar resultados (Imágenes y Gráficas de reporte)
        tk.Button(control_frame, text="Descargar Imagen", command=self.descargar_imagen, bg="#90ee90").pack(fill=tk.X, pady=2)
        tk.Button(control_frame, text="Generar Informe (Gráfica)", command=self.generar_curva_calidad, bg="#ffeb3b").pack(fill=tk.X, pady=2)

        # Etiquetas para mostrar métricas de error (MSE y PSNR)
        self.label_stats = tk.Label(control_frame, text="\nMétricas:\nMSE: -\nPSNR: -", justify=tk.LEFT)
        self.label_stats.pack(fill=tk.X, pady=10)

        # --- ÁREA DE GRÁFICAS (MATPLOTLIB) ---
        # Definimos dos ejes (ax1 y ax2) para comparar Original vs Reconstruida
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.limpiar_ejes()

    def limpiar_ejes(self):

        """Reinicia los recuadros de visualización."""

        self.ax1.clear()
        self.ax2.clear()
        self.ax1.axis('off')
        self.ax2.axis('off')
        self.ax1.set_title("Original")
        self.ax2.set_title("Reconstruida")
        self.canvas.draw()

    def cargar_imagen(self):

        """Usa OpenCV para leer la imagen y convertirla a escala de grises."""

        ruta_img = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")])
        if ruta_img:
            self.img_original = cv2.imread(ruta_img, cv2.IMREAD_GRAYSCALE)
            self.ax1.imshow(self.img_original, cmap='gray')
            self.ax1.set_title("Original")
            self.ax1.axis('off')
            self.canvas.draw()

    def quitar_imagen(self):

        """Limpia la memoria y la interfaz para iniciar un nuevo análisis."""

        self.img_original = None
        self.img_procesada = None
        self.label_stats.config(text="\nMétricas:\nMSE: -\nPSNR: -")
        self.limpiar_ejes()

    def descargar_imagen(self):

        """Guarda el resultado procesado en el disco duro."""

        if self.img_procesada is None:
            messagebox.showwarning("Advertencia", "No hay imagen procesada.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".jpg")
        if ruta:
            cv2.imwrite(ruta, self.img_procesada)
            messagebox.showinfo("Éxito", "Imagen guardada.")

    def generar_curva_calidad(self):
        """
        Genera el reporte gráfico y lo guarda en la carpeta 'grafica' 
        ubicada en la carpeta principal del proyecto (Comprimidor Fourier).
        """
        if self.img_original is None:
            messagebox.showerror("Error", "Carga una imagen primero.")
            return

        # --- Lógica para encontrar la carpeta del proyecto (Comprimidor Fourier) ---
        # Si es un .exe, usamos sys.executable. Si es .py, usamos __file__
        import sys
        if getattr(sys, 'frozen', False):
            # Estamos en el ejecutable (.exe), subimos un nivel para salir de 'dist'
            ruta_ejecutable = os.path.dirname(sys.executable)
            ruta_proyecto = os.path.dirname(ruta_ejecutable) 
        else:
            # Estamos corriendo el script .py normalmente
            ruta_proyecto = os.path.dirname(os.path.abspath(__file__))

        # Definimos la carpeta 'grafica' dentro de Comprimidor Fourier
        carpeta_destino = os.path.join(ruta_proyecto, "grafica")

        # 1. Asegurar que la carpeta existe en la raíz del proyecto
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)
        
        niveles = [float(n) for n in self.opciones_niveles]
        lista_psnr = []
        
        for p in niveles:
            f_transform = np.fft.fft2(self.img_original)
            f_shift = np.fft.fftshift(f_transform)
            magnitud = np.abs(f_shift)
            umbral = np.percentile(magnitud, 100 - p)
            f_shift_filtrada = f_shift * (magnitud >= umbral)
            img_back = np.abs(np.fft.ifft2(np.fft.ifftshift(f_shift_filtrada)))
            img_back = np.clip(img_back, 0, 255).astype(np.uint8)
            
            mse = np.mean((self.img_original - img_back) ** 2)
            psnr = 20 * np.log10(255.0 / np.sqrt(mse)) if mse > 0 else 100
            lista_psnr.append(psnr)

        # 2. Configuración de la gráfica
        plt.figure(figsize=(6, 4))
        plt.plot(niveles, lista_psnr, 'ro-', linewidth=2)
        plt.title("Curva: Calidad (PSNR) vs Compresión (%)")
        plt.xlabel("Coeficientes conservados (%)")
        plt.ylabel("PSNR (dB)")
        plt.grid(True)
        
        # 3. Construir la ruta absoluta y guardar
        ruta_completa = os.path.join(carpeta_destino, 'curva_calidad_fourier.png')
        plt.savefig(ruta_completa)
        plt.close()
        
        messagebox.showinfo("Informe Listo", f"Gráfica guardada en:\n{ruta_completa}")

    def procesar(self):
        """
        CORAZÓN DEL PROYECTO: Aplica la Transformada de Fourier y el Truncamiento.
        Cumple con la estrategia 'Por magnitud (top-p%)'.
        """

        # 0. Validacion del cargado de imagen.
        if self.img_original is None:
            messagebox.showerror("Error", "Primero carga una imagen")
            return

        # 1. Obtener el porcentaje p del menú desplegable.
        p = float(self.seleccion_p.get())
        
        # 2. Transformada Rápida de Fourier 2D (FFT2)
        # Pasa del dominio del espacio (píxeles) al dominio de la frecuencia (coeficientes complejos)
        f_transform = np.fft.fft2(self.img_original)

        # Centra los componentes de baja frecuencia en el medio de la matriz (Shift)
        f_shift = np.fft.fftshift(f_transform)

        # 3. TRUNCAMIENTO (Compresión)
        # Calculamos la magnitud (valor absoluto) para saber qué coeficientes tienen más 'energía'
        magnitud = np.abs(f_shift)

        # Identificamos el valor umbral (threshold) que deja fuera al (100-p)% de los datos más pequeños
        umbral = np.percentile(magnitud, 100 - p)

        # Aplicamos el filtro: Si la magnitud es < umbral, el coeficiente se vuelve CERO
        f_shift_filtrada = f_shift * (magnitud >= umbral)
        
        # 4. RECONSTRUCCIÓN (Transformada Inversa)
        # Regresamos las frecuencias a su posición original y aplicamos la inversa de Fourier
        img_back = np.abs(np.fft.ifft2(np.fft.ifftshift(f_shift_filtrada)))

        # Aseguramos que los valores estén en el rango de 8 bits (0-255)
        self.img_procesada = np.clip(img_back, 0, 255).astype(np.uint8)

        # 5. CÁLCULO DE MÉTRICAS (Mínimos requeridos)
        # MSE: Promedio de las diferencias al cuadrado entre píxeles
        mse = np.mean((self.img_original - self.img_procesada) ** 2)
        psnr = 20 * np.log10(255.0 / np.sqrt(mse)) if mse > 0 else 100

        # Actualizar la pantalla
        self.ax2.clear()
        self.ax2.imshow(self.img_procesada, cmap='gray')
        self.ax2.set_title(f"Reconstruida ({p}%)")
        self.ax2.axis('off')
        self.canvas.draw()
        self.label_stats.config(text=f"\nMétricas:\nMSE: {mse:.2f}\nPSNR: {psnr:.2f} dB")

# --- BLOQUE DE CIERRE Y EJECUCIÓN ---
if __name__ == "__main__":
    def on_closing():
        """Asegura que el proceso se detenga totalmente al cerrar la X."""
        plt.close('all') # Cierra todas las figuras de matplotlib
        root.quit()      # Detiene el loop de tkinter
        root.destroy()   # Destruye la ventana

    root = tk.Tk()
    app = AppCompresion(root)
    
    # Este protocolo detecta cuando presionas la 'X' de la ventana
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()