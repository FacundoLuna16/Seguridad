## 🗳️ Desafío: Broken Access Control – Sistema de votación (nueva versión)

### 🧠 Descripción del caso

En esta nueva versión del sistema de votación, se implementaron controles adicionales para impedir que un usuario vote más de una vez. A diferencia del caso anterior, ahora el sistema no solo valida la cookie, sino que también introduce una verificación por dirección IP.

---

### 📌 Caso

**Votación – Nueva versión**

> *Un compañero me acaba de enviar un link de una página que realiza una extraña votación, en la cual participa nuestra facultad. Estaría bueno que votes, ¿podrá ganar la UTN?*

**Pista 1:** *Obtendrás el código HASH cuando la cantidad de votos de la UTN supere a Harvard.*

**Pista 2:** *Como desean que cada persona vote solo una única vez han reforzado las defensas en el código para conseguir esto. ¿Pero habrá sido suficiente?*

---

### 🔍 Análisis técnico

- **Método:** `POST`  
- **Endpoint:** `/src/ctl/votacion.ctl.php`  
- **Parámetro enviado:** `opUniversidad=1`

Al enviar un primer voto, la solicitud se procesaba correctamente.  
Sin embargo, al intentar votar nuevamente, aparecía el siguiente mensaje:

```
No se puede votar más de una vez desde la misma IP
```

Esto indicaba que, además del control por cookie, ahora el servidor también estaba **verificando la IP del cliente**.

---

### 🛠️ Explotación

Durante el análisis de la solicitud HTTP se identificó que el backend estaba tomando la dirección IP desde la cabecera:

```http
X-Forwarded-For
```

Esto permitió simular distintas IPs en cada petición, simplemente generando valores aleatorios para esa cabecera (incluso no válidos) y evadir el control.

#### 🧪 Ejemplo de cabecera modificada:

```http
X-Forwarded-For: 123.45.67.89
```

El servidor no validaba si la IP era real ni si provenía de una fuente confiable, por lo tanto era posible falsificarla.
![](./img/x-forwarded-for.png)

---

### 🧨 Vulnerabilidad encontrada

Esta variante del sistema sigue siendo vulnerable a **Broken Access Control** por:

- Confiar ciegamente en una cabecera manipulable por el cliente (`X-Forwarded-For`).
- No implementar validaciones server-side más robustas como tokens únicos, detección de comportamiento anómalo o firmas temporales.
- Permitir múltiples votos si se altera esa cabecera.

---

### 💻 Script de explotación

El script automatiza el envío de múltiples votos, generando IPs falsas en cada ciclo mediante la cabecera `X-Forwarded-For`.

📁 Archivo: [`broken-access-control/votacionMejorada.py`](./votacionMejorada.py)
