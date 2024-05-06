from PIL import Image, ImageTk
import time


class TrafficLights:
	lights_positions = {"1": (780, 600), "2": (910, 710), "3": (1030, 470)}
	light_phases = ["off", "green", "orange", "red"]
	light_img_file = "../images/traffic_lights/car_#.png"
	tr_lights_dict = {}
	tr_lights_main_sec = {"main": [], "secondary": []}
	current_mode = "normal"
	time_on = time.time()

	def __init__(self, images, direction, canvas, window):
		self.images = images
		self.direction = direction
		self.command = "off"
		self.phase = "off"
		self.x = TrafficLights.lights_positions[str(self.direction)][0]
		self.y = TrafficLights.lights_positions[str(self.direction)][1]
		self.root = window
		self.canvas = canvas
		self.tr_light = self.canvas.create_image(self.x, self.y, image=self.images[self.phase])
		if self.direction == 1 or self.direction == 3:
			TrafficLights.tr_lights_main_sec["main"].append(self)
		else:
			TrafficLights.tr_lights_main_sec["secondary"].append(self)
		TrafficLights.tr_lights_dict[str(self.direction)] = self
		self.change()

	def change(self):
		"""Μέθοδος που πραγματοποιεί την αλλαγή φάσης στον κάθε φωτεινό σηματοδότη"""
		if self.command != self.phase:
			self.phase = self.command
			self.canvas.itemconfig(self.tr_light, image=self.images[self.phase])
		self.canvas.tag_raise(self.tr_light)
		self.root.after(100, self.change)

	@classmethod
	def operation(cls):
		"""Μέθοδος η οποία διαχειρίζεται τη λειτουργία των φωτεινών σηματοδοτών"""
		if TrafficLights.current_mode == "night":
			for val in TrafficLights.tr_lights_main_sec["main"]:
				if val.command != "off":
					val.command = "off"
			for val in TrafficLights.tr_lights_main_sec["secondary"]:
				if val.command == "off":
					val.command = "orange"
				elif val.command == "orange":
					val.command = "off"
		elif TrafficLights.current_mode == "normal":
			pass
		TrafficLights.tr_lights_dict["1"].root.after(1000, TrafficLights.operation)

	@classmethod
	def traffic_lights_creator(cls, lights_images, canvas, root):
		"""Μέθοδος η οποία δημιουργεί τους φωτεινούς σηματοδότες"""
		for i in TrafficLights.lights_positions.keys():
			TrafficLights(images=lights_images[i], direction=int(i), canvas=canvas, window=root)

	@classmethod
	def create_images(cls):
		"""Δημιουργία λεξικού με τις φωτογραφίες των φωτεινών σηματοδοτών ανάλογα
		με την κατεύθυνση του κάθε ενός"""
		images = {}
		for x in TrafficLights.lights_positions.keys():
			dir_images = {}
			for i in TrafficLights.light_phases:
				dir_images[i] = ImageTk.PhotoImage(Image.open(TrafficLights.light_img_file.replace("#", i)).rotate(90 * int(x), expand=True))
			images[x] = dir_images
		return images
