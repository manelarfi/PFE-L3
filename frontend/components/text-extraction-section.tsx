"use client"

import { useState } from "react"
import ExtractionForm from "@/components/extraction/extraction-form"
import ExtractionResult from "@/components/extraction/extraction-result"

// Define the base URL and endpoints
const BASE_URL = "http://127.0.0.1:5000/api/steganography"
const ENDPOINTS = {
  lsb: `${BASE_URL}/lsb/decode`,
  dct: `${BASE_URL}/dct/decode`,
  dwt: `${BASE_URL}/dwt/decode`,
}

export default function TextExtractionSection() {
  const [extractedText, setExtractedText] = useState<string | null>(null)
  const [isExtracting, setIsExtracting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleExtract = async (image: File, method: string) => {
    try {
      setIsExtracting(true)
      setError(null)

      console.log('Starting extraction with method:', method)
      console.log('Image file:', image)

      // Create form data to send to the backend
      const formData = new FormData()
      formData.append('image', image)

      // Get the correct endpoint based on the method
      const endpoint = ENDPOINTS[method as keyof typeof ENDPOINTS]
      console.log('Using endpoint:', endpoint)

      if (!endpoint) {
        throw new Error('Invalid steganography method selected')
      }

      // Make the API request
      console.log('Making API request to:', endpoint)
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
        },
        body: formData,
      })

      console.log('Response status:', response.status)

      if (!response.ok) {
        throw new Error(`Extraction failed: ${response.statusText}`)
      }

      // Get the extracted text from the response
      const data = await response.json()
      console.log('Received data:', data)
      setExtractedText(data.text)
    } catch (err) {
      console.error('Extraction error:', err)
      setError(err instanceof Error ? err.message : 'An error occurred during extraction')
    } finally {
      setIsExtracting(false)
    }
  }

  const handleExtractAnother = () => {
    setExtractedText(null)
    setError(null)
  }

  return (
    <section id="extraction" className="py-20 bg-secondary/10 relative">
      {/* Enhanced background elements with texture */}
      <div className="absolute inset-0 texture-overlay opacity-15"></div>
      <div className="absolute top-10 left-10 w-32 h-32 border border-primary/20 rounded-full"></div>
      <div className="absolute bottom-10 right-10 w-24 h-24 border border-secondary/30 rounded-full"></div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              <span className="text-primary">Text</span> Extraction
            </h2>
            <p className="text-lg text-muted-foreground">Extract hidden messages from steganographic images</p>
          </div>

          {extractedText === null ? (
            <ExtractionForm onExtract={handleExtract} isLoading={isExtracting} />
          ) : (
            <ExtractionResult extractedText={extractedText} onExtractAnother={handleExtractAnother} />
          )}
        </div>
      </div>
    </section>
  )
}
