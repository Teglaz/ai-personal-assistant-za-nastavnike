
import gradio as gr
import os
import json
from dotenv import load_dotenv
import openai

# Učitaj .env (API KEY)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Učitaj izdavače iz JSON fajla
with open("izdavaci_srednje_skole.json", encoding="utf-8") as f:
    IZDAVACI = json.load(f)

# Učitaj sve škole i gradove iz .txt fajla
with open("srednje_skole_clean_SR.txt", encoding="utf-8") as f:
    LINIJE = [line.strip() for line in f if "|" in line]

# Gradovi i mape škola po gradu
GRADOVI = sorted(set([linija.split("|")[0] for linija in LINIJE]))
SKOLE_PO_GRADU = {}
for linija in LINIJE:
    grad, skola = linija.split("|")
    if grad not in SKOLE_PO_GRADU:
        SKOLE_PO_GRADU[grad] = []
    SKOLE_PO_GRADU[grad].append(skola)

STILOVI_NASTAVE = [
    "Klasična",
    "Radionica",
    "Diskusija",
    "Inovativna",
    "Istraživačka",
    "Interaktivna"
]

# Funkcija za generisanje pripreme
def generisi_pripremu(izdavac, grad, skola, predmet, razred, tema, ishodi, stil):
    if not (tema and predmet and razred and izdavac and skola and grad):
        return "[GREŠKA] Popuni sva obavezna polja!"

    prompt = (
        f"Generiši kompletnu, stručnu i originalnu pripremu časa za srednju školu.\n"
        f"Izdavač: {izdavac}\n"
        f"Grad: {grad}\n"
        f"Škola: {skola}\n"
        f"Predmet: {predmet}\n"
        f"Razred: {razred}\n"
        f"Tema časa: {tema}\n"
        f"Ishodi časa: {ishodi if ishodi else 'nije specificirano'}\n"
        f"Stil nastave: {stil}\n\n"
        f"Struktura: Uvod, Glavni deo (razrada, pitanja, zadaci, aktivnosti, primeri), Zaključak. "
        f"Budi stručan, ali jasan i razumljiv, kao iskusan profesor koji pravi pripremu za kolege. "
        f"Koristi konkretne primere, srpski jezik, i koristi markdown formatiranje (## Naslovi, - stavke, **bold**)."
    )

    try:
        odgovor = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ti si iskusan nastavnik koji piše digitalne pripreme za čas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.45,
            max_tokens=1300
        )
        return odgovor.choices[0].message.content.strip()
    except Exception as e:
        return f"[GREŠKA - AI] {e}"

# Dinamičko ažuriranje škola na osnovu izabranog grada
def upd_skole(grad):
    lista_skola = sorted(SKOLE_PO_GRADU.get(grad, []))
    return gr.update(choices=lista_skola, value=None)

with gr.Blocks(theme=gr.themes.Base(), css="body {background-color: #222;}") as demo:
    gr.Markdown(
        "# AI Priprema za Nastavnike\n"
        "*Generiši kompletnu pripremu časa za par sekundi sa odabranim stilom izvođenja i školom po gradu!*"
    )

    with gr.Row():
        with gr.Column():
            grad_dd = gr.Dropdown(choices=GRADOVI, label="Grad", interactive=True)
            skola_dd = gr.Dropdown(choices=[], label="Škola", interactive=True)
            izdavac_dd = gr.Dropdown(choices=IZDAVACI, label="Izdavač", interactive=True)
            predmet_tb = gr.Textbox(label="Predmet", placeholder="npr. Matematika", lines=1)
            razred_tb = gr.Textbox(label="Razred", placeholder="npr. III razred srednje škole", lines=1)
            tema_tb = gr.Textbox(label="Tema časa", placeholder="npr. Francuska revolucija", lines=1)
            ishodi_tb = gr.Textbox(label="Ishodi časa (opciono)", placeholder="npr. Razume uzroke i posledice ustanka", lines=2)
            stil_dd = gr.Dropdown(choices=STILOVI_NASTAVE, label="Stil nastave", value="Klasična")
            dugme = gr.Button("Generiši pripremu")
            gr.ClearButton([predmet_tb, razred_tb, tema_tb, ishodi_tb, stil_dd], value="Očisti polja")

        with gr.Column():
            prikaz = gr.Textbox(label="Priprema za čas", lines=22, interactive=False, show_copy_button=True)

    grad_dd.change(fn=upd_skole, inputs=grad_dd, outputs=skola_dd)
    dugme.click(
        generisi_pripremu,
        inputs=[izdavac_dd, grad_dd, skola_dd, predmet_tb, razred_tb, tema_tb, ishodi_tb, stil_dd],
        outputs=prikaz
    )

if __name__ == "__main__":
    port = int(os.environ.get("GRADIO_SERVER_PORT", 7870))
    demo.launch(server_name="127.0.0.1", server_port=port, show_error=True)
