export interface Hackathon {
  id: string
  topic: string
  date: string
  prize: boolean
  prizeDetails?: string
  location: string
  link?: string
}

export interface FeedbackEntry {
  id: string
  type: 'bug' | 'feature' | 'other'
  message: string
}
