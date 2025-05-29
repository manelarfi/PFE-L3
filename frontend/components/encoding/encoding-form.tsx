"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import ImageUpload from "@/components/shared/image-upload"
import { Loader2 } from "lucide-react"

interface EncodingFormProps {
  onEncode: (image: File, text: string, method: string) => void
  isLoading: boolean
}

export default function EncodingForm({ onEncode, isLoading }: EncodingFormProps) {
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [text, setText] = useState("")
  const [method, setMethod] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (selectedImage && text && method) {
      onEncode(selectedImage, text, method)
    }
  }

  const isFormValid = selectedImage && text.trim() && method

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Encode Text into Image</CardTitle>
        <CardDescription>Select an image, enter your secret message, and choose a steganography method</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="method">Steganography Method</Label>
            <Select value={method} onValueChange={setMethod}>
              <SelectTrigger>
                <SelectValue placeholder="Choose encoding method" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="lsb">LSB (Least Significant Bit)</SelectItem>
                <SelectItem value="dct">DCT (Discrete Cosine Transform)</SelectItem>
                <SelectItem value="dwt">DWT (Discrete Wavelet Transform)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>Upload Image</Label>
            <ImageUpload onImageSelect={setSelectedImage} selectedImage={selectedImage} accept="image/*" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="text">Secret Message</Label>
            <Textarea
              id="text"
              placeholder="Enter the text you want to hide in the image..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              rows={4}
              className="resize-none"
            />
            <p className="text-sm text-muted-foreground">{text.length} characters</p>
          </div>

          <Button type="submit" className="w-full" disabled={!isFormValid || isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Encoding...
              </>
            ) : (
              "Encode Text"
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
