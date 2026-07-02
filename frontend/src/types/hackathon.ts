export interface Hackathon {
  id: string
  name: string
  description?: string
  url?: string
  startDate?: string
  endDate?: string
  location?: string
  mode?: "in-person" | "online" | "hybrid"
  organizer?: string
  hasPrize?: boolean
  prizeDetails?: string
  tags?: string[]
  status: "draft" | "pending" | "published" | "needs-changes"
  submittedAt?: string
  updatedAt?: string
  interestCount?: number
  discordChannelId?: string
}
