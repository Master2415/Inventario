import os
import sys
import subprocess

# Nombre del ejecutable
APP_NAME = "SistemaInventario"

# Archivo principal
MAIN_SCRIPT = "Inventario.py"

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"{package} no encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = importlib.import_module(package)

def build():
    # Asegurar que PyInstaller está instalado e importado
    try:
        import PyInstaller.__main__
    except ImportError:
        install_and_import('PyInstaller')
        import PyInstaller.__main__

    print("Iniciando compilación con PyInstaller...")
    
    args = [
        MAIN_SCRIPT,
        '--name=%s' % APP_NAME,
        '--onefile',  # Crear un solo archivo ejecutable
        '--windowed', # No mostrar consola (para aplicaciones GUI)
        '--clean',    # Limpiar caché antes de construir
        '--noconfirm', # No confirmar sobreescritura
        
        # Importaciones ocultas que a veces PyInstaller no detecta
        '--hidden-import=mysql.connector',
        '--hidden-import=tkcalendar',
        '--hidden-import=babel.numbers',
        
        # Incluir carpetas de código fuente
        '--paths=.',
    ]
    
    PyInstaller.__main__.run(args)
    print(f"\n¡Compilación completada! El ejecutable está en la carpeta 'dist/{APP_NAME}.exe'")

if __name__ == "__main__":
    build()
