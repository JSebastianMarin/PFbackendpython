# Configuración de PostgreSQL para Movimientos Financieros

Este proyecto ha sido configurado para usar PostgreSQL como base de datos principal.

## 🗄️ Ventajas de PostgreSQL

- **Rendimiento superior**: Mejor para aplicaciones con muchos datos
- **Funciones avanzadas**: Índices, triggers, procedimientos almacenados
- **Escalabilidad**: Maneja grandes volúmenes de datos eficientemente
- **Integridad de datos**: Mejor control de transacciones
- **Soporte JSON**: Nativo para datos estructurados
- **Concurrencia**: Mejor manejo de múltiples usuarios

## 🛠️ Instalación y Configuración

### 1. Instalar Dependencias

```bash
pip install psycopg2-binary python-dotenv
```

### 2. Instalar PostgreSQL

#### Windows

1. Descarga PostgreSQL desde: https://www.postgresql.org/download/windows/
2. Ejecuta el instalador
3. Anota la contraseña del usuario `postgres`
4. Instala pgAdmin (opcional, para gestión visual)

#### macOS

```bash
brew install postgresql
brew services start postgresql
```

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 3. Crear Base de Datos

#### Opción 1: Usando psql

```bash
# Conectar como usuario postgres
sudo -u postgres psql

# Crear base de datos
CREATE DATABASE movimientos_financieros;

# Crear usuario (opcional)
CREATE USER mi_usuario WITH PASSWORD 'mi_password';
GRANT ALL PRIVILEGES ON DATABASE movimientos_financieros TO mi_usuario;

# Salir
\q
```

#### Opción 2: Usando pgAdmin

1. Abre pgAdmin
2. Conecta al servidor PostgreSQL
3. Clic derecho en "Databases"
4. "Create" > "Database"
5. Nombre: `movimientos_financieros`

### 4. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Copia el archivo de ejemplo
cp env_example.txt .env
```

Edita el archivo `.env` con tus credenciales:

```env
# Configuración de PostgreSQL
DB_NAME=movimientos_financieros
DB_USER=postgres
DB_PASSWORD=tu_password_real
DB_HOST=localhost
DB_PORT=5432

# Configuración de Django
SECRET_KEY=tu_secret_key_segura
DEBUG=True
```

### 5. Aplicar Migraciones

```bash
python manage.py migrate
```

### 6. Crear Superusuario

```bash
python manage.py createsuperuser
```

## 🔧 Configuración de Desarrollo

### Variables de Entorno Recomendadas

```env
# Desarrollo
DB_NAME=movimientos_financieros_dev
DB_USER=postgres
DB_PASSWORD=dev_password
DB_HOST=localhost
DB_PORT=5432
DEBUG=True

# Producción
DB_NAME=movimientos_financieros_prod
DB_USER=app_user
DB_PASSWORD=strong_password_here
DB_HOST=db.example.com
DB_PORT=5432
DEBUG=False
```

### Configuración de Conexión

El proyecto está configurado para usar variables de entorno:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "movimientos_financieros"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "tu_password"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
        "OPTIONS": {
            "charset": "utf8",
        },
    }
}
```

## 🚀 Optimizaciones de PostgreSQL

### Índices Recomendados

```sql
-- Índice para búsquedas por fecha
CREATE INDEX idx_movimiento_fecha ON api_movimientofinanciero(fecha);

-- Índice para búsquedas por categoría
CREATE INDEX idx_movimiento_categoria ON api_movimientofinanciero(categoria);

-- Índice compuesto para reportes
CREATE INDEX idx_movimiento_fecha_categoria ON api_movimientofinanciero(fecha, categoria);

-- Índice para ordenamiento por monto
CREATE INDEX idx_movimiento_monto ON api_movimientofinanciero(monto DESC);
```

### Configuración de Rendimiento

```sql
-- Aumentar memoria compartida
ALTER SYSTEM SET shared_buffers = '256MB';

-- Configurar work_mem para consultas complejas
ALTER SYSTEM SET work_mem = '4MB';

-- Configurar effective_cache_size
ALTER SYSTEM SET effective_cache_size = '1GB';

-- Recargar configuración
SELECT pg_reload_conf();
```

## 🔍 Monitoreo y Mantenimiento

### Comandos Útiles

```sql
-- Ver tamaño de la base de datos
SELECT pg_size_pretty(pg_database_size('movimientos_financieros'));

-- Ver tablas y su tamaño
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Ver conexiones activas
SELECT * FROM pg_stat_activity WHERE datname = 'movimientos_financieros';

-- Analizar uso de índices
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### Backup y Restore

```bash
# Backup
pg_dump -h localhost -U postgres -d movimientos_financieros > backup.sql

# Restore
psql -h localhost -U postgres -d movimientos_financieros < backup.sql

# Backup con formato personalizado (más eficiente)
pg_dump -h localhost -U postgres -Fc movimientos_financieros > backup.dump

# Restore desde formato personalizado
pg_restore -h localhost -U postgres -d movimientos_financieros backup.dump
```

## 🐛 Solución de Problemas

### Error de Conexión

```
django.db.utils.OperationalError: could not connect to server
```

**Solución:**

1. Verifica que PostgreSQL esté ejecutándose
2. Confirma las credenciales en `.env`
3. Verifica que la base de datos exista

### Error de Permisos

```
django.db.utils.OperationalError: permission denied for database
```

**Solución:**

```sql
GRANT ALL PRIVILEGES ON DATABASE movimientos_financieros TO tu_usuario;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tu_usuario;
```

### Error de Codificación

```
django.db.utils.OperationalError: invalid byte sequence for encoding "UTF8"
```

**Solución:**

```sql
-- Crear base de datos con codificación correcta
CREATE DATABASE movimientos_financieros WITH ENCODING 'UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8';
```

## 📊 Migración desde SQLite

Si ya tienes datos en SQLite y quieres migrar a PostgreSQL:

```bash
# 1. Hacer backup de SQLite
cp db.sqlite3 db.sqlite3.backup

# 2. Cambiar configuración a PostgreSQL
# (ya está hecho en settings.py)

# 3. Aplicar migraciones
python manage.py migrate

# 4. Cargar datos (si tienes fixtures)
python manage.py loaddata datos.json
```

## 🔒 Seguridad

### Buenas Prácticas

1. **Usar variables de entorno** para credenciales
2. **Crear usuario específico** para la aplicación
3. **Limitar permisos** del usuario de la aplicación
4. **Usar SSL** en producción
5. **Hacer backups regulares**
6. **Monitorear logs** de PostgreSQL

### Configuración de Seguridad

```sql
-- Crear usuario con permisos limitados
CREATE USER app_user WITH PASSWORD 'strong_password';
GRANT CONNECT ON DATABASE movimientos_financieros TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;
```

## 🎯 Próximos Pasos

1. **Instalar PostgreSQL** en tu sistema
2. **Crear la base de datos** `movimientos_financieros`
3. **Configurar el archivo `.env`** con tus credenciales
4. **Instalar dependencias**: `pip install psycopg2-binary python-dotenv`
5. **Aplicar migraciones**: `python manage.py migrate`
6. **Probar la aplicación** con PostgreSQL

¿Necesitas ayuda con algún paso específico de la configuración?
