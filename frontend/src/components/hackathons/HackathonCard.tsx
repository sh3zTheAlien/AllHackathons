import { LinkIcon } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import type { Hackathon } from '@/types/hackathon'

export default function HackathonCard({ hackathon }: { hackathon: Hackathon }) {
  return (
    <Card>
      <CardHeader className="relative">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">{hackathon.name}</CardTitle>
          {hackathon.url && (
            <a
              href={hackathon.url}
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
        {hackathon.startDate && <p>Date: {hackathon.startDate}</p>}
        {hackathon.hasPrize === true ? (
          <p>Prize: {hackathon.prizeDetails || 'Yes'}</p>
        ) : hackathon.hasPrize === false ? (
          <p>Prize: No</p>
        ) : null}
        {hackathon.location && <p>Location: {hackathon.location}</p>}
      </CardContent>
    </Card>
  )
}
