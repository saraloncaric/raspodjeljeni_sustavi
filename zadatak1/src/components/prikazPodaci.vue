<script setup>
import { ref, onMounted } from 'vue'

const podaci = ref(null)
const greska = ref('')

const klaseProriteta = {
  visok: 'bg-danger-soft text-danger',
  srednji: 'bg-[#fdf3dc] text-[#8a5a00]',
  nizak: 'bg-page text-muted'
}

onMounted(async () => {
  try {
    const odgovor = await fetch(`${import.meta.env.BASE_URL}podaci.json`)
    if (!odgovor.ok) {
      throw new Error('Greška pri učitavanju')
    }
    podaci.value = await odgovor.json()
  } catch {
    greska.value = 'Nije moguće učitati podaci.json.'
  }
})

function formatDatum(iso) {
  return new Date(iso).toLocaleDateString('hr-HR')
}

function nazivKategorije(oznaka) {
  const k = podaci.value.kategorije.find(k => k.oznaka === oznaka)
  return k ? k.naziv : oznaka
}

function inicijal(ime) {
  return ime.charAt(0).toUpperCase()
}
</script>

<template>
  <section class="mt-14 border-t border-line pt-8">
    <header>
      <h2 class="text-2xl font-bold tracking-tight">Podaci iz Python programa</h2>
      <p class="mt-1 text-sm text-muted">
        Pripremljeno asinkronim dohvaćanjem (asyncio) i spremljeno u podaci.json
      </p>
    </header>

    <p
      v-if="greska"
      class="mt-4 rounded-xl border border-[#f0c9c6] bg-danger-soft px-3.5 py-3 text-danger"
      role="alert"
    >
      {{ greska }}
    </p>
    <p v-else-if="!podaci" class="mt-4 text-muted">Učitavanje...</p>

    <template v-else>
      <h3 class="mt-7 mb-2.5 text-xs font-semibold tracking-widest text-muted uppercase">Zadaci</h3>
      <ul class="divide-y divide-line overflow-hidden rounded-xl border border-line bg-paper shadow-card">
        <li
          v-for="z in podaci.zadaci"
          :key="z.id"
          class="flex items-center justify-between gap-3 px-4 py-3"
        >
          <div class="flex min-w-0 flex-col">
            <span class="break-words" :class="z.gotov ? 'text-done line-through' : ''">
              {{ z.naslov }}
            </span>
            <span class="text-sm text-muted">
              {{ nazivKategorije(z.kategorija) }} · rok {{ formatDatum(z.rok) }}
              <template v-if="z.gotov"> · gotovo</template>
            </span>
          </div>
          <span
            class="shrink-0 rounded-full px-2.5 py-0.5 text-xs font-semibold"
            :class="klaseProriteta[z.prioritet]"
          >
            {{ z.prioritet }}
          </span>
        </li>
      </ul>

      <h3 class="mt-7 mb-2.5 text-xs font-semibold tracking-widest text-muted uppercase">Kategorije</h3>
      <div class="flex flex-wrap gap-2.5">
        <div
          v-for="k in podaci.kategorije"
          :key="k.oznaka"
          class="flex min-w-32 flex-col rounded-xl border border-line bg-paper px-4 py-3 shadow-card"
        >
          <strong>{{ k.naziv }}</strong>
          <span class="text-sm text-muted">
            {{ k.broj_zadataka }} {{ k.broj_zadataka === 1 ? 'zadatak' : 'zadataka' }}
          </span>
        </div>
      </div>

      <h3 class="mt-7 mb-2.5 text-xs font-semibold tracking-widest text-muted uppercase">Korisnici</h3>
      <div class="flex flex-col gap-2.5">
        <div
          v-for="k in podaci.korisnici"
          :key="k.ime"
          class="flex items-center gap-3 rounded-xl border border-line bg-paper px-4 py-3 shadow-card"
        >
          <div
            class="grid size-9 shrink-0 place-items-center rounded-full bg-accent-soft font-bold text-accent"
          >
            {{ inicijal(k.ime) }}
          </div>
          <div class="flex min-w-0 flex-1 flex-col">
            <strong>{{ k.ime }}</strong>
            <span class="text-sm text-muted">{{ k.uloga }}</span>
          </div>
          <div class="flex flex-col items-end text-xl leading-tight font-bold">
            {{ k.otvoreni_zadaci }}
            <small class="text-xs font-normal text-muted">
              {{ k.otvoreni_zadaci === 1 ? 'otvoren' : 'otvorenih' }}
            </small>
          </div>
        </div>
      </div>
    </template>
  </section>
</template>