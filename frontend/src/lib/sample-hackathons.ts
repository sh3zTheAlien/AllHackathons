import type { Hackathon } from './types'

export const sampleHackathons: Hackathon[] = [
  {
    id: 'sample-1',
    topic: 'ETHGlobal Bangkok',
    date: '2026-11-15',
    prize: true,
    prizeDetails: '$25,000 USD in prizes + travel grants',
    location: 'Bangkok, Thailand',
    link: 'https://ethglobal.com',
  },
  {
    id: 'sample-2',
    topic: 'Solana Hacker House NYC',
    date: '2026-09-10',
    prize: true,
    prizeDetails: '$10,000 USDC + NFT rewards',
    location: 'New York, USA',
    link: 'https://solana.com',
  },
  {
    id: 'sample-3',
    topic: 'AI x Blockchain Hackathon',
    date: '2026-07-22',
    prize: false,
    location: 'Berlin, Germany',
  },
  {
    id: 'sample-4',
    topic: 'Polkadot Web3 Summit',
    date: '2026-05-08',
    prize: true,
    prizeDetails: '50,000 DOT tokens pool',
    location: 'Lisbon, Portugal',
    link: 'https://polkadot.network',
  },
  {
    id: 'sample-5',
    topic: 'Local Dev Meetup',
    date: '2026-08-01',
    prize: false,
    location: '',
  },
]
