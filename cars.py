import tkinter as tk
import functools
import random

CARS_STARTING_POSITIONS = {"1": [(-40, 530), (-40, 475)], "2": [(830, 950), (890, 950)],
                           "3": [(1640, 365), (1640, 420)], "4": [(710, -40), (770, -40)]}


class Car:
    cars_limit = 10
    cars_list = []

    def __init__(self, image, direction, lane, canvas, window):
        self.image = image
        self.direction = direction
        self.lane = lane
        self.speed = self.find_speed()
        self.moving = True
        self.stopped = None
        self.x = CARS_STARTING_POSITIONS[str(self.direction)][self.lane][0]
        self.y = CARS_STARTING_POSITIONS[str(self.direction)][self.lane][1]
        self.root = window
        self.canvas = canvas
        self.car = self.canvas.create_image(self.x, self.y, image=self.image)
        Car.cars_list.append(self)
        self.move_car()

    def find_speed(self):
        if self.direction == 1:
            return 6, 0
        elif self.direction == 2:
            return 0, -6
        elif self.direction == 3:
            return -6, 0
        else:
            return 0, 6

    def move_car(self):
        if self.moving:
            for car in Car.cars_list:
                if self != car and self.direction == car.direction and self.lane == car.lane:
                    if (self.direction == 1 or self.direction == 3) and abs(self.x - car.x) < 150:
                        self.moving = False
                        self.stopped = car
                        self.speed = (0, 0)
                        self.root.after(30, self.move_car)
                    elif (self.direction == 2 or self.direction == 4) and abs(self.y - car.y) < 150:
                        self.moving = False
                        self.stopped = car
                        self.speed = (0, 0)
                        self.root.after(30, self.move_car)
        if self.moving:
            if -100 < self.x < 1700 and -100 < self.y < 1000:
                self.canvas.move(self.car, self.speed[0], self.speed[1])
                self.x += self.speed[0]
                self.y += self.speed[1]
                self.root.after(30, self.move_car)
            else:
                self.delete_car()
        if not self.moving:
            if (self.direction == 1 or self.direction == 3) and abs(self.x - self.stopped.x) > 180:
                self.moving = True
                self.stopped = None
                self.speed = self.find_speed()
                self.root.after(500, self.move_car)
            elif (self.direction == 2 or self.direction == 4) and abs(self.y - self.stopped.y) > 180:
                self.moving = True
                self.stopped = None
                self.speed = self.find_speed()
                self.root.after(500, self.move_car)

    def delete_car(self):
        Car.cars_list.remove(self)
        self.canvas.delete(self.car)

    @classmethod
    def car_creator(cls, car_images, canvas, root):
        if len(Car.cars_list) < Car.cars_limit:
            rand_num = random.randint(1, 100)
            if rand_num <= 15:
                direction = 1
            elif rand_num <= 50:
                direction = 2
            elif rand_num <= 65:
                direction = 3
            else:
                direction = 4
            lane = random.choice([0, 1])
            car_type = random.choice([0, 1])
            Car(image=car_images[str(direction)][car_type], direction=direction, lane=lane, canvas=canvas, window=root)
        root.after(4000, functools.partial(Car.car_creator, car_images, canvas, root))
