import tkinter as tk
from buttons import OpButton, PauseButton
from PIL import ImageTk, Image
from cars import Car


BG_IMAGE = "images/double_intersection.jpg"
PAUSE_IMAGE = "images/buttons/pause_btn.png"
ON_OFF_RED = "images/buttons/on_off_red.png"
ON_OFF_GRN = "images/buttons/on_off_grn.png"
CAR_IMAGE_1 = "images/cars/car_01.png"
CAR_IMAGE_2 = "images/cars/car_02.png"
CAR_IMAGES_DICT = {}
CARS_STARTING_POSITIONS = {"1": (1200, 900), "2": (1750, 380), "3": [(1640, 365), (1640, 420)], "4": (-40, 460)}
CAR_LIGHTS_INFO = [[640, 410, 2], [470, 430, 4], [535, 310, 3, 11000, 3000, 34000]]
PEDESTRIAN_INFO = [[610, 300, 1], [620, 540, 3], [495, 300, 1], [495, 540, 3],
                   [640, 335, 4], [470, 340, 2], [640, 505, 4], [470, 505, 2]]

root = tk.Tk()
root.title("Traffic Simulator")
lights_operation = True
bg = ImageTk.PhotoImage(Image.open(BG_IMAGE))
pause_img = ImageTk.PhotoImage(Image.open(PAUSE_IMAGE))
on_off_red = ImageTk.PhotoImage(Image.open(ON_OFF_RED))
on_off_green = ImageTk.PhotoImage(Image.open(ON_OFF_GRN))
for i in range(0, 4):
    CAR_IMAGES_DICT[str(i+1)] = [ImageTk.PhotoImage(Image.open(CAR_IMAGE_1).rotate(90*i, expand=True)),
                                 ImageTk.PhotoImage(Image.open(CAR_IMAGE_2).rotate(90*i, expand=True))]
root.geometry(f"{bg.width()}x{bg.height()}")
canvas = tk.Canvas(root, width=bg.width(), height=bg.height())
canvas.pack(fill="both", expand=True)
back_ground = canvas.create_image(bg.width()/2, bg.height()/2, image=bg)
PauseButton(x=1000, y=50, image=pause_img, window=root)
OpButton(x=1100, y=50, images=(on_off_green, on_off_red), window=root)
Car.car_creator(car_images=CAR_IMAGES_DICT, car_st_pos=(1640, 420), speed=(-6, 0), canvas=canvas, root=root)


root.mainloop()
