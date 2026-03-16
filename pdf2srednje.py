import pdfplumber

PDF_NAME = "Adresar srednjih skola.pdf"
TXT_OUT = "srednje_skole.txt"

rows = []

with pdfplumber.open(PDF_NAME) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if not table:
            continue
        for r in table[1:]:
            if len(r) < 2:
                continue
            grad = r[0].strip()
            skola = r[1].strip()  # KOLUMNA 1 = Naziv škole (NE adresa!)
            if grad and skola and len(skola) > 4:
                rows.append(f"{grad}|{skola}")

with open(TXT_OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(rows)))

print(f"✅ Ispravno izvučeno {len(rows)} srednjih škola u {TXT_OUT}")
