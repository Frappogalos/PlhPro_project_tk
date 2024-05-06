import tkinter as tk
from traffic_lights import TrafficLights


class OpButton:
	"""Κλάση για τη δημιουργία κουμπιού λειτουργίας των φαναριών της προσομοίωσης"""
	modes = ["night", "normal"]

	def __init__(self, x, y, images, window):
		self.posx = x
		self.posy = y
		self.images = images
		self.current_image = self.images[1]
		self.operation = "normal"
		self.button = tk.Button(window, image=self.current_image, command=self.btn_click)
		self.button.place(x=self.posx, y=self.posy)

	def btn_click(self):
		"""Συνάρτηση για τη λειτουργία του κουμπιού όταν αυτό πατηθεί"""
		self.current_image = self.images[self.images.index(self.current_image)-1]
		self.button.config(image=self.current_image)
		self.operation = OpButton.modes[OpButton.modes.index(self.operation)-1]
		TrafficLights.current_mode = self.operation


class PauseButton:
	"""Κλάση για τη δημιουργία κουμπιού παύσης της προσομοίωσης"""
	def __init__(self, x, y, image, window):
		self.posx = x
		self.posy = y
		self.image = image
		self.operation = True
		self.button = tk.Button(window, image=self.image, command=self.btn_click)
		self.button.place(x=self.posx, y=self.posy)

	def btn_click(self):
		"""Συνάρτηση για τη λειτουργία του κουμπιού όταν αυτό πατηθεί"""
		if self.operation:
			self.operation = False
		else:
			self.operation = True
