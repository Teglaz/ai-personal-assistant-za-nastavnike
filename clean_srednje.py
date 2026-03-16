from unidecode import unidecode

ULICE = [
    "ulica", "trg", "bulevar", "brigada", "gospodara", "cara",
    "vladike", "zarka", "narodnih", "platona", "ribnikar", "ribnikara", 
    "heroja", "lasarevica", "temerinska", "decanska"
]

def sadrzi_ulicu(naziv):
    naziv_lower = unidecode(naziv.lower())
    return any(ul in naziv_lower for ul in ULICE)

input_file = "srednje_skole.txt"
output_file = "srednje_skole_clean.txt"

cleaned = []

with open(input_file, encoding="utf-8") as f:
    for linija in f:
        linija = linija.strip()
        if "|" not in linija:
            continue
        grad, skola = [unidecode(x.strip()) for x in linija.split("|", 1)]
        if not skola or len(skola) < 5:
            continue
        if sadrzi_ulicu(skola):
            continue
        cleaned.append(f"{grad}|{skola}")

with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(cleaned)))

print(f"✅ Očišćeno i upisano {len(cleaned)} škola u {output_file}")
