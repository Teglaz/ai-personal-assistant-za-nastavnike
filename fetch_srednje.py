# fetch_srednje.py
# preuzima zvaničan CSV spisak srednjih škola i pravi skole_rs.txt
import csv, requests, pathlib

CSV_URL = "https://opendata.mpn.gov.rs/datasets/knz14281_adresar_srednjih_skola.csv"

def main():
    out_file = pathlib.Path("skole_rs.txt")
    rows = []

    print("▶️  Preuzimam CSV sa Ministarstva prosvete…")
    response = requests.get(CSV_URL, timeout=30)
    response.raise_for_status()                   # (raise) baci grešku ako HTTP ≠ 200
    lines = response.content.decode("utf-8").splitlines()

    reader = csv.DictReader(lines)
    for r in reader:
        grad  = r["Opština"].strip()
        skola = r["Naziv ustanove"].strip()
        rows.append(f"{grad}|{skola}")

    out_file.write_text("\n".join(sorted(rows)), encoding="utf-8")
    print(f"✔️  Upisano {len(rows)} redova u {out_file}")

if __name__ == "__main__":
    main()
