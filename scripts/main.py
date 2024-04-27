import tkinter as tk
from buttons import OpButton, PauseButton
from PIL import ImageTk, Image
from cars import Car


BG_IMAGE = "../images/double_intersection.jpg"
PAUSE_IMAGE = "../images/buttons/pause_btn.png"
ON_OFF_RED = "../images/buttons/on_off_red.png"
ON_OFF_GRN = "../images/buttons/on_off_grn.png"
CAR_IMAGE_1 = "../images/cars/car_01.png"
CAR_IMAGE_2 = "../images/cars/car_02.png"
CAR_IMAGES_DICT = {}

# Δημιουργία παραθύρου
root = tk.Tk()
# Τίτλος παραθύρου
root.title("Traffic Simulator")
lights_operation = True
# Φόρτωση εικόνων φόντου και κουμπιών
bg = ImageTk.PhotoImage(Image.open(BG_IMAGE))
pause_img = ImageTk.PhotoImage(Image.open(PAUSE_IMAGE))
on_off_red = ImageTk.PhotoImage(Image.open(ON_OFF_RED))
on_off_green = ImageTk.PhotoImage(Image.open(ON_OFF_GRN))
# Δημιουργία λεξικού με τις φωτογραφίες των αυτοκινήτων ανάλογα με την κατεύθυνση
# του κάθε οχήματος
for i in range(0, 3):
    CAR_IMAGES_DICT[str(i+1)] = [ImageTk.PhotoImage(Image.open(CAR_IMAGE_1).rotate(90*i, expand=True)),
                                 ImageTk.PhotoImage(Image.open(CAR_IMAGE_2).rotate(90*i, expand=True))]
# Μέγεθος παραθύρου
root.geometry(f"{bg.width()}x{bg.height()}")
# Δημιουργία καμβά όπου θα τρέχει η προσομοίωση
canvas = tk.Canvas(root, width=bg.width(), height=bg.height())
canvas.pack(fill="both", expand=True)
# Ορισμός φόντου στον καμβά
back_ground = canvas.create_image(bg.width()/2, bg.height()/2, image=bg)
# Δημιουργία των κουμπιών
PauseButton(x=1000, y=50, image=pause_img, window=root)
OpButton(x=1100, y=50, images=(on_off_green, on_off_red), window=root)
# Κλήση της συνάρτησης που δημιουργεί συνεχώς αυτοκίνητα
Car.car_creator(car_images=CAR_IMAGES_DICT, canvas=canvas, root=root)

root.mainloop()
