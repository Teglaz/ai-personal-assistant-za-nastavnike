import json

JSON_ULAZ = "skole_osnovne.json"
TXT_IZLAZ = "skole_rs.txt"

with open(JSON_ULAZ, "r", encoding="utf-8") as f:
    podaci = json.load(f)

skole = podaci.get("KontaktPodaci", [])

rows = []
for skola in skole:
    grad = skola.get("mesto", "").strip()
    naziv = skola.get("nazivUstanove", "").strip()

    if grad and naziv:
        rows.append(f"{grad}|{naziv}")

with open(TXT_IZLAZ, "w", encoding="utf-8") as f:
    f.write("\n".join(rows))

print(f"✅ Sačuvano {len(rows)} škola u '{TXT_IZLAZ}'")
