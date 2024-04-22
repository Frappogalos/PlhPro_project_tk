import tkinter as tk
import functools
import random


class Car:
	cars_limit = 10
	cars_list = []

	def __init__(self, pos, image, speed, direction, lane, canvas, window):
		self.x = pos[0]
		self.y = pos[1]
		self.image = image
		self.speed = speed
		self.direction = direction
		self.lane = lane
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
			self.root.after(30, self.move_car)
		else:
			self.delete_car()

	def delete_car(self):
		self.canvas.delete(self.car)
		Car.cars_list.remove(self)

	@classmethod
	def car_creator(cls, car_images, car_st_pos, speed, canvas, root):
		if len(Car.cars_list) < Car.cars_limit:
			rand_num = random.randint(1, 200)
			if rand_num <= 15:
				direction = 1
			elif rand_num <= 50:
				direction = 2
			elif rand_num <= 65:
				direction = 3
			else:
				direction = 4
			lane = random.choice([1, 2])
			Car(pos=car_st_pos, image=car_images, speed=speed, direction=direction, lane=lane, canvas=canvas, window=root)
		root.after(4000, functools.partial(Car.car_creator, car_images, car_st_pos, speed, canvas, root))
