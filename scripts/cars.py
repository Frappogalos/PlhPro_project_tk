import tkinter as tk
import functools
import random
from PIL import ImageTk, Image
import math
from traffic_lights import TrafficLights


class Car:
    """Κλάση Car για τη δημιουργία των αυτοκινήτων και τις λειτουργίες τους"""
    # Οι θέσεις όπου εμφανίζονται τα αυτοκίνητα όταν δημιουργούνται
    cars_starting_positions = {"1": [(-40, 645), (-40, 570)], "2": [(870, 1030), (960, 1030)],
                               "3": [(1882, 440), (1882, 510)]}
    speed = 6
    speed_by_direction = {"1": (speed, 0), "2": (0, -speed), "3": (-speed, 0)}
    num_of_car_images = 2
    front_car_min_distance = 120
    car_image = "../images/cars/car_#.png"
    orig_img_ratio = 0.1
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
        self.speed = Car.speed_by_direction[str(self.direction)]
        self.moving = True
        self.stopped = None
        self.x = Car.cars_starting_positions[str(self.direction)][self.lane][0]
        self.y = Car.cars_starting_positions[str(self.direction)][self.lane][1]
        self.root = window
        self.canvas = canvas
        self.car = self.canvas.create_image(self.x, self.y, image=self.image)
        Car.cars_dict[str(self.direction)][self.lane].append(self)
        Car.total_car_list.append(self)
        self.move_car()
        if self.spawn_collision():
            self.delete_car()

    def front_car_collision(self):
        """Μέθοδος που ελέγχει την απόσταση από το προπορευόμενο όχημα και αν αυτή είναι μικρότερη
        από την οριζόμενη τιμή ακινητοποιείται"""
        if self.moving:
            # Εφόσον το αυτοκίνητο κινείται ελέγχει την απόσταση από το προπορευόμενο αυτοκίνητο
            # και αν αυτή είναι κάτω από την οριζόμενη τιμή ακινητοποιείται
            for car in Car.cars_dict[str(self.direction)][self.lane]:
                if self != car and self.direction == car.direction and self.lane == car.lane:
                    if self.direction == 1 and 0 < car.x - self.x < Car.front_car_min_distance:
                        self.moving = False
                        self.speed = (0, 0)
                        self.stopped = car
                        self.root.after(30, self.move_car)
                    elif self.direction == 3 and 0 < self.x - car.x < Car.front_car_min_distance:
                        self.moving = False
                        self.speed = (0, 0)
                        self.stopped = car
                        self.root.after(30, self.move_car)
                    elif self.direction == 2 and 0 < self.y - car.y < Car.front_car_min_distance:
                        self.moving = False
                        self.speed = (0, 0)
                        self.stopped = car
                        self.root.after(30, self.move_car)

    def check_traffic_lights(self):
        if (TrafficLights.tr_lights_dict[str(self.direction)].phase == "red" or
            TrafficLights.tr_lights_dict[str(self.direction)].phase == "orange"):
            self.moving = False
            self.speed = (0, 0)
            self.stopped = TrafficLights.tr_lights_dict[str(self.direction)]
            self.root.after(30, self.move_car)

    def move_car(self):
        """Μέθοδος όπου διαχειρίζεται την κίνηση του κάθε αυτοκινήτου"""
        self.front_car_collision()
        if self.moving:
            # Εφόσον κινείται το αυτοκίνητο, αν είναι εντός των ορίων του καμβά συνεχίζει την κίνησή του
            # αλλιώς διαγράφεται
            if -100 < self.x < 1932 and -100 < self.y < 1180:
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
                self.speed = Car.speed_by_direction[str(self.direction)]
                self.stopped = None
                self.root.after(500, self.move_car)
            elif self.direction == 2 and abs(self.y - self.stopped.y) > 180:
                self.moving = True
                self.speed = Car.speed_by_direction[str(self.direction)]
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
        for i in Car.speed_by_direction.keys():
            images[i] = []
            for x in range(0, Car.num_of_car_images):
                car_img = Image.open(Car.car_image.replace("#", str(x+1)))
                resized_car = car_img.resize((int(car_img.width*Car.orig_img_ratio),
                                              int(car_img.height*Car.orig_img_ratio)))
                rotated_image = resized_car.rotate(90 * (int(i)-1), expand=True)
                images[i].append(ImageTk.PhotoImage(rotated_image))
        return images
