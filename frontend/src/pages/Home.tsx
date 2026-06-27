import { useState, useEffect } from 'react'
import Header from '../components/Header'
import Footer from '../components/Footer'
import HackathonCard from '../components/HackathonCard'
import SubmitHackathonModal from '../components/SubmitHackathonModal'
import { sampleHackathons } from '../lib/sample-hackathons'
import type { Hackathon } from '../lib/types'

const STORAGE_KEY = 'allhackathons'
const USER_KEY = 'allhackathons_user'

function loadHackathons(): Hackathon[] {
  const samples = sampleHackathons
  try {
    const userRaw = localStorage.getItem(USER_KEY)
    const user: Hackathon[] = userRaw ? JSON.parse(userRaw) : []
    return [...user, ...samples]
  } catch {
    return samples
  }
}

function saveHackathons(all: Hackathon[]) {
  const samples = sampleHackathons
  const user = all.filter((h) => !samples.some((s) => s.id === h.id))
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export default function Home() {
  const [hackathons, setHackathons] = useState<Hackathon[]>(loadHackathons)
  const [modalOpen, setModalOpen] = useState(false)

  useEffect(() => {
    saveHackathons(hackathons)
  }, [hackathons])

  function addHackathon(h: Hackathon) {
    setHackathons((prev) => [h, ...prev])
  }

  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="flex items-start justify-between mb-6">
          <h1 className="text-2xl font-bold">Hackathons</h1>
          <button
            onClick={() => setModalOpen(true)}
            className="flex cursor-pointer items-center gap-1.5 rounded-lg border border-input bg-background px-3 py-2 text-sm text-foreground shadow-xs hover:bg-accent hover:text-accent-foreground"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <line x1="8" y1="3" x2="8" y2="13" />
              <line x1="3" y1="8" x2="13" y2="8" />
            </svg>
            Add New
          </button>
        </div>
        {hackathons.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-muted-foreground">
            <p className="text-lg">No hackathons yet.</p>
            <p className="text-sm">Click the + button to add one.</p>
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {hackathons.map((h) => (
              <HackathonCard key={h.id} hackathon={h} />
            ))}
          </div>
        )}
      </main>
      <Footer />
      <SubmitHackathonModal
        open={modalOpen}
        onOpenChange={setModalOpen}
        onSubmit={addHackathon}
      />
    </div>
  )
}
