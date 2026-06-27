import { LinkIcon } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import type { Hackathon } from '../lib/types'

export default function HackathonCard({ hackathon }: { hackathon: Hackathon }) {
  return (
    <Card>
      <CardHeader className="relative">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">{hackathon.topic}</CardTitle>
          {hackathon.link && (
            <a
              href={hackathon.link}
              target="_blank"
              rel="noopener noreferrer"
              className="flex size-7 shrink-0 cursor-pointer items-center justify-center rounded-md border border-input text-muted-foreground hover:bg-accent hover:text-accent-foreground"
            >
              <LinkIcon size={14} />
            </a>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-1 text-sm text-muted-foreground">
        <p>Date: {hackathon.date}</p>
        {hackathon.prize ? (
          <p>Prize: {hackathon.prizeDetails || 'Yes'}</p>
        ) : (
          <p>Prize: No</p>
        )}
        {hackathon.location && <p>Location: {hackathon.location}</p>}
      </CardContent>
    </Card>
  )
}
