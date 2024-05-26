import math


class Pedestrian:
    """Κλάση Pedestrian για τη δημιουργία των πεζών και τις λειτουργίες τους"""
    def __init__(self, image, direction, params, canvas, window, lights, total_ped_list, ped_dict, cars_dict):
        """Μέθοδος που δέχεται τις παραμέτρους και δημιουργεί ένα καινούριο πεζό"""
        # Λεξικό με τις εικόνες που χρησιμοποιεί ο πεζός
        self.image = image
        # Κατεύθυνση του πεζού
        self.direction = direction
        self.ped_speed = params["ped_speed"]
        direction_speed = {"1": (self.ped_speed, 0), "2": (0, -self.ped_speed), "3": (-self.ped_speed, 0),
                           "4": (0, self.ped_speed)}
        # Ταχύτητα του πεζού, δηλαδή σε πόσα pixel κινείται σε κάθε άξονα σε κάθε μετακίνηση
        self.speed = direction_speed[str(self.direction)]
        self.cur_speed = self.speed
        # Μεταβλητή boolean για το αν ο πεζός κινείται ή είναι σταματημένος
        self.moving = True
        self.lights = lights
        # Λεξικό στο οποίο καταχωρούνται τα αντικείμενα για τα οποία έχει ακινητοποιηθεί
        # ο πεζός
        self.stopped = {"<class 'cars.Car'>": None, "<class 'traffic_lights.PedestrianLights'>": None,
                        "<class 'pedestrians.Pedestrian'>": None}
        # Μεταβλητή που δείχνει σε πιο βήμα βρίσκεται ο πεζός
        self.step = 0
        # Μεταβλητή που δείχνει σε ποιο σημείο της μετακίνησης βρίσκεται ο πεζός
        # ώστε να αλλάξει βήμα
        self.frames = 0
        # Μεταβλητή για τους πεζούς που βρίσκονται σε σβησμένο
        # σηματοδότη πεζών για το αν μπορούν ή όχι να διασχίσουν το δρόμο
        self.leave_on_off = False
        # Η θέση στον άξoνα X
        self.x = params["pos"][str(self.direction)][0]
        # Η θέση στον άξoνα Υ
        self.y = params["pos"][str(self.direction)][1]
        # Ελάχιστη απόσταση από τον προπορευόμενο πεζό
        self.ped_min_dist = params["ped_min_dist"]
        # Εύρος απόστασης που ακινητοποιείται ο πεζός από το φανάρι
        self.dist_to_light = params["dist_to_light"]
        # Αριθμός εικόνων κίνησης για κάθε πεζό
        self.num_of_steps = params["num_of_steps"]
        # Αριθμός μετακινήσεων του πεζού που αφού ολοκληρωθούν αλλάζει βήμα η εικόνα του πεζού
        self.frames_to_next_step = params["frames_to_next_step"]
        # Μεταβλητή του παραθύρου που έχει δημιουργηθεί
        self.root = window
        # Μεταβλητή του καμβά που έχει δημιουργηθεί και πάνω στην οποία θα προσθέτονται
        # τα νέα αντικείμενα
        self.canvas = canvas
        # Δημιουργία αντικειμένου πάνω στον καμβά
        self.pedestrian = self.canvas.create_image(self.x, self.y, image=self.image["st"])
        # Λεξικό με τους ενεργούς πεζούς ανάλογα με την κατεύθυνση που κινούνται
        self.ped_dict = ped_dict
        # Λίστα με τους ενεργούς πεζούς
        self.total_ped_list = total_ped_list
        self.cars_dict = cars_dict
        # Κλήση της μεθόδου με την οποία ελέγχεται η κίνηση του πεζού
        self.move_ped()

    def find_distance(self, entity):
        """Συνάρτηση η οποία δέχεται σαν όρισμα ένα άλλο αντικείμενο και βρίσκει την
        απόσταση από αυτό"""
        return math.sqrt(abs(self.x - entity.x)**2 + abs(self.y - entity.y)**2)

    def stop_movement(self, entity):
        """Μέθοδος η οποία ακινητοποιεί τον πεζό"""
        self.moving = False
        self.cur_speed = (0, 0)
        self.stopped[str(type(entity))] = entity
        self.canvas.itemconfig(self.pedestrian, image=self.image["st"])

    def restart_movement(self, entity_type):
        """Μέθοδος η οποία δέχεται σαν όρισμα τον τύπο του αντικειμένου που σταμάτησε
        τον πεζό και ξεκινάει την κίνησή του"""
        self.moving = True
        self.cur_speed = self.speed
        self.stopped[entity_type] = None

    def front_ped_collision(self):
        """Μέθοδος που ελέγχει την απόσταση από τον προπορευόμενο πεζό και αν αυτή είναι μικρότερη
        από την οριζόμενη τιμή καταχωρεί το αντικείμενο στο λεξικό stopped και επιστρέφει τιμή True"""
        collision = False
        for ped in self.ped_dict[str(self.direction)]:
            if self != ped and self.direction == ped.direction:
                if ((self.direction == 1 and 0 < self.axis_distance(ped) < self.ped_min_dist) or
                        (self.direction == 3 and 0 < self.axis_distance(ped) < self.ped_min_dist) or
                        (self.direction == 2 and 0 < self.axis_distance(ped) < self.ped_min_dist) or
                        (self.direction == 4 and 0 < self.axis_distance(ped) < self.ped_min_dist)):
                    collision = True
                    self.stopped[str(type(ped))] = ped
        return collision

    def check_traffic_lights(self):
        """Μέθοδος που ελέγχει την κατάσταση των φωτεινών σηματοδοτών και αν αυτή δεν επιτρέπει
        την κίνηση του πεζού καταχωρεί τον σηματοδότη στο λεξικό stopped και επιστρέφει τιμή True"""
        stop_to_light = False
        ped_lights = self.lights.ped_lights_dict[str(self.direction)]
        for light in ped_lights:
            if (self.lights.current_mode == "normal" and
                    self.dist_to_light[0] < self.axis_distance(light) < self.dist_to_light[1] and
                    light.phase == "red"):
                stop_to_light = True
                self.stopped[str(type(light))] = light
            elif (self.lights.current_mode == "night" and not self.leave_on_off and
                  self.dist_to_light[0] < self.axis_distance(light) < self.dist_to_light[1]):
                stop_to_light = True
                self.stopped[str(type(light))] = light
        return stop_to_light

    def move_ped(self):
        """Μέθοδος όπου διαχειρίζεται την κίνηση του κάθε πεζού"""
        # εάν κινείται
        if self.moving and self.lights.operation_mode:
            # και εάν ένας από τους παρακάτω ελέγχους επιστρέψει True ο
            # πεζός ακινητοποιείται
            if self.front_ped_collision() or self.check_traffic_lights():
                for i in self.stopped.values():
                    if i:
                        self.stop_movement(i)
            # αλλιώς εάν βρίσκεται εντός των αποδεκτών συντεταγμένων του παραθύρου
            # κινείται
            elif -200 < self.x < 2032 and -200 < self.y < 1280:
                self.canvas.move(self.pedestrian, self.speed[0], self.speed[1])
                self.x += self.speed[0]
                self.y += self.speed[1]
                self.frames += 1
                if self.frames == self.frames_to_next_step:
                    self.step += 1
                    self.frames = 0
                if self.step == self.num_of_steps:
                    self.step = 0
                self.canvas.itemconfig(self.pedestrian, image=self.image[str(self.step)])
        # Εάν ο πεζός δεν κινείται, ελέγχεται ο λόγος για τον οποίο έχει
        # σταματήσει και αν περάσει τους κάτωθι λογικούς ελέγχους ξεκινάει
        # πάλι η κίνησή του
        else:
            for x, y in self.stopped.items():
                if x == "<class 'pedestrians.Pedestrian'>" and y:
                    if self.find_distance(self.stopped[x]) > self.ped_min_dist + 50:
                        self.restart_movement(x)
                if x == "<class 'traffic_lights.PedestrianLights'>" and y:
                    if self.lights.current_mode == "normal" and y.phase == "green":
                        self.restart_movement(x)
                    elif self.lights.current_mode == "night":
                        leave = True
                        for key, car_list_1 in self.cars_dict.items():
                            if int(key) % 2 != self.direction % 2:
                                for car_list_2 in car_list_1:
                                    for i in car_list_2:
                                        if self.find_distance(i) < 600:
                                            leave = False
                        self.leave_on_off = leave
                        self.restart_movement(x)
        self.root.after(30, self.move_ped)

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
