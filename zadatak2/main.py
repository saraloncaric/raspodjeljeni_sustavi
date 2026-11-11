import asyncio
import random 
import time
import json
from pathlib import Path
from podaci import zadaci, korisnici, kategorije

random.seed(42)

vrijeme_zadataka = random.randint(1, 3)
vrijeme_korisnika = random.randint(1, 3)
vrijeme_kategorija = random.randint(1, 3)

async def dohvati_zadatke():
    print("Dohvaćam zadatke")
    await asyncio.sleep(vrijeme_zadataka)
    print("Zadaci dohvaćeni")
    return zadaci

async def dohvati_korisnike():
    print("Dohvaćam korisnike")
    await asyncio.sleep(vrijeme_korisnika)
    print("Korisnici dohvaćeni")
    return korisnici

async def dohvati_kategoriju():
    print("Dohvaćam kategoriju")
    await asyncio.sleep(vrijeme_kategorija)
    print("Kategorije dohvaćene")
    return kategorije

async def main():
    print(f"Vremena čekanja: zadaci {vrijeme_zadataka} s, korisnici {vrijeme_korisnika} s, kategorije {vrijeme_kategorija} s")
    print("\nSekvencijalno izvršavanje:")
    pocetak = time.perf_counter()

    zadaci = await dohvati_zadatke()
    korisnici = await dohvati_korisnike()
    kategorije = await dohvati_kategoriju()

    sekvencijalno = time.perf_counter() - pocetak
    rez_sekvencijalno = {
        "zadaci": zadaci,
        "korisnici": korisnici,
        "kategorije": kategorije
    }
    print(f"Vrijeme izvršavanja: {sekvencijalno:.2f} sekundi")

    print("\bKonkurentno izvršavanje:")
    pocetak = time.perf_counter()

    zadaci, korisnici, kategorije = await asyncio.gather(
        dohvati_zadatke(), 
        dohvati_korisnike(),
        dohvati_kategoriju()
    )

    konkurentno = time.perf_counter() - pocetak
    rez_konkuretno = {
        "zadaci": zadaci,
        "korisnici": korisnici,
        "kategorije": kategorije
    }
    print(f"Vrijeme izvršavanja: {konkurentno:.2f} sekundi")

    print("\nTest redoslijeda u gather():")
    redoslijedi = {
        "zadaci, korisnici, kategorije": [dohvati_zadatke, dohvati_korisnike, dohvati_kategoriju],
        "kategorije, zadaci, korisnici": [dohvati_kategoriju, dohvati_zadatke, dohvati_korisnike],
        "korisnici, kategorije, zadaci": [dohvati_korisnike, dohvati_kategoriju, dohvati_zadatke],
    }
    for naziv, korutine in redoslijedi.items():
        print(f"\ngather({naziv})")
        rezultati = await asyncio.gather(*(k() for k in korutine))
        for i, r in enumerate(rezultati):
            prva = r[0].get("naslov") or r[0].get("ime") or r[0].get("naziv")
            print(f" rezultati[{i}] počinje s: {prva}")

    putanja = Path(__file__).parent / "podaci.json"
    with open(putanja, "w", encoding="utf-8") as f:
        json.dump(rez_konkuretno, f, ensure_ascii=False, indent=2)
    print("\nPodaci spremljeni u podaci.json")

asyncio.run(main())