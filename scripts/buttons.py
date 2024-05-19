import tkinter as tk
from traffic_lights import TrafficLights
from pedestrians import Pedestrian
from cars import Car
from lights_controller import LightsController
from PIL import ImageTk, Image


class OpButton:
    """Κλάση για τη δημιουργία κουμπιού λειτουργίας των φαναριών της προσομοίωσης"""
    modes = ["night", "normal"]
    on_off_red = "../images/buttons/on_off_red.png"
    on_off_grn = "../images/buttons/on_off_grn.png"

    def __init__(self, x, y, window):
        self.posx = x
        self.posy = y
        self.images = [ImageTk.PhotoImage(Image.open(OpButton.on_off_grn)),
                       ImageTk.PhotoImage(Image.open(OpButton.on_off_red))]
        self.current_image = self.images[1]
        self.operation = "normal"
        self.button = tk.Button(window, image=self.current_image, command=self.btn_click)
        self.button.place(x=self.posx, y=self.posy)

    def btn_click(self):
        """Συνάρτηση για τη λειτουργία του κουμπιού όταν αυτό πατηθεί"""
        self.current_image = self.images[self.images.index(self.current_image)-1]
        self.button.config(image=self.current_image)
        self.operation = OpButton.modes[OpButton.modes.index(self.operation)-1]
        LightsController.initialise(LightsController.controller, self.operation)


class PauseButton:
    """Κλάση για τη δημιουργία κουμπιού παύσης της προσομοίωσης"""
    pause_image = "../images/buttons/pause_btn.png"

    def __init__(self, x, y, window):
        self.posx = x
        self.posy = y
        self.image = ImageTk.PhotoImage(Image.open(PauseButton.pause_image))
        self.operation = True
        self.button = tk.Button(window, image=self.image, command=self.btn_click)
        self.button.place(x=self.posx, y=self.posy)

    def btn_click(self):
        """Συνάρτηση για τη λειτουργία του κουμπιού όταν αυτό πατηθεί"""
        if self.operation:
            self.operation = False
            self.pause_unpause()
        else:
            self.operation = True
            self.pause_unpause()

    def pause_unpause(self):
        Car.operation = Pedestrian.operation = LightsController\
            .operation_mode = TrafficLights.operation_mode = self.operation
