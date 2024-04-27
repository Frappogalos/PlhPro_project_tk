import tkinter as tk


class OpButton:
	"""Κλάση για τη δημιουργία κουμπιού λειτουργίας των φαναριών της προσομοίωσης"""
	def __init__(self, x, y, images, window):
		self.posx = x
		self.posy = y
		self.on_image = images[0]
		self.off_image = images[1]
		self.operation = True
		self.button = tk.Button(window, image=self.on_image, command=self.btn_click)
		self.button.place(x=self.posx, y=self.posy)

	def btn_click(self):
		"""Συνάρτηση για τη λειτουργία του κουμπιού όταν αυτό πατηθεί"""
		if self.operation:
			self.button.config(image=self.off_image)
			self.operation = False
		else:
			self.button.config(image=self.on_image)
			self.operation = True


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
