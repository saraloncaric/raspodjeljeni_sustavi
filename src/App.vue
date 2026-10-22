<script setup>
import { ref, computed, watch } from 'vue'

const KEY = 'zadaci-v1'

function load() {
  try {
    return JSON.parse(localStorage.getItem(KEY)) || []
  } catch {
    return []
  }
}

const tasks = ref(load())
const newText = ref('')
const filter = ref('all')
let nextId = tasks.value.reduce((m, t) => Math.max(m, t.id), 0) + 1

watch(tasks, (v) => {
  try { localStorage.setItem(KEY, JSON.stringify(v)) } catch {}
}, { deep: true })

const visible = computed(() => {
  if (filter.value === 'open') return tasks.value.filter(t => !t.done)
  if (filter.value === 'done') return tasks.value.filter(t => t.done)
  return tasks.value
})

const openCount = computed(() => tasks.value.filter(t => !t.done).length)

const filters = [
  { id: 'all', label: 'Svi' },
  { id: 'open', label: 'Otvoreni' },
  { id: 'done', label: 'Gotovi' }
]

function addTask() {
  const text = newText.value.trim()
  if (!text) return
  tasks.value.unshift({ id: nextId++, text, done: false })
  newText.value = ''
}

function removeTask(id) {
  tasks.value = tasks.value.filter(t => t.id !== id)
}

function clearDone() {
  tasks.value = tasks.value.filter(t => !t.done)
}
</script>

<template>
  <main class="wrap">
    <header>
      <h1>Zadaci</h1>
      <p class="count">
        {{ openCount }} {{ openCount === 1 ? 'otvoren zadatak' : 'otvorenih zadataka' }}
      </p>
    </header>

    <div class="add">
      <input
        v-model="newText"
        type="text"
        placeholder="Što treba napraviti?"
        aria-label="Novi zadatak"
        @keyup.enter="addTask"
      />
      <button class="primary" @click="addTask">Dodaj zadatak</button>
    </div>

    <div class="filters" role="group" aria-label="Filtriraj zadatke">
      <button
        v-for="f in filters"
        :key="f.id"
        :class="{ active: filter === f.id }"
        :aria-pressed="filter === f.id"
        @click="filter = f.id"
      >
        {{ f.label }}
      </button>
    </div>

    <ul v-if="visible.length" class="list">
      <li v-for="t in visible" :key="t.id" :class="{ done: t.done }">
        <label>
          <input v-model="t.done" type="checkbox" />
          <span>{{ t.text }}</span>
        </label>
        <button class="remove" :aria-label="`Obriši zadatak: ${t.text}`" @click="removeTask(t.id)">
          Obriši
        </button>
      </li>
    </ul>
    <p v-else class="empty">
      {{ tasks.length ? 'Nema zadataka u ovom filtru.' : 'Lista je prazna. Upiši prvi zadatak gore.' }}
    </p>

    <footer v-if="tasks.some(t => t.done)">
      <button class="link" @click="clearDone">Ukloni gotove zadatke</button>
    </footer>
  </main>
</template>

<style scoped>
.wrap {
  max-width: 560px;
  margin: 0 auto;
  padding: 3rem 1.25rem 4rem;
}

h1 {
  margin: 0;
  font-size: 2.25rem;
  letter-spacing: -0.02em;
}

.count {
  margin: 0.25rem 0 1.75rem;
  color: var(--muted);
}

.add {
  display: flex;
  gap: 0.5rem;
}

.add input {
  flex: 1;
  min-width: 0;
  padding: 0.65rem 0.8rem;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--paper);
  color: var(--ink);
}

button {
  cursor: pointer;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--paper);
  color: var(--ink);
  padding: 0.5rem 0.9rem;
}

button.primary {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

.filters {
  display: flex;
  gap: 0.4rem;
  margin: 1.25rem 0 0.75rem;
}

.filters button.active {
  border-color: var(--accent);
  color: var(--accent);
  font-weight: 600;
}

.list {
  list-style: none;
  margin: 0;
  padding: 0;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 6px;
}

.list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.7rem 0.9rem;
}

.list li + li { border-top: 1px solid var(--line); }

.list label {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  flex: 1;
  min-width: 0;
  cursor: pointer;
}

.list input[type='checkbox'] {
  width: 1.1rem;
  height: 1.1rem;
  accent-color: var(--accent);
}

.list span { overflow-wrap: anywhere; }

.done span {
  color: var(--done);
  text-decoration: line-through;
}

.remove {
  border: none;
  background: none;
  color: var(--muted);
  padding: 0.25rem 0.4rem;
}

.remove:hover { color: #a3322b; }

.empty {
  padding: 1.5rem 0;
  color: var(--muted);
}

footer { margin-top: 1rem; }

.link {
  border: none;
  background: none;
  padding: 0;
  color: var(--accent);
  text-decoration: underline;
}
</style>