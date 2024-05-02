from PIL import Image, ImageOps
file = "../images/pedestrians/Person_1_st.png"
img = Image.open(file)
# mirror_img = ImageOps.mirror(img)
ratio = 1.2
img = img.resize((int(img.width*ratio), int(img.height*ratio)))
# img = img.rotate(270)
img.save(file)
