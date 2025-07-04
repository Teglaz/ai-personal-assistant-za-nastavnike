import os
import json
import time
from openai import OpenAI

# ✅ API ključ iz okruženja
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Putanja do fajla sa podacima po izdavaču
with open("sadrzaj_po_izdavacu.json", "r", encoding="utf-8") as f:
    podaci = json.load(f)

# ✅ Lista razreda
razredi = ["I", "II", "III", "IV"]

# ✅ Prazna struktura za rezultat
sadrzaj = {}

# ✅ Funkcija za poziv LLM
def generisi_sadrzaj(predmet, razred):
    prompt = (
        f"Generiši detaljan sadržaj lekcija za predmet '{predmet}' za {razred} razred srednje škole "
        f"u skladu sa srpskim nastavnim programom. Uključi nazive svih lekcija i očekivane ishode učenja "
        f"za svaku lekciju. Formatiraj kao listu rečnika sa ključevima: 'lekcija', 'ishodi'."
    )

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ti si stručni kreator nastavnih planova i programa."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ API poziv neuspešan za {predmet} {razred}: {e}")
        return f"[GREŠKA] {e}"

# ✅ Glavna petlja
for izdavac, predmeti in podaci.items():
    print(f"\n📚 Izdavač: {izdavac}")
    sadrzaj[izdavac] = {}

    for predmet in predmeti:
        sadrzaj[izdavac][predmet] = {}

        for razred in razredi:
            print(f"🔄 {izdavac} | {predmet} | {razred}")
            rezultat = generisi_sadrzaj(predmet, razred)
            sadrzaj[izdavac][predmet][razred] = rezultat

            # Appropriately spaced API calls to respect rate limits
            # OpenAI recommends at least 3-5 seconds between requests for sustained usage
            time.sleep(3)
            
            # Optional: Add progress tracking for long operations
            total_calls = len(podaci) * len(predmeti) * len(razredi)
            current_call = sum(1 for _ in podaci for _ in predmeti for _ in razredi)
            if current_call % 5 == 0:  # Progress update every 5 calls
                print(f"📈 Napredak: {current_call}/{total_calls} poziva završeno")

# ✅ Snimi rezultat u JSON fajl (UTF-8, sa našim slovima)
with open("generisan_sadrzaj.json", "w", encoding="utf-8") as f:
    json.dump(sadrzaj, f, indent=2, ensure_ascii=False)

print("\n✅ Gotovo. Podaci su sačuvani u 'generisan_sadrzaj.json'")
