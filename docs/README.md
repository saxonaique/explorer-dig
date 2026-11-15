# Índice documental — Génesis DIG

**Repositorio:** `saxonaique/explorer-dig`  
**Responsable documental:** ChatGPT  
**Dirección científica:** JMPR

Este índice describe la organización actual del repositorio. No implica que todos los experimentos estén reproducidos o validados.

## Código fundacional

- [DIG_Explorer_v1/](../DIG_Explorer_v1/README.md): paquete original del Explorer v1.0.
- [dig_core_v1.py](../DIG_Explorer_v1/dig_core_v1.py): motor Core fundacional.
- [dig_explorer.py](../DIG_Explorer_v1/dig_explorer.py): motor Explorer fundacional.

Estos motores se conservan como originales. Las campañas comparativas deben identificar expresamente cuál de ellos utilizan y no confundirlos con versiones experimentales posteriores.

## Protocolos y gestión

- [Protocolo de documentación de Génesis DIG](PROTOCOLO_DOCUMENTACION_GENESIS_DIG.md): estados de evidencia, conservación de versiones y flujo documental.
- [Plantilla experimental maestra](PLANTILLA_EXPERIMENTAL_GENESIS_DIG.md): estructura común para diseñar y documentar experimentos.

## Comparativa 001 — Core vs Explorer

- [Auditoría preliminar GDIG-101/102](AUDITORIA_PRELIMINAR_GDIG101_102.md): hallazgos, límites de evidencia y próximos pasos de reproducción.
- [Correspondencia óptima GDIG-102 — transcripción comunicada (JSON)](GDIG102_distancia_correspondencia_optima_comunicado.json): diez pares por motor con distancias directas, óptimas y permutaciones comunicadas.
- [Resultados estructurados GDIG-101/102 (JSON)](GDIG101_102_reproduccion_resultados.json): diez registros GDIG-101 con matrices de slots de ambos motores y resumen comunicado de GDIG-102.
- [Resumen tabular GDIG-101/102 (CSV)](GDIG101_102_reproduccion_resultados.csv): métricas resumidas por condición y semilla.

**Estado documental:** los archivos JSON y CSV de la Comparativa 001 están presentes en el repositorio. Las señales originales CSV de GDIG-101 todavía no constan en el árbol inspeccionado. Las medias de distancias directas y óptimas del análisis de correspondencia GDIG-102 se han comprobado aritméticamente desde la transcripción del contenido comunicado por JMPR; esta transcripción no sustituye al JSON original. La fórmula, el script y la optimalidad global de las permutaciones siguen pendientes de auditoría independiente. No debe confundirse una comprobación aritmética con una reproducción experimental.

## Organización prevista para nuevos materiales

- `docs/`: protocolos, índices, auditorías e informes.
- `experiments/`: scripts y definiciones de campañas cuando se incorporen.
- `results/`: resultados derivados, tablas y figuras cuando se incorporen.
- `data/`: entradas y datasets, con procedencia y licencias documentadas.
- `archive/`: materiales históricos que deban conservarse sin mezclarlos con versiones activas.

Las carpetas previstas no se crean vacías ni se mueven archivos por anticipado. Cada incorporación debe responder a una campaña concreta y mantener trazabilidad.

---

**Regla de integridad:** no mover ni sobrescribir motores originales, preregistros o resultados históricos sin una razón documentada. Los datos no se modifican para ajustarlos a la teoría.
