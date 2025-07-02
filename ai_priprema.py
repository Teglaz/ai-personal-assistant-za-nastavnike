import os, gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

# --------------------------------------------------
# KONFIGURACIJA
# --------------------------------------------------
load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --------------------------------------------------
# DEMO BAZA ŠKOLA (OSNOVNE)
# --------------------------------------------------
MESTA = ["Beograd", "Novi Sad", "Niš", "Subotica", "Kragujevac"]
OSN_SK = {
    "Beograd":    ["OŠ Vuk Karadžić", "OŠ Sveti Sava"],
    "Novi Sad":   ["OŠ Dositej Obradović", "OŠ Jovan Popović"],
    "Niš":        ["OŠ Stevan Sremac", "OŠ Car Konstantin"],
    "Subotica":   ["OŠ Ivan Goran Kovačić", "OŠ Majšanski put"],
    "Kragujevac": ["OŠ Stanislav Sremčević", "OŠ Vuk Karadžić KG"],
}

# --------------------------------------------------
# HELPER FUNKCIJE
# --------------------------------------------------

def upd_skole(mesto: str):
    """Vrati Dropdown.update sa listom škola ili prazno."""
    return gr.Dropdown.update(choices=OSN_SK.get(mesto, []), value=None)


def gen(mesto, skola, predmet, razred, tema, ish, stil, izd):
    if not skola:
        return "⚠️  Izaberi školu iz liste ili upiši ručno."
    prompt = f"""Priprema časa – {skola}, {mesto}\nPredmet: {predmet} | Razred: {razred}\nTema: {tema}\nIshodi: {ish or 'Nisu navedeni'}\nStil: {stil} | Izdavač: {izd}\nUključi sve obavezne delove (tok časa, zadatke, test, domaći, kviz…)."""
    try:
        r = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "AI asistent za nastavnike osnovnih škola Srbije."},
                {"role": "user", "content": prompt}
            ]
        )
        return r.choices[0].message.content.strip()
    except Exception as e:
        return f"Greška: {e}"

# --------------------------------------------------
# UI
# --------------------------------------------------
with gr.Blocks() as app:
    gr.Markdown("## AI Priprema za **Osnovne Škole** 🇷🇸")

    with gr.Row():
        mesto = gr.Dropdown(MESTA, label="Mesto (grad/opština)")
        skola = gr.Dropdown([], value=None, label="Škola", interactive=True)

    predmet = gr.Dropdown(["Matematika", "Srpski jezik", "Priroda i društvo", "Svet oko nas",
                           "Likovno", "Muzika", "Fizičko"], label="Predmet")

    with gr.Row():
        razred = gr.Textbox(label="Razred", placeholder="IV-2")
        tema   = gr.Textbox(label="Tema časa", placeholder="Sabiranje do 100")
        ishodi = gr.Textbox(label="Ishodi (opciono)")

    stil = gr.Dropdown(["Klasična", "Projektna", "Igra/Simulacija", "Diskusija", "Radionica"], label="Stil nastave")
    izd  = gr.Dropdown(["Zavod za udžbenike", "BIGZ", "Klett", "Kreativni centar", "Eduka", "Logos", "Data Status", "Drugo"], label="Izdavač")

    btn = gr.Button("Generiši pripremu")
    out = gr.Markdown()

    mesto.change(upd_skole, mesto, skola)
    btn.click(gen, [mesto, skola, predmet, razred, tema, ishodi, stil, izd], out)

if __name__ == "__main__":
    app.launch()
