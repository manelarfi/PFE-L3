"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import ImageUpload from "@/components/shared/image-upload"
import { Loader2 } from "lucide-react"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface ExtractionFormProps {
  onExtract: (image: File, method: string) => Promise<void>
  isLoading: boolean
}

export default function ExtractionForm({ onExtract, isLoading }: ExtractionFormProps) {
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [method, setMethod] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (selectedImage && method) {
      onExtract(selectedImage, method)
    }
  }

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Extract Hidden Text</CardTitle>
        <CardDescription>Upload an image that contains hidden text to extract the secret message</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="method">Steganography Method</Label>
            <Select value={method} onValueChange={setMethod}>
              <SelectTrigger>
                <SelectValue placeholder="Choose extraction method" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="lsb">LSB (Least Significant Bit)</SelectItem>
                <SelectItem value="dct">DCT (Discrete Cosine Transform)</SelectItem>
                <SelectItem value="dwt">DWT (Discrete Wavelet Transform)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>Upload Encoded Image</Label>
            <ImageUpload onImageSelect={setSelectedImage} selectedImage={selectedImage} accept="image/*" />
          </div>

          <Button type="submit" className="w-full" disabled={!selectedImage || !method || isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Extracting...
              </>
            ) : (
              "Extract Text"
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
