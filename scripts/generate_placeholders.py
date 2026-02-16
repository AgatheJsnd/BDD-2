from PIL import Image, ImageDraw, ImageFont
import os
import random

PRODUCTS = [
    "sac", "sac-a-main", "handbag",
    "travel-bag", "sac-de-voyage", "sac-weekend",
    "montre", "watch",
    "parfum", "perfume",
    "wallet", "portefeuille",
    "accessoires", "accessories",
    "bijoux", "jewelry"
]

OUTPUT_DIR = "assets/products"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_placeholder(slug):
    width, height = 400, 400
    color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
    text_color = (50, 50, 50)
    
    img = Image.new('RGB', (width, height), color)
    d = ImageDraw.Draw(img)
    
    # Try to load a default font, otherwise use default bitmap font
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()
        
    # Draw slug text
    # text_width, text_height = d.textsize(slug, font=font) # specific to older PIL
    # Newer Pillow use textbbox or textlength. Let's keep it simple and center roughly.
    d.text((width/2 - 50, height/2 - 10), slug, fill=text_color, font=font) # Rough centering
    
    output_path = os.path.join(OUTPUT_DIR, f"{slug}.png")
    img.save(output_path)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    for p in PRODUCTS:
        generate_placeholder(p)
