# Sistema de Inventario y Ventas

Este es un sistema integral de gestión empresarial (ERP simplificado) desarrollado en Python utilizando `tkinter` para la interfaz gráfica y MySQL como motor de base de datos. Está diseñado para pequeñas y medianas empresas que requieren administrar su inventario, ventas, nómina y configuración operativa de manera eficiente y centralizada.
Este sistema permite a un punto de venta operar completamente offline, controlando ventas, inventario, empleados y finanzas desde la misma computadora. Solo necesita internet si quieres respaldo remoto, actualizaciones o integración con servicios externos, pero para la operación diaria, funciona perfectamente sin conexión.

## 🚀 Características Principales

### 🛒 Punto de Venta (POS) y Facturación
*   **Registro de Ventas**: Interfaz ágil para procesar ventas, con búsqueda de productos y carrito de compras.
*   **Generación de Recibos**: Emisión automática de tirillas de venta (recibos) con formato profesional, incluyendo datos de la empresa, cliente y detalle de productos.
*   **Gestión de Clientes**: Registro y selección de clientes durante la venta.

### 📦 Gestión de Inventario
*   **Control de Stock**: Monitoreo en tiempo real de existencias.
*   **Administración de Productos**: Creación, edición y eliminación de productos con precios y categorías.
*   **Proveedores**: Gestión de la base de datos de proveedores.

### 💰 Nómina y Finanzas
*   **Sistema de Nómina**:
    *   Cálculo de pagos a empleados por **Horas Trabajadas** o **Monto Fijo** (Bonos/Adelantos).
    *   Registro histórico de pagos realizados.
    *   Interfaz dedicada para la gestión de pagos a empleados.
*   **Cálculo de Utilidad**:
    *   Reporte financiero que calcula la **Utilidad Neta** real.
    *   Fórmula: `(Ventas - Costo Mercancía) - Nómina Pagada`.
    *   Filtrado por rangos de fecha para análisis precisos.

### ⚙️ Administración y Configuración
*   **Configuración de Empresa**: Panel para personalizar los datos del negocio (Nombre, NIT/RUT, Dirección, Slogan, Mensaje del Recibo) que aparecen en los documentos generados.
*   **Gestión de Usuarios y Roles**: Control de acceso basado en roles (Administrador, Cajero, etc.).
*   **Reportes**: Generación de informes exportables a CSV (Ventas, Inventario, Empleados).

### 🔧 Portabilidad y Despliegue
*   **Docker**: Soporte completo para despliegue en contenedores (App + BD).
*   **Instalador Windows**: Script incluido para generar un ejecutable `.exe` standalone para fácil distribución.

## 📋 Requisitos Previos

*   Python 3.10+
*   MySQL Server 8.0+
*   Librerías Python (ver `requirements.txt`)

## 🛠️ Instalación y Ejecución

### Opción 1: Ejecución Local (Desarrollo)

1.  **Clonar el repositorio**:
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd Inventario
    ```

2.  **Crear entorno virtual e instalar dependencias**:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    
    pip install -r requirements.txt
    ```

3.  **Configurar Base de Datos**:
    *   Asegúrate de tener MySQL corriendo.
    *   Importa el script SQL ubicado en `script_baseDatos/` (si aplica) o deja que la aplicación inicialice las tablas.
    *   Configura las credenciales en `Conexion/Conexion.py` o usa variables de entorno (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`).

4.  **Ejecutar la aplicación**:
    ```bash
    python Inventario.py
    ```

### Opción 2: Docker

Para ejecutar el proyecto usando contenedores Docker (incluyendo la base de datos), consulta la guía detallada:
👉 [Guía de Docker](README_DOCKER.md)

### Opción 3: Generar Ejecutable (.exe)

Para crear un archivo ejecutable portable para Windows, consulta la guía de instalación:
👉 [Guía de Instalador](README_INSTALLER.md)

## 📂 Estructura del Proyecto

*   `Conexion/`: Lógica de conexión a base de datos.
*   `Model/`: Objetos de Acceso a Datos (DAO) y lógica de negocio (Ventas, Nómina, Configuración, etc.).
*   `View/`: Interfaces gráficas (Ventanas y Frames) construidas con Tkinter.
*   `Windows/`: Ventanas auxiliares y configuración principal de la GUI.
*   `script_baseDatos/`: Scripts SQL para inicializar la BD.
*   `build_exe.py`: Script para compilar el proyecto a .exe.


*   **Autor**: [Douglas](https://github.com/Master2415)
