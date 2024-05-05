from PIL import Image, ImageTk
import time


class TrafficLights:
	lights_positions = {"1": (), "2": (), "3": ()}
	light_phases = ["off", "green", "orange", "red"]
	light_img_file = "../images/traffic_lights/car_#.png"

	def __init__(self):
		pass

	@classmethod
	def create_images(cls):
		"""Δημιουργία λεξικού με τις φωτογραφίες των φωτεινών σηματοδοτών ανάλογα
		με την κατεύθυνση του κάθε ενός"""
		images = {}
		for x in range(0, len(TrafficLights.lights_positions)):
			dir_images = {}
			for i in TrafficLights.light_phases:
				dir_images[str(x + 1)][i] = ImageTk.PhotoImage(Image.open(TrafficLights.light_img_file.replace("#", i)).rotate(90 * x, expand=True))
			images[str(x + 1)] = dir_images
		return images
