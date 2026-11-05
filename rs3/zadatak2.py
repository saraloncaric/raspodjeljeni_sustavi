import asyncio
import time

async def dohvati_korisnike():
    await asyncio.sleep(3)
    return[
        {'id': 1, 'ime': 'Ana', 'grad': 'Pula'},
        {'id': 2, 'ime': 'Marko', 'grad': 'Rijeka'},
        {'id': 3, 'ime': 'Ivana', 'grad': 'Zagreb'},
    ]

async def dohvati_proizvode():
    await asyncio.sleep(5)
    return [
        {'id': 1, 'naziv': 'Laptop', 'cijena': 899},
        {'id': 2, 'naziv': 'Miš', 'cijena': 25},
        {'id': 3, 'naziv': 'Monitor', 'cijena': 199},
    ]

async def main():
    t1 = time.perf_counter()
    korisnici, proizvodi = await asyncio.gather(
        dohvati_korisnike(),
        dohvati_proizvode()
    )
    t2 = time.perf_counter()
    print("Korisnici:", korisnici)
    print("Proizvodi:", proizvodi)
    print(f"Vrijeme izvođenja: {t2 - t1:.2f} sekundi")

asyncio.run(main())