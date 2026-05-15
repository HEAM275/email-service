# 📧 Email Service - Servicio de Envío de Correos

Un servicio especializado de envío de correos electrónicos construido con **FastAPI** y **Celery**, diseñado para ser consumido por otros microservicios como Auth-System. Proporciona envío confiable de emails con reintentos automáticos y soporte para múltiples proveedores SMTP.

## 📋 Tabla de Contenidos

- [Objetivo del Proyecto](#objetivo-del-proyecto)
- [Características](#características)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [API Endpoints](#api-endpoints)
- [Arquitectura](#arquitectura)
- [Ejemplos de Uso](#ejemplos-de-uso)

---

## 🎯 Objetivo del Proyecto

Este proyecto es un **servicio de email centralizado** que actúa como intermediario para el envío de correos electrónicos en una arquitectura de microservicios. Sus responsabilidades principales son:

1. **Recibir Peticiones HTTP**: De otros servicios que necesiten enviar correos
2. **Procesar Correos Asincronicamente**: Usar Celery para no bloquear la API
3. **Reintentos Automáticos**: En caso de fallo temporal en SMTP
4. **Soporte SMTP**: Compatible con Gmail, SendGrid, Mailgun y otros
5. **Logging y Monitoreo**: Registro detallado de cada envío
6. **Escalabilidad**: Múltiples workers Celery para procesar en paralelo
7. **Desacoplamiento**: Los servicios consumidores no necesitan saber de SMTP

### Ventajas de esta Arquitectura

- ✅ Los servicios consumidores **no esperan el envío** (respuesta inmediata)
- ✅ **Reintentos automáticos** si falla el servidor SMTP
- ✅ **Escalable**: Agregar más workers Celery sin parar el servicio
- ✅ **Mantenible**: Cambiar proveedor SMTP en un solo lugar
- ✅ **Monitoreable**: Logs centralizados de todos los correos enviados
- ✅ **Confiable**: Colas en Redis garantizan que los correos se enviarán

---

## ✨ Características

- ✉️ **Envío SMTP Confiable** con reintentos automáticos
- ✉️ **Soporte HTML y Plain Text** en correos
- 🔄 **Reintentos Inteligentes**: Espera exponencial entre intentos
- ⚡ **Procesamiento Asincrónico**: Celery + Redis como broker
- 📊 **Logging Detallado**: Registro de cada intento y resultado
- 🔌 **API REST Simple**: Fácil de consumir desde otros servicios
- 🔐 **Compatible con SMTP Seguro**: TLS/SSL soportado
- 📈 **Escalable**: Múltiples workers simultáneos
- 🎯 **Flexible**: Soporta múltiples proveedores SMTP
- ⚙️ **Configurable**: Todo mediante variables de entorno

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.10+
- Redis
- Acceso a servidor SMTP (Gmail, SendGrid, Mailgun, etc.)
- Git

### Pasos de Instalación

```bash
# 1. Navegar al proyecto
cd email-service

# 2. Crear ambiente virtual
python -m venv venv

# 3. Activar ambiente virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Crear archivo .env (copiar desde .env.example si existe)
# Si no existe, crear manualmente
touch .env
```

---

## 🛠️ Configuración

### Variables de Entorno (`.env`)

```env
# ===== CONFIGURACIÓN SMTP =====
# Para Gmail:
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password  # Usar App Password, NO contraseña normal
SMTP_FROM_NAME=Tu Nombre o Empresa
SMTP_FROM_EMAIL=tu-email@gmail.com
SMTP_TLS=True
SMTP_SSL=False

# ===== CONFIGURACIÓN REDIS =====
CELERY_BROKER_URL=redis://localhost:6380/0
CELERY_RESULT_BACKEND=redis://localhost:6380/0

# ===== CONFIGURACIÓN CELERY =====
CELERY_TASK_TIME_LIMIT=300          # Timeout de 5 minutos por tarea
CELERY_WORKER_CONCURRENCY=4         # Número de workers paralelos
CELERY_TASK_MAX_RETRIES=3           # Reintentos máximos
CELERY_TASK_DEFAULT_RETRY_DELAY=60  # Esperar 60s antes de reintentar

# ===== CONFIGURACIÓN DE APLICACIÓN =====
DEBUG=False
LOG_LEVEL=INFO
API_PORT=8002
API_HOST=0.0.0.0

# ===== CONFIGURACIÓN TIMEOUT =====
EMAIL_SEND_TIMEOUT=30  # Timeout en segundos para envío de email
```

### Obtener Credenciales SMTP

#### Gmail

1. Habilitar autenticación de 2 pasos en tu cuenta Google
2. Generar "App Password":
   - Ir a https://myaccount.google.com/apppasswords
   - Seleccionar App: "Mail" y Dispositivo: "Windows Computer" (u otro)
   - Copiar la contraseña generada
3. Usar esa contraseña en `SMTP_PASSWORD`

#### SendGrid

1. Crear cuenta en https://sendgrid.com
2. Obtener API Key en Settings → API Keys
3. Usar como `SMTP_PASSWORD` (el API Key)
4. `SMTP_USER` = "apikey"
5. `SMTP_HOST` = "smtp.sendgrid.net"
6. `SMTP_PORT` = 587

#### Otros Proveedores

Consultar documentación oficial de tu proveedor SMTP.

---

## ▶️ Ejecución

### Terminal 1: Celery Worker

```bash
# Importante: Especificar la cola "email_tasks"
celery -A app.core.celery_app worker --queue email_tasks --loglevel=info --pool=solo

# Para múltiples workers (recomendado en producción):
celery -A app.core.celery_app worker --queue email_tasks --loglevel=info --concurrency=4
```

### Terminal 2: Servidor FastAPI

```bash
# Desarrollo con recarga automática
uvicorn app.main:app --reload --port 8002

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8002
```

### Verificar que todo está funcionando

```bash
# Acceder a la documentación
http://localhost:8002/docs

# Probar health check
curl http://localhost:8002/health
# Respuesta: {"status": "ok"}
```

---

## 📡 API Endpoints

### Salud del Servicio

```
GET /health
```

**Respuesta:**
```json
{
  "status": "ok"
}
```

---

### Enviar Correo Simple

```
POST /email/send
```

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "to_email": "destinatario@example.com",
  "subject": "Bienvenido a nuestra plataforma",
  "body": "Gracias por registrarte",
  "body_html": "<html><body><h1>Bienvenido</h1><p>Gracias por registrarte</p></body></html>"
}
```

**Response (200 OK):**
```json
{
  "message": "Email enviado correctamente",
  "task_id": "abc123def456",
  "status": "queued"
}
```

**Posibles Errores:**
```json
{
  "detail": "Email inválido"
}
```

---

### Enviar Correo a Múltiples Destinatarios

```
POST /email/send-batch
```

**Request Body:**
```json
{
  "to_emails": [
    "usuario1@example.com",
    "usuario2@example.com",
    "usuario3@example.com"
  ],
  "subject": "Notificación importante",
  "body": "Contenido del correo",
  "body_html": "<html><body>Contenido HTML</body></html>"
}
```

**Response (200 OK):**
```json
{
  "message": "Emails encolados para envío",
  "task_ids": [
    "task_id_1",
    "task_id_2",
    "task_id_3"
  ],
  "total": 3
}
```

---

### Verificar Estado de Envío

```
GET /email/status/{task_id}
```

**Response (200 OK):**
```json
{
  "task_id": "abc123def456",
  "status": "success",
  "result": {
    "message_id": "<msg-id@gmail.com>",
    "sent_at": "2026-02-15T10:30:00Z"
  }
}
```

**Posibles Estados:**
- `pending`: En cola, aún no se procesa
- `in_progress`: Celery actualmente procesando
- `success`: Enviado correctamente
- `failure`: Error en el envío
- `retry`: Intentando nuevamente

---

## 🏗️ Arquitectura

### Estructura del Proyecto

```
app/
├── main.py                          # Punto de entrada FastAPI
├── schemas.py                       # Esquemas Pydantic para validación
├── core/
│   ├── celery_app.py                # Configuración de Celery
│   └── __init__.py
├── routes/
│   ├── email.py                     # Rutas POST /email/send, etc.
│   └── __init__.py
├── tasks/
│   ├── email_tasks.py               # Tareas Celery que envían emails
│   └── __init__.py
├── utils/
│   ├── email.py                     # Lógica de envío SMTP
│   └── __init__.py
└── __init__.py

config/
├── settings.py                      # Variables de entorno
└── __init__.py
```

### Flujo de Envío de Email

```
1. Cliente HTTP → POST /email/send {to_email, subject, body}
   ↓
2. FastAPI valida el request (Pydantic schema)
   ↓
3. Endpoint crea tarea Celery con los datos
   ↓
4. Tarea se encola en Redis (broker)
   ↓
5. Response inmediata al cliente: {task_id, status: "queued"}
   ↓
6. Celery Worker procesa la tarea
   ↓
7. Se conecta al servidor SMTP (ej: smtp.gmail.com)
   ↓
8. Autentica con SMTP_USER y SMTP_PASSWORD
   ↓
9. Envía el email a través de SMTP
   ↓
10. Registra resultado (success/failure) en Redis
   ↓
11. Si falla, Celery reintentar automáticamente (hasta 3 veces)
```

### Reintentos Inteligentes

```
Intento 1: Inmediato
    ↓ FALLO
Intento 2: Esperar 60 segundos → Reintentar
    ↓ FALLO
Intento 3: Esperar 120 segundos → Reintentar
    ↓ FALLO
Intento 4: Esperar 240 segundos → Reintentar
    ↓ FALLO FINAL (3 reintentos completados)
Registrar error en logs/base de datos
```

---

## 💡 Ejemplos de Uso

### Desde Python (requests)

```python
import requests
import json

# URL del servicio
EMAIL_SERVICE_URL = "http://localhost:8002"

# 1. Enviar email de bienvenida
response = requests.post(
    f"{EMAIL_SERVICE_URL}/email/send",
    json={
        "to_email": "usuario@example.com",
        "subject": "Bienvenido a nuestra plataforma",
        "body": "Gracias por registrarte",
        "body_html": """
        <html>
            <body>
                <h1>¡Bienvenido!</h1>
                <p>Gracias por crear tu cuenta con nosotros.</p>
                <a href="https://ejemplo.com">Visitar plataforma</a>
            </body>
        </html>
        """
    }
)

print(response.json())
# Resultado: {"message": "Email enviado correctamente", "task_id": "..."}

# 2. Verificar estado
task_id = response.json()["task_id"]
status_response = requests.get(f"{EMAIL_SERVICE_URL}/email/status/{task_id}")
print(status_response.json())
```

### Desde cURL

```bash
# Enviar email
curl -X POST http://localhost:8002/email/send \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "usuario@example.com",
    "subject": "Test Email",
    "body": "Este es un correo de prueba",
    "body_html": "<p>Este es un correo de <b>prueba</b></p>"
  }'

# Verificar estado
curl -X GET http://localhost:8002/email/status/TASK_ID
```

### Desde Auth-System (integración real)

```python
# En auth_sys/src/core/email.py
import httpx
from src.core.config import settings

async def send_verification_email(to_email: str, token: str):
    """Envía correo de verificación a través de Email-Service"""
    
    verification_link = f"{settings.AUTH_SERVICE_URL}/auth/verify-email?token={token}"
    
    body_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Verifica tu correo electrónico</h2>
            <p>Haz clic en el enlace para verificar tu cuenta:</p>
            <a href="{verification_link}" style="background-color: #007bff; 
               color: white; padding: 10px 20px; text-decoration: none;">
                Verificar Email
            </a>
            <p>O copia este enlace en tu navegador:</p>
            <p>{verification_link}</p>
        </body>
    </html>
    """
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.EMAIL_SERVICE_URL}/email/send",
            json={
                "to_email": to_email,
                "subject": "Verifica tu correo electrónico",
                "body": f"Verifica tu cuenta: {verification_link}",
                "body_html": body_html
            },
            timeout=settings.EMAIL_SERVICE_TIMEOUT
        )
        return response.json()
```

---

## 🔐 Seguridad

### Recomendaciones de Seguridad

1. **Nunca subir `.env`** a repositorio (usar `.env.example`)
2. **Usar App Passwords** en Gmail (no contraseña regular)
3. **Limitar acceso a la API**: Usar API keys o autenticación
4. **HTTPS en Producción**: Usar SSL/TLS
5. **Validar emails**: Verificar formato antes de enviar
6. **Rate Limiting**: Implementar límites de envío por IP
7. **Logging seguro**: No loguear contraseñas o tokens
8. **Mantener dependencias actualizadas**: `pip install --upgrade`

### Agregar Autenticación a Email-Service

```python
# En app/main.py
from fastapi import Depends, HTTPException, status, Header

async def verify_api_key(x_api_key: str = Header(None)):
    """Verificar que la petición viene con API key válida"""
    VALID_API_KEYS = ["your-secret-key-123"]
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválido"
        )
    return x_api_key

# Usa en los endpoints:
@app.post("/email/send")
async def send_email(email_data: EmailSchema, api_key: str = Depends(verify_api_key)):
    # ...
```

---

## 📊 Monitoreo y Logs

### Ver logs de Celery

```bash
# Celery worker muestra logs por defecto
# Búscadefecto: "[INFO/MainProcess]"
# Búsca por "Email sent successfully" para confirmaciones
```

### Verificar tareas en Cola

```bash
# Viemdo

 redis-cli
redis-cli> KEYS celery*
redis-cli> LLEN celery  # Número de tareas en cola
```

### Obtener Estadísticas

```bash
# En otro terminal
celery -A app.core.celery_app events

# Verá eventos en tiempo real de tareas siendo procesadas
```

---

## 🐛 Troubleshooting

### Error: "Connection refused to Redis"
```bash
# Verificar que Redis está corriendo
redis-cli ping  # Debe retornar PONG

# Si no está:
# Windows: redis-server
# Linux: sudo systemctl start redis-server
```

### Error: "SMTP connection refused"
```bash
# 1. Verificar SMTP_HOST y SMTP_PORT son correctos
# 2. Verificar SMTP_USER y SMTP_PASSWORD
# 3. Checkear que Gmail tiene habiliados 2FA + App Password
# 4. Verificar firewall permite puerto 587/465
```

### Error: "Email address appears to be invalid"
```bash
# El email en to_email tiene formato inválido
# Verificar: ejemplo@dominio.com (debe tener @ y dominio)
```

### Los emails no se envían
```bash
# 1. Verificar que Celery worker está corriendo
# 2. Verificar que Redis está disponible
# 3. Revisar logs del worker: celery -A app.core.celery_app worker --loglevel=debug
# 4. Verificar que credenciales SMTP son correctas
# 5. Checkear si hay errores en redis logs
```

---

## 📈 Escalabilidad

### Agregar más workers (para procesar más emails en paralelo)

```bash
# Terminal 1: Worker 1
celery -A app.core.celery_app worker -l info -n worker1@%h --queue email_tasks

# Terminal 2: Worker 2
celery -A app.core.celery_app worker -l info -n worker2@%h --queue email_tasks

# Terminal 3: Worker 3
celery -A app.core.celery_app worker -l info -n worker3@%h --queue email_tasks
```

Ahora procesará 3 emails simultáneamente en lugar de 1.

### Con Docker (Producción)

```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["celery", "-A", "app.core.celery_app", "worker", "--queue", "email_tasks", "--loglevel=info"]
```

---

## 📚 Dependencias Principales

| Paquete | Versión | Propósito |
|---------|---------|----------|
| FastAPI | 0.129+ | Framework web asincrónico |
| Celery | 5.6+ | Tareas asincrónicas |
| Redis | 6.4+ | Broker y cache |
| aiosmtplib | 5.1+ | Cliente SMTP asincrónico |
| Pydantic | 2.0+ | Validación de datos |
| python-dotenv | 1.2+ | Cargar variables .env |
| httpx | 0.28+ | Cliente HTTP asincrónico |

---

## 📞 Integración con Otros Servicios

### Auth-System

Este servicio es consumido por **auth_sys** para enviar:
- ✉️ Correos de verificación de cuenta
- ✉️ Correos de reseteo de contraseña
- ✉️ Notificaciones de login sospechoso

Ver documentación en [Auth-System README](../authentication-sys/README.md)

---

## 📄 Licencia

MIT License - Puedes usar este código libremente

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

## 📞 Contacto & Soporte

Para reportar bugs o sugerencias, abre un issue en el repositorio.

**Última actualización**: 15 de febrero de 2026
