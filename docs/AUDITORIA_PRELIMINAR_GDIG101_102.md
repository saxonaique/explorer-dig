# Auditoría preliminar — Comparativa 001 (GDIG-101/102)

**Proyecto:** Génesis DIG  
**Dirección científica y autoría:** JMPR  
**Responsable de apoyo documental:** ChatGPT  
**Repositorio:** `saxonaique/explorer-dig`  
**Estado:** Auditoría preliminar; no equivale a reproducción ni verificación experimental.  
**Fecha de registro:** 2026-11-15

## 1. Alcance y separación de líneas

Este documento registra el estado de la revisión de la Comparativa 001 entre los dos motores fundacionales:

- `DIG_Explorer_v1/dig_core_v1.py` — Core fundacional.
- `DIG_Explorer_v1/dig_explorer.py` — Explorer fundacional.

No deben confundirse con los motores experimentales DIG Explorer v1.0, v1.1 o v1.2. La auditoría de estos últimos constituye una línea independiente.

Los motores fundacionales se mantienen intactos. No se han cambiado parámetros ni se han modificado datos para favorecer una hipótesis.

## 2. Material localizado

En el repositorio están presentes:

- `docs/GDIG101_102_reproduccion_resultados.json`
- `docs/GDIG101_102_reproduccion_resultados.csv`

El JSON se pudo abrir y analizar estructuralmente. Contiene diez registros: dos condiciones (2 clases y 3 clases), con semillas 0–4. Cada registro incluye matrices de tres slots para ambos motores y una referencia a un archivo de señal.

Las rutas referenciadas por el campo `signal_file` son del tipo `output/reproduccion_controlada/GDIG101_2clases_seed0.csv`. Esas señales originales no constaban en el árbol del commit inspeccionado durante esta revisión.

No se ha localizado todavía el script auxiliar que generó el paquete ni la implementación exacta del cálculo de distancias GDIG-102. Los motores fundacionales inspeccionados no contienen una función explícita identificable como cálculo de esa distancia.

## 3. GDIG-101 — representación de patrones

El CSV contiene diez ejecuciones y 400 asignaciones de test por ejecución. Resumen calculado a partir de esos diez registros:

| Métrica | Resultado |
|---|---:|
| Asignaciones al slot A | 3965 / 4000 (99,125 %) |
| Asignaciones al slot B | 35 / 4000 (0,875 %) |
| Asignaciones al slot C | 0 / 4000 (0 %) |
| Ejecuciones con alguna asignación a B | 5 / 10 |
| Ejecuciones con alguna asignación a C | 0 / 10 |
| ESI medio de Explorer | 4,841828 |
| SP medio de Explorer | 0,963398 |
| KS medio de Explorer | 0,733500 |
| IC medio de Core | 0,200325 |

Medias por condición:

| Condición | IC Core | ESI Explorer | SP Explorer | KS Explorer | A (media) | B (media) | C (media) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2 clases | 0,164183 | 4,906619 | 0,972333 | 0,736000 | 397,4 | 2,6 | 0 |
| 3 clases | 0,236467 | 4,777038 | 0,954463 | 0,731000 | 395,6 | 4,4 | 0 |

### Lectura provisional

- En estas ejecuciones, Explorer concentra prácticamente todas las asignaciones en A.
- B recibe una fracción muy pequeña y C permanece vacío en las diez ejecuciones.
- Este resultado no demuestra por sí solo que Explorer sea inferior; sí indica que, bajo estas condiciones, no se observa una diferenciación funcional efectiva de tres slots.
- Un SP alto no debe interpretarse automáticamente como diversidad de representación: junto con la concentración de asignaciones puede ser compatible con una distribución muy estable pero dominada por un único slot.
- La comparación entre IC de Core y ESI/SP/KS de Explorer no es directa: son métricas diferentes y no deben ordenarse como si midieran lo mismo.

**Pregunta experimental pendiente:** ¿Explorer representa estructuras informacionales diferenciadas o concentra la representación en un único atractor?

Para avanzar hay que inspeccionar las matrices de los slots por condición y semilla: normas, similitudes cruzadas y contenido representado, comprobando si A mezcla patrones distintos. No se deben cambiar parámetros antes de completar este análisis.

## 4. GDIG-102 — dependencia del estado inicial

El JSON comunica los siguientes resúmenes:

- Distancia media Core: 2,878267994887334.
- Distancia media Explorer: 1,0922392135710526.

Listas comunicadas:

- Core: 4,0161725568394715; 3,338750364908108; 2,4296067739875666; 3,190543600732124; 2,4187836792779875; 2,6707363324344615; 2,785093403914202; 2,1901781997550067; 3,215643889861431; 2,5271711471629783.
- Explorer: 1,0333841305510374; 1,075162038260802; 1,0030016185435937; 1,1628468425745098; 1,0788024704243186; 1,1338171469750453; 1,1458775940540888; 1,0701056695780122; 1,1252421198886569; 1,094152504860462.

Estos valores se registran como resultados comunicados pendientes de reproducción. No se debe inferir qué fórmula se utilizó (Frobenius, coseno u otra) sin localizar la implementación original.

Hay además una diferencia metodológica que impide interpretar la distancia como comparación estricta de respuesta a una misma entrada: en la reproducción descrita, Core recibió patrones sintéticos de rejilla (clases A/B/C), mientras Explorer recibió señales temporales de 120 s a 250 Hz con ráfagas de frecuencias distintas. La distancia puede describir estabilidad interna dentro de cada motor, pero no establece por sí sola cuál responde mejor ante entradas equivalentes.


## 7. Actualización GDIG-102 — correspondencia óptima entre slots

**Datos recibidos de JMPR el 2026-11-15.** La transcripción estructurada del contenido pegado se conserva en `docs/GDIG102_distancia_correspondencia_optima_comunicado.json`. Este archivo es una transcripción del material comunicado, no el JSON original generado por el entorno experimental.

El análisis contiene diez pares de semillas por motor y, para cada par, una distancia directa y otra tras aplicar la permutación de slots comunicada como óptima.

| Motor | Distancia directa media | Distancia óptima media | Reducción media |
|---|---:|---:|---:|
| DIG Core v1.0 | 2,878268 | 2,823041 | 0,055227 |
| DIG Explorer v1.0 | 1,092239 | 1,092239 | 0,000000 |

**Permutaciones comunicadas:** Core conserva la identidad en 8 de 10 pares y aplica el intercambio A↔B en 2 pares ([1,0,2]); Explorer conserva la identidad en los 10 pares.

### Qué queda respaldado por los datos recibidos

- La estructura de diez pares por motor, las permutaciones transcritas y las medias anteriores se han comprobado aritméticamente a partir del contenido pegado por JMPR y conservado en el JSON de transcripción.
- La optimización reduce ligeramente la distancia media de Core; la reducción no elimina la diferencia entre las medias de ambos motores.
- En Explorer, las permutaciones comunicadas son todas la identidad y no producen reducción.

Esta lectura describe la alineación de las representaciones entre semillas según el procedimiento comunicado. No demuestra que Explorer sea más correcto, más expresivo o científicamente superior. Tampoco resuelve la diferencia metodológica ya señalada: Core y Explorer no recibieron entradas equivalentes.

### Auditoría todavía pendiente

No se ha contrastado la transcripción con el JSON original generado por el entorno ni con el script que produjo los resultados. Tampoco se ha verificado todavía:

1. La fórmula exacta de distancia y la construcción de las matrices/costes.
2. Que las permutaciones seleccionadas sean el mínimo global entre todas las permutaciones admisibles.
3. El tratamiento de empates, el orden de slots y la correspondencia entre matrices.
4. La reproducción independiente desde los artefactos originales, con parámetros, versiones y hashes.

Por tanto, las medias están **verificadas aritméticamente desde la transcripción**, pero el algoritmo, la métrica y la optimalidad global siguen pendientes de auditoría.

## 5. Próximos pasos de auditoría

1. Localizar el script auxiliar que generó el JSON/CSV y calculó GDIG-102.
2. Localizar las señales originales GDIG-101 referenciadas en `signal_file`.
3. Verificar procedencia, hashes y correspondencia entre scripts, señales y resultados.
4. Inspeccionar las matrices de slots de GDIG-101 y generar gráficas de normas y similitudes cruzadas.
5. Recalcular GDIG-102 únicamente cuando se conozca la fórmula original exacta. Si no aparece, documentar la limitación antes de proponer una métrica alternativa, claramente separada de la reproducción.
6. Si se plantea una comparación estricta entre motores, derivar entradas equivalentes a partir de las mismas señales y preregistrar el procedimiento.
7. Conservar resultados negativos, slots vacíos y fallos; no retocar parámetros a posteriori.

## 6. Estado de evidencia

| Elemento | Estado |
|---|---|
| JSON y CSV GDIG-101/102 presentes en GitHub | Verificado por lectura del repositorio |
| Estructura del JSON y diez registros GDIG-101 | Inspeccionado |
| Resumen de asignaciones GDIG-101 | Calculado desde el CSV disponible |
| Matrices de slots | Presentes en JSON; análisis de contenido pendiente |
| Señales originales GDIG-101 | No localizadas en el árbol inspeccionado |
| Script auxiliar de reproducción | Pendiente de localizar |
| Fórmula original GDIG-102 | Pendiente de localizar |
| Distancias directas/óptimas y medias de la transcripción comunicada | Verificadas aritméticamente |
| Optimalidad global de las permutaciones GDIG-102 | Pendiente de auditar algoritmo y matrices/costes |
| Contraste con el JSON original de ejecución | Pendiente |
| Comparación estricta con entradas equivalentes | No realizada |

---

**Principio de integridad:** este informe registra lo que se ha podido inspeccionar y separa explícitamente los resultados comunicados de los verificados. No constituye una validación de la teoría DIG ni una reproducción completa de la campaña.

**Autoría científica:** JMPR.
