# GÉNESIS DIG
## Plantilla maestra de documentación experimental

**Proyecto:** Teoría de la Dualidad Información-Gravedad (DIG)  
**Instrumento:** DIG Explorer — Microscopio Informacional  
**Autor:** José María Pérez Rodríguez (JMPR)  
**Versión de la plantilla:** 1.0  
**Estado:** Documento reutilizable

> Esta plantilla documenta experimentos; no ejecuta simulaciones ni modifica DIG Explorer. Los resultados comunicados en investigaciones anteriores no se consideran reproducidos por el mero hecho de aparecer aquí.

---

## 1. Identificación del experimento

- **Código:**
- **Serie:**
- **Nombre:**
- **Fecha:**
- **Responsable:**
- **Estado:** diseñado / en ejecución / completado / bloqueado / descartado.
- **Experimentos relacionados:**

**Descripción breve:** ¿Qué se va a investigar y por qué?

## 2. Objetivo y pregunta de investigación

- **Objetivo principal:**
- **Pregunta central:** ¿Cómo evoluciona el espacio informacional al recibir esta información?
- **Hipótesis inicial:**
- **Hipótesis alternativa:**
- **Criterio de éxito o de resultado informativo:**

Un resultado negativo también puede aportar conocimiento. No se debe modificar el criterio de éxito después de conocer los resultados sin dejar constancia.

## 3. Simulador físico

Esta sección describe exclusivamente el sistema físico que genera los datos.

- **Sistema o fenómeno estudiado:**
- **Modelo matemático y ecuaciones:**
- **Método numérico e integrador:**
- **Resolución espacial y temporal:**
- **Condiciones de contorno:**

### Propiedades físicas representadas

| Propiedad | Valor / definición | ¿Está implementada? | Evidencia en el código |
|---|---|---|---|
| Masa | | | |
| Carga eléctrica | | | |
| Espín | | | |
| Energía | | | |
| Momento | | | |
| Potencial | | | |
| Interacciones | | | |
| Otras | | | |

**Propiedades relevantes no implementadas:** indicar expresamente qué características reales no contempla el modelo. No atribuir al experimento efectos que el simulador no puede producir.

## 4. Parámetros y condiciones iniciales

| Parámetro | Valor | Unidad | Observaciones |
|---|---:|---|---|
| Tiempo inicial | | | |
| Tiempo final | | | |
| Número de pasos | | | |
| Posición inicial | | | |
| Velocidad / momento inicial | | | |
| Energía inicial | | | |
| Resolución espacial | | | |
| Paso temporal | | | |

- **Geometría y configuración:**
- **Barreras o potenciales:**
- **Campos externos:**
- **Otras condiciones:**
- **Número de semillas:**
- **Semillas exactas:**
- **Código, versión o commit del simulador:**
- **Configuración guardada:**

## 5. Controles y comprobación física previa

Antes de introducir datos en Explorer, comprobar que el simulador ha producido realmente el fenómeno que se pretende estudiar.

| Comprobación | Resultado / evidencia |
|---|---|
| La partícula alcanza la región de interacción | |
| La barrera modifica la evolución, si corresponde | |
| El campo externo está activo y afecta al sistema | |
| El tiempo simulado es suficiente | |
| Las condiciones iniciales son correctas | |
| No hay errores numéricos relevantes | |
| La evolución concuerda con el modelo esperado | |
| Existe un control sin interacción, cuando proceda | |

**Observaciones y gráficas de control:**

Si la interacción no llega a producirse, no puede estudiarse su efecto. Registrar desplazamientos, tiempos, escalas y evidencia directa, no solo la configuración solicitada.

## 6. Datos originales generados por el simulador

Describir los datos físicos antes de cualquier transformación.

- **Archivos originales y ubicación:**
- **Formato:**
- **Dimensiones:**
- **Número de muestras:**
- **Variables y unidades:**
- **Resolución espacial y temporal:**

### Información disponible

- [ ] Amplitud
- [ ] Fase
- [ ] Función de onda compleja
- [ ] Parte real e imaginaria
- [ ] Evolución temporal completa
- [ ] Distribución espacial
- [ ] Espín u otras variables físicas
- [ ] Otras:

**Información no conservada o no generada:**  
**Integridad:** hash/checksum, código generador y registro de generación.

## 7. Adaptador y representación de entrada

El adaptador transforma los datos físicos para que Explorer pueda procesarlos. Debe quedar claro qué información conserva, transforma o descarta.

- **Código y versión del adaptador:**
- **Representación utilizada:** amplitud / fase / compleja / espacio-temporal / otra.
- **Dimensiones originales:**
- **Dimensiones entregadas a Explorer:**
- **Normalización y escalado:**
- **Redimensionamiento o reducción dimensional:**
- **Filtrado, interpolación u otras transformaciones:**
- **Información conservada:**
- **Información perdida o alterada:**
- **Justificación de la representación:**

### Controles de fase y datos complejos

- [ ] La fase se trata como magnitud circular, no como variable lineal ordinaria.
- [ ] Se evitan discontinuidades artificiales en el salto entre +π y −π.
- [ ] Se trata adecuadamente la fase indefinida donde la amplitud es prácticamente cero.
- [ ] La representación compleja conserva parte real e imaginaria.
- [ ] No se elimina evolución temporal relevante sin justificarlo.
- [ ] Se conservan los datos originales junto a los transformados.

## 8. Identificación e integridad de DIG Explorer

- **Versión exacta:**
- **Repositorio y ruta:**
- **Commit:**
- **Archivos ejecutados:**
- **Configuración completa:**
- **Entorno y dependencias:**

| Parámetro de Explorer | Valor |
|---|---:|
| Número de slots | |
| Dimensión del campo | |
| Beta | |
| Bootstrap | |
| Semillas | |
| Duración de entrenamiento | |
| Duración de evaluación | |
| Otros | |

**Integridad del motor:**
- [ ] Se ha utilizado la versión original identificada.
- [ ] Se ha conservado una copia intacta.
- [ ] Se han registrado cambios de parámetros.
- [ ] Se ha registrado cualquier modificación de código.
- [ ] Los hashes o commits permiten identificar exactamente la versión.

Cualquier modificación del núcleo debe tratarse como una versión experimental independiente. No sustituir ni alterar silenciosamente la versión de referencia.

## 9. Registro temporal de la dinámica interna

Esta sección es central: no observar únicamente el estado final. Registrar qué sucede durante la evolución del motor, en la medida en que la versión utilizada permita observarlo.

### 9.1 Campo dinámico
- Estado inicial:
- Evolución del campo:
- Variaciones de intensidad:
- Distribución espacial:
- Momentos de reorganización:
- Estado final:
- Archivos y frecuencia de registro:

### 9.2 Actividad y ocupación de slots

| Tiempo / paso | Actividad slot 1 | Actividad slot 2 | Actividad slot 3 | Slot dominante / ocupación |
|---|---:|---:|---:|---|
| Inicial | | | | |
| 25 % | | | | |
| 50 % | | | | |
| 75 % | | | | |
| Final | | | | |

Registrar también competencia, cambios de ocupación y transiciones entre slots, si están disponibles.

### 9.3 Patrones almacenados
- Patrones iniciales:
- Patrones incorporados:
- Patrones modificados:
- Patrones olvidados:
- Patrones consolidados:
- Cambios o transferencias entre slots:

### 9.4 Novedad y reorganización
- Evolución temporal de la novedad:
- Cambios bruscos:
- Transiciones:
- Periodos de estabilidad:
- Cambios persistentes:
- Diferencias entre semillas:

### 9.5 Huella temporal
- **Archivo:**
- **Número de pasos registrados:**
- **Frecuencia de registro:**
- **Variables incluidas:**
- **Formato:**
- **Limitaciones de observabilidad:**

No dar por disponibles variables que el motor no expone. Si obtenerlas exige modificar el núcleo, documentarlo como trabajo futuro en una versión experimental separada; no alterar el motor de referencia para completar esta plantilla.

## 10. Resultados finales de Explorer

Registrar las métricas tal como las produce la versión utilizada, junto con su definición y variabilidad.

| Métrica | Resultado | Variabilidad / intervalo | Definición y observaciones |
|---|---:|---:|---|
| Aprendizaje final | | | |
| Novedad final | | | |
| ESI | | | |
| SP | | | |
| KS | | | |
| Ocupación de slots | | | |
| Otras | | | |

- **Resultados por semilla:**
- **Curvas temporales:**
- **Diferencias respecto a controles:**
- **Advertencias de cálculo o estabilidad:**

No sustituir las series temporales por promedios cuando la pregunta investigada se refiera a la dinámica interna.

## 11. Análisis externo

Esta sección corresponde a herramientas o análisis posteriores a Explorer.

- **Método utilizado:**
- **Clasificador o modelo externo (si existe):**
- **Características utilizadas:**
- **División entrenamiento / prueba:**
- **Unidad de separación:** trayectoria / semilla / ejecución / otra.
- **Validación independiente:**

### Resultados estadísticos
- Accuracy y baseline:
- Matriz de confusión:
- Intervalos de confianza:
- Valores p:
- Tamaño del efecto:
- Otros:

### Independencia y prevención de fugas
- [ ] Las trayectorias de prueba son independientes de las de entrenamiento.
- [ ] Las semillas de prueba no aparecen en entrenamiento cuando se afirma generalización a semillas nuevas.
- [ ] No hay muestras duplicadas o ventanas solapadas repartidas entre ambos conjuntos.
- [ ] Las transformaciones y normalizaciones se ajustan solo con entrenamiento cuando corresponde.
- [ ] La selección de características no utiliza información del conjunto de prueba.
- [ ] Se conserva una evaluación externa o bloqueada, si está disponible.

Un clasificador externo puede encontrar diferencias en las huellas temporales, pero eso no significa que Explorer haya realizado esa clasificación. Informar por separado el comportamiento del motor y el rendimiento del analizador.

## 12. Resultados del experimento

### A. Resultados positivos
¿Qué se observó y qué evidencia lo respalda?

### B. Resultados negativos
¿Qué se esperaba y no apareció?

### C. Anomalías
¿Qué comportamientos no previstos surgieron?

### D. Resultados ambiguos
¿Qué no puede interpretarse todavía?

### E. Reproducibilidad
¿Se repitió con semillas o trayectorias independientes? ¿Qué se mantuvo y qué cambió?

## 13. Interpretación y límites

Separar tres niveles:

1. **Hechos observados:** resultados directos del simulador, registros de Explorer y mediciones.
2. **Interpretación del comportamiento:** qué parece indicar la respuesta del sistema y qué explicaciones alternativas existen.
3. **Hipótesis DIG:** posibles conexiones con la Teoría de la Dualidad Información-Gravedad.

- **Conclusión principal:**
- **Limitaciones del simulador:**
- **Limitaciones de la representación y el adaptador:**
- **Limitaciones de Explorer:**
- **Limitaciones estadísticas:**
- **Qué hemos aprendido:**
- **Qué no podemos afirmar todavía:**

No presentar una correlación o una métrica como demostración de un mecanismo físico fundamental. Distinguir resultados de simulación, resultados del instrumento y evidencia experimental del mundo físico.

## 14. Archivos, datos y logs que deben conservarse

- [ ] Código y versión del simulador.
- [ ] Ecuaciones y configuración.
- [ ] Semillas y condiciones iniciales.
- [ ] Datos físicos originales.
- [ ] Datos transformados y código del adaptador.
- [ ] Versión intacta de Explorer y commit.
- [ ] Configuración de ejecución y dependencias.
- [ ] Huellas temporales y registros internos disponibles.
- [ ] Métricas y resultados por semilla.
- [ ] Datos y código del análisis externo.
- [ ] Gráficas, logs completos y errores.
- [ ] Documento de síntesis.
- [ ] Hashes/checksums de los archivos importantes.

**Ubicación:**  
**Repositorio o carpeta:**  
**Copia de seguridad:**  

## 15. Comprobaciones previas obligatorias

- [ ] **Entrada reducida o incompleta:** comprobar que no se ha sustituido una evolución espacio-temporal por un perfil final u otra representación empobrecida sin justificarlo.
- [ ] **Fase incorrecta:** tratarla circularmente y controlar saltos ±π y regiones de amplitud nula.
- [ ] **Interacción no alcanzada:** demostrar que la partícula o el sistema llega a la región de interacción y que esta modifica la evolución.
- [ ] **Propiedades físicas ausentes:** verificar en el código qué masa, carga, espín, campos e interacciones están realmente implementados.
- [ ] **Fuga entre entrenamiento y prueba:** separar trayectorias o semillas independientes y evitar duplicados o ventanas relacionadas.
- [ ] **Confusión entre clasificador y motor:** informar por separado lo que produce Explorer y lo que deduce un analizador externo.
- [ ] **Versión alterada:** identificar el commit y conservar intacta la versión de referencia.
- [ ] **Solo métrica final:** conservar y estudiar la evolución temporal cuando esté disponible.

## 16. Cierre del experimento

- **Estado:** completado / incompleto / bloqueado / descartado.
- **Conclusión resumida:**
- **Principal hallazgo:**
- **Principal limitación:**
- **Archivos conservados:**
- **Siguiente experimento justificado:**

No iniciar automáticamente nuevas pruebas. La siguiente etapa debe decidirse a partir de los resultados obtenidos.

---

## Principio rector de Génesis DIG

La investigación no debe adaptar el motor para obtener un resultado esperado. Debe observar qué ocurre cuando la información entra en el espacio informacional, estudiar cómo evoluciona y descubrir qué organización emerge de sus reglas de interacción.

**No estudiar únicamente qué produce Explorer. Estudiar qué sucede dentro de Explorer mientras funciona.**

**JMPR — Génesis DIG**
