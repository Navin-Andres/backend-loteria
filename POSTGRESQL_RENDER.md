# 🎯 Configurar PostgreSQL en Render - Solución Persistencia de Datos

## 🔴 PROBLEMA
En el plan gratuito de Render, cuando el servicio se suspende (tras 15 min de inactividad), se **pierde todo lo almacenado en archivos locales** (incluida la base de datos SQLite `lottery.db`).

## ✅ SOLUCIÓN
Usar **PostgreSQL** de Render (también gratuito), que **mantiene los datos persistentes** incluso cuando el servicio se suspende.

---

## 📋 PASO 1: Crear PostgreSQL Database en Render

### 1.1 Acceder a Render
1. Ve a: https://dashboard.render.com/
2. Inicia sesión

### 1.2 Crear PostgreSQL
1. Click en **"New +"** (botón azul superior derecho)
2. Selecciona **"PostgreSQL"**

### 1.3 Configurar PostgreSQL
```
Name:           sorteo-loteria-db
Database:       sorteo_db
User:           sorteo_user
Region:         Oregon (USA) - la misma que tu Web Service
PostgreSQL Ver: 15
```

**Plan:**
```
Plan: Free (⚠️ Expira en 90 días, pero puedes renovar gratis)
```

### 1.4 Crear Database
1. Click en **"Create Database"**
2. Espera 2-3 minutos mientras Render aprovisiona la base de datos
3. **IMPORTANTE:** Guarda la URL de conexión

---

## 📋 PASO 2: Configurar Web Service para usar PostgreSQL

### 2.1 Ir a tu Web Service
1. En el dashboard de Render, click en tu servicio web: `sorteo-loteria-api`
2. Ve a la pestaña **"Environment"** (en el menú izquierdo)

### 2.2 Añadir Variable de Entorno
1. Click en **"Add Environment Variable"**
2. Añade:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `[Copiar Internal Database URL de tu PostgreSQL]` |

**Para obtener la Internal Database URL:**
1. Ve a tu PostgreSQL database en Render
2. En la sección **"Connections"**
3. Copia la **"Internal Database URL"** (empieza con `postgres://`)
4. **NO** uses la "External Database URL"

Ejemplo:
```
postgres://sorteo_user:xxxxxxxxxxxxx@dpg-xxxxx/sorteo_db
```

### 2.3 Re-desplegar
1. Después de agregar la variable de entorno
2. Render automáticamente re-desplegará tu servicio
3. El código detectará automáticamente `DATABASE_URL` y usará PostgreSQL en lugar de SQLite

---

## 📋 PASO 3: Verificar que Funciona

### 3.1 Ver Logs del Despliegue
1. Ve a la pestaña **"Logs"** en tu Web Service
2. Busca el mensaje:
```
✅ Database initialized successfully (PostgreSQL)
```

Si ves esto, ¡funciona correctamente! 🎉

### 3.2 Probar la API
```bash
# Health check
curl https://sorteo-loteria-api.onrender.com/health

# Registrar usuario
curl -X POST https://sorteo-loteria-api.onrender.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test123"}'
```

---

## 🔄 Migración de Datos (Si ya tenías usuarios en SQLite)

Si ya tenías usuarios y datos en SQLite local, necesitas migrarlos:

### Opción A: Conectar directamente a PostgreSQL (Recomendado)

```bash
# Instalar psql (PostgreSQL client)
# Windows: Descargar desde https://www.postgresql.org/download/windows/

# Conectar a tu database de Render
psql "postgres://sorteo_user:PASSWORD@dpg-xxxxx/sorteo_db"

# Verificar tablas creadas
\dt

# Ver usuarios (si los hay)
SELECT * FROM users;
```

### Opción B: Registrar nuevos usuarios manualmente
Simplemente vuelve a registrar los usuarios desde la app.

---

## 📊 Comparación: SQLite vs PostgreSQL

| Característica | SQLite (Antes) | PostgreSQL (Ahora) |
|----------------|----------------|-------------------|
| **Persistencia** | ❌ Se borra al suspender | ✅ Datos permanentes |
| **Costo** | Gratis | Gratis (90 días renovables) |
| **Rendimiento** | Rápido (local) | Rápido (red interna) |
| **Backup** | Manual | Automático por Render |
| **Escalabilidad** | Limitada | Alta |

---

## 🎯 Ventajas de PostgreSQL en Render

✅ **Datos persistentes** - No se borran cuando el servicio se suspende
✅ **Backups automáticos** - Render hace respaldos diarios
✅ **Seguridad** - Conexiones encriptadas
✅ **Escalable** - Si creces, puedes mejorar el plan fácilmente
✅ **Gratis** - Plan free de 90 días (renovable)

---

## ⚠️ Importante

### Plan Free de PostgreSQL
- **Duración:** 90 días
- **Almacenamiento:** 1 GB
- **Renovación:** Puedes renovar cada 90 días de forma gratuita
- **Alternativa:** Si necesitas más tiempo permanente, considera otros servicios:
  - **ElephantSQL** (PostgreSQL gratis permanente hasta 20MB)
  - **Supabase** (PostgreSQL gratis permanente hasta 500MB)
  - **Neon** (PostgreSQL gratis permanente hasta 3GB)

### Código Compatible
El código actualizado es **compatible con ambas bases de datos**:
- **Desarrollo local:** Usa SQLite automáticamente
- **Producción (Render):** Usa PostgreSQL cuando detecta `DATABASE_URL`

---

## 🆘 Solución de Problemas

### Error: "relation does not exist"
Las tablas no se han creado. Verifica que el servicio se reinició después de agregar `DATABASE_URL`.

### Error: "password authentication failed"
La URL de conexión es incorrecta. Verifica que copiaste la **Internal Database URL** correctamente.

### Error: "could not connect to server"
Asegúrate de usar la **Internal Database URL**, NO la External.

### Los datos se siguen borrando
Verifica que la variable `DATABASE_URL` esté configurada correctamente en el Web Service.

---

## 📚 Referencias

- [Render PostgreSQL Docs](https://render.com/docs/databases)
- [Render Environment Variables](https://render.com/docs/environment-variables)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

---

## ✅ Checklist Final

- [ ] PostgreSQL database creada en Render
- [ ] Variable `DATABASE_URL` añadida al Web Service
- [ ] Servicio re-desplegado exitosamente
- [ ] Logs muestran "Database initialized successfully (PostgreSQL)"
- [ ] API funcionando correctamente
- [ ] Datos persisten después de que el servicio se suspende

¡Todo listo! Ahora tus datos estarán seguros incluso cuando Render suspenda el servicio. 🎉
