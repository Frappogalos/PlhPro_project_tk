import tkinter as tk
import functools
import random
from PIL import ImageTk, Image
import math
from traffic_lights import TrafficLights


class Car:
    """Κλάση Car για τη δημιουργία των αυτοκινήτων και τις λειτουργίες τους"""
    # Οι θέσεις όπου εμφανίζονται τα αυτοκίνητα όταν δημιουργούνται
    cars_starting_positions = {"1": [(-140, 645), (-140, 570)], "2": [(870, 1130), (960, 1130)],
                               "3": [(1982, 440), (1982, 510)]}
    speed = 6
    speed_by_direction = {"1": (speed, 0), "2": (0, -speed), "3": (-speed, 0)}
    num_of_car_images = 2
    front_car_min_distance = 150
    dist_to_light = (150, 220)
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
        self.leave_on_orange = False
        self.stopped = {"<class 'cars.Car'>": None, "<class 'traffic_lights.TrafficLights'>": None,
                        "<class 'pedestrians.Pedestrian'>": None}
        self.x = Car.cars_starting_positions[str(self.direction)][self.lane][0]
        self.y = Car.cars_starting_positions[str(self.direction)][self.lane][1]
        self.root = window
        self.canvas = canvas
        self.car = self.canvas.create_image(self.x, self.y, image=self.image)
        Car.cars_dict[str(self.direction)][self.lane].append(self)
        Car.total_car_list.append(self)
        self.move_car()

    def front_car_collision(self):
        """Μέθοδος που ελέγχει την απόσταση από το προπορευόμενο όχημα και αν αυτή είναι μικρότερη
        από την οριζόμενη τιμή ακινητοποιείται"""
        collision = False
        for car in Car.cars_dict[str(self.direction)][self.lane]:
            if self != car and self.direction == car.direction and self.lane == car.lane:
                if ((self.direction == 1 and 0 < self.axis_distance(car) < Car.front_car_min_distance)
                        or (self.direction == 3 and 0 < self.axis_distance(car) < Car.front_car_min_distance)
                        or (self.direction == 2 and 0 < self.axis_distance(car) < Car.front_car_min_distance)):
                    collision = True
                    self.stopped[str(type(car))] = car
        return collision

    def check_traffic_lights(self):
        stop_to_light = False
        tr_light = TrafficLights.tr_lights_dict[str(self.direction)]
        if (TrafficLights.current_mode == "normal" and
                Car.dist_to_light[0] < self.axis_distance(tr_light) < Car.dist_to_light[1] and
                (tr_light.phase == "red" or tr_light.phase == "orange")):
            stop_to_light = True
            self.stopped[str(type(tr_light))] = tr_light
        elif (TrafficLights.current_mode == "night" and self.direction == 2 and not self.leave_on_orange and
              Car.dist_to_light[0] < self.axis_distance(tr_light) < Car.dist_to_light[1]):
            stop_to_light = True
            self.stopped[str(type(tr_light))] = tr_light
        return stop_to_light

    def stop_car(self, entity):
        self.moving = False
        self.speed = (0, 0)
        self.stopped[str(type(entity))] = entity

    def move_car(self):
        """Μέθοδος όπου διαχειρίζεται την κίνηση του κάθε αυτοκινήτου"""
        if self.moving:
            if self.front_car_collision() or self.check_traffic_lights():
                for i in self.stopped.values():
                    if i:
                        self.stop_car(i)
            elif -200 < self.x < 2000 and -200 < self.y < 1230:
                self.canvas.move(self.car, self.speed[0], self.speed[1])
                self.x += self.speed[0]
                self.y += self.speed[1]
            else:
                self.delete_car()
        else:
            for x, y in self.stopped.items():
                if x == "<class 'cars.Car'>" and y:
                    if self.find_distance(self.stopped[str(type(self))]) > Car.front_car_min_distance + 50:
                        self.restart_movement(str(type(y)))
                if x == "<class 'traffic_lights.TrafficLights'>" and y:
                    if TrafficLights.current_mode == "normal" and (y.phase == "green" or y.phase == "off"):
                        self.restart_movement(str(type(y)))
                    elif TrafficLights.current_mode == "night" and self.direction != 2:
                        self.restart_movement(str(type(y)))
                    elif TrafficLights.current_mode == "night":
                        leave = True
                        for key, car_list_1 in Car.cars_dict.items():
                            if int(key) % 2 != self.direction % 2:
                                for car_list_2 in car_list_1:
                                    for i in car_list_2:
                                        if self.find_distance(i) < 400+(abs(i.y-self.y)/2):
                                            leave = False
                        self.leave_on_orange = leave
                        self.restart_movement(str(type(y)))
        self.root.after(30, self.move_car)

    def restart_movement(self, entity_type):
        self.moving = True
        self.speed = Car.speed_by_direction[str(self.direction)]
        self.stopped[entity_type] = None

    def delete_car(self):
        """Μέθοδος η οποία διαγράφει το αυτοκίνητο εφόσον εξέλθει των ορίων του καμβά"""
        self.moving = False
        Car.total_car_list.remove(self)
        Car.cars_dict[str(self.direction)][self.lane].remove(self)
        self.canvas.delete(self.car)

    def find_distance(self, entity):
        return math.sqrt(abs(self.x - entity.x)**2 + abs(self.y - entity.y)**2)

    def axis_distance(self, entity):
        dist = 0
        if self.direction == 1:
            dist = entity.x - self.x
        elif self.direction == 2:
            dist = self.y - entity.y
        elif self.direction == 3:
            dist = self.x - entity.x
        elif self.direction == 4:
            dist = entity.y - self.y
        return dist

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
