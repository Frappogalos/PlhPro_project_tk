import tkinter as tk
import functools
import random
from PIL import ImageTk, Image
import math


class Car:
    """Κλάση Car για τη δημιουργία των αυτοκινήτων και τις λειτουργίες τους"""
    # Οι θέσεις όπου εμφανίζονται τα αυτοκίνητα όταν δημιουργούνται
    CARS_STARTING_POSITIONS = {"1": [(-40, 530), (-40, 475)], "2": [(730, 950), (800, 950)],
                               "3": [(1550, 365), (1550, 420)]}
    SPEED = 6
    CAR_IMAGE_1 = "../images/cars/car_01.png"
    CAR_IMAGE_2 = "../images/cars/car_02.png"
    # Μέγιστος αριθμός αυτοκινήτων που μπορούν να υπάρχουν ταυτόχρονα
    cars_limit = 10
    # Λίστα με τα ενεργά αυτοκίνητα
    cars_dict = {"1": [[], []], "2": [[], []], "3": [[], []]}
    total_car_list = []

    def __init__(self, image, direction, lane, canvas, window):
        """Μέθοδος που δέχεται τις παραμέτρους και δημιουργεί ένα καινούριο αυτοκίνητο"""
        self.image = image
        self.direction = direction
        self.lane = lane
        self.speed = self.find_speed()
        self.moving = True
        self.stopped = None
        self.x = Car.CARS_STARTING_POSITIONS[str(self.direction)][self.lane][0]
        self.y = Car.CARS_STARTING_POSITIONS[str(self.direction)][self.lane][1]
        self.root = window
        self.canvas = canvas
        self.car = self.canvas.create_image(self.x, self.y, image=self.image)
        Car.cars_dict[str(self.direction)][self.lane].append(self)
        Car.total_car_list.append(self)
        self.move_car()
        if self.spawn_collision():
            self.delete_car()

    def find_speed(self):
        """Μέθοδος όπου ανάλογα με την κατεύθυνση του αυτοκινήτου επιστρέφει την ανάλογη ταχύτητα"""
        if self.direction == 1:
            return Car.SPEED, 0
        elif self.direction == 2:
            return 0, -Car.SPEED
        elif self.direction == 3:
            return -Car.SPEED, 0

    def move_car(self):
        """Μέθοδος όπου διαχειρίζεται την κίνηση του κάθε αυτοκινήτου"""
        if self.moving:
            # Εφόσον το αυτοκίνητο κινείται ελέγχει την απόσταση από το προπορευόμενο αυτοκίνητο
            # και αν αυτή είναι κάτω από την οριζόμενη τιμή ακινητοποιείται
            for car in Car.cars_dict[str(self.direction)][self.lane]:
                if self != car and self.direction == car.direction and self.lane == car.lane:
                    if self.direction == 1 and 0 < car.x - self.x < 120:
                        self.moving = False
                        self.speed = (0, 0)
                        self.stopped = car
                        self.root.after(30, self.move_car)
                    elif self.direction == 3 and 0 < self.x - car.x < 120:
                        self.moving = False
                        self.speed = (0, 0)
                        self.stopped = car
                        self.root.after(30, self.move_car)
                    elif self.direction == 2 and 0 < self.y - car.y < 120:
                        self.moving = False
                        self.speed = (0, 0)
                        self.stopped = car
                        self.root.after(30, self.move_car)
        if self.moving:
            # Εφόσον κινείται το αυτοκίνητο αν είναι εντός των ορίων του καμβά συνεχίζει την κίνησή του
            # αλλιώς διαγράφεται το αυτοκίνητο
            if -100 < self.x < 1600 and -100 < self.y < 1000:
                self.canvas.move(self.car, self.speed[0], self.speed[1])
                self.x += self.speed[0]
                self.y += self.speed[1]
                self.root.after(30, self.move_car)
            else:
                self.delete_car()
        else:
            # Εφόσον είναι σταματημένο το αυτοκίνητο, αν μεγαλώσει η απόσταση από το αυτοκίνητο για το
            # οποίο σταμάτησε ξεκινάει πάλι να κινείται
            if (self.direction == 1 or self.direction == 3) and abs(self.x - self.stopped.x) > 180:
                self.moving = True
                self.speed = self.find_speed()
                self.stopped = None
                self.root.after(500, self.move_car)
            elif self.direction == 2 and abs(self.y - self.stopped.y) > 180:
                self.moving = True
                self.speed = self.find_speed()
                self.stopped = None
                self.root.after(500, self.move_car)

    def delete_car(self):
        """Μέθοδος η οποία διαγράφει το αυτοκίνητο εφόσον εξέλθει των ορίων του καμβά"""
        self.canvas.delete(self.car)
        Car.cars_dict[str(self.direction)][self.lane].remove(self)
        Car.total_car_list.remove(self)

    def spawn_collision(self):
        """Μέθοδος η οποία ελέγχει αν το αυτοκίνητο που θα δημιουργηθεί θα συγκρουσθεί με ήδη
        υπάρχον αυτοκίνητο"""
        for car in Car.cars_dict[str(self.direction)][self.lane]:
            if car != self and math.sqrt(abs(self.x - car.x)**2 + abs(self.y - car.y)**2) < 81:
                return True
        return False

    @classmethod
    def car_creator(cls, images, canvas, root):
        """Μέθοδος η οποία δημιουργεί συνεχώς ένα καινούριο αυτοκίνητο μετά το πέρας ενός
           συγκεκριμένου χρονικού διαστήματος"""
        car_images = images
        if len(Car.total_car_list) < Car.cars_limit:
            rand_num = random.randint(1, 100)
            if rand_num <= 40:
                direction = 1
            elif rand_num <= 60:
                direction = 2
            else:
                direction = 3
            lane = random.choice([0, 1])
            car_image = random.choice(car_images[str(direction)])
            Car(image=car_image, direction=direction, lane=lane, canvas=canvas, window=root)
        root.after(4000, functools.partial(Car.car_creator, car_images, canvas, root))

    @classmethod
    def create_images(cls):
        # Δημιουργία λεξικού με τις φωτογραφίες των αυτοκινήτων ανάλογα με την κατεύθυνση
        # του κάθε οχήματος
        images = {}
        for i in range(0, 3):
            images[str(i + 1)] = [ImageTk.PhotoImage(Image.open(Car.CAR_IMAGE_1).rotate(90 * i, expand=True)),
                                  ImageTk.PhotoImage(Image.open(Car.CAR_IMAGE_2).rotate(90 * i, expand=True))]
        return images
