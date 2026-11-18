![Origen](https://img.shields.io/badge/Origen-Curso%20Empresa-blueviolet)
![Plataforma](https://img.shields.io/badge/Plataforma-softwareseguro.com.ar-informational)
![Categoría](https://img.shields.io/badge/Vulnerabilidad-Default%20Creds%20%2B%20JWT%20%2B%20IDOR-critical)

# 🏫 Desafío: Notas Universitarias

> ℹ️ **Nota:** Desafío del **curso de ciberseguridad pagado por la empresa** en la plataforma [softwareseguro.com.ar](https://app.softwareseguro.com.ar).

---

### 🧠 Descripción del caso

Plataforma universitaria en **Django** con múltiples fallos de configuración. Se dispone de credenciales de un alumno y de un **token JWT de refresco filtrado** (vía infoStealer) que fue añadido a una blacklist.

- **Alumno:** `benjamin.sosa142` / `nsdfjklewe..`
- **Refresh token filtrado** (user_id 36, jti `a93f2c1ab49644bb8659c0927fd0bc54`) → bloqueado por la blacklist.
- El **panel admin de Django** está habilitado en su URL por defecto y el superusuario conserva credenciales de instalación.

**Objetivo:** modificar la nota de `benjamin.sosa142` en **"Análisis Matemático I"**, elevándola a **9**.

---

### 🔍 Análisis técnico

Reconocimiento de rutas. Como la app corre con **`DEBUG = True`**, una URL inexistente devuelve el **URLconf completo**:

```
admin/
api/token/refresh/     [token_refresh]
   (raíz = login)       [login]
home/                  [home]
logout/                [logout]
challenge-status/      [challenge_status]
```

Hallazgos:
- `/admin/` → panel de Django por defecto.
- `/api/token/refresh/` → endpoint JWT (SimpleJWT) con **token blacklist**.
- `/home/` → dashboard; **para alumnos muestra sus notas en solo lectura**, pero **para un profesor muestra un formulario de carga de notas**.
- No existe ninguna API de notas: la edición ocurre en `POST /home/`.

---

### 💥 Explotación (cadena de 3 fallas)

**1) Credenciales por defecto — acceso de superusuario.**
`/admin/login/` acepta **`admin:admin`** (superusuario sin cambiar desde la instalación).

**2) Bypass de la blacklist de JWT.**
El refresh token filtrado estaba bloqueado:

```http
POST /api/token/refresh/   {"refresh":"<token>"}
→ 401 {"detail":"Token is blacklisted"}
```

Desde el admin se elimina la entrada de **`token_blacklist/blacklistedtoken`** correspondiente; tras eso, el mismo token vuelve a ser válido y `/api/token/refresh/` devuelve un **access token de la profesora** (user 36, `graciela`). *(El panel de profesor también se alcanza reseteando su contraseña desde el admin de Django.)*

**3) IDOR / Broken Access Control en la carga de notas.**
El panel de la profesora (materia "Física II") trae un formulario por alumno con **campos ocultos manipulables**:

```html
<form method="post" action="/home/">
  <input type="hidden" name="materia_id"     value="7">   <!-- materia de la profe -->
  <input type="hidden" name="estudiante_id"  value="8">   <!-- id del alumno -->
  <input type="text"   name="nota"           value="7.0">
</form>
```

El servidor **no valida** que el `materia_id` sea de una materia que la profesora dicta, ni que el `estudiante_id` sea alumno suyo. Benjamín cursa Física II → de esa tabla se obtiene su `estudiante_id = 8`. Las materias están numeradas en orden, por lo que **Análisis Matemático I = `materia_id = 2`** (una materia que la profesora **no** dicta).

Se envía el POST con esos valores cruzados:

```python
# sesión de la profesora
data = {"csrfmiddlewaretoken": csrf,
        "materia_id": "2",       # Análisis Matemático I (NO la dicta -> IDOR)
        "estudiante_id": "8",    # benjamin.sosa142
        "nota": "9.0"}
requests.post(BASE + "/home/", data=data, cookies=prof_session)
# -> 302 (guardado)
```

---

### ✅ Resultado

Verificado en el panel de `benjamin.sosa142`:

| Materia | Antes | Después |
|---|---|---|
| **Análisis Matemático I** | 2.00 | **9.00** ✅ |
| (resto de materias) | — | sin cambios |

Código de superación entregado por la plataforma:

```
660b416167e7fd839bc06c61bb5a184b
```

---

### 🔓 Vulnerabilidades encontradas

1. **Credenciales por defecto** en el panel admin de Django expuesto en su URL por defecto.
2. **Gestión deficiente de tokens:** un atacante con acceso al admin puede quitar un token de la blacklist y reutilizar un refresh token comprometido.
3. **IDOR / Broken Access Control** en `POST /home/`: el backend confía en `materia_id` y `estudiante_id` enviados por el cliente, permitiendo a un profesor modificar notas de materias y alumnos que no le corresponden.
4. **`DEBUG = True` en producción:** filtra el URLconf y trazas internas, facilitando el reconocimiento.

---

### 🛡️ Mitigación recomendada

- Cambiar las **credenciales por defecto** y restringir/ocultar el panel admin; no exponerlo en la URL por defecto.
- **Autorización a nivel de objeto:** validar en el servidor que el profesor dicte esa materia y que el alumno le corresponda, ignorando los IDs enviados por el cliente.
- Tratar los tokens comprometidos como **revocados de forma definitiva**; no depender de una blacklist editable por una cuenta administrativa.
- **`DEBUG = False`** en producción y páginas de error genéricas.
