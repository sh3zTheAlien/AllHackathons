export default function Footer() {
  return (
    <footer className="border-t mt-auto">
      <div className="container mx-auto flex h-14 items-center justify-center gap-1 px-4 text-sm text-muted-foreground">
        Made by{' '}
        <a
          href="https://github.com/Sh3z"
          target="_blank"
          rel="noopener noreferrer"
          className="font-medium underline underline-offset-4 hover:text-foreground"
        >
          Sh3z
        </a>
        {' & '}
        <a
          href="https://github.com/Deathwish"
          target="_blank"
          rel="noopener noreferrer"
          className="font-medium underline underline-offset-4 hover:text-foreground"
        >
          Deathwish
        </a>
      </div>
    </footer>
  )
}
