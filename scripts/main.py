import tkinter as tk
from buttons import OpButton, PauseButton
from PIL import ImageTk, Image
from cars import Car
from pedestrians import Pedestrian
from lights_controller import LightsController
import configuration as config

# Δημιουργία παραθύρου
root = tk.Tk()
# Τίτλος παραθύρου
root.title("Traffic Simulator")
# Φόρτωση εικόνας φόντου
bg = ImageTk.PhotoImage(Image.open(config.bg_image))

# Μέγεθος παραθύρου
root.geometry(f"{bg.width()}x{bg.height()}")
# Δημιουργία καμβά όπου θα τρέχει η προσομοίωση
canvas = tk.Canvas(root, width=bg.width(), height=bg.height())
canvas.pack(fill="both", expand=True)
# Ορισμός φόντου στον καμβά
back_ground = canvas.create_image(bg.width()/2, bg.height()/2, image=bg)
# Κλήση της μεθόδου που ξεκινάει τη λειτουργία των φωτεινών σηματοδοτών
controller = LightsController(tl_parameters=config.car_tl_params, canvas=canvas, root=root)
# Κλήση της συνάρτησης που δημιουργεί συνεχώς αυτοκίνητα
Car.car_creator(car_images=Car.create_images(), canvas=canvas, root=root, lights=controller)
# Κλήση της συνάρτησης που δημιουργεί συνεχώς πεζούς
Pedestrian.pedestrian_creator(ped_images=Pedestrian.create_images(), canvas=canvas, root=root, lights=controller)
# Δημιουργία του κουμπιού για την εναλλαγή των λειτουργιών των φωτεινών σηματοδοτών
PauseButton(x=config.pause_params["pos"][0], y=config.pause_params["pos"][1], image=config.pause_params["img"],
            window=root, lights_controller=controller)
OpButton(x=config.op_btn_params["pos"][0], y=config.op_btn_params["pos"][1], images=config.op_btn_params["images"],
         window=root, lights_controller=controller)

root.mainloop()
