![Origen](https://img.shields.io/badge/Origen-Curso%20Empresa-blueviolet)
![Plataforma](https://img.shields.io/badge/Plataforma-softwareseguro.com.ar-informational)
![Categoría](https://img.shields.io/badge/Vulnerabilidad-Client%20Side%20Bypass%20%2F%20Reversing-critical)

# 🧮 Desafío: Calculadora

> ℹ️ **Nota:** Desafío del **curso de ciberseguridad pagado por la empresa** en la plataforma [softwareseguro.com.ar](https://app.softwareseguro.com.ar).

---

### 🧠 Descripción del caso

> *Sos un operario que por cada trabajo realizado en la fábrica necesitás subir un código desde una aplicación.*
> *El código A significa "Trabajo realizado", B "En progreso", C "Pendiente de revisión", D "Cancelado o no aprobado".*
> *Además de esos 4 códigos hay muchos más pero no puedes enviarlos. Te los han prohibido.*
> *Sin embargo, espiaste la tabla de códigos y el código **ABCD** significa "Todo perfecto, ¡merece un aumento de sueldo!". Aumentate el sueldo y obtené el hash.*

**Objetivo:** enviar el código prohibido `ABCD` y obtener el hash.

Se entrega un **`calculadora.jar`** (app de escritorio Java/Swing) que solo permite enviar los códigos A/B/C/D.

---

### 🔍 Análisis técnico (reversing estático del JAR)

Un `.jar` es un ZIP con clases Java compiladas. **No se ejecuta** (código no confiable): se analiza de forma estática.

```bash
unzip calculadora.jar -d extracted      # Calculadora.class + Calculadora$PulsaRaton.class
javap -p -c -constants Calculadora       # desensamblar el bytecode
```

En la clase interna `Calculadora$PulsaRaton` (el listener del botón **"Finalizar"**) se ve la lógica de envío:

```
// Al pulsar "Finalizar":
ldc  "aHR0cHM6Ly9jYWxjdWxhZG9yYS5zaGFyZWQuc29mdHdhcmVzZWd1cm8uY29tLmFyL3ZlcmlmaWNhci1jb2RpZ28tY2FsY3VsYWRvcmEvP3Q9"
invokestatic  Calculadora.deobfuscateURL   // Base64 decode
...
getText (lblResultado)                     // el codigo que armaste en pantalla
invokedynamic makeConcatWithConstants      // url + codigo
invokevirtual Calculadora.sendGET          // GET a (url + codigo)
```

Y los métodos de "ofuscación" son simplemente Base64:

```java
public static String obfuscateURL(String s)   { return Base64.getEncoder().encodeToString(s.getBytes()); }
public static String deobfuscateURL(String s)  { return new String(Base64.getDecoder().decode(s)); }
```

Decodificando la URL ofuscada:

```
aHR0cHM6Ly9jYWxjdWxhZG9yYS5zaGFyZWQuc29mdHdhcmVzZWd1cm8uY29tLmFyL3ZlcmlmaWNhci1jb2RpZ28tY2FsY3VsYWRvcmEvP3Q9
    │ Base64 decode ▼
https://calculadora.shared.softwareseguro.com.ar/verificar-codigo-calculadora/?t=
```

> 💡 La "prohibición" de códigos vive **solo en el cliente** (la UI únicamente ofrece botones A/B/C/D). El servidor recibe el código por `?t=` y **no valida** nada. Ofuscar la URL en Base64 no es protección: se recupera al decompilar.

---

### 💥 Explotación

Con el endpoint a la vista, se saltea por completo la app y se envía el código prohibido `ABCD` directo por GET:

```bash
curl "https://calculadora.shared.softwareseguro.com.ar/verificar-codigo-calculadora/?t=ABCD"
```

```python
import requests
BASE = "https://calculadora.shared.softwareseguro.com.ar/verificar-codigo-calculadora/?t="
print(requests.get(BASE + "A").text)      # "Guardado exitosamente"  (codigo normal)
print(requests.get(BASE + "ABCD").text)   # el hash del aumento
```

---

### ✅ Resultado

| Código enviado | Respuesta |
|---|---|
| `t=A` | `"Guardado exitosamente"` |
| **`t=ABCD`** | **`110bacfb41660e03ba586822ab7600ff`** |

El hash del aumento es **`110bacfb41660e03ba586822ab7600ff`**. ✅ Reto superado.

---

### 🔓 Vulnerabilidad encontrada

**Validación del lado del cliente (Client-Side Control) + ofuscación por oscuridad:**

- La restricción de "códigos permitidos" se aplica únicamente en la UI del cliente; el servidor acepta **cualquier** valor de `?t=`.
- La URL del endpoint se "protege" con Base64, que es **codificación, no cifrado**: cualquiera con el binario la recupera.
- Al distribuir el cliente (`.jar`), toda su lógica queda expuesta a análisis estático (decompilación).

---

### 🛡️ Mitigación recomendada

- **Validar en el servidor** qué códigos puede enviar cada usuario/rol; nunca confiar en que el cliente "no deja" enviar algo.
- No depender de la ofuscación (Base64, nombres raros) como medida de seguridad: no protege contra reversing.
- Autenticar y autorizar cada request en el backend, registrando qué código envía cada operario.
