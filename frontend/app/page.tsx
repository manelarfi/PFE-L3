import Navigation from "@/components/navigation"
import LandingSection from "@/components/landing-section"
import TextEncodingSection from "@/components/text-encoding-section"
import TextExtractionSection from "@/components/text-extraction-section"
import AboutSection from "@/components/about-section"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <main>
        <LandingSection />
        <TextEncodingSection />
        <TextExtractionSection />
        <AboutSection />
      </main>
    </div>
  )
}
