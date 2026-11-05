import asyncio

async def timer(name, delay):
    for i in range(delay, 0, -1):
        print(f'{name}: {i} sekundi preostalo...')
        await asyncio.sleep(1)
    print(f'{name}: Vrijeme je isteklo!')

async def main():
    timers = [
        asyncio.create_task(timer('Timer 1', 3)),
        asyncio.create_task(timer('Timer 2', 5)),
        asyncio.create_task(timer('Timer 3', 7))
    ]
    await asyncio.gather(*timers)

asyncio.run(main())

# Koraci ponašanja:
# 1. asyncio.run() pokrene event loop i main().
# 2. create_task rasporedi tri timera, ali se još ne izvršavaju.
# 3. await asyncio.gather(*timers) pauzira main() i event loop počne izvršavati timere.
# 4. Svaki timer ispiše poruku i na await asyncio.sleep(1) se pauzira, a loop pokrene idući. Tako se timeri izmjenjuju svake sekunde.
# 5. Timeri završavaju jedan po jedan (nakon 3, 5 i 7 s), a kad su svi gotovi, main() se nastavlja i završava, pa se event loop zatvara.