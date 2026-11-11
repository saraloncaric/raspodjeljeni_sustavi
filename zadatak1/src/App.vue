<script setup>
import { ref, computed, onMounted } from 'vue'
import prikazPodaci from './components/prikazPodaci.vue'

const API = 'https://raspodjeljeni-sustavi-v1.onrender.com/api'

const tasks = ref([])
const newText = ref('')
const filter = ref('all')
const greska = ref('')
const ucitavanje = ref(false)

onMounted(() => {
  ucitajZadatke()
})

async function ucitajZadatke() {
  ucitavanje.value = true
  greska.value = ''

  try {
    const odgovor = await fetch(`${API}/zadaci`)

    if (!odgovor.ok) {
      throw new Error('Greška pri dohvaćanju zadataka')
    }

    tasks.value = await odgovor.json()
  } catch (error) {
    greska.value = 'Nije moguće dohvatiti zadatke s poslužitelja.'
  } finally {
    ucitavanje.value = false
  }
}

const visible = computed(() => {
  if (filter.value === 'open') return tasks.value.filter(t => !t.done)
  if (filter.value === 'done') return tasks.value.filter(t => t.done)
  return tasks.value
})

const openCount = computed(() => tasks.value.filter(t => !t.done).length)
const doneCount = computed(() => tasks.value.filter(t => t.done).length)

const napredak = computed(() =>
  tasks.value.length ? Math.round((doneCount.value / tasks.value.length) * 100) : 0
)

const filters = [
  { id: 'all', label: 'Svi' },
  { id: 'open', label: 'Otvoreni' },
  { id: 'done', label: 'Gotovi' }
]

function brojZa(id) {
  if (id === 'open') return openCount.value
  if (id === 'done') return doneCount.value
  return tasks.value.length
}

async function addTask() {
  const text = newText.value.trim()
  if (!text) return

  greska.value = ''

  try {
    const odgovor = await fetch(`${API}/zadaci`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    })

    if (!odgovor.ok) {
      throw new Error('Greška pri dodavanju zadatka')
    }

    const zadatak = await odgovor.json()
    tasks.value.unshift(zadatak)
    newText.value = ''
  } catch (error) {
    greska.value = 'Nije moguće dodati zadatak.'
  }
}

async function updateTask(zadatak, done) {
  greska.value = ''

  try {
    const odgovor = await fetch(`${API}/zadaci/${zadatak.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ done })
    })

    if (!odgovor.ok) {
      throw new Error('Greška pri izmjeni zadatka')
    }

    const izmijenjeni = await odgovor.json()
    const index = tasks.value.findIndex(t => t.id === zadatak.id)

    if (index !== -1) {
      tasks.value[index] = izmijenjeni
    }
  } catch (error) {
    greska.value = 'Nije moguće izmijeniti zadatak.'
    await ucitajZadatke()
  }
}

async function removeTask(id) {
  greska.value = ''

  try {
    const odgovor = await fetch(`${API}/zadaci/${id}`, {
      method: 'DELETE'
    })

    if (!odgovor.ok) {
      throw new Error('Greška pri brisanju zadatka')
    }

    tasks.value = tasks.value.filter(t => t.id !== id)
  } catch (error) {
    greska.value = 'Nije moguće obrisati zadatak.'
  }
}

async function clearDone() {
  const gotovi = tasks.value.filter(t => t.done)

  for (const zadatak of gotovi) {
    await removeTask(zadatak.id)
  }
}
</script>

<template>
  <main class="mx-auto max-w-2xl px-5 pt-12 pb-16">
    <header class="mb-7">
      <h1 class="text-4xl font-bold tracking-tight max-sm:text-3xl">Zadaci</h1>
      <p class="mt-1 mb-4 text-muted">
        {{ openCount }} {{ openCount === 1 ? 'otvoren zadatak' : 'otvorenih zadataka' }}
      </p>

      <template v-if="tasks.length">
        <div
          class="h-1.5 overflow-hidden rounded-full bg-line"
          role="progressbar"
          aria-valuemin="0"
          aria-valuemax="100"
          :aria-valuenow="napredak"
        >
          <div
            class="h-full rounded-full bg-accent transition-all duration-300"
            :style="{ width: napredak + '%' }"
          ></div>
        </div>
        <p class="mt-1.5 text-sm text-muted">{{ doneCount }} od {{ tasks.length }} gotovo</p>
      </template>
    </header>

    <p v-if="ucitavanje" class="mb-4 text-muted">
      Učitavanje zadataka...
    </p>
    <p
      v-if="greska"
      class="mb-4 rounded-xl border border-[#f0c9c6] bg-danger-soft px-3.5 py-3 text-danger"
      role="alert"
    >
      {{ greska }}
    </p>

    <div class="flex gap-2 max-sm:flex-col">
      <input
        v-model="newText"
        type="text"
        placeholder="Što treba napraviti?"
        aria-label="Novi zadatak"
        class="min-w-0 flex-1 rounded-xl border border-line bg-paper px-4 py-3 shadow-card focus:border-accent focus:outline-none"
        @keyup.enter="addTask"
      />
      <button
        class="rounded-xl border border-accent bg-accent px-4 py-2 text-white transition-colors hover:border-accent-dark hover:bg-accent-dark"
        @click="addTask"
      >
        Dodaj zadatak
      </button>
    </div>

    <div class="mt-5 mb-3 flex flex-wrap gap-1.5" role="group" aria-label="Filtriraj zadatke">
      <button
        v-for="f in filters"
        :key="f.id"
        class="rounded-full border px-3.5 py-1 transition-colors"
        :class="
          filter === f.id
            ? 'border-accent bg-accent-soft font-semibold text-accent'
            : 'border-line bg-paper text-ink hover:border-accent'
        "
        :aria-pressed="filter === f.id"
        @click="filter = f.id"
      >
        {{ f.label }}
        <span class="ml-1.5 text-xs" :class="filter === f.id ? 'text-accent' : 'text-muted'">
          {{ brojZa(f.id) }}
        </span>
      </button>
    </div>

    <ul
      v-if="visible.length"
      class="divide-y divide-line overflow-hidden rounded-xl border border-line bg-paper shadow-card"
    >
      <li
        v-for="t in visible"
        :key="t.id"
        class="flex items-center justify-between gap-3 px-4 py-3.5 transition-colors hover:bg-[#f7f9fb]"
      >
        <label class="flex min-w-0 flex-1 cursor-pointer items-center gap-3">
          <input
            type="checkbox"
            class="size-5 accent-accent"
            :checked="t.done"
            @change="updateTask(t, $event.target.checked)"
          />
          <span class="break-words" :class="t.done ? 'text-done line-through' : ''">
            {{ t.text }}
          </span>
        </label>

        <button
          class="rounded-md px-2.5 py-1 text-muted transition-colors hover:bg-danger-soft hover:text-danger"
          :aria-label="`Obriši zadatak: ${t.text}`"
          @click="removeTask(t.id)"
        >
          Obriši
        </button>
      </li>
    </ul>

    <p
      v-else-if="!ucitavanje"
      class="rounded-xl border border-dashed border-line bg-paper px-4 py-10 text-center text-muted"
    >
      {{ tasks.length ? 'Nema zadataka u ovom filtru.' : 'Lista je prazna. Upiši prvi zadatak gore.' }}
    </p>

    <footer v-if="tasks.some(t => t.done)" class="mt-4 text-right">
      <button class="text-accent underline" @click="clearDone">Ukloni gotove zadatke</button>
    </footer>

    <PrikazPodaci />
  </main>
</template>