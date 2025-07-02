import pdfplumber, pandas as pd

PDF_NAME = "adresar_srednjih_skola.pdf"
TXT_OUT  = "skole_rs.txt"

rows = []

with pdfplumber.open(PDF_NAME) as pdf:
    for page in pdf.pages:
        # svaka stranica je tabela sa 7 kolona,
        # nama trebaju samo kolone 0 (grad) i 2 (naziv škole)
        table = page.extract_table()
        if not table:
            continue
        for r in table[1:]:          # preskoči header
            grad   = r[0].strip()
            skola  = r[2].strip()
            # sitno čišćenje – prazne retke preskačemo
            if grad and skola:
                rows.append(f"{grad}|{skola}")

# snimi u txt (jedan red = grad|škola)
with open(TXT_OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(rows))

print(f"✔️  Upisano {len(rows)} škola u {TXT_OUT}")
