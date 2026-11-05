import asyncio

baza_korisnika = [
    {'korisnicko_ime': 'mirko123', 'email': 'mirko123@gmail.com'},
    {'korisnicko_ime': 'ana_anic', 'email': 'aanic@gmail.com'},
    {'korisnicko_ime': 'maja_0x', 'email': 'majaaaaa@gmail.com'},
    {'korisnicko_ime': 'zdeslav032', 'email': 'deso032@gmail.com'}
]

baza_lozinka = [
    {'korisnicko_ime': 'mirko123', 'lozinka': 'lozinka123'},
    {'korisnicko_ime': 'ana_anic', 'lozinka': 'super_teska_lozinka'},
    {'korisnicko_ime': 'maja_0x', 'lozinka': 's324SDFfdsj234'},
    {'korisnicko_ime': 'zdeslav032', 'lozinka': 'deso123'}
]

async def autorizacija(korisnik_iz_baze, lozinka):
    await asyncio.sleep(2)
    ime = korisnik_iz_baze['korisnicko_ime']

    for zapis in baza_lozinka:
        if zapis['korisnicko_ime'] == ime:
            if zapis['lozinka'] == lozinka:
                return f"Korisnik {ime}: Autorizacija uspješna."
            return f"Korisnik {ime}: Autorizacija neuspješna."
    return f"Korisnik {ime}: Autorizacija neuspješna."

async def autentifikacija(korisnik):
    await asyncio.sleep(3)
    korisnik_iz_baze = None
    for zapis in baza_korisnika:
        if(zapis['korisnicko_ime'] == korisnik['korisnicko_ime'] and zapis['email'] == korisnik['email']):
            korisnik_iz_baze = zapis
            break

    if korisnik_iz_baze is None:
        return f"Korisnik {korisnik['korisnicko_ime']} nije pronađen."

    return await autorizacija(korisnik_iz_baze, korisnik['lozinka'])

async def main():
    korisnik_ok = {
        'korisnicko_ime': 'ana_anic',
        'email': 'aanic@gmail.com',
        'lozinka': 'super_teska_lozinka'
    }
    korisnik_kriva_lozinka = {
        'korisnicko_ime': 'mirko123',
        'email': 'mirko123@gmail.com',
        'lozinka': 'pogresna'
    }
    korisnik_nepostojeci = {
        'korisnicko_ime': 'nepoznati',
        'email': 'nepoznati@gmail.com',
        'lozinka': 'bilo_sto'
    }

    rezultati = await asyncio.gather(
        autentifikacija(korisnik_ok),
        autentifikacija(korisnik_kriva_lozinka),
        autentifikacija(korisnik_nepostojeci)
    )
    for r in rezultati:
        print(r)

asyncio.run(main())