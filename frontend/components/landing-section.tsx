"use client"

import { Button } from "@/components/ui/button"
import { Shield, Lock, Eye, Zap } from "lucide-react"

export default function LandingSection() {
  const scrollToEncoding = () => {
    const element = document.getElementById("encoding")
    if (element) {
      element.scrollIntoView({ behavior: "smooth" })
    }
  }

  return (
    <section id="home" className="pt-16 min-h-screen flex items-center relative overflow-hidden">
      {/* Enhanced background with texture overlay */}
      <div className="absolute inset-0 texture-overlay opacity-30"></div>
      <div className="absolute inset-0 grid-overlay opacity-40"></div>

      {/* Animated background elements */}
      <div className="absolute top-20 left-10 w-2 h-2 bg-primary rounded-full animate-pulse"></div>
      <div className="absolute top-40 right-20 w-1 h-1 bg-primary rounded-full animate-ping"></div>
      <div className="absolute bottom-40 left-20 w-1.5 h-1.5 bg-secondary-500 rounded-full animate-pulse"></div>
      <div className="absolute bottom-20 right-10 w-2 h-2 bg-primary rounded-full animate-ping"></div>

      <div className="container mx-auto px-4 py-20 relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6 matrix-text">
            Hide Messages in Plain Sight
          </h1>
          <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-3xl mx-auto">
            Advanced steganography tool using <span className="text-primary font-semibold">LSB</span>,{" "}
            <span className="text-primary font-semibold">DCT</span>, and{" "}
            <span className="text-primary font-semibold">DWT</span> algorithms to securely embed and extract text from
            images
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <Button onClick={scrollToEncoding} size="lg" className="text-lg px-8 py-3 glow-primary">
              <Zap className="mr-2 h-5 w-5" />
              Start Encoding
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="text-lg px-8 py-3 border-primary text-primary hover:bg-primary hover:text-black"
              onClick={() => document.getElementById("about")?.scrollIntoView({ behavior: "smooth" })}
            >
              Learn More
            </Button>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mt-16">
            <div className="text-center group">
              <div className="bg-secondary/20 border border-primary/30 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:glow-primary transition-all duration-300">
                <Shield className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-primary">Secure</h3>
              <p className="text-muted-foreground">Advanced encryption algorithms ensure your messages stay hidden</p>
            </div>
            <div className="text-center group">
              <div className="bg-secondary/20 border border-primary/30 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:glow-primary transition-all duration-300">
                <Lock className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-primary">Private</h3>
              <p className="text-muted-foreground">All processing happens locally in your browser</p>
            </div>
            <div className="text-center group">
              <div className="bg-secondary/20 border border-primary/30 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:glow-primary transition-all duration-300">
                <Eye className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-primary">Invisible</h3>
              <p className="text-muted-foreground">Messages are completely invisible to the naked eye</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
