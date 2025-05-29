"use client"

import { useState } from "react"
import EncodingForm from "@/components/encoding/encoding-form"
import EncodingResult from "@/components/encoding/encoding-result"

// Define the base URL and endpoints
const BASE_URL = "http://127.0.0.1:5000/api/steganography"
const ENDPOINTS = {
  lsb: `${BASE_URL}/lsb/encode`,
  dct: `${BASE_URL}/dct/encode`,
  dwt: `${BASE_URL}/dwt/encode`,
}

export default function TextEncodingSection() {
  const [encodedImage, setEncodedImage] = useState<string | null>(null)
  const [isEncoding, setIsEncoding] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleEncode = async (image: File, text: string, method: string) => {
    try {
      setIsEncoding(true)
      setError(null)

      // Create form data to send to the backend
      const formData = new FormData()
      formData.append('image', image)
      formData.append('message', text)

      // Get the correct endpoint based on the method
      const endpoint = ENDPOINTS[method as keyof typeof ENDPOINTS]
      if (!endpoint) {
        throw new Error('Invalid steganography method selected')
      }

      // Make the API request
      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Encoding failed: ${response.statusText}`)
      }

      // Assuming the backend returns the encoded image as a blob
      const encodedBlob = await response.blob()
      const encodedDataUrl = URL.createObjectURL(encodedBlob)
      setEncodedImage(encodedDataUrl)
    } catch (err) {
      console.error('Encoding error:', err)
      setError(err instanceof Error ? err.message : 'An error occurred during encoding')
    } finally {
      setIsEncoding(false)
    }
  }

  const handleEncodeAnother = () => {
    setEncodedImage(null)
    setError(null)
    // Clean up the object URL to prevent memory leaks
    if (encodedImage) {
      URL.revokeObjectURL(encodedImage)
    }
  }

  return (
    <section id="encoding" className="py-20 bg-black relative">
      {/* Enhanced background pattern with texture */}
      <div className="absolute inset-0 texture-overlay opacity-20"></div>
      <div className="absolute inset-0 grid-overlay opacity-25"></div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              <span className="text-primary">Text</span> Encoding
            </h2>
            <p className="text-lg text-muted-foreground">
              Hide your secret message inside an image using advanced steganography techniques
            </p>
          </div>

          {!encodedImage ? (
            <EncodingForm onEncode={handleEncode} isLoading={isEncoding} />
          ) : (
            <EncodingResult encodedImage={encodedImage} onEncodeAnother={handleEncodeAnother} />
          )}
        </div>
      </div>
    </section>
  )
}
