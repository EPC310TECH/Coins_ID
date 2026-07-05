import sys

from PIL import Image, ImageDraw

path, out = sys.argv[1], sys.argv[2]
img = Image.open(path).convert("RGB")
w, h = img.size
draw = ImageDraw.Draw(img)

step = 0.05
for i in range(1, int(1 / step)):
    x = int(i * step * w)
    draw.line([(x, 0), (x, h)], fill=(255, 0, 0), width=2)
    draw.text((x + 3, 3), f"{i*step:.2f}", fill=(255, 0, 0))
    y = int(i * step * h)
    draw.line([(0, y), (w, y)], fill=(0, 120, 255), width=2)
    draw.text((3, y + 3), f"{i*step:.2f}", fill=(0, 120, 255))

img.save(out, quality=90)
print(out, img.size)
