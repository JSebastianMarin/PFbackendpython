# CRUD de Movimientos Financieros

Este proyecto implementa un sistema completo de gestión de movimientos financieros (ingresos y gastos) usando Django REST Framework.

## Características

### Modelo: MovimientoFinanciero

- **Descripción**: Texto (máximo 200 caracteres)
- **Monto**: Número decimal (mínimo 0.01)
- **Categoría**: Ingreso o Gasto
- **Fecha**: Fecha del movimiento
- **Notas**: Campo opcional para notas adicionales
- **Campos automáticos**: Fecha de creación y actualización

### Operaciones CRUD

#### 1. Crear Movimiento (POST)

```http
POST /api/movimientos/
Content-Type: application/json

{
    "descripcion": "Salario mensual",
    "monto": "2500.00",
    "categoria": "ingreso",
    "fecha": "2024-01-15",
    "notas": "Salario de enero"
}
```

#### 2. Listar Movimientos (GET)

```http
GET /api/movimientos/
```

**Parámetros de filtrado:**

- `categoria`: 'ingreso' o 'gasto'
- `fecha_desde`: fecha inicial (YYYY-MM-DD)
- `fecha_hasta`: fecha final (YYYY-MM-DD)
- `ordenar_por`: 'fecha', 'monto', 'fecha_creacion'
- `orden`: 'asc' o 'desc'

**Ejemplos:**

```http
GET /api/movimientos/?categoria=ingreso
GET /api/movimientos/?fecha_desde=2024-01-01&fecha_hasta=2024-01-31
GET /api/movimientos/?ordenar_por=monto&orden=desc
```

#### 3. Obtener Movimiento Específico (GET)

```http
GET /api/movimientos/{id}/
```

#### 4. Actualizar Movimiento (PUT/PATCH)

```http
PUT /api/movimientos/{id}/
Content-Type: application/json

{
    "descripcion": "Salario mensual actualizado",
    "monto": "2600.00",
    "categoria": "ingreso",
    "fecha": "2024-01-15",
    "notas": "Salario de enero con bonificación"
}
```

#### 5. Eliminar Movimiento (DELETE)

```http
DELETE /api/movimientos/{id}/
```

### Funcionalidades Adicionales

#### Resumen de Movimientos

```http
GET /api/movimientos/resumen/
```

**Parámetros opcionales:**

- `fecha_desde`: fecha inicial (YYYY-MM-DD)
- `fecha_hasta`: fecha final (YYYY-MM-DD)

**Respuesta:**

```json
{
  "resumen": {
    "total_ingresos": 5000.0,
    "total_gastos": 2500.0,
    "balance": 2500.0,
    "total_movimientos": 10,
    "movimientos_ingresos": 5,
    "movimientos_gastos": 5
  },
  "rango_fechas": {
    "fecha_desde": "2024-01-01",
    "fecha_hasta": "2024-01-31"
  }
}
```

#### Reporte Mensual

```http
GET /api/movimientos/reporte_mensual/?año=2024&mes=1
```

**Respuesta:**

```json
{
    "reporte_mensual": {
        "año": 2024,
        "mes": 1,
        "total_ingresos": 5000.00,
        "total_gastos": 2500.00,
        "balance": 2500.00,
        "total_movimientos": 10,
        "top_movimientos": [...]
    }
}
```

## Instalación y Configuración

### 1. Instalar dependencias

```bash
pip install django djangorestframework
```

### 2. Aplicar migraciones

```bash
python manage.py migrate
```

### 3. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 4. Ejecutar servidor

```bash
python manage.py runserver
```

## URLs Disponibles

- **API REST**: `http://localhost:8000/api/movimientos/`
- **Admin Django**: `http://localhost:8000/admin/`
- **Autenticación API**: `http://localhost:8000/api-auth/`

## Ejemplos de Uso

### Crear un ingreso

```bash
curl -X POST http://localhost:8000/api/movimientos/ \
  -H "Content-Type: application/json" \
  -d '{
    "descripcion": "Salario",
    "monto": "3000.00",
    "categoria": "ingreso",
    "fecha": "2024-01-15"
  }'
```

### Crear un gasto

```bash
curl -X POST http://localhost:8000/api/movimientos/ \
  -H "Content-Type: application/json" \
  -d '{
    "descripcion": "Supermercado",
    "monto": "150.50",
    "categoria": "gasto",
    "fecha": "2024-01-16",
    "notas": "Compra semanal"
  }'
```

### Obtener resumen del mes

```bash
curl "http://localhost:8000/api/movimientos/resumen/?fecha_desde=2024-01-01&fecha_hasta=2024-01-31"
```

## Validaciones

- El monto debe ser mayor a 0
- La fecha no puede ser futura
- La categoría debe ser 'ingreso' o 'gasto'
- La descripción es obligatoria

## Características del Admin

El modelo está registrado en el admin de Django con:

- Lista con filtros por categoría, fecha y fecha de creación
- Búsqueda por descripción y notas
- Jerarquía de fechas
- Campos organizados en secciones
- Campos de solo lectura para fechas automáticas
