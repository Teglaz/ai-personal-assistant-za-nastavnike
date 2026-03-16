# AI Asistent za Nastavnike

Web aplikacija koja nastavnicima pomaze da automatski generisu nastavne materijale koristeci Anthropic Claude AI.

## Funkcionalnosti

- **Generator kvizova** — kreira testove sa visestrukim izborom (A, B, C, D) za zadatu temu i razred
- **Planer casa** — generise detaljan plan casa sa ciljevima, aktivnostima i evaluacijom
- **Kreator domacih zadataka** — priprema domace zadatke prilagodjene uzrastu

Sve funkcije su dostupne za **osnovnu skolu** (razredi 1–8) i **srednju skolu** (razredi 1–4).

## Tehnologije

- Python 3.13
- Django 5.2.4
- Anthropic Claude API (`claude-opus-4-6`)
- SQLite

## Pokretanje

```bash
# 1. Kloniraj repozitorij
git clone https://github.com/Teglaz/ai-personal-assistant-za-nastavnike.git
cd ai-personal-assistant-za-nastavnike

# 2. Kreiraj i aktiviraj virtualno okruzenje
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Instaliraj zavisnosti
pip install -r requirements.txt

# 4. Dodaj Anthropic API kljuc u .env fajl
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# 5. Pokreni server
python manage.py runserver
```

Aplikacija je dostupna na `http://127.0.0.1:8000/`.

## Struktura projekta

```
ai_asistent/        # Django konfiguracija (settings, urls)
nastavnici/         # Glavna aplikacija
  templates/        # HTML sabloni
  views.py          # Logika i AI pozivi
  urls.py           # URL rute
manage.py
requirements.txt
.env                # API kljuc (nije u repozitoriju)
```

## Autor

**Milan Tegeltija** — profesor, AI entuzijasta i pokretac digitalne revolucije u ucionici.

> "AI za prosvetu — jer nastavnik ne sme da gori."

Za saradnju ili komercijalnu licencu: **milan.tegeltija@gmail.com**

---

© 2025 Milan Tegeltija. Sva prava zadrzana.
