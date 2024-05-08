import tkinter as tk
import functools
import random
import math
from PIL import ImageTk, Image


class Pedestrian:
    """Κλάση Pedestrian για τη δημιουργία των πεζών και τις λειτουργίες τους"""
    # Οι θέσεις όπου εμφανίζονται οι πεζοί όταν δημιουργούνται
    pedestrian_starting_positions = {"1": (-40, 360), "2": (780, 1130),
                                     "3": (1882, 720), "4": (1060, -40)}
    speed = 3
    speed_by_direction = {"1": (speed, 0), "2": (0, -speed), "3": (-speed, 0), "4": (0, speed)}
    num_of_person_images = 2
    num_of_steps = 2
    distance_ped = 50
    frames_to_next_step = 9
    ped_img_file = f"../images/pedestrians/Person_#_$.png"
    orig_img_ratio = 0.3
    # Μέγιστος αριθμός πεζών που μπορούν να υπάρχουν ταυτόχρονα
    pedestrian_limit = 10
    # Λίστα με τους ενεργούς πεζούς
    ped_dict = {"1": [], "2": [], "3": [], "4": []}
    total_ped_list = []

    def __init__(self, image, direction, canvas, window):
        """Μέθοδος που δέχεται τις παραμέτρους και δημιουργεί ένα καινούριο αυτοκίνητο"""
        self.image = image
        self.direction = direction
        self.speed = Pedestrian.speed_by_direction[str(self.direction)]
        self.moving = True
        self.stopped = {"<class 'cars.Car'>": None, "<class 'traffic_lights.TrafficLights'>": None,
                        "<class 'pedestrians.Pedestrian'>": None}
        self.step = 0
        self.frames = 0
        self.x = Pedestrian.pedestrian_starting_positions[str(self.direction)][0]
        self.y = Pedestrian.pedestrian_starting_positions[str(self.direction)][1]
        self.root = window
        self.canvas = canvas
        self.pedestrian = self.canvas.create_image(self.x, self.y, image=self.image["st"])
        Pedestrian.ped_dict[str(self.direction)].append(self)
        Pedestrian.total_ped_list.append(self)
        self.move_ped()

    def find_distance(self, entity):
        return math.sqrt(abs(self.x - entity.x)**2 + abs(self.y - entity.y)**2)

    def stop_ped(self, entity):
        self.moving = False
        self.speed = (0, 0)
        self.stopped[str(type(entity))] = entity
        self.canvas.itemconfig(self.pedestrian, image=self.image["st"])

    def restart_movement(self, entity_type):
        self.moving = True
        self.speed = Pedestrian.speed_by_direction[str(self.direction)]
        self.stopped[entity_type] = None

    def move_ped(self):
        """Μέθοδος όπου διαχειρίζεται την κίνηση του κάθε πεζού"""
        # TODO moving and collision logic for traffic lights and cars
        if self.moving:
            # Εφόσον ο πεζός κινείται ελέγχει την απόσταση από τον προπορευόμενο πεζό
            # και αν αυτή είναι κάτω από την οριζόμενη τιμή ακινητοποιείται
            for ped in Pedestrian.ped_dict[str(self.direction)]:
                if self != ped and self.direction == ped.direction:
                    if (self.direction == 1 and 0 < ped.x - self.x < Pedestrian.distance_ped or
                            self.direction == 3 and 0 < self.x - ped.x < Pedestrian.distance_ped or
                            self.direction == 2 and 0 < self.y - ped.y < Pedestrian.distance_ped or
                            self.direction == 4 and 0 < ped.y - self.y < Pedestrian.distance_ped):
                        self.stop_ped(ped)
        if self.moving:
            # Εφόσον κινείται ο πεζός αν είναι εντός των ορίων του καμβά συνεχίζει την κίνησή του
            # αλλιώς διαγράφεται
            if -100 < self.x < 1932 and -100 < self.y < 1180:
                self.canvas.move(self.pedestrian, self.speed[0], self.speed[1])
                self.x += self.speed[0]
                self.y += self.speed[1]
                self.frames += 1
                if self.frames == Pedestrian.frames_to_next_step:
                    self.step += 1
                    self.frames = 0
                if self.step == Pedestrian.num_of_steps:
                    self.step = 0
                self.canvas.itemconfig(self.pedestrian, image=self.image[str(self.step)])
                self.root.after(30, self.move_ped)
            else:
                self.delete_ped()
        else:
            for x, y in self.stopped.items():
                if x == "<class 'pedestrians.Pedestrian'>" and y:
                    if self.find_distance(self.stopped[x]) > Pedestrian.distance_ped + 50:
                        self.restart_movement(x)
        self.root.after(30, self.move_ped)

    def delete_ped(self):
        """Μέθοδος η οποία διαγράφει τον πεζό εφόσον εξέλθει των ορίων του καμβά"""
        self.canvas.delete(self.pedestrian)
        Pedestrian.ped_dict[str(self.direction)].remove(self)
        Pedestrian.total_ped_list.remove(self)

    @classmethod
    def pedestrian_creator(cls, ped_images, canvas, root):
        """Μέθοδος η οποία δημιουργεί συνεχώς ένα καινούριο αυτοκίνητο μετά το πέρας ενός
           συγκεκριμένου χρονικού διαστήματος"""
        if len(Pedestrian.total_ped_list) < Pedestrian.pedestrian_limit:
            rand_num = random.randint(1, 100)
            if rand_num <= 35:
                direction = 1
            elif rand_num <= 50:
                direction = 2
            elif rand_num <= 75:
                direction = 3
            else:
                direction = 4
            ped_image = random.choice(list(ped_images[str(direction)].values()))
            Pedestrian(image=ped_image, direction=direction, canvas=canvas, window=root)
        root.after(4000, functools.partial(Pedestrian.pedestrian_creator, ped_images, canvas, root))

    @classmethod
    def create_images(cls):
        # Δημιουργία λεξικού με τις φωτογραφίες των πεζών ανάλογα με την κατεύθυνση
        # του κάθε ενός
        images = {}
        for x in Pedestrian.speed_by_direction.keys():
            ped_images = {}
            for i in range(0, Pedestrian.num_of_person_images):
                ped_images[str(i + 1)] = {}
                for y in range(0, Pedestrian.num_of_steps):
                    pedestrian_img = Image.open(Pedestrian.ped_img_file.replace("#", str(i)).replace("$", str(y)))
                    resized_img = pedestrian_img.resize((int(pedestrian_img.width*Pedestrian.orig_img_ratio),
                                                         int(pedestrian_img.height*Pedestrian.orig_img_ratio)))
                    rotated_img = resized_img.rotate(90 * (int(x)-1), expand=True)
                    ped_images[str(i + 1)][str(y)] = ImageTk.PhotoImage(rotated_img)
                pedestrian_img = Image.open(Pedestrian.ped_img_file.replace("#", str(i)).replace("$", "st"))
                resized_img = pedestrian_img.resize((int(pedestrian_img.width * Pedestrian.orig_img_ratio),
                                                     int(pedestrian_img.height * Pedestrian.orig_img_ratio)))
                rotated_img = resized_img.rotate(90 * (int(x) - 1), expand=True)
                ped_images[str(i + 1)]["st"] = ImageTk.PhotoImage(rotated_img)
            images[x] = ped_images
        return images
