import tkinter as tk
from buttons import OpButton, PauseButton
from PIL import ImageTk, Image
from lights_controller import LightsController
from traffic_manager import TrafficManager
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
# Κλήση της κλάσης που δημιουργεί και διαχειρίζεται τους φωτεινούς σηματοδότες
controller = LightsController(tl_parameters=config.car_tl_params, canvas=canvas, root=root)
# Κλήση της κλάσης που δημιουργεί και διαχειρίζεται τη δημιουργία και διαγραφή των
# αυτοκινήτων και των πεζών.
traffic_manager = TrafficManager(car_params=config.cars_params, ped_params=config.peds_params,
                                 canvas=canvas, root=root, lights=controller)
# Δημιουργία του κουμπιού για την παύση λειτουργίας της προσομοίωσης
PauseButton(x=config.pause_params["pos"][0], y=config.pause_params["pos"][1],
            image=config.pause_params["img"], window=root, lights_controller=controller)
# Δημιουργία του κουμπιού για την εναλλαγή των λειτουργιών των φωτεινών σηματοδοτών
OpButton(x=config.op_btn_params["pos"][0], y=config.op_btn_params["pos"][1],
         images=config.op_btn_params["images"], window=root, lights_controller=controller)

root.mainloop()
