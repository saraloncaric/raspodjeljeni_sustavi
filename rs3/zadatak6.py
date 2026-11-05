import asyncio, time

async def fetch_data(param):
    print(f"Nešto radim s {param}...")
    await asyncio.sleep(param)
    print(f'Dovršio sam s {param}.')
    return f"Rezultat za {param}"

async def main():
    task1 = asyncio.create_task(fetch_data(1)) 
    task2 = asyncio.create_task(fetch_data(2)) 
    result1 = await task1
    print("Fetch 1 uspješno završen.")
    await asyncio.sleep(2)  
    return [result1]

t1 = time.perf_counter()
results = asyncio.run(main()) 
t2 = time.perf_counter()
print(results)
print(f"Vrijeme izvođenja {t2 - t1:.2f} sekunde")


# task2 se rasporedi u event loop i počne se izvršavati čim main() prvi put preda kontrolu. Problem je što main() čeka samo task1, 
# pa se nakon 1 s završi i event loop ubije task2 prije nego što ispiše poruku. Rješenje je da main() ostane živa dovoljno dugo, pa sam dodala 
# await asyncio.sleep(2). Dok main() spava, event loop dovrši task2 i ispiše “Dovršio sam s 2.”, bez await task2.