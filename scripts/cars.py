import math


class Car:
    """Κλάση Car για τη δημιουργία των αυτοκινήτων και τις λειτουργίες τους"""

    def __init__(self, image, direction, lane, params, canvas, window, lights, total_car_list, cars_dict):
        """Μέθοδος που δέχεται τις παραμέτρους και δημιουργεί ένα καινούριο αυτοκίνητο"""
        # Εικόνα που χρησιμοποιεί το αυτοκίνητο
        self.image = image
        # Κατεύθυνση του αυτοκινήτου
        self.direction = direction
        # Λορίδα κυκλοφορίας
        self.lane = lane
        self.lights = lights
        # Η μεταβολή της θέσης του κάθε αυτοκινήτου ανάλογα με την πορεία του
        self.speed = params["direction_speed"][str(self.direction)]
        self.cur_speed = self.speed
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
        self.x = params["pos"][str(self.direction)][self.lane][0]
        # Η θέση στον άξoνα Υ
        self.y = params["pos"][str(self.direction)][self.lane][1]
        # Ελάχιστη απόσταση από το προπορευόμενο όχημα
        self.car_min_dist = params["car_min_dist"]
        # Εύρος απόστασης που ακινητοποιείται το όχημα από το φανάρι,
        self.dist_to_light = params["dist_to_light"]
        # Μεταβλητή του παραθύρου που έχει δημιουργηθεί
        self.root = window
        # Μεταβλητή του καμβά που έχει δημιουργηθεί και πάνω στην οποία θα προσθέτονται
        # τα νέα αντικείμενα
        self.canvas = canvas
        # Δημιουργία αντικειμένου πάνω στον καμβά
        self.car = self.canvas.create_image(self.x, self.y, image=self.image)
        self.total_car_list = total_car_list
        self.cars_dict = cars_dict
        # Κλήση της μεθόδου με την οποία ελέγχεται η κίνηση του αυτοκινήτου
        self.move_car()

    def front_car_collision(self):
        """Μέθοδος που ελέγχει την απόσταση από το προπορευόμενο όχημα και αν αυτή είναι μικρότερη
        από την οριζόμενη τιμή καταχωρεί το αντικείμενο στο λεξικό stopped και επιστρέφει τιμή True"""
        collision = False
        for car in self.cars_dict[str(self.direction)][self.lane]:
            if self != car and self.direction == car.direction and self.lane == car.lane:
                if ((self.direction == 1 and 0 < self.axis_distance(car) < self.car_min_dist)
                        or (self.direction == 3 and 0 < self.axis_distance(car) < self.car_min_dist)
                        or (self.direction == 2 and 0 < self.axis_distance(car) < self.car_min_dist)):
                    collision = True
                    self.stopped[str(type(car))] = car
        return collision

    def check_traffic_lights(self):
        """Μέθοδος που ελέγχει την κατάσταση των φωτεινών σηματοδοτών και αν αυτή δεν επιτρέπει
        την κίνηση του αυτοκινήτου καταχωρεί τον σηματοδότη στο λεξικό stopped και επιστρέφει τιμή True"""
        stop_to_light = False
        tr_light = self.lights.tr_lights_dict[str(self.direction)]
        if (self.lights.current_mode == "normal" and
                self.dist_to_light[0] < self.axis_distance(tr_light) < self.dist_to_light[1] and
                (tr_light.phase == "red" or tr_light.phase == "orange")):
            stop_to_light = True
            self.stopped[str(type(tr_light))] = tr_light
        elif (self.lights.current_mode == "night" and self.direction == 2 and not self.leave_on_orange and
              self.dist_to_light[0] < self.axis_distance(tr_light) < self.dist_to_light[1]):
            stop_to_light = True
            self.stopped[str(type(tr_light))] = tr_light
        return stop_to_light

    def stop_car(self, entity):
        """Μέθοδος η οποία ακινητοποιεί το όχημα"""
        self.moving = False
        self.cur_speed = (0, 0)
        self.stopped[str(type(entity))] = entity

    def move_car(self):
        """Μέθοδος όπου διαχειρίζεται την κίνηση του κάθε αυτοκινήτου, δηλαδή αν πρέπει
        να σταματήσει η κίνησή του ή να ξεκινήσει εκ νέου"""
        # εάν κινείται,
        if self.moving and self.lights.operation_mode:
            # και εάν ένας από τους παρακάτω ελέγχους επιστρέψει True το
            # αυτοκίνητο ακινητοποιείται
            if self.front_car_collision() or self.check_traffic_lights():
                for i in self.stopped.values():
                    if i:
                        self.stop_car(i)
            # αλλιώς εάν βρίσκεται εντός των αποδεκτών συντεταγμένων του παραθύρου
            # κινείται
            elif -220 < self.x < 2200 and -220 < self.y < 1350:
                self.canvas.move(self.car, self.cur_speed[0], self.cur_speed[1])
                self.x += self.cur_speed[0]
                self.y += self.cur_speed[1]
        # Εάν το αυτοκίνητο δεν κινείται ελέγχεται ο λόγος για τον οποίο έχει
        # σταματήσει και αν περάσει τους κάτωθι λογικούς ελέγχους ξεκινάει
        # πάλι η κίνησή του
        else:
            for x, y in self.stopped.items():
                if x == "<class 'cars.Car'>" and y:
                    if self.find_distance(self.stopped[x]) > self.car_min_dist + 50:
                        self.restart_movement(x)
                if x == "<class 'traffic_lights.TrafficLights'>" and y:
                    if self.lights.current_mode == "normal" and y.phase == "green":
                        self.restart_movement(x)
                    elif self.lights.current_mode == "night" and self.direction != 2:
                        self.restart_movement(x)
                    elif self.lights.current_mode == "night":
                        leave = True
                        for key, car_list_1 in self.cars_dict.items():
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
        self.cur_speed = self.speed
        self.stopped[entity_type] = None

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
