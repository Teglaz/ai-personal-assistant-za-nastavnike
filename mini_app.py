#!/usr/bin/env python3
# mini_app.py
# AI asistent za pripremu časa (srednje škole) – minimalna, stabilna verzija

import json
import gradio as gr
from pathlib import Path

ROOT = Path(__file__).parent

# -------------------------------------------------------------------------
# 1) Učitaj liste gradova i škola iz  srednje_skole_clean.txt  (format: grad|škola)
# -------------------------------------------------------------------------
CITY2SCHOOLS: dict[str, list[str]] = {}
try:
    with open(ROOT / "srednje_skole_clean.txt", encoding="utf-8") as fh:
        for line in fh:
            if "|" not in line:
                continue
            city, school = [seg.strip() for seg in line.split("|", 1)]
            CITY2SCHOOLS.setdefault(city, []).append(school)
    # sortiraj svakom gradu školu, i listu gradova
    for sch_lst in CITY2SCHOOLS.values():
        sch_lst.sort()
    CITIES = sorted(CITY2SCHOOLS.keys())
except FileNotFoundError:
    raise SystemExit(
        "❌ Nije pronađen fajl 'srednje_skole_clean.txt'."
        " Provjeri da li se nalazi u istom folderu kao mini_app.py."
    )

# -------------------------------------------------------------------------
# 2) Učitaj listu predmeta (predmeti_srednje_skole.json – jednostavna lista)
# -------------------------------------------------------------------------
PREDMETI = []
try:
    with open(ROOT / "predmeti_srednje_skole.json", encoding="utf-8") as fh:
        PREDMETI = sorted(json.load(fh))
except FileNotFoundError:
    raise SystemExit("❌ Nedostaje 'predmeti_srednje_skole.json'.")

# -------------------------------------------------------------------------
# 3) Sadržaj po izdavaču  (izdavač ➜ predmet ➜ razred ➜ [lekcije])
# -------------------------------------------------------------------------
SADRZAJ = {}
try:
    with open(ROOT / "sadrzaj_po_izdavacu.json", encoding="utf-8") as fh:
        SADRZAJ = json.load(fh)
    IZDAVACI = sorted(SADRZAJ.keys())
except FileNotFoundError:
    raise SystemExit("❌ Nedostaje 'sadrzaj_po_izdavacu.json'.")

GRADES = ["I", "II", "III", "IV"]

# -------------------------------------------------------------------------
# Pomoćne funkcije za dinamičke dropdown-ove
# -------------------------------------------------------------------------
def f_skole(city: str) -> list[str]:
    """Vraća sortiranu listu škola za dati grad."""
    return CITY2SCHOOLS.get(city, [])

def f_lekcije(izd: str, predmet: str, razred: str) -> list[str]:
    """Vraća listu lekcija (nastavnih jedinica) na osnovu izbora."""
    try:
        return [item["lekcija"] for item in SADRZAJ[izd][predmet][razred]]
    except KeyError:
        return []


# -------------------------------------------------------------------------
# Generisanje teksta pripreme (vrlo uprošćeno – možeš proširiti po želji)
# -------------------------------------------------------------------------
def generisi_pripremu(
    city, school, smjer, predmet, izdavac, razred, lekcija, ishod, stil
) -> str:
    if not (city and school and predmet and izdavac and razred and lekcija):
        return "⚠️ Potrebno je popuniti polja Grad, Škola, Predmet, Izdavač, Razred i Nastavna jedinica."
    return (
        f"## Priprema časa\n\n"
        f"- **Škola:** {school}, {city}\n"
        f"- **Smer / Struka:** {smjer or '—'}\n"
        f"- **Predmet:** {predmet}\n"
        f"- **Izdavač:** {izdavac}\n"
        f"- **Razred:** {razred}\n"
        f"- **Nastavna jedinica:** {lekcija}\n"
        f"- **Ishod časa:** {ishod}\n"
        f"- **Stil časa:** {stil}\n\n"
        f"*(Ovde ubaci detaljnu pripremu – ciljeve, tok časa, aktivnosti...)*"
    )


# -------------------------------------------------------------------------
# Gradio UI
# -------------------------------------------------------------------------
with gr.Blocks(title="AI asistent za pripremu časa — srednje škole") as demo:
    gr.Markdown("### 🧠 AI asistent za pripremu časa — srednje škole")

    with gr.Row():
        city_dd = gr.Dropdown(CITIES, label="Grad / Opština", interactive=True)
        school_dd = gr.Dropdown(label="Škola", interactive=True)

    smjer_dd = gr.Dropdown(
        label="Smer / Struka (opciono)",
        interactive=True,
        allow_custom_value=True,  # korisnik može dopisati ako želi
    )

    predmet_dd = gr.Dropdown(PREDMETI, label="Predmet", interactive=True)

    with gr.Row():
        izdavac_dd = gr.Dropdown(IZDAVACI, label="Izdavač", value=IZDAVACI[0], interactive=True)
        razred_dd = gr.Dropdown(GRADES, label="Razred", interactive=True)

    lekcija_dd = gr.Dropdown(label="Nastavna jedinica", interactive=True)

    ishod_dd = gr.Radio(["Osnovni", "Napredni"], label="Ishod časa", value="Osnovni")
    stil_dd = gr.Radio(["Standardni", "Kreativni", "Diskusioni"], label="Stil časa", value="Standardni")

    generisi_btn = gr.Button("🧑‍🏫 Generiši pripremu časa")
    prikaz_md = gr.Markdown()

    # ---- Eventi ----------------------------------------------------------
    city_dd.change(
        lambda c: gr.Dropdown.update(choices=f_skole(c), value=None),
        inputs=city_dd,
        outputs=school_dd,
    )

    # kad se bilo koji od tri dropdown-a promijeni, ažuriraj lekcije
    for comp in (izdavac_dd, predmet_dd, razred_dd):
        comp.change(
            lambda izd, pr, rz: gr.Dropdown.update(
                choices=f_lekcije(izd, pr, rz), value=None
            ),
            inputs=[izdavac_dd, predmet_dd, razred_dd],
            outputs=lekcija_dd,
        )

    generisi_btn.click(
        generisi_pripremu,
        inputs=[
            city_dd,
            school_dd,
            smjer_dd,
            predmet_dd,
            izdavac_dd,
            razred_dd,
            lekcija_dd,
            ishod_dd,
            stil_dd,
        ],
        outputs=prikaz_md,
    )

# Pokreni na prvom slobodnom portu od 7860 na-dalje
demo.launch()
