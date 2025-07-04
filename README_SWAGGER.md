# API de Movimientos Financieros con Swagger

Este proyecto implementa un sistema completo de gestión de movimientos financieros con documentación automática usando Swagger/OpenAPI.

## 🚀 Características

- ✅ **CRUD Completo** para movimientos financieros
- ✅ **Documentación Automática** con Swagger UI
- ✅ **Interfaz Interactiva** para probar la API
- ✅ **Filtros Avanzados** y ordenamiento
- ✅ **Reportes Financieros** con resúmenes
- ✅ **Validaciones** automáticas
- ✅ **Paginación** de resultados

## 📚 Documentación Interactiva

### Swagger UI

Accede a la interfaz interactiva de Swagger para probar la API:

```
http://127.0.0.1:8000/api/docs/
```

### ReDoc (Documentación Alternativa)

Interfaz más limpia y organizada:

```
http://127.0.0.1:8000/api/redoc/
```

### Esquema OpenAPI

Esquema JSON de la API:

```
http://127.0.0.1:8000/api/schema/
```

## 🛠️ Instalación

### 1. Instalar dependencias

```bash
pip install django djangorestframework drf-spectacular
```

### 2. Aplicar migraciones

```bash
python manage.py migrate
```

### 3. Ejecutar servidor

```bash
python manage.py runserver
```

## 📖 Cómo usar Swagger

### 1. Acceder a Swagger UI

Ve a `http://127.0.0.1:8000/api/docs/`

### 2. Explorar Endpoints

- **movimientos**: Operaciones CRUD básicas
- **reportes**: Funcionalidades de reportes y resúmenes
- **información**: Información general de la API

### 3. Probar Endpoints

1. Haz clic en cualquier endpoint
2. Haz clic en "Try it out"
3. Completa los parámetros requeridos
4. Haz clic en "Execute"

## 🔧 Endpoints Disponibles

### Operaciones CRUD

| Método | Endpoint                 | Descripción           |
| ------ | ------------------------ | --------------------- |
| GET    | `/api/movimientos/`      | Listar movimientos    |
| POST   | `/api/movimientos/`      | Crear movimiento      |
| GET    | `/api/movimientos/{id}/` | Obtener movimiento    |
| PUT    | `/api/movimientos/{id}/` | Actualizar movimiento |
| DELETE | `/api/movimientos/{id}/` | Eliminar movimiento   |

### Reportes

| Método | Endpoint                            | Descripción        |
| ------ | ----------------------------------- | ------------------ |
| GET    | `/api/movimientos/resumen/`         | Resumen financiero |
| GET    | `/api/movimientos/reporte_mensual/` | Reporte mensual    |

## 📝 Ejemplos de Uso con Swagger

### Crear un Ingreso

1. Ve a `POST /api/movimientos/`
2. Haz clic en "Try it out"
3. Usa el ejemplo "Crear ingreso":

```json
{
  "descripcion": "Salario mensual",
  "monto": "3000.00",
  "categoria": "ingreso",
  "fecha": "2024-01-15",
  "notas": "Salario de enero"
}
```

### Crear un Gasto

1. Ve a `POST /api/movimientos/`
2. Haz clic en "Try it out"
3. Usa el ejemplo "Crear gasto":

```json
{
  "descripcion": "Supermercado",
  "monto": "150.50",
  "categoria": "gasto",
  "fecha": "2024-01-16",
  "notas": "Compra semanal"
}
```

### Filtrar Movimientos

1. Ve a `GET /api/movimientos/`
2. Haz clic en "Try it out"
3. Completa los parámetros:
   - `categoria`: `ingreso` o `gasto`
   - `fecha_desde`: `2024-01-01`
   - `fecha_hasta`: `2024-01-31`
   - `ordenar_por`: `monto`
   - `orden`: `desc`

### Obtener Resumen

1. Ve a `GET /api/movimientos/resumen/`
2. Haz clic en "Try it out"
3. Opcionalmente agrega fechas de filtro

## 🎯 Ventajas de Swagger

### Para Desarrolladores

- **Documentación Automática**: Se actualiza automáticamente con el código
- **Pruebas Interactivas**: Prueba la API directamente desde el navegador
- **Ejemplos Incluidos**: Ejemplos predefinidos para cada endpoint
- **Validación Visual**: Ve los esquemas de request/response

### Para Usuarios

- **Interfaz Intuitiva**: Fácil de usar sin conocimientos técnicos
- **Pruebas en Tiempo Real**: Ejecuta requests y ve las respuestas
- **Documentación Clara**: Descripción detallada de cada operación
- **Múltiples Formatos**: Swagger UI y ReDoc disponibles

## 🔍 Características de la Documentación

### Parámetros Documentados

- **Query Parameters**: Filtros, ordenamiento, paginación
- **Path Parameters**: IDs de recursos
- **Request Body**: Esquemas JSON para crear/actualizar

### Respuestas Documentadas

- **Códigos de Estado**: 200, 400, 404, 500
- **Ejemplos de Respuesta**: Respuestas reales de ejemplo
- **Esquemas de Error**: Formato de errores

### Tags Organizados

- **movimientos**: Operaciones CRUD
- **reportes**: Funcionalidades de reportes
- **información**: Información general

## 🚀 Próximos Pasos

1. **Probar la API**: Usa Swagger UI para crear movimientos de prueba
2. **Explorar Filtros**: Prueba diferentes combinaciones de filtros
3. **Generar Reportes**: Usa los endpoints de reportes
4. **Personalizar**: Modifica la documentación según tus necesidades

## 📞 Soporte

Si tienes problemas con la API o la documentación:

1. Revisa los logs del servidor
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que las migraciones estén aplicadas
4. Consulta la documentación de Django REST Framework y drf-spectacular
