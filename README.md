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

*   Imagenes del proyecto funcionando

*   <img width="1918" height="727" alt="dashboard" src="https://github.com/user-attachments/assets/e852ef8c-7012-4601-84b3-9d70cee24ca3" />
<img width="1918" height="922" alt="generarVenta" src="https://github.com/user-attachments/assets/12ce9b6d-38e3-49a3-a32b-552109d05e29" />
<img width="1918" height="923" alt="inventario" src="https://github.com/user-attachments/assets/c4f78368-7adb-4d17-86f5-4224e8b3c5f3" />
<img width="1918" height="1077" alt="login" src="https://github.com/user-attachments/assets/6c4a9722-7ea4-41b6-914e-d0916814017a" />
<img width="1918" height="883" alt="productos" src="https://github.com/user-attachments/assets/4e6b0808-d986-4c85-b728-8c0f3004e918" />
<img width="1918" height="1078" alt="reportes" src="https://github.com/user-attachments/assets/672150ad-5d62-486a-8adc-b2299e3ea44b" />
<img width="1918" height="1078" alt="resumen_ventas" src="https://github.com/user-attachments/assets/407c6698-1433-4410-9adf-c40bce57d6a6" />
<img width="1918" height="966" alt="venta_generada" src="https://github.com/user-attachments/assets/dc51f676-3166-4b6f-ab56-6f9853a2a69b" />
<img width="1918" height="1078" alt="apertura_caja" src="https://github.com/user-attachments/assets/81b8f5e6-a0ea-42bc-8ae8-a8ba75f8b69d" />
<img width="1918" height="821" alt="caja_abierta" src="https://github.com/user-attachments/assets/9f24eb15-0006-4926-9a89-39e56a24cae5" />
<img width="1918" height="892" alt="cerrar_caja" src="https://github.com/user-attachments/assets/0a48cc73-ff3c-46b6-9480-b968cc2b70d8" />

