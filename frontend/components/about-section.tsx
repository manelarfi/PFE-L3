import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ImageIcon, Cpu, Waves, Code, Database, Shield } from "lucide-react"

export default function AboutSection() {
  return (
    <section id="about" className="py-20 bg-black relative">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 border border-primary/10 rounded-full animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-48 h-48 border border-secondary/20 rounded-full animate-ping"></div>
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              About <span className="text-primary">Steganography</span>
            </h2>
            <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
              Steganography is the practice of concealing information within another medium. Our tool uses three
              advanced algorithms to hide text messages in images.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mb-12">
            <Card className="bg-card/50 border-primary/20 hover:border-primary/40 transition-all duration-300 hover:glow-primary">
              <CardHeader>
                <div className="bg-primary/10 w-12 h-12 rounded-lg flex items-center justify-center mb-4 border border-primary/30">
                  <ImageIcon className="w-6 h-6 text-primary" />
                </div>
                <CardTitle className="text-primary">LSB (Least Significant Bit)</CardTitle>
                <CardDescription className="text-muted-foreground">
                  The simplest and most common steganographic technique
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  LSB steganography works by replacing the least significant bits of pixel values with bits from the
                  secret message. This creates minimal visual distortion while effectively hiding data.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card/50 border-primary/20 hover:border-primary/40 transition-all duration-300 hover:glow-primary">
              <CardHeader>
                <div className="bg-primary/10 w-12 h-12 rounded-lg flex items-center justify-center mb-4 border border-primary/30">
                  <Cpu className="w-6 h-6 text-primary" />
                </div>
                <CardTitle className="text-primary">DCT (Discrete Cosine Transform)</CardTitle>
                <CardDescription className="text-muted-foreground">
                  Frequency domain steganography technique
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  DCT transforms image data into frequency components, allowing data to be hidden in less perceptible
                  frequency coefficients. This method is more robust against compression and filtering.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card/50 border-primary/20 hover:border-primary/40 transition-all duration-300 hover:glow-primary">
              <CardHeader>
                <div className="bg-primary/10 w-12 h-12 rounded-lg flex items-center justify-center mb-4 border border-primary/30">
                  <Waves className="w-6 h-6 text-primary" />
                </div>
                <CardTitle className="text-primary">DWT (Discrete Wavelet Transform)</CardTitle>
                <CardDescription className="text-muted-foreground">
                  Advanced multi-resolution analysis technique
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  DWT decomposes images into different frequency subbands, providing excellent imperceptibility and
                  robustness. It's particularly effective for hiding larger amounts of data.
                </p>
              </CardContent>
            </Card>
          </div>

          <div className="bg-secondary/20 border border-primary/20 rounded-lg p-8 animated-border">
            <h3 className="text-2xl font-bold text-foreground mb-4">
              Why Use <span className="text-primary">Steganography</span>?
            </h3>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="flex items-start gap-3">
                <Shield className="w-6 h-6 text-primary mt-1 flex-shrink-0" />
                <div>
                  <h4 className="text-lg font-semibold mb-2 text-primary">Security Through Obscurity</h4>
                  <p className="text-muted-foreground">
                    Unlike encryption which makes data unreadable, steganography makes data invisible. The very
                    existence of the hidden message is concealed.
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <Database className="w-6 h-6 text-primary mt-1 flex-shrink-0" />
                <div>
                  <h4 className="text-lg font-semibold mb-2 text-primary">Digital Watermarking</h4>
                  <p className="text-muted-foreground">
                    Protect intellectual property by embedding ownership information directly into digital media files.
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <Code className="w-6 h-6 text-primary mt-1 flex-shrink-0" />
                <div>
                  <h4 className="text-lg font-semibold mb-2 text-primary">Covert Communication</h4>
                  <p className="text-muted-foreground">
                    Enable secure communication channels where the transmission of encrypted data might raise suspicion.
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <Shield className="w-6 h-6 text-primary mt-1 flex-shrink-0" />
                <div>
                  <h4 className="text-lg font-semibold mb-2 text-primary">Data Integrity</h4>
                  <p className="text-muted-foreground">
                    Embed checksums or authentication data to verify the integrity and authenticity of digital content.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
