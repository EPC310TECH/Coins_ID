import sys
from PIL import Image

path, x0, y0, x1, y1, out = sys.argv[1:7]
img = Image.open(path)
w, h = img.size
box = (int(float(x0)*w), int(float(y0)*h), int(float(x1)*w), int(float(y1)*h))
crop = img.crop(box)
# upscale 2x for readability
crop = crop.resize((crop.width*2, crop.height*2), Image.LANCZOS)
crop.save(out)
print(out, crop.size)
