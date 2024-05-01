from PIL import Image, ImageOps
file = "../images/pedestrians/Person_2_st.png"
img = Image.open(file)
# mirror_img = ImageOps.mirror(img)
# img = img.resize((30, 30))
img = img.rotate(270)
img.save(file)

