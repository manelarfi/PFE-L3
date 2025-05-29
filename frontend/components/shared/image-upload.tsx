"use client"

import { useCallback } from "react"
import { useDropzone } from "react-dropzone"
import { Upload, X, ImageIcon } from "lucide-react"
import { Button } from "@/components/ui/button"
import Image from "next/image"

interface ImageUploadProps {
  onImageSelect: (file: File | null) => void
  selectedImage: File | null
  accept?: string
}

export default function ImageUpload({ onImageSelect, selectedImage, accept = "image/*" }: ImageUploadProps) {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        onImageSelect(acceptedFiles[0])
      }
    },
    [onImageSelect],
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"],
    },
    multiple: false,
  })

  const removeImage = () => {
    onImageSelect(null)
  }

  if (selectedImage) {
    const imageUrl = URL.createObjectURL(selectedImage)

    return (
      <div className="relative">
        <div className="relative aspect-video w-full overflow-hidden rounded-lg border">
          <Image src={imageUrl || "/placeholder.svg"} alt="Selected image" fill className="object-contain" />
        </div>
        <div className="flex items-center justify-between mt-2">
          <p className="text-sm text-muted-foreground truncate">
            {selectedImage.name} ({(selectedImage.size / 1024 / 1024).toFixed(2)} MB)
          </p>
          <Button variant="outline" size="sm" onClick={removeImage} className="ml-2">
            <X className="h-4 w-4" />
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div
      {...getRootProps()}
      className={`
        border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
        ${
          isDragActive
            ? "border-primary bg-primary/5"
            : "border-muted-foreground/25 hover:border-primary/50 hover:bg-muted/50"
        }
      `}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center space-y-4">
        <div className="bg-muted rounded-full p-4">
          {isDragActive ? (
            <Upload className="h-8 w-8 text-primary" />
          ) : (
            <ImageIcon className="h-8 w-8 text-muted-foreground" />
          )}
        </div>
        <div>
          <p className="text-lg font-medium">
            {isDragActive ? "Drop the image here" : "Choose an image or drag it here"}
          </p>
          <p className="text-sm text-muted-foreground mt-1">Supports PNG, JPG, JPEG, GIF, BMP, and WebP formats</p>
        </div>
        <Button variant="outline" type="button">
          Browse Files
        </Button>
      </div>
    </div>
  )
}
