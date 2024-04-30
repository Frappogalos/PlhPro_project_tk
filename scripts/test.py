from PIL import Image, ImageOps

img = Image.open("../images/pedestrians/Person_2_r.png")
# mirror_img = ImageOps.mirror(img)
img = img.resize((30, 30))
img.save("../images/pedestrians/Person_02_r.png")

