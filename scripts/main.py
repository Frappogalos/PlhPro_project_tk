import tkinter as tk
from buttons import OpButton, PauseButton
from PIL import ImageTk, Image
from cars import Car
from pedestrians import Pedestrian


BG_IMAGE = "../images/double_intersection.jpg"
PAUSE_IMAGE = "../images/buttons/pause_btn.png"
ON_OFF_RED = "../images/buttons/on_off_red.png"
ON_OFF_GRN = "../images/buttons/on_off_grn.png"
PED_DIRECTIONS = 4
NUM_OF_PERSON_IMAGES = 2
NUM_OF_STEPS = 2
PED_IMG_FILE = f"../images/pedestrians/Person_#_$.png"
PEDESTRIAN_IMAGES_DICT = {}

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
# Δημιουργία λεξικού με τις φωτογραφίες των πεζών ανάλογα με την κατεύθυνση
# του κάθε ένα
for x in range(0, 4):
    ped_images = {}
    for i in range(0, 2):
        ped_images[str(i + 1)] = {}
        for y in range(0, NUM_OF_STEPS):
            ped_images[str(i + 1)][str(y)] = ImageTk.PhotoImage(Image.open(PED_IMG_FILE.replace("#", str(i)).replace("$", str(y))).rotate(90*x, expand=True))
        ped_images[str(i+1)]["st"] = ImageTk.PhotoImage(Image.open(PED_IMG_FILE.replace("#", str(i)).replace("$", "st")).rotate(90*x, expand=True))
    PEDESTRIAN_IMAGES_DICT[str(x+1)] = ped_images

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
Car.car_creator(images=Car.create_images(), canvas=canvas, root=root)

Pedestrian.pedestrian_creator(ped_images=PEDESTRIAN_IMAGES_DICT, canvas=canvas, root=root)

root.mainloop()
