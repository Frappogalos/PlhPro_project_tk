import tkinter as tk
import functools
import random
import math
# Οι θέσεις όπου εμφανίζονται οι πεζοί όταν δημιουργούνται
PEDESTRIAN_STARTING_POSITIONS = {"1": (-40, 350), "2": (700, 950),
                                 "3": (1550, 600), "4": (800, -40)}
SPEED = 6


class Pedestrian:
    """Κλάση Pedestrian για τη δημιουργία των πεζών και τις λειτουργίες τους"""
    # Μέγιστος αριθμός πεζών που μπορούν να υπάρχουν ταυτόχρονα
    pedestrian_limit = 10
    # Λίστα με τους ενεργούς πεζούς
    ped_dict = {"1": [], "2": [], "3": [], "4": []}
    total_ped_list = []

    def __init__(self, image, direction, canvas, window):
        """Μέθοδος που δέχεται τις παραμέτρους και δημιουργεί ένα καινούριο αυτοκίνητο"""
        self.image = image["st"]
        self.direction = direction
        self.speed = self.find_speed()
        self.moving = True
        self.stopped = None
        self.x = PEDESTRIAN_STARTING_POSITIONS[str(self.direction)][0]
        self.y = PEDESTRIAN_STARTING_POSITIONS[str(self.direction)][1]
        self.root = window
        self.canvas = canvas
        self.pedestrian = self.canvas.create_image(self.x, self.y, image=self.image)
        Pedestrian.ped_dict[str(self.direction)].append(self)
        Pedestrian.total_ped_list.append(self)
        self.move_ped()
        if self.spawn_collision():
            self.delete_ped()

    def find_speed(self):
        """Μέθοδος όπου ανάλογα με την κατεύθυνση του αυτοκινήτου επιστρέφει την ανάλογη ταχύτητα"""
        if self.direction == 1:
            return SPEED, 0
        elif self.direction == 2:
            return 0, -SPEED
        elif self.direction == 3:
            return -SPEED, 0
        else:
            return 0, SPEED

    def move_ped(self):
        """Μέθοδος όπου διαχειρίζεται την κίνηση του κάθε πεζού"""
        if self.moving:
            # Εφόσον ο πεζός κινείται ελέγχει την απόσταση από τον προπορευόμενο πεζό
            # και αν αυτή είναι κάτω από την οριζόμενη τιμή ακινητοποιείται
            for ped in Pedestrian.ped_dict[str(self.direction)]:
                if self != ped and self.direction == ped.direction:
                    if self.direction == 1 and 0 < ped.x - self.x < 120:
                        self.moving = False
                        self.speed = (0, 0)
                        self.stopped = ped
                        self.root.after(30, self.move_ped)
                    elif self.direction == 3 and 0 < self.x - ped.x < 120:
                        self.moving = False
                        self.speed = (0, 0)
                        self.stopped = ped
                        self.root.after(30, self.move_ped)
                    elif self.direction == 2 and 0 < self.y - ped.y < 120:
                        self.moving = False
                        self.speed = (0, 0)
                        self.stopped = ped
                        self.root.after(30, self.move_ped)
                    elif self.direction == 4 and 0 < ped.y - self.y < 120:
                        self.moving = False
                        self.speed = (0, 0)
                        self.stopped = ped
                        self.root.after(30, self.move_ped)
        if self.moving:
            # Εφόσον κινείται ο πεζός αν είναι εντός των ορίων του καμβά συνεχίζει την κίνησή του
            # αλλιώς διαγράφεται
            if -100 < self.x < 1600 and -100 < self.y < 1000:
                self.canvas.move(self.pedestrian, self.speed[0], self.speed[1])
                self.x += self.speed[0]
                self.y += self.speed[1]
                self.root.after(30, self.move_ped)
            else:
                self.delete_ped()
        else:
            # Εφόσον είναι σταματημένος ο πεζός, αν μεγαλώσει η απόσταση από τον πεζό για το
            # οποίο σταμάτησε ξεκινάει πάλι να κινείται
            if (self.direction == 1 or self.direction == 3) and abs(self.x - self.stopped.x) > 180:
                self.moving = True
                self.speed = self.find_speed()
                self.stopped = None
                self.root.after(500, self.move_ped)
            elif self.direction == 2 and abs(self.y - self.stopped.y) > 180:
                self.moving = True
                self.speed = self.find_speed()
                self.stopped = None
                self.root.after(500, self.move_ped)

    def delete_ped(self):
        """Μέθοδος η οποία διαγράφει τον πεζό εφόσον εξέλθει των ορίων του καμβά"""
        self.canvas.delete(self.pedestrian)
        Pedestrian.ped_dict[str(self.direction)].remove(self)
        Pedestrian.total_ped_list.remove(self)

    def spawn_collision(self):
        """Μέθοδος η οποία ελέγχει αν ο πεζός που θα δημιουργηθεί θα συγκρουσθεί με ήδη
        υπάρχον πεζό"""
        for ped in Pedestrian.ped_dict[str(self.direction)]:
            if ped != self and math.sqrt(abs(self.x - ped.x)**2 + abs(self.y - ped.y)**2) < 81:
                return True
        return False

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