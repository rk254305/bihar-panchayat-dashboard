from PIL import Image

im = Image.open(r"C:\Users\Raushan KUMAR\.gemini\antigravity\brain\cf2396fe-2bd0-44d9-950a-2fb0b36fdf3b\charts_area_check.png")
# Let's crop around the middle where charts are
w, h = im.size
crop_im = im.crop((0, 300, w, min(h, 1100)))
crop_im.save(r"C:\Users\Raushan KUMAR\.gemini\antigravity\brain\cf2396fe-2bd0-44d9-950a-2fb0b36fdf3b\charts_cropped.png")
print("Saved charts_cropped.png with size", crop_im.size)
