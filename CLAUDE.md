# CLAUDE.md — Examen Parcial II (IN1042 · Aprendizaje Automático III)

Contexto para Claude y para el equipo. Fecha límite: **viernes 6 nov 2026, 23:59**. Se califica el último commit antes de esa hora.
**Corte de seguridad: commit + push a las 22:30.** Lo que llegue después es mejora.

## Equipo y reparto

| Integrante | Responsable de | Archivos que le pertenecen |
|---|---|---|
| **Luis** | Problema 2 · Compra Fácil Bajío (reseñas) | `resenas/DEV_resenas.ipynb`, `resenas/resultados_resenas.csv`, `resenas/modelo/` |
| **Francisco** | Problema 1 · CardioRitmo (ECG) | `ecg/DEV_ecg.ipynb`, `ecg/resultados_ecg.csv`, `ecg/modelo/` |
| **Mares** | Folletos, maquetas del PMV, README, app PMV (extra) | `ecg/folleto_ecg.pdf`, `resenas/folleto_resenas.pdf`, `pmv/`, `README.md` |

Revisión cruzada: Luis revisa ECG, Francisco revisa Reseñas, y Mares revisa que los números de los folletos coincidan con los CSV.

**Regla del examen:** cada quien sube **sus propios commits** con su cuenta. Lo que diga el README sobre quién hizo qué debe verse en el historial. No hagan commits del trabajo de otro.

## Reglas que no se rompen

- Copiar **literal** la carga y la división del PDF (ya están en los cuadernos esqueleto; no las modifiquen).
- **La prueba se evalúa una sola vez**, al final, con los modelos ya congelados. Todo se decide con validación.
- Umbral fijo en **0.5**. Para cumplir especificaciones se usa `class_weight`, arquitectura o datos; nunca se mueve el umbral.
- Fijar semillas (`SEED = 42`) en `random`, `numpy` y `tensorflow`/`torch`.
- Los transformadores (escalador, vectorizador, tokenizador) se ajustan **solo con train**.
- El cuaderno se entrega **ejecutado de arriba abajo con salidas**: reiniciar el kernel y ejecutar todo antes del commit final.
- Archivos de más de 100 MB no van al repo: se suben a Hugging Face o Drive y el enlace va en el README.

## Problema 1 · ECG (Francisco)

- **Especificaciones (prueba, umbral 0.5):** sensibilidad ≥ 0.95, especificidad ≥ 0.95, **≤ 20,000 parámetros entrenables**.
- Validación: 20 % estratificado de `X_resto` (`random_state=42`). `reshape (n, 140, 1)` para Conv1D/RNN.
- Línea base: `DummyClassifier(strategy="most_frequent")`.
- Modelos: MLP 140→64→32→1 (~11.2k), Conv1D pequeño (~2.8k, `convolucional`), GRU/LSTM(32) (~3–5k, `recurrente`). EarlyStopping sobre `val_loss`.
- Elegir: cumple ambas especificaciones en validación con margen y luego tiene menos parámetros.
- `resultados_ecg.csv`: `modelo, tipo, parametros, sensibilidad, especificidad, auc, cumple, elegido`.
- 3 errores: graficar los latidos mal clasificados (FN y FP) contra el promedio de su clase.
- Guardar `ecg/modelo/modelo_ecg.keras`.
- Límite clave: un solo paciente con insuficiencia cardiaca; los latidos vienen ya segmentados y normalizados.

## Problema 2 · Reseñas (Luis)

- **Especificaciones (prueba, umbral 0.5):** exhaustividad ≥ 0.90, precisión ≥ 0.85. Modelo propio (un LLM por API no cuenta).
- Reseñas de 3★: **se quitan** de train y de validación, porque son ambiguas y la prueba no las incluye. Hay que justificarlo en una línea en el cuaderno.
- Validación: partición `validation` sin las de 3★.
- Línea base: `DummyClassifier`.
- Modelos: TF-IDF (1 y 2 gramas) + red densa; Embedding + Bi-LSTM (`recurrente`); BETO ajustado (`dccuchile/bert-base-spanish-wwm-cased`, 40–60k reseñas, `max_len` 128, 1–2 épocas en Colab con GPU, `transformer`).
- `resultados_resenas.csv`: `modelo, tipo, parametros, exhaustividad, precision, exactitud, cumple, elegido`.
- 3 errores: mostrar el texto (sarcasmo, "bueno pero llegó roto", reseñas cortas).
- BETO pesa ~440 MB: subir a Hugging Face y poner el enlace en el README. Si se elige TF-IDF, guardar el `.keras` y el vectorizador `.pkl` en `resenas/modelo/`.

## Folletos (Mares) — PDF de 2 cuartillas como máximo, dirigidos al director

1. Problema y propuesta de valor.
2. Maqueta del PMV (captura de Gradio, Figma o Canva).
3. Desempeño en palabras del cliente ("de cada 100 latidos anormales, marca 97"), diciendo si **cumple** cada especificación.
4. Limitaciones, cada una respaldada por un número o un error concreto del DEV.
5. Aviso ético y propuesta de mejora.
6. Si un modelo no cumple, decirlo y explicar qué faltaría (así se rescatan 5 de 10 puntos).

Los números se toman de los CSV finales; pídanselos a Luis y Francisco en cuanto evalúen la prueba.

## PMV (extra, Mares)

App de Gradio en `pmv/` que carga el modelo de `modelo/` y clasifica. Medio punto por problema. Incluir instrucciones en el README y una captura o un video corto.

## Cronograma

| Bloque | Francisco (ECG) | Luis (Reseñas) | Mares |
|---|---|---|---|
| 1 | Exploración y preparación | Exploración y preparación; lanzar BETO en Colab | README y plantilla del folleto |
| 2 | 3 modelos, selección en validación | TF-IDF + densa, Bi-LSTM | Maquetas del PMV |
| 3 | Prueba única, CSV, 3 errores, guardar modelo | Prueba única, CSV, 3 errores, subir a HF | Llenar folletos con los números |
| 4 | Reiniciar y ejecutar todo con salidas | Reiniciar y ejecutar todo con salidas | Exportar PDF, README final |
| Extra | | | Gradio en `pmv/` |

## Checklist final

- [ ] Liga del repo (público) en Moodle
- [ ] Los dos `.ipynb` ejecutados de arriba abajo con salidas
- [ ] La prueba se usó una sola vez
- [ ] Los dos CSV con columnas exactas y `elegido=True` en una sola fila
- [ ] Modelos en `modelo/`, o enlace en el README si pasan de 100 MB
- [ ] Folletos PDF de 2 cuartillas como máximo
- [ ] README con integrantes, quién hizo qué (coincide con los commits) y el modelo elegido

**Duda abierta con el profesor:** la columna `tipo` solo acepta `linea base, recurrente, convolucional, conjunto, embeddings, transformer`. Si no responde, el MLP y TF-IDF + densa usan la categoría más cercana (`embeddings` para TF-IDF) y se anota en el cuaderno.
