"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Copy, RotateCcw, Check } from "lucide-react"
import { useState } from "react"

interface ExtractionResultProps {
  extractedText: string
  onExtractAnother: () => void
}

export default function ExtractionResult({ extractedText, onExtractAnother }: ExtractionResultProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(extractedText)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error("Failed to copy text: ", err)
    }
  }

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="text-green-600">Text Extracted Successfully!</CardTitle>
        <CardDescription>The hidden message has been successfully extracted from the image.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium">Extracted Message:</label>
            <Button variant="outline" size="sm" onClick={handleCopy} className="h-8">
              {copied ? (
                <>
                  <Check className="mr-1 h-3 w-3" />
                  Copied
                </>
              ) : (
                <>
                  <Copy className="mr-1 h-3 w-3" />
                  Copy
                </>
              )}
            </Button>
          </div>
          <Textarea value={extractedText} readOnly rows={4} className="resize-none bg-muted/50" />
          <p className="text-sm text-muted-foreground">{extractedText.length} characters extracted</p>
        </div>

        <Button variant="outline" onClick={onExtractAnother} className="w-full">
          <RotateCcw className="mr-2 h-4 w-4" />
          Extract Another Text
        </Button>

        <div className="bg-muted/50 rounded-lg p-4">
          <p className="text-sm text-muted-foreground">
            <strong>Success!</strong> The steganographic algorithm successfully detected and extracted the hidden
            message from your image. The text above is what was secretly embedded in the image.
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
