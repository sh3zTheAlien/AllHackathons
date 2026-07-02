import type { Hackathon } from '@/types/hackathon'

export const sampleHackathons: Hackathon[] = [
  {
    id: 'sample-1',
    name: 'ETHGlobal Bangkok',
    startDate: '2026-11-15',
    hasPrize: true,
    prizeDetails: '$25,000 USD in prizes + travel grants',
    location: 'Bangkok, Thailand',
    url: 'https://ethglobal.com',
    status: 'published',
  },
  {
    id: 'sample-2',
    name: 'Solana Hacker House NYC',
    startDate: '2026-09-10',
    hasPrize: true,
    prizeDetails: '$10,000 USDC + NFT rewards',
    location: 'New York, USA',
    url: 'https://solana.com',
    status: 'published',
  },
  {
    id: 'sample-3',
    name: 'AI x Blockchain Hackathon',
    startDate: '2026-07-22',
    hasPrize: false,
    location: 'Berlin, Germany',
    status: 'published',
  },
  {
    id: 'sample-4',
    name: 'Polkadot Web3 Summit',
    startDate: '2026-05-08',
    hasPrize: true,
    prizeDetails: '50,000 DOT tokens pool',
    location: 'Lisbon, Portugal',
    url: 'https://polkadot.network',
    status: 'published',
  },
  {
    id: 'sample-5',
    name: 'Local Dev Meetup',
    startDate: '2026-08-01',
    hasPrize: false,
    status: 'published',
  },
]
