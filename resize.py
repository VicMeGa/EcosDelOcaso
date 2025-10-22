from PIL import Image
import os

input_folder = "/run/media/victor/se/mis_programas/EcosDelOcaso/mapa/Building"
output_folder = "/run/media/victor/se/mis_programas/EcosDelOcaso/mapa/Building"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # Obtener tamaño original
        width, height = img.size

        # Calcular nuevo tamaño (1/4 del original)
        new_size = (width // 4, height // 4)

        # Redimensionar con LANCZOS
        img_resized = img.resize(new_size, Image.Resampling.LANCZOS)

        save_path = os.path.join(output_folder, filename)
        img_resized.save(save_path)

        print(f"Imagen {filename} reducida a {new_size[0]}x{new_size[1]}~ 💕")

print("¡Todas las imágenes fueron reducidas a 1/4 de su tamaño original uwu~! 🌸")
