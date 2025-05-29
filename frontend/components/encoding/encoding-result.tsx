"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Download, RotateCcw } from "lucide-react"
import Image from "next/image"

interface EncodingResultProps {
  encodedImage: string
  onEncodeAnother: () => void
}

export default function EncodingResult({ encodedImage, onEncodeAnother }: EncodingResultProps) {
  const handleSave = () => {
    const link = document.createElement("a")
    link.href = encodedImage
    link.download = "encoded-image.png"
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="text-green-600">Encoding Successful!</CardTitle>
        <CardDescription>
          Your text has been successfully hidden in the image. The encoded image looks identical to the original.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="relative aspect-video w-full overflow-hidden rounded-lg border">
          <Image src={encodedImage || "/placeholder.svg"} alt="Encoded image" fill className="object-contain" />
        </div>

        <div className="flex flex-col sm:flex-row gap-3">
          <Button onClick={handleSave} className="flex-1">
            <Download className="mr-2 h-4 w-4" />
            Save Image
          </Button>
          <Button variant="outline" onClick={onEncodeAnother} className="flex-1">
            <RotateCcw className="mr-2 h-4 w-4" />
            Encode Another Image
          </Button>
        </div>

        <div className="bg-muted/50 rounded-lg p-4">
          <p className="text-sm text-muted-foreground">
            <strong>Important:</strong> Save this encoded image to extract the hidden message later. The original image
            and this encoded image may look identical, but only the encoded version contains your hidden text.
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
