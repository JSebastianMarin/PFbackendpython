# Movimientos Financieros – Backend Django

## Descripción

API REST para la gestión de movimientos financieros personales (ingresos y gastos), con autenticación de usuarios, reportes y documentación interactiva.

---

## Características principales

- **CRUD de movimientos**: Crea, consulta, edita y elimina ingresos/gastos.
- **Vinculación a usuario**: Cada movimiento pertenece a un usuario autenticado.
- **Filtros avanzados**: Por fecha, categoría, monto, etc.
- **Reportes**: Resumen y reporte mensual de ingresos/gastos.
- **Autenticación por token**: Registro, login y protección de endpoints.
- **Documentación interactiva**: Swagger UI y ReDoc.
- **Base de datos PostgreSQL**: Configuración profesional y escalable.

---

## Instalación rápida

1. **Clona el repositorio y entra al proyecto**
2. **Instala dependencias**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configura tu base de datos PostgreSQL**  
   Crea la base de datos y el usuario, y configura el archivo `.env`:
   ```
   DB_NAME=movimientos_financieros
   DB_USER=postgres
   DB_PASSWORD=tu_password
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=tu_clave_secreta
   DEBUG=True
   ```
4. **Aplica migraciones**
   ```bash
   python manage.py migrate
   ```
5. **Crea un superusuario (opcional)**
   ```bash
   python manage.py createsuperuser
   ```
6. **Ejecuta el servidor**
   ```bash
   python manage.py runserver
   ```

---

## Endpoints principales

| Método | Endpoint                            | Descripción                      |
| ------ | ----------------------------------- | -------------------------------- |
| POST   | `/api/registro/`                    | Registro de usuario              |
| POST   | `/api/login/`                       | Login y obtención de token       |
| GET    | `/api/movimientos/`                 | Listar movimientos (autenticado) |
| POST   | `/api/movimientos/`                 | Crear movimiento                 |
| GET    | `/api/movimientos/{id}/`            | Ver detalle de movimiento        |
| PUT    | `/api/movimientos/{id}/`            | Editar movimiento                |
| DELETE | `/api/movimientos/{id}/`            | Eliminar movimiento              |
| GET    | `/api/movimientos/resumen/`         | Resumen de ingresos/gastos       |
| GET    | `/api/movimientos/reporte_mensual/` | Reporte mensual                  |

---

## Autenticación

- **Registro:**  
  `POST /api/registro/`  
  Body: `{ "username": "...", "password": "...", "email": "..." }`

- **Login:**  
  `POST /api/login/`  
  Body: `{ "username": "...", "password": "..." }`  
  Respuesta: `{ "token": "..." }`

- **Usa el token en el header:**
  ```
  Authorization: Token TU_TOKEN
  ```

---

## Documentación interactiva

- **Swagger UI:**  
  [https://pfbackendpy.uvdev.online/api/docs/](https://pfbackendpy.uvdev.online/api/docs/)

- **ReDoc:**  
  [https://pfbackendpy.uvdev.online/api/redoc/](https://pfbackendpy.uvdev.online/api/redoc/)

---

## Ejemplo de uso (crear movimiento)

1. **Autorízate en Swagger con tu token**
2. **POST /api/movimientos/**
   ```json
   {
     "descripcion": "Pago de alquiler",
     "monto": "800.00",
     "categoria": "gasto",
     "fecha": "2024-07-05",
     "notas": "Alquiler de julio"
   }
   ```

---

## Recomendaciones de seguridad

- No subas tu archivo `.env` ni archivos de base de datos al repositorio.
- Usa contraseñas seguras y cambia el `SECRET_KEY` en producción.
- Haz backups regulares de tu base de datos PostgreSQL.

---

## Créditos

Desarrollado con Django, Django REST Framework y PostgreSQL.
