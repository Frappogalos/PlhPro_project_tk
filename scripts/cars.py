import random
from PIL import ImageTk, Image
import math
from traffic_lights import TrafficLights


class Car:
    """Κλάση Car για τη δημιουργία των αυτοκινήτων και τις λειτουργίες τους"""
    # Μεταβλητές κλάσης:
    # Οι θέσεις όπου εμφανίζονται τα αυτοκίνητα όταν δημιουργούνται
    cars_starting_positions = {"1": [(-140, 645), (-140, 570)], "2": [(870, 1130), (960, 1130)],
                               "3": [(1982, 440), (1982, 510)]}
    # Η ταχύτητα με την οποία κινούνται τα οχήματα, δηλαδή πόσα pixel κινείται
    # το κάθε όχημα σε κάθε μετακίνησή του
    speed = 6
    # Η μεταβολή της θέσης του κάθε αυτοκινήτου ανάλογα με την πορεία του
    speed_by_direction = {"1": (speed, 0), "2": (0, -speed), "3": (-speed, 0)}
    # Ποσότητα διαφορετικών εικόνων οχημάτων
    num_of_car_images = 2
    # Ελάχιστη απόσταση από το προπορευόμενο όχημα
    front_car_min_distance = 150
    # Εύρος απόστασης που ακινητοποιείται το όχημα από το φανάρι,
    # δηλαδή ακινητοποιείται εφόσον βρίσκεται σε απόσταση ανάμεσα
    # από 150 και 220 pixel από το φανάρι
    dist_to_light = (150, 220)
    # Σχετική διεύθυνση των εικόνων που χρησιμοποιούνται για τα οχήματα
    car_image = "../images/cars/car_#.png"
    # Ύψος που πρέπει να έχει η εικόνα στο πρόγραμμα
    target_height = 55
    # Μέγιστος αριθμός αυτοκινήτων που μπορούν να υπάρχουν ταυτόχρονα
    cars_limit = 10
    # Λεξικό με τα ενεργά αυτοκίνητα ανάλογα με την κατεύθυνση
    # και τη λορίδα που κινούνται
    cars_dict = {"1": [[], []], "2": [[], []], "3": [[], []]}
    # Λίστα με όλα τα ενεργά οχήματα
    total_car_list = []
    # Μεταβλητή για το εάν το πρόγραμμα λειτουργεί ή
    # βρίσκεται σε παύση
    operation = True

    def __init__(self, image, direction, lane, canvas, window):
        """Μέθοδος που δέχεται τις παραμέτρους και δημιουργεί ένα καινούριο αυτοκίνητο"""
        # Εικόνα που χρησιμοποιεί το αυτοκίνητο
        self.image = image
        # Κατεύθυνση του αυτοκινήτου
        self.direction = direction
        # Λορίδα κυκλοφορίας
        self.lane = lane
        # Ταχύτητα του αυτοκινήτου, δηλαδή σε πόσα pixel κινείται σε κάθε άξονα σε κάθε μετακίνηση
        self.speed = Car.speed_by_direction[str(self.direction)]
        # Μεταβλητή boolean για το αν το αυτοκίνητο κινείται ή είναι σταματημένο
        self.moving = True
        # Μεταβλητή για τα αυτοκίνητα που βρίσκονται σε παλλόμενο πορτοκαλί
        # σηματοδότη για το αν μπορούν ή όχι να διασχίσουν το δρόμο
        self.leave_on_orange = False
        # Λεξικό στο οποίο καταχωρούνται τα αντικείμενα για τα οποία έχει ακινητοποιηθεί
        # το αυτοκίνητο
        self.stopped = {"<class 'cars.Car'>": None, "<class 'traffic_lights.TrafficLights'>": None,
                        "<class 'pedestrians.Pedestrian'>": None}
        # Η θέση στον άξoνα X
        self.x = Car.cars_starting_positions[str(self.direction)][self.lane][0]
        # Η θέση στον άξoνα Υ
        self.y = Car.cars_starting_positions[str(self.direction)][self.lane][1]
        # Μεταβλητή του παραθύρου που έχει δημιουργηθεί
        self.root = window
        # Μεταβλητή του καμβά που έχει δημιουργηθεί και πάνω στην οποία θα προσθέτονται
        # τα νέα αντικείμενα
        self.canvas = canvas
        # Δημιουργία αντικειμένου πάνω στον καμβά
        self.car = self.canvas.create_image(self.x, self.y, image=self.image)
        #  Καταχώριση του αντικειμένου στο λεξικό ανάλογα με την κατεύθυνσή του
        #  και τη λορίδα κυκλοφορίας
        Car.cars_dict[str(self.direction)][self.lane].append(self)
        # Καταχώριση στη λίστα με όλα τα αυτοκίνητα
        Car.total_car_list.append(self)
        # Κλήση της μεθόδου με την οποία ελέγχεται η κίνηση του αυτοκινήτου
        self.move_car()

    def front_car_collision(self):
        """Μέθοδος που ελέγχει την απόσταση από το προπορευόμενο όχημα και αν αυτή είναι μικρότερη
        από την οριζόμενη τιμή καταχωρεί το αντικείμενο στο λεξικό stopped και επιστρέφει τιμή True"""
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
        """Μέθοδος που ελέγχει την κατάσταση των φωτεινών σηματοδοτών και αν αυτή δεν επιτρέπει
        την κίνηση του αυτοκινήτου καταχωρεί τον σηματοδότη στο λεξικό stopped και επιστρέφει τιμή True"""
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
        """Μέθοδος η οποία ακινητοποιεί το όχημα"""
        self.moving = False
        self.speed = (0, 0)
        self.stopped[str(type(entity))] = entity

    def move_car(self):
        """Μέθοδος όπου διαχειρίζεται την κίνηση του κάθε αυτοκινήτου, δηλαδή αν πρέπει
        να σταματήσει η κίνησή του ή να ξεκινήσει εκ νέου"""
        # Εάν το αυτοκίνητο είναι στη συνολική λίστα,
        if self in Car.total_car_list:
            # εάν κινείται,
            if self.moving and Car.operation:
                # και εάν ένας από τους παρακάτω ελέγχους επιστρέψει True το
                # αυτοκίνητο ακινητοποιείται
                if self.front_car_collision() or self.check_traffic_lights():
                    for i in self.stopped.values():
                        if i:
                            self.stop_car(i)
                # αλλιώς εάν βρίσκεται εντός των αποδεκτών συντεταγμένων του παραθύρου
                # κινείται
                elif -200 < self.x < 2000 and -200 < self.y < 1230:
                    self.canvas.move(self.car, self.speed[0], self.speed[1])
                    self.x += self.speed[0]
                    self.y += self.speed[1]
                # αλλιώς καταστρέφεται
                else:
                    self.delete_car()
            # Εάν το αυτοκίνητο δεν κινείται ελέγχεται ο λόγος για τον οποίο έχει
            # σταματήσει και αν περάσει τους κάτωθι λογικούς ελέγχους ξεκινάει
            # πάλι η κίνησή του
            else:
                for x, y in self.stopped.items():
                    if x == "<class 'cars.Car'>" and y:
                        if self.find_distance(self.stopped[x]) > Car.front_car_min_distance + 50:
                            self.restart_movement(x)
                    if x == "<class 'traffic_lights.TrafficLights'>" and y:
                        if TrafficLights.current_mode == "normal" and y.phase == "green":
                            self.restart_movement(x)
                        elif TrafficLights.current_mode == "night" and self.direction != 2:
                            self.restart_movement(x)
                        elif TrafficLights.current_mode == "night":
                            leave = True
                            for key, car_list_1 in Car.cars_dict.items():
                                if int(key) % 2 != self.direction % 2:
                                    for car_list_2 in car_list_1:
                                        for i in car_list_2:
                                            if self.find_distance(i) < 400+(abs(i.y-self.y)/2):
                                                leave = False
                            self.leave_on_orange = leave
                            self.restart_movement(x)
            self.root.after(30, self.move_car)

    def restart_movement(self, entity_type):
        """Μέθοδος η οποία δέχεται σαν όρισμα τον τύπο του αντικειμένου που σταμάτησε
        το όχημα και ξεκινάει την κίνησή του"""
        self.moving = True
        self.speed = Car.speed_by_direction[str(self.direction)]
        self.stopped[entity_type] = None

    def delete_car(self):
        """Μέθοδος η οποία διαγράφει το αυτοκίνητο εφόσον εξέλθει των ορίων του καμβά"""
        Car.total_car_list.remove(self)
        Car.cars_dict[str(self.direction)][self.lane].remove(self)
        self.canvas.delete(self.car)

    def find_distance(self, entity):
        """Συνάρτηση η οποία δέχεται σαν όρισμα ένα άλλο αντικείμενο και βρίσκει την
        απόσταση από αυτό"""
        return math.sqrt(abs(self.x - entity.x)**2 + abs(self.y - entity.y)**2)

    def axis_distance(self, entity):
        """Συνάρτηση η οποία δέχεται σαν όρισμα ένα άλλο αντικείμενο και βρίσκει την
        απόσταση από αυτό πάνω στον άξονα στον οποίο κινείται"""
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
    def car_creator(cls, car_images, canvas, root):
        """Μέθοδος η οποία δημιουργεί συνεχώς ένα καινούριο αυτοκίνητο μετά το πέρας ενός
           συγκεκριμένου χρονικού διαστήματος"""
        if Car.operation:
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
        root.after(4000, Car.car_creator, car_images, canvas, root)

    @classmethod
    def create_images(cls):
        """Δημιουργία λεξικού με τις εικόνες των αυτοκινήτων ανάλογα με την κατεύθυνση
        του κάθε οχήματος"""
        images = {}
        for i in Car.speed_by_direction.keys():
            images[i] = []
            for x in range(0, Car.num_of_car_images):
                car_img = Image.open(Car.car_image.replace("#", str(x+1)))
                resized_car = car_img.resize((int(car_img.width*(Car.target_height/car_img.height)), Car.target_height))
                rotated_image = resized_car.rotate(90 * (int(i)-1), expand=True)
                images[i].append(ImageTk.PhotoImage(rotated_image))
        return images
