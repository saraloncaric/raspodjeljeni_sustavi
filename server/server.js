import express from 'express'
import cors from 'cors'

const app = express() 
const PORT = process.env.PORT || 3000

app.use(cors({
  origin: 'https://raspodjeljeni-sustavi.onrender.com',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type']
}))

app.use(express.json())

let zadaci = [
  { id: 1, text: 'Naučiti Express', done: false },
  { id: 2, text: 'Napraviti Vue aplikaciju', done: true }
]
let nextId = 3

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' })
})

app.get('/api/zadaci', (req, res) => {
  const { done } = req.query
  if (done === 'true' || done === 'false') {
    return res.json(zadaci.filter(z => z.done === (done === 'true')))
  }
  res.json(zadaci)
})

app.get('/api/zadaci/:id', (req, res) => {
  const zadatak = zadaci.find(z => z.id === Number(req.params.id))
  if (!zadatak) {
    return res.status(404).json({ greska: 'Zadatak nije pronađen' })
  }
  res.json(zadatak)
})

app.post('/api/zadaci', (req, res) => {
  const text = typeof req.body?.text === 'string' ? req.body.text.trim() : ''
  if (!text) {
    return res.status(400).json({ greska: 'Polje "text" je obavezno' })
  }
  const zadatak = { id: nextId++, text, done: false }
  zadaci.push(zadatak)
  res.status(201).json(zadatak)
})

app.put('/api/zadaci/:id', (req, res) => {
  const zadatak = zadaci.find(z => z.id === Number(req.params.id))
  if (!zadatak) {
    return res.status(404).json({ greska: 'Zadatak nije pronađen' })
  }

  const { text, done } = req.body ?? {}

  if (text !== undefined) {
    if (typeof text !== 'string' || !text.trim()) {
      return res.status(400).json({ greska: 'Polje "text" mora biti neprazan tekst' })
    }
    zadatak.text = text.trim()
  }
  if (done !== undefined) {
    if (typeof done !== 'boolean') {
      return res.status(400).json({ greska: 'Polje "done" mora biti true ili false' })
    }
    zadatak.done = done
  }

  res.json(zadatak)
})

app.delete('/api/zadaci/:id', (req, res) => {
  const id = Number(req.params.id)
  const postoji = zadaci.some(z => z.id === id)
  if (!postoji) {
    return res.status(404).json({ greska: 'Zadatak nije pronađen' })
  }
  zadaci = zadaci.filter(z => z.id !== id)
  res.status(204).end()
})

// nepoznata ruta
app.use((req, res) => {
  res.status(404).json({ greska: 'Ruta ne postoji' })
})

app.listen(PORT, () => {
  console.log(`API radi na http://localhost:${PORT}`)
})