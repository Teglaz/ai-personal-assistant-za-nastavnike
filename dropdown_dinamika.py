import gradio as gr

# Simulacija baze podataka
skole_po_gradu = {
    "Novi Sad": ["Jovan Jovanović Zmaj", "Svetozar Marković", "Laza Kostić"],
    "Beograd": ["Treća gimnazija", "Petnica", "Deseta gimnazija"],
    "Niš": ["Bora Stanković", "Stevan Sremac"]
}

def promeni_skole(grad):
    if grad and grad in skole_po_gradu:
        return gr.update(choices=skole_po_gradu[grad], value=None)
    else:
        return gr.update(choices=[], value=None)

with gr.Blocks() as demo:
    grad = gr.Dropdown(choices=list(skole_po_gradu.keys()), label="Grad")
    skola = gr.Dropdown(choices=[], label="Škola")
    prikaz = gr.Textbox(label="Izbor")

    grad.change(promeni_skole, inputs=grad, outputs=skola)
    skola.change(lambda x: f"Izabrana škola: {x}", inputs=skola, outputs=prikaz)

demo.launch(server_name="127.0.0.1", server_port=8898, show_error=True)
