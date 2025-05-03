from stegano import lsbset
from stegano.lsbset import generators
from PIL import Image



secret_message = "Bonjour, ceci est un message secret."


image_path = "image.jpg"  



image = Image.open(image_path)


secret_image = lsbset.hide(
    image, 
    secret_message,
    generator=generators.eratosthenes()
)


output_image_path = "image_stego.png"  
secret_image.save(output_image_path)

print("caché", output_image_path)


extracted_message = lsbset.reveal(
    Image.open(output_image_path),
    generator=generators.eratosthenes()
)

print(" Message est:", extracted_message)
