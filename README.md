# aa3-examen-p2-equipo-LuisFranMares

Examen del Parcial II — IN1042 Aprendizaje Automático III (Otoño 2026, grupo A7).

## Integrantes y quién hizo qué

| Integrante | Trabajo |
|---|---|
| Luis | Problema 2 · Compra Fácil Bajío (reseñas): DEV, resultados y modelo |
| Francisco | Problema 1 · CardioRitmo (ECG): DEV, resultados y modelo |
| Mares | Folletos de ambos problemas, maquetas del PMV, README y app PMV |

## Modelo elegido por problema

| Problema | Modelo elegido | ¿Cumple? | Archivo / enlace |
|---|---|---|---|
| CardioRitmo (ECG) | _pendiente_ | _pendiente_ | `ecg/modelo/` |
| Compra Fácil Bajío (reseñas) | BETO ajustado (`dccuchile/bert-base-spanish-wwm-cased`) | Sí: exhaustividad 0.957, precisión 0.931 en prueba | ~440 MB, no cabe en GitHub: [huggingface.co/LuisPablo54/beto-resenas-negativas](https://huggingface.co/LuisPablo54/beto-resenas-negativas) |

## Estructura

```
├── README.md
├── ecg/
│   ├── DEV_ecg.ipynb
│   ├── resultados_ecg.csv
│   ├── modelo/
│   └── folleto_ecg.pdf
├── resenas/
│   ├── DEV_resenas.ipynb
│   ├── resultados_resenas.csv
│   ├── modelo/
│   └── folleto_resenas.pdf
└── pmv/
```

## PMV (opcional)

_Pendiente: instrucciones para correr la app y captura._
