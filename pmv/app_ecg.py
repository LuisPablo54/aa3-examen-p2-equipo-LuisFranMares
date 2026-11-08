"""PMV CardioRitmo: tamizaje de latidos con el Conv1D elegido (ecg/modelo/modelo_ecg.keras).

Correr desde la raíz del repo:  python pmv/app_ecg.py
Luego abrir http://127.0.0.1:7860
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import gradio as gr
import keras
from sklearn.model_selection import train_test_split

RAIZ = Path(__file__).resolve().parent.parent
MODELO = RAIZ / "ecg" / "modelo" / "modelo_ecg.keras"
UMBRAL = 0.5

# Modelo elegido en el DEV
modelo = keras.models.load_model(MODELO)

# Mismos datos y misma división que el enunciado, para tener latidos de demostración
ecg = pd.read_csv("https://storage.googleapis.com/download.tensorflow.org/data/ecg.csv", header=None)
X = ecg.iloc[:, :-1].to_numpy("float32")
y = 1 - ecg.iloc[:, -1].to_numpy("int64")  # 1 = ANORMAL
_, X_demo, _, y_demo = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)


def analizar(indice):
    i = int(indice)
    latido = X_demo[i]
    p = float(modelo.predict(latido.reshape(1, 140, 1), verbose=0)[0, 0])
    anormal = p >= UMBRAL

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(latido, color="#c0392b" if anormal else "#2e86c1", linewidth=2)
    ax.set_xlabel("Muestra (140 por latido)")
    ax.set_ylabel("Amplitud normalizada")
    ax.set_title(f"Latido #{i}")
    ax.grid(alpha=0.3)
    fig.tight_layout()

    if anormal:
        veredicto = f"### ANORMAL: enviar al cardiólogo\nProbabilidad de anomalía: **{p:.1%}**"
    else:
        veredicto = f"### Normal: no requiere revisión\nProbabilidad de anomalía: **{p:.1%}**"
    real = "anormal" if y_demo[i] == 1 else "normal"
    veredicto += f"\n\n_Etiqueta real de este latido de demostración: {real}._"

    return {"Anormal": p, "Normal": 1 - p}, veredicto, fig


def aleatorio():
    return int(np.random.randint(len(X_demo)))


TEMA = gr.themes.Default(primary_hue="red", neutral_hue="slate", font=[gr.themes.GoogleFont("Inter"), "sans-serif"]).set(
    body_background_fill="#f7f8fa",
    background_fill_primary="#ffffff",
    background_fill_secondary="#f7f8fa",
    block_background_fill="#ffffff",
    block_border_color="#e3e6eb",
    block_shadow="0 1px 3px rgba(0, 0, 0, 0.06)",
)
CSS = ".gradio-container {max-width: 980px !important; margin: auto;} footer {display: none !important;}"
# Fuerza el modo claro aunque el navegador esté en modo oscuro
JS_CLARO = """() => {
  const url = new URL(window.location);
  if (url.searchParams.get('__theme') !== 'light') {
    url.searchParams.set('__theme', 'light');
    window.location.href = url.href;
  }
}"""


with gr.Blocks(title="CardioRitmo · Tamizaje de latidos") as demo:
    gr.Markdown(
        "# CardioRitmo · Tamizaje de latidos\n"
        "Elige un latido del registro Holter. El modelo (Conv1D, 1,521 parámetros) lo marca como "
        "**anormal** si la probabilidad es de 50 % o más, para que el cardiólogo revise solo esos.\n\n"
        "> Herramienta de **tamizaje**, no de diagnóstico."
    )
    with gr.Row():
        indice = gr.Slider(0, len(X_demo) - 1, value=0, step=1, label="Número de latido")
        with gr.Column():
            boton = gr.Button("Analizar latido", variant="primary")
            boton_azar = gr.Button("Latido al azar")
    with gr.Row():
        etiqueta = gr.Label(label="Resultado", num_top_classes=2)
        veredicto = gr.Markdown()
    grafica = gr.Plot(label="Señal del latido")

    boton.click(analizar, inputs=indice, outputs=[etiqueta, veredicto, grafica])
    boton_azar.click(aleatorio, outputs=indice).then(
        analizar, inputs=indice, outputs=[etiqueta, veredicto, grafica]
    )
    demo.load(analizar, inputs=indice, outputs=[etiqueta, veredicto, grafica])

if __name__ == "__main__":
    demo.launch(theme=TEMA, css=CSS, js=JS_CLARO)
