"""PMV Compra Fácil Bajío: detector de reseñas negativas con el BETO ajustado del DEV.

El modelo pesa ~440 MB y está en Hugging Face (no cabe en GitHub):
https://huggingface.co/LuisPablo54/beto-resenas-negativas
La primera vez se descarga solo; después queda guardado en la computadora.

Correr desde la raíz del repo:  python pmv/app_resenas.py
Luego abrir http://127.0.0.1:7860
"""
import gradio as gr
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODELO = "LuisPablo54/beto-resenas-negativas"
UMBRAL = 0.5

tokenizer = AutoTokenizer.from_pretrained(MODELO)
modelo = AutoModelForSequenceClassification.from_pretrained(MODELO)
modelo.eval()


def clasificar(texto):
    if not texto or not texto.strip():
        return {}, "Escribe o pega una reseña."
    entrada = tokenizer(texto, truncation=True, max_length=128, return_tensors="pt")
    with torch.no_grad():
        probs = torch.softmax(modelo(**entrada).logits, dim=-1)[0]
    p_neg = float(probs[1])  # salida 1 = reseña NEGATIVA

    if p_neg >= UMBRAL:
        veredicto = (f"### NEGATIVA: prioridad alta\nAtención a clientes debe responder primero.\n\n"
                     f"Probabilidad de que sea negativa: **{p_neg:.1%}**")
    else:
        veredicto = (f"### Positiva: prioridad normal\n\n"
                     f"Probabilidad de que sea negativa: **{p_neg:.1%}**")
    return {"Negativa": p_neg, "Positiva": 1 - p_neg}, veredicto


ejemplos = [
    "Llegó roto y el vendedor no contesta. No lo vuelvo a comprar.",
    "Excelente calidad, llegó antes de lo esperado. Muy recomendable.",
    "El producto de 10. El envío pésimo, dejaron el paquete en un buzón exterior.",
    "Tiene buena calidad, no me gusta su estética, pero para gusto hay colores.",
]

TEMA = gr.themes.Default(primary_hue="blue", neutral_hue="slate", font=[gr.themes.GoogleFont("Inter"), "sans-serif"]).set(
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


with gr.Blocks(title="Compra Fácil Bajío · Reseñas negativas") as demo:
    gr.Markdown(
        "# Compra Fácil Bajío · Detector de reseñas negativas\n"
        "Pega una reseña. El modelo (BETO ajustado) la marca como **negativa** si la probabilidad es "
        "de 50 % o más, para que atención a clientes responda primero a quien está molesto."
    )
    texto = gr.Textbox(lines=4, label="Reseña del cliente", placeholder="Escribe o pega una reseña…")
    boton = gr.Button("Clasificar", variant="primary")
    with gr.Row():
        etiqueta = gr.Label(label="Resultado", num_top_classes=2)
        veredicto = gr.Markdown()
    gr.Examples(ejemplos, inputs=texto)

    boton.click(clasificar, inputs=texto, outputs=[etiqueta, veredicto])
    texto.submit(clasificar, inputs=texto, outputs=[etiqueta, veredicto])

if __name__ == "__main__":
    demo.launch(theme=TEMA, css=CSS, js=JS_CLARO)
