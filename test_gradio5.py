import gradio as gr

def prikazi_izbor(izbor):
    return f"Odabrao si: {izbor}"

with gr.Blocks() as demo:
    dropdown = gr.Dropdown(choices=["Opcija 1", "Opcija 2", "Opcija 3"], label="Izaberi nešto")
    output = gr.Textbox(label="Rezultat")
    dropdown.change(prikazi_izbor, dropdown, output)

demo.launch(server_name="127.0.0.1", server_port=8899, show_error=True)
