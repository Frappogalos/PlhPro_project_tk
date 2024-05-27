import tkinter as tk
from pedestrians import Pedestrian
from cars import Car
from PIL import ImageTk, Image


class OpButton:
    """Κλάση για τη δημιουργία κουμπιού λειτουργίας των φαναριών της προσομοίωσης"""
    modes = ["night", "normal"]

    def __init__(self, x, y, images, window, lights_controller):
        self.posx = x
        self.posy = y
        self.images = [ImageTk.PhotoImage(Image.open(images[0])),
                       ImageTk.PhotoImage(Image.open(images[1]))]
        self.current_image = self.images[1]
        self.operation = "normal"
        self.controller = lights_controller
        self.button = tk.Button(window, image=self.current_image, command=self.btn_click)
        self.button.place(x=self.posx, y=self.posy)

    def btn_click(self):
        """Συνάρτηση για τη λειτουργία του κουμπιού όταν αυτό πατηθεί"""
        self.current_image = self.images[self.images.index(self.current_image)-1]
        self.button.config(image=self.current_image)
        self.operation = OpButton.modes[OpButton.modes.index(self.operation)-1]
        self.controller.initialise(self.operation)


class PauseButton:
    """Κλάση για τη δημιουργία κουμπιού παύσης της προσομοίωσης"""

    def __init__(self, x, y, image, window, lights_controller):
        self.posx = x
        self.posy = y
        self.image = ImageTk.PhotoImage(Image.open(image))
        self.controller = lights_controller
        self.button = tk.Button(window, image=self.image, command=self.pause_unpause)
        self.button.place(x=self.posx, y=self.posy)

    def pause_unpause(self):
        self.controller.change_mode()


class CarsSpeedControl:
    def __init__(self, x, y, window, traffic_manager, default_speed, speed_range):
        self.posx = x
        self.posy = y
        self.traffic_manager = traffic_manager
        var = tk.DoubleVar(value=default_speed)
        self.label = tk.Label(window, text="Ταχύτητα οχημάτων", bg="lightblue", font=("Arial", 16, "bold"),
                              relief=tk.RAISED)
        self.label.place(x=self.posx-40, y=self.posy-30)
        self.spinbox = tk.Spinbox(window, from_=speed_range[0], to=speed_range[1], textvariable=var, width=10,
                                  relief="sunken", repeatdelay=500, repeatinterval=100, font=("Arial", 12),
                                  bg="lightgrey", fg="blue", command=self.change_speed)
        self.spinbox.config(state="normal", cursor="hand2", bd=3, justify="center", wrap=True)
        self.spinbox.place(x=self.posx, y=self.posy)

    def change_speed(self):
        value = int(self.spinbox.get())
        self.traffic_manager.change_car_speed(value)

