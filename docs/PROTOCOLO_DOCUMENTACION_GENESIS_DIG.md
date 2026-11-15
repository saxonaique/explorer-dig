# Protocolo de documentación y control de Génesis DIG

**Autoría del proyecto:** JMPR  
**Mantenimiento documental:** ChatGPT, mediante la conexión autorizada al repositorio GitHub  
**Repositorio:** `saxonaique/explorer-dig`  
**Estado:** vigente  
**Fecha:** 2026-11-15

## 1. Objetivo

Este protocolo establece cómo se registra, conserva y actualiza la investigación Génesis DIG. GitHub será el archivo maestro del proyecto: debe permitir reconstruir decisiones, versiones, experimentos y resultados sin depender del historial de conversaciones.

## 2. Responsabilidad documental

ChatGPT se encargará de:
- proponer qué información tiene valor documental y en qué ubicación debe guardarse;
- distinguir hechos comprobados, resultados comunicados por terceros, hipótesis, decisiones y tareas pendientes;
- redactar y actualizar documentos de seguimiento;
- conservar versiones anteriores y evitar sobrescrituras destructivas;
- comprobar el estado del repositorio antes de modificar archivos;
- informar al autor de cada cambio realizado, indicando ruta y commit.

JMPR conserva la dirección científica del proyecto y la decisión final sobre hipótesis, interpretación y aceptación de resultados. La documentación por sí sola no equivale a validación científica.

## 3. Qué debe registrarse

### 3.1 Código y versiones
- Código fuente de cada versión identificada.
- Hashes de los archivos cuando se realicen auditorías o ejecuciones reproducibles.
- Cambios entre versiones, motivo de cada cambio y pruebas asociadas.
- Estado de conservación: activo, experimental, congelado, obsoleto o archivado.

### 3.2 Diseño experimental
- Pregunta, hipótesis y predicciones.
- Protocolo y preregistro, con versiones inmutables.
- Parámetros, unidades, semillas, controles y criterios de exclusión.
- Identidad exacta del motor y del código auxiliar utilizado.
- Diferencias entre arquitecturas que impidan equiparar parámetros.

### 3.3 Ejecuciones y resultados
- Comandos y entorno de ejecución cuando estén disponibles.
- Datos de entrada, datos derivados y resultados individuales.
- CSV/JSON, logs, figuras y scripts de análisis.
- Hashes de entradas, código y artefactos cuando sea viable.
- Resultados negativos, fallos, excepciones y desviaciones del protocolo.
- Limitaciones y conclusiones permitidas por los datos.

### 3.4 Decisiones y continuidad
- Decisiones metodológicas y su justificación.
- Cuestiones abiertas, dependencias y siguiente hito.
- Relación entre campañas, sin mezclar motores o líneas experimentales distintas.

## 4. Qué no debe registrarse como hecho

No se presentarán como comprobados:
- resultados descritos en una conversación pero cuyos artefactos no se han inspeccionado;
- ejecuciones comunicadas por otra IA o persona sin evidencia reproducible;
- hipótesis, interpretaciones o expectativas;
- archivos supuestamente guardados si no se ha verificado su presencia en GitHub;
- conclusiones causales basadas únicamente en correlaciones o métricas no auditadas.

Estos elementos sí pueden documentarse, etiquetados expresamente como **comunicados**, **provisionales**, **hipótesis** o **pendientes de verificación**.

## 5. Estados documentales normalizados

- **Diseñado:** protocolo definido, aún no ejecutado.
- **Comunicado:** ejecución o resultado informado por una fuente, no verificado independientemente.
- **Ejecutado:** existe evidencia de ejecución y artefactos identificables.
- **Reproducido:** una repetición controlada ha generado resultados consistentes bajo el protocolo descrito.
- **Verificado:** identidad, integridad y cálculos relevantes han sido comprobados de forma independiente.
- **Cerrado:** análisis y documentación de la campaña completados; no implica que la hipótesis haya sido confirmada.

No se avanzará de estado sin evidencia suficiente.

## 6. Política de versiones y conservación

- No sobrescribir versiones congeladas, originales o preregistros cerrados.
- Crear una nueva versión para cada cambio sustantivo.
- Mantener un historial de cambios que indique qué cambió y por qué.
- No modificar retrospectivamente criterios de éxito, umbrales o exclusiones después de observar resultados. Cualquier análisis exploratorio posterior debe etiquetarse como tal.
- Mantener separados los motores fundacionales originales y las versiones experimentales posteriores.

## 7. Organización recomendada

La estructura existente del repositorio se respetará. Como criterio general:

- `docs/`: protocolos, auditorías, decisiones e informes.
- `audit/` o carpeta equivalente: preregistros, listas de comprobación y verificaciones.
- `experiments/` o carpeta equivalente: campañas y scripts de ejecución.
- `results/` o carpeta equivalente: datos, resúmenes y figuras.

Antes de crear nuevas carpetas se comprobará la estructura real del repositorio para evitar duplicidades.

## 8. Flujo de trabajo obligatorio

1. Identificar si el material corresponde a teoría, código, diseño, ejecución o interpretación.
2. Comprobar si existe ya un documento o expediente relacionado.
3. Verificar los artefactos disponibles y su procedencia.
4. Redactar con etiquetas de estado explícitas.
5. Conservar versiones anteriores.
6. Guardar en GitHub con un mensaje de commit descriptivo.
7. Verificar que el archivo y el commit aparecen en el repositorio.
8. Comunicar a JMPR la ruta, el enlace y cualquier limitación.

## 9. Regla científica central

**Los datos no se alteran para ajustarlos a la teoría. Si los resultados contradicen una hipótesis, se revisa la hipótesis o su interpretación.**

La documentación debe preservar también resultados negativos, incertidumbres, errores y límites de validez.

---

Este protocolo regula la gestión documental del proyecto; no certifica por sí mismo la validez de ninguna teoría, motor o resultado experimental.
