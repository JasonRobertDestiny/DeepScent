import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Sensora | Fragrance That Feels You',
  description: 'Experience the future of perfumery. Sensora uses neural interfaces and bio-calibration to create your perfect, personalized fragrance.',
  keywords: ['perfume', 'fragrance', 'AI', 'personalized', 'luxury', 'neural', 'bio-calibration'],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen overflow-x-hidden">
        {/* Aurora background effect */}
        <div className="aurora-bg" />

        {/* Floating particles */}
        <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="particle"
              style={{
                left: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 8}s`,
                animationDuration: `${8 + Math.random() * 4}s`,
              }}
            />
          ))}
        </div>

        {/* Main content */}
        <main className="relative z-10">
          {children}
        </main>
      </body>
    </html>
  )
}
