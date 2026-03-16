def ucitaj_skole(putanja_fajla):
    gradovi_skole = {}  # primer: {'Novi Sad': ['Zmaj', 'Tehnička'], ...}

    with open(putanja_fajla, "r", encoding="utf-8") as f:
        for linija in f:
            if "|" in linija:
                grad, skola = linija.strip().split("|")
                if grad not in gradovi_skole:
                    gradovi_skole[grad] = []
                gradovi_skole[grad].append(skola)

    return gradovi_skole

def dohvati_gradove(putanja_fajla):
    return sorted(ucitaj_skole(putanja_fajla).keys())

def dohvati_skole_za_grad(putanja_fajla, izabrani_grad):
    sve_skole = ucitaj_skole(putanja_fajla)
    return sorted(sve_skole.get(izabrani_grad, []))
