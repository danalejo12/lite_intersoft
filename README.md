# lite_intersoft
app de intersoft lite

Sistema de inventario hecho con Django y PostgreSQL: productos, categorías, clientes, ventas y movimientos de stock.

## Instalación

1. Crear y activar un entorno virtual:
   ```powershell
   python -m venv env
   env\Scripts\activate
   ```
2. Instalar las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
3. Copiar `.env.example` como `.env` y poner tus datos (clave secreta y contraseña de PostgreSQL).
4. Crear la base de datos `lite` en PostgreSQL y aplicar las migraciones:
   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Ejecutar el servidor:
   ```powershell
   python manage.py runserver
   ```

Abrir http://127.0.0.1:8000/ (aplicación) o http://127.0.0.1:8000/admin/ (administrador).
