# Guía para Crear Instalador / Ejecutable

Este proyecto incluye un script para generar un archivo ejecutable (`.exe`) independiente, ideal para distribuir la aplicación en computadoras con Windows sin necesidad de instalar Python.

## Pasos para generar el .exe

1.  **Asegúrate de estar en el entorno virtual** (si usas uno).
2.  **Ejecuta el script de construcción**:
    Abre la terminal en la carpeta del proyecto y ejecuta:

    ```bash
    python build_exe.py
    ```

    Este script instalará `pyinstaller` (si no lo tienes) y comenzará el proceso de compilación.

3.  **Localizar el ejecutable**:
    Una vez finalizado, encontrarás tu aplicación en:
    `dist/SistemaInventario.exe`

4.  **Distribuir**:
    Solo necesitas copiar ese archivo `SistemaInventario.exe` a la computadora destino. No se requiere instalar Python ni librerías adicionales en esa máquina.

## Notas Importantes

- **Base de Datos**: El ejecutable **NO** incluye la base de datos MySQL. La computadora donde se ejecute el programa debe tener acceso a un servidor MySQL (local o remoto) y las credenciales deben ser correctas (o configuradas mediante variables de entorno como se explicó en la guía de Docker).
- **Antivirus**: A veces los antivirus detectan los ejecutables creados con PyInstaller como falsos positivos. Esto es normal en aplicaciones no firmadas.
