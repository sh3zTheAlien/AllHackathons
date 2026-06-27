import { useState } from 'react'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from './ui/dialog'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Textarea } from './ui/textarea'
import { Label } from './ui/label'
import { Switch } from './ui/switch'
import type { Hackathon } from '../lib/types'

interface Props {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (hackathon: Hackathon) => void
}

export default function SubmitHackathonModal({ open, onOpenChange, onSubmit }: Props) {
  const [topic, setTopic] = useState('')
  const [date, setDate] = useState('')
  const [prize, setPrize] = useState(false)
  const [prizeDetails, setPrizeDetails] = useState('')
  const [location, setLocation] = useState('')
  const [link, setLink] = useState('')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!topic.trim() || !date.trim()) return
    onSubmit({
      id: crypto.randomUUID(),
      topic: topic.trim(),
      date: date.trim(),
      prize,
      prizeDetails: prize ? prizeDetails.trim() : '',
      location: location.trim(),
      link: link.trim() || undefined,
    })
    setTopic('')
    setDate('')
    setPrize(false)
    setPrizeDetails('')
    setLocation('')
    setLink('')
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Submit a Hackathon</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="topic">Topic</Label>
            <Input
              id="topic"
              placeholder="e.g. ETHGlobal Bangkok"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="date">Date</Label>
            <Input
              id="date"
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              required
            />
          </div>
          <div className="flex items-center justify-between">
            <Label htmlFor="prize">Prize</Label>
            <Switch id="prize" checked={prize} onCheckedChange={setPrize} />
          </div>
          {prize && (
            <div className="space-y-2">
              <Label htmlFor="prizeDetails">Prize Details</Label>
              <Textarea
                id="prizeDetails"
                placeholder="e.g. $10,000 USD + free travel"
                value={prizeDetails}
                onChange={(e) => setPrizeDetails(e.target.value)}
              />
            </div>
          )}
          <div className="space-y-2">
            <Label htmlFor="location">Location</Label>
            <Input
              id="location"
              placeholder="e.g. Bangkok, Thailand"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="link">Link</Label>
            <Input
              id="link"
              placeholder="e.g. https://ethglobal.com"
              type="url"
              value={link}
              onChange={(e) => setLink(e.target.value)}
            />
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" className="cursor-pointer" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit" className="cursor-pointer">Submit</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
