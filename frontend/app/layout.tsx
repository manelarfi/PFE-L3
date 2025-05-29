import type React from "react"
import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "Scrycto - Advanced Steganography Tool",
  description: "Hide messages in plain sight with advanced steganography using LSB, DCT, and DWT algorithms",
  generator: "v0.dev",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body suppressHydrationWarning={true} className="min-h-screen bg-background font-sans antialiased">
        {children}
      </body>
    </html>
  )
}
