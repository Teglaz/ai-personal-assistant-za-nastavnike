import gradio as gr

PLH = "⟨ izaberi školu ⟩"
MESTA = ["Novi Sad"]
ŠKOLE = {"Novi Sad": ["Jovan Jovanović Zmaj", "Tehnička škola"]}

def upd(mesto):
    # placeholder + liste škola, value = placeholder
    return gr.Dropdown.update(choices=[PLH] + ŠKOLE[mesto], value=PLH)

with gr.Blocks() as demo:
    gr.Markdown("## Mini test – bez crvene ivice")

    mesto = gr.Dropdown(MESTA, label="Grad / opština")
    skola = gr.Dropdown([PLH], value=PLH, label="Škola", interactive=True)

    mesto.change(fn=upd, inputs=mesto, outputs=skola)

demo.launch()
