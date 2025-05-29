"use client"

import { useState } from "react"
import Link from "next/link"
import { Menu, X, Shield } from "lucide-react"

export default function Navigation() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: "smooth" })
    }
    setIsMenuOpen(false)
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-black/95 backdrop-blur border-b border-primary/20">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="text-xl font-bold text-primary flex items-center gap-2">
              <Shield className="w-6 h-6" />
              Scrycto
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <button
                onClick={() => scrollToSection("home")}
                className="text-foreground hover:text-primary px-3 py-2 rounded-md text-sm font-medium transition-colors border border-transparent hover:border-primary/30"
              >
                Home
              </button>
              <button
                onClick={() => scrollToSection("encoding")}
                className="text-foreground hover:text-primary px-3 py-2 rounded-md text-sm font-medium transition-colors border border-transparent hover:border-primary/30"
              >
                Encode
              </button>
              <button
                onClick={() => scrollToSection("extraction")}
                className="text-foreground hover:text-primary px-3 py-2 rounded-md text-sm font-medium transition-colors border border-transparent hover:border-primary/30"
              >
                Extract
              </button>
              <button
                onClick={() => scrollToSection("about")}
                className="text-foreground hover:text-primary px-3 py-2 rounded-md text-sm font-medium transition-colors border border-transparent hover:border-primary/30"
              >
                About
              </button>
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button onClick={() => setIsMenuOpen(!isMenuOpen)} className="text-foreground hover:text-primary p-2">
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-black/95 border-t border-primary/20">
              <button
                onClick={() => scrollToSection("home")}
                className="text-foreground hover:text-primary block px-3 py-2 rounded-md text-base font-medium w-full text-left transition-colors hover:bg-primary/10"
              >
                Home
              </button>
              <button
                onClick={() => scrollToSection("encoding")}
                className="text-foreground hover:text-primary block px-3 py-2 rounded-md text-base font-medium w-full text-left transition-colors hover:bg-primary/10"
              >
                Encode
              </button>
              <button
                onClick={() => scrollToSection("extraction")}
                className="text-foreground hover:text-primary block px-3 py-2 rounded-md text-base font-medium w-full text-left transition-colors hover:bg-primary/10"
              >
                Extract
              </button>
              <button
                onClick={() => scrollToSection("about")}
                className="text-foreground hover:text-primary block px-3 py-2 rounded-md text-base font-medium w-full text-left transition-colors hover:bg-primary/10"
              >
                About
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
