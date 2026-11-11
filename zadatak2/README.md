# Vježba 2: Priprema podataka za web-aplikaciju

Nadogradnja aplikacije iz prve vježbe

Javni URL: https://raspodjeljeni-sustavi-v1.onrender.com

## Struktura

- `zadatak1/` --> aplikacija iz prve vježbe, podatke prikazuje komponenta `src/components/prikazPodaci.vue`, a `podaci.json` je kopiran u `public/podaci.json`.
- `zadatak2/` --> Python program i generirani `podaci.json`

## Podaci i operacije koje simuuliram

Program ima tri korutine koje međusobno nisu ovisne, nijedna ne treba rezultat druge.

- dohvati_zadatke() --> lista od 6 zadataka (id, naslov, kategorija, prioritet, rok, gotov) 
- dohvati_kategoriju() --> lista od 3 kategorije (oznaka, naziv, broj zadataka) 
- dohvati_korisnike() --> lista od 3 korisnika (ime, uloga, broj otvorenih zadataka)

Svaka korutina ispiše poruku na početku, čeka pomoču `asyncio.sleep()`, ispiše poruku na kraju i vrati podatke.
Podaci su ručno napisani u datoteci `podaci.py`, a pravih HTTP zahtjeva nema.

## Vremena čekanja i mjerenja

Na početku programa je `random.seed(42)`, pa su vremena čekanja svaki put ista. Generirana su jednom, prije mjerenja, i ista su u obje verzije.

Korutina i čekanje:

- zadaci --> 3 s 
- korisnici --> 1 s 
- kategorije --> 1 s

Zbroj čekanja je 5 s, a najdulje čekanje je 3 s.

Verzija i izmjereno vrijeme:

- sekvencijalno --> 5.02 s 
- konkurentno --> 3.01 s

Rezultati obje verzije spremljeni su u rječnik iste strukture. Rezultat konkurentne verzije sprema se u `podaci.json`.

## Pokretanje

U mapi `zadatak2` pokrenuti `python main.py`. Program ispiše sekvencijalnu i konkurentnu verziju, test redoslijeda u `gather()` i napravi `podaci.json`. 
Za frontend sam tu datoteku ručno kopirala u `zadatak1/public/podaci.json`, a zatim pokrenula `npm run build` i deployala frontend na Render.

## Odgovori na pitanja

**Koliko traje izvođenje programa pri sekvencijalnoj obradi? Zašto?**
Oko 5 s (izmjereno 5.02 s). Svaki `await` čeka da se korutina potpuno dovrši prije nego što se pokrene sljedeća, pa se vremena zbrajaju: 3 + 1 + 1 = 5 s.

**Koliko traje izvođenje programa pri konkurentnoj jednodretvenoj obradi? Zašto?**
Oko 3 s (izmjereno 3.01 s), koliko traje najdulja korutina (zadaci). `asyncio.gather` rasporedi sve tri korutine u event loop. Kad prva dođe do `await asyncio.sleep()`,  
ona se pauzira i event loop pokrene sljedeću, pa sve tri čekaju istovremeno.

**Koja je glavna razlika između ovih dvaju načina izvođenja? Kako se korutine izvršavaju unutar event loopa?**
Kod sekvencijalnog izvođenja sljedeća korutina ne počinje dok prethodna nije gotova. Kod konkurentnog se sve korutine rasporede unaprijed, a event loop ih izmjenjuje: pokrene korutinu,  
ona dođe do `await` i vrati mu kontrolu, pa on pokrene sljedeću. Kad istekne čekanje neke korutine, event loop je nastavi od mjesta gdje je stala. U ispisu konkurentne verzije se vidi da sve  
tri počnu jedna za drugom ("Dohvaćam zadatke, korisnike, kategoriju"), a završe redom po duljini čekanja: korisnici i kategorije nakon 1 s, a zadaci nakon 3 s.

**Što se događa ako se `asyncio.sleep` zamijeni s `time.sleep`? Koja je tehnička razlika?**
Ako napišem `await time.sleep(x)`, dobijem `TypeError: object NoneType can't be used in 'await' expression`, jer `time.sleep` vraća `None`, a to nije awaitable objekt.  
Ako napišem samo `time.sleep(x)` bez `await`, program radi, ali blokira cijelu dretvu pa event loop ne može prijeći na drugu korutinu dok čekanje ne istekne. Kad sam `time.sleep` stavila u  
sve tri korutine, konkurentna verzija trajala je oko 5 s, isto kao sekvencijalna, jer se čekanja više ne preklapaju. Kad bih ga stavila samo u `dohvati_zadatke`,  
trajalo bi oko 4 s: zadaci blokiraju 3 s, a tek nakon toga korisnici i kategorije čekaju zajedno 1 s. `asyncio.sleep` je korutina koja pauzira samo sebe i vraća kontrolu event loopu,  
pa se u međuvremenu mogu izvršavati druge korutine.

**Vraća li `asyncio.gather()` rezultate uvijek istim redoslijedom? Odgovara li taj redoslijed redoslijedu proslijeđenih korutina ili redoslijedu njihova dovršavanja?**
Rezultati dolaze redoslijedom kojim su korutine proslijeđene u `gather()`, a ne redoslijedom dovršavanja. Isprobala sam tri različita poretka argumenata. U sva tri slučaja korutine su se dovršile istim  
redom (korisnici i kategorije nakon 1 s, zadaci nakon 3 s), ali je lista rezultata svaki put pratila poredak argumenata.
