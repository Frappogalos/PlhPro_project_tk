from PIL import Image, ImageOps
file = "../images/1.jpg"
img = Image.open(file)
# mirror_img = ImageOps.mirror(img)
ratio = 1.2
# img = img.resize((int(img.width*ratio), int(img.height*ratio)))
img = img.resize((1832, 1080))
# img = img.rotate(270)
img.save(file)
