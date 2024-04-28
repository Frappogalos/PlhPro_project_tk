from PIL import Image, ImageOps

img = Image.open("../images/pedestrians/Person_1_l.png")
mirror_img = ImageOps.mirror(img)
mirror_img.save("../images/pedestrians/Person_1_r.png")