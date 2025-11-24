# Guía de Portabilidad y Docker

Este proyecto ha sido configurado para ser portable y ejecutable en entornos Linux y Docker.

## Requisitos Previos
- **Docker Desktop** instalado.
- **Servidor X11** (para ver la interfaz gráfica desde Docker):
  - **Windows**: Instalar [VcXsrv](https://sourceforge.net/projects/vcxsrv/).
  - **Linux**: Generalmente ya incluido.

## Ejecución con Docker Compose (Recomendado)

1. **Configurar X11 en Windows (VcXsrv)**:
   - Ejecutar XLaunch.
   - Seleccionar "Multiple windows".
   - **Importante**: Marcar "Disable access control".
   - Finalizar configuración.

2. **Construir y Ejecutar**:
   Abrir una terminal en la carpeta del proyecto y ejecutar:
   ```bash
   docker-compose up --build
   ```

3. **Notas**:
   - La base de datos MySQL se iniciará automáticamente en el puerto 3306.
   - La aplicación intentará conectarse a la base de datos usando las variables de entorno definidas en `docker-compose.yml`.

## Ejecución Manual en Linux (Sin Docker)

1. **Instalar dependencias del sistema**:
   ```bash
   sudo apt-get update
   sudo apt-get install python3-tk python3-pip
   ```

2. **Instalar librerías Python**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**:
   ```bash
   python Inventario.py
   ```

## Variables de Entorno
El archivo `Conexion/Conexion.py` ahora soporta las siguientes variables de entorno para configurar la base de datos sin modificar el código:
- `DB_HOST`: Host de la base de datos (default: `localhost`)
- `DB_NAME`: Nombre de la base de datos (default: `inventario`)
- `DB_USER`: Usuario (default: `root`)
- `DB_PASSWORD`: Contraseña (default: `root`)
