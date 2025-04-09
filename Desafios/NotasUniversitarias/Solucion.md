# 🏫 Desafío: Modificación de Notas Universitarias

Este repositorio documenta el análisis y la solución al desafío de seguridad relacionado con la modificación de notas en una plataforma universitaria desarrollada con Django.

## 📝 Enunciado del Desafío

En una universidad que utiliza una plataforma desarrollada con Django, se han detectado múltiples fallos de seguridad que podrían comprometer la integridad de los datos académicos.

Se ha identificado un usuario con las siguientes credenciales válidas:
- **Usuario**: `benjamin.sosa142`
- **Contraseña**: `nsdfjklewe..`

Además, se obtuvo mediante un infoStealer un token JWT de refresco válido:


```eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6NDg2NjEyODQwOCwiaWF0IjoxNzQ0MDY0NDA4LCJqdGkiOiJhOTNmMmMxYWI0OTY0NGJiODY1OWMwOTI3ZmQwYmM1NCIsInVzZXJfaWQiOjM2fQ.MienEEx2ZuN-xdFj7Qti8HYXILlqZmVfjMhC-Hun_tw```

Este token puede ser usado para obtener un nuevo token de acceso enviando una solicitud POST a la URL `/api/token/refresh/`. Sin embargo, al detectarse su fuga, fue añadido a una lista negra de tokens y ahora está bloqueado.

Se ha comprobado además que el panel de administración de Django se encuentra habilitado en su URL por defecto y que las credenciales del superusuario no han sido modificadas desde la instalación.

**Objetivo**: Modificar la nota del usuario `benjamin.sosa142` en la materia "Análisis Matemático I", elevándola a 9.

## 🔍 Análisis y Solución

1. **Acceso al Panel de Administración**:
   - Se accedió al panel de administración de Django utilizando las credenciales por defecto (`admin:admin`).

    !!! CAUTION Es fundamental cambiar las credenciales predeterminadas después de la instalación para prevenir accesos no autorizados.

2. **Identificación del ID de la Materia**:
   - Al explorar el panel de administración, se observó que las materias estaban listadas en un orden específico. Se dedujo que "Análisis Matemático I" correspondía al `materia_id=2`, basándose en su posición en la lista.
   

3. **Modificación de la Nota**:
   - Se realizó una solicitud POST al endpoint correspondiente con los parámetros adecuados (`materia_id=2`, `estudiante_id` de Benjamin y `nota=9.0`), logrando modificar la nota exitosamente.

## 📸 Evidencias

A continuación, se presentan capturas de pantalla que ilustran cada paso del proceso:

1. **Acceso al Panel de Administración**:
   ![Acceso al Panel de Administración](./img/administrador.png)

2. **Listado de Materias**:
   ![](./img/materias.png)

3. **Solicitud POST para Modificar la Nota**:
   ![Solicitud POST](./img/post.png)

## 🎓 Lecciones Aprendidas

- **Importancia de Cambiar Credenciales por Defecto**: Las credenciales predeterminadas representan un riesgo significativo si no se modifican, ya que pueden ser explotadas fácilmente por atacantes.

- **Configuración Segura del Panel de Administración**: Además de cambiar las credenciales, es recomendable modificar la URL por defecto del panel de administración para dificultar su detección por parte de actores malintencionados.

- **Gestión de Tokens**: Es esencial implementar mecanismos robustos para la revocación y gestión de tokens comprometidos, asegurando que no puedan ser reutilizados.

## 🔐 Recomendaciones de Seguridad

- **Políticas de Contraseñas Fuertes**: Implementar políticas que requieran contraseñas complejas y únicas para todas las cuentas, especialmente las de alto privilegio.

- **Monitoreo y Auditoría**: Establecer sistemas de monitoreo para detectar accesos no autorizados y realizar auditorías periódicas de las configuraciones de seguridad.

- **Actualizaciones y Parches**: Mantener el software y las dependencias actualizadas para protegerse contra vulnerabilidades conocidas.

## 🏁 Conclusión

Este desafío resaltó la importancia de una configuración segura y la necesidad de seguir las mejores prácticas en ciberseguridad para proteger la integridad de los sistemas y datos académicos.