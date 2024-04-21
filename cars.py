import tkinter as tk


class Car:
	cars_list = []

	def __init__(self, pos, image, speed, canvas, window):
		self.x = pos[0]
		self.y = pos[1]
		self.image = image
		self.speed = speed
		self.root = window
		self.canvas = canvas
		self.car = self.canvas.create_image(self.x, self.y, image=self.image)
		Car.cars_list.append(self)
		self.move_car()

	def move_car(self):
		if self.x < 1700:
			self.canvas.move(self.car, self.speed[0], self.speed[1])
			self.x += self.speed[0]
			self.y += self.speed[1]
			self.root.after(10, self.move_car)
		else:
			self.delete_car()

	def delete_car(self):
		self.canvas.delete(self.car)
		Car.cars_list.remove(self)
