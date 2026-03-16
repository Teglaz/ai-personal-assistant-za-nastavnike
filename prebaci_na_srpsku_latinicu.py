# -*- coding: utf-8 -*-

# Mapiranje "amerikanizovanih" slova na pravu latinicu
ZAMENE = [
    ("sh", "š"),
    ("ch", "č"),
    ("zh", "ž"),
    ("dj", "đ"),
    ("ts", "ć"),  # ili "c" -> "ć" po potrebi, ali "ts" najčešće bude "ć"
    ("Dj", "Đ"),
    ("Sh", "Š"),
    ("Ch", "Č"),
    ("Zh", "Ž"),
    ("Ts", "Ć"),
]

def konvertuj_latinicu(linija):
    for iz, u in ZAMENE:
        linija = linija.replace(iz, u)
    return linija

# Učitaj originalni fajl
with open("srednje_skole_clean.txt", encoding="utf-8") as f:
    linije = f.readlines()

# Konvertuj sve redove
konvertovane = [konvertuj_latinicu(l) for l in linije]

# Sačuvaj kao novi fajl (ili prebriši isti)
with open("srednje_skole_clean_SR.txt", "w", encoding="utf-8") as f:
    f.writelines(konvertovane)

print("✅ Gotovo! Novi fajl je srednje_skole_clean_SR.txt sa čistom srpskom latinicom.")
