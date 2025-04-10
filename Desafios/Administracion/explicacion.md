## 🔐 Desafío: Administración – Tokens comprometidos

### 🧾 Enunciado resumido

Se detectó una filtración de tokens producto de un infostealer. Entre ellos, **tres tokens firmados por Google** pertenecen a usuarios involucrados en ataques.  
Aunque los tokens hayan expirado, su análisis puede revelar los **correos electrónicos** de los atacantes.  
El formato de respuesta debía ser:  
```text
correo1|correo2|correo3
```
Separados por `|` y ordenados alfabéticamente.

---

### 🧠 Enfoque de resolución

#### 🔍 Paso 1: Análisis básico

Los tokens eran JWTs con estructura `header.payload.signature`. Inicialmente se intentó:
- Buscar tokens con **misma firma (`SIGNATURE`)**
- Filtrar por `iss = https://accounts.google.com`

➡️ Resultado: demasiados tokens firmados por Google y **todas las firmas eran únicas**.

---

#### 🧠 Paso 2: Observación clave – `azp`

Al analizar los `payloads`, surgió un patrón interesante:

> Tres tokens compartían el mismo valor de `azp` (Authorized Party)

🔑 **¿Qué es `azp`?**

`azp` representa la **aplicación cliente** que pidió el token.  
Si tres tokens tienen el mismo `azp`, probablemente fueron obtenidos usando la **misma app maliciosa** o punto de entrada.

---

### ✅ Script de resolución final

```python
import base64, json
from collections import defaultdict

with open("tokens.txt") as f:
    tokens = [line.strip() for line in f if line.strip()]

azp_groups = defaultdict(list)

for token in tokens:
    parts = token.split(".")
    if len(parts) != 3:
        continue

    _, payload_b64, _ = parts
    padded = payload_b64 + "=" * (-len(payload_b64) % 4)

    try:
        payload = json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))
        if payload.get("iss") == "https://accounts.google.com":
            azp = payload.get("azp")
            email = payload.get("email")
            if azp and email:
                azp_groups[azp].append(email)
    except:
        continue

for azp, emails in azp_groups.items():
    if len(emails) == 3:
        print('|'.join(sorted(emails)))
        break
```

---

### 🎯 Respuesta final enviada

```text
camilapereyra5386@gmail.com|franco.cabrera7486@gmail.com|n.arias4760@gmail.com
```

✔️ ¡Aceptada como correcta!

---

### 📚 Aprendizajes

- No siempre los atacantes dejan patrones obvios como firmas repetidas.
- En tokens JWT, campos como `azp` pueden revelar relaciones entre usuarios.
- El análisis forense de tokens puede ayudar a rastrear puntos de entrada y apps comprometidas.
