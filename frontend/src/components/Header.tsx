import { Link, useLocation } from 'react-router-dom'

export default function Header() {
  const location = useLocation()

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link to="/" className="text-xl font-bold tracking-tight">
          AllHackathons
        </Link>
        <nav className="flex items-center gap-4">
          <Link
            to="/"
            className={`text-sm font-medium transition-colors hover:text-primary ${
              location.pathname === '/' ? 'text-foreground' : 'text-muted-foreground'
            }`}
          >
            Hackathons
          </Link>
          <Link
            to="/feedback"
            className={`text-sm font-medium transition-colors hover:text-primary ${
              location.pathname === '/feedback' ? 'text-foreground' : 'text-muted-foreground'
            }`}
          >
            Feedback
          </Link>
        </nav>
      </div>
    </header>
  )
}
