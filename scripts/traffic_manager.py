from cars import Car
from pedestrians import Pedestrian
from PIL import Image, ImageTk
import random


class TrafficManager:
    """Κλάση που δημιουργεί και διαγράφει τα αυτοκίνητα και τους πεζούς"""
    def __init__(self, car_params, ped_params, canvas, root, lights):
        # Μεταβλητή του καμβά που έχει δημιουργηθεί και πάνω στην οποία θα προσθέτονται
        # τα νέα αντικείμενα
        self.canvas = canvas
        # Μεταβλητή του παραθύρου που έχει δημιουργηθεί
        self.root = root
        # Μεταβλητή που αποθηκεύεται ο χειριστής των φαναριών
        self.lights = lights
        # Οι παράμετροι λειτουργίας των αυτοκινήτων
        self.car_params = car_params
        # Οι θέσεις όπου εμφανίζονται τα αυτοκίνητα όταν δημιουργούνται
        self.car_pos = car_params["pos"]
        # Ποσότητα διαφορετικών εικόνων οχημάτων
        self.distinct_cars = car_params["distinct_cars"]
        # Σχετική διεύθυνση των εικόνων που χρησιμοποιούνται για τα οχήματα
        self.car_img = car_params["img"]
        # Ύψος που πρέπει να έχει η εικόνα στο πρόγραμμα
        self.car_height = car_params["height"]
        # Μέγιστος αριθμός αυτοκινήτων που μπορούν να υπάρχουν ταυτόχρονα
        self.car_limit = car_params["car_limit"]
        self.ped_params = ped_params
        # Οι θέσεις όπου εμφανίζονται οι πεζοί όταν δημιουργούνται
        self.ped_pos = ped_params["pos"]
        # Ποσότητα διαφορετικών εικόνων πεζών
        self.distinct_peds = ped_params["distinct_peds"]
        # Αριθμός εικόνων κίνησης για κάθε πεζό
        self.num_of_steps = ped_params["num_of_steps"]
        # Σχετική διεύθυνση των εικόνων που χρησιμοποιούνται για τους πεζούς
        self.ped_img = ped_params["img"]
        # Ύψος που πρέπει να έχει η εικόνα στο πρόγραμμα
        self.ped_height = ped_params["height"]
        # Μέγιστος αριθμός πεζών που μπορούν να υπάρχουν ταυτόχρονα
        self.pedestrian_limit = ped_params["pedestrian_limit"]
        # Λεξικό με τα ενεργά αυτοκίνητα ανάλογα με την κατεύθυνση
        # και τη λορίδα που κινούνται
        self.cars_dict = {"1": [[], []], "2": [[], []], "3": [[], []]}
        # Λίστα με όλα τα ενεργά οχήματα
        self.total_car_list = []
        # Λεξικό με τους ενεργούς πεζούς ανάλογα με την κατεύθυνση που κινούνται
        self.ped_dict = {"1": [], "2": [], "3": [], "4": []}
        # Λίστα με τους ενεργούς πεζούς
        self.total_ped_list = []
        # Μεταβλητή στην οποία αποθηκεύονται οι εικόνες που θα χρησιμοποιηθούν
        # από το πρόγραμμα για τη δημιουργία των αυτοκινήτων
        self.car_images = self.create_car_images()
        # Κλήση της μεθόδου που δημιουργεί συνεχώς αυτοκίνητα
        self.car_creator()
        # Κλήση της μεθόδου που διαγράφει τα αυτοκίνητα που βγαίνουν από τα
        # όρια του παραθύρου
        self.delete_car()
        # Μεταβλητή στην οποία αποθηκεύονται οι εικόνες που θα χρησιμοποιηθούν
        # από το πρόγραμμα για τη δημιουργία των πεζών
        self.ped_images = self.create_ped_images()
        # Κλήση της μεθόδου που δημιουργεί συνεχώς πεζούς
        self.pedestrian_creator()
        # Κλήση της μεθόδου που διαγράφει τους πεζούς που βγαίνουν από τα
        # όρια του παραθύρου
        self.delete_ped()

    def create_car_images(self):
        """Συνάρτηση που δημιουργεί λεξικό με τις εικόνες των αυτοκινήτων ανά κατεύθυνση"""
        images = {}
        for i in self.car_pos.keys():
            images[i] = []
            for x in range(0, self.distinct_cars):
                car_image = Image.open(self.car_img.replace("#", str(x + 1)))
                resized_car = car_image.resize(
                    (int(car_image.width * (self.car_height / car_image.height)), self.car_height))
                rotated_image = resized_car.rotate(90 * (int(i) - 1), expand=True)
                images[i].append(ImageTk.PhotoImage(rotated_image))
        return images

    def car_creator(self):
        """Μέθοδος η οποία δημιουργεί συνεχώς ένα καινούριο αυτοκίνητο μετά το πέρας ενός
           συγκεκριμένου χρονικού διαστήματος"""
        if self.lights.operation_mode:
            if len(self.total_car_list) < self.car_limit:
                rand_num = random.randint(1, 100)
                if rand_num <= 40:
                    direction = 1
                elif rand_num <= 60:
                    direction = 2
                else:
                    direction = 3
                lane = random.choice([0, 1])
                car_image = random.choice(self.car_images[str(direction)])
                new_car = Car(image=car_image, direction=direction, lane=lane, params=self.car_params,
                              canvas=self.canvas, window=self.root, lights=self.lights,
                              total_car_list=self.total_car_list, cars_dict=self.cars_dict)
                #  Καταχώριση του αντικειμένου στο λεξικό ανάλογα με την κατεύθυνσή του
                #  και τη λορίδα κυκλοφορίας
                self.cars_dict[str(new_car.direction)][new_car.lane].append(new_car)
                # Καταχώριση στη λίστα με όλα τα αυτοκίνητα
                self.total_car_list.append(new_car)
        self.root.after(4000, self.car_creator)

    def delete_car(self):
        """Μέθοδος η οποία καλείται συνεχώς και διαγράφει τα αυτοκίνητα
        που έχουν εξέλθει από τα όρια του παραθύρου"""
        for car in self.total_car_list:
            if car.x < -140 or car.x > 1982 or car.y < -100 or car.y > 1130:
                self.total_car_list.remove(car)
                self.cars_dict[str(car.direction)][car.lane].remove(car)
                self.canvas.delete(car.car)
                del car
        self.root.after(100, self.delete_car)

    def create_ped_images(self):
        """Συνάρτηση που δημιουργεί λεξικό με τις εικόνες των πεζών ανά κατεύθυνση"""
        images = {}
        for x in self.ped_pos.keys():
            ped_images = {}
            for i in range(0, self.distinct_peds):
                ped_images[str(i + 1)] = {}
                for y in range(0, self.num_of_steps):
                    pedestrian_img = Image.open(self.ped_img.replace("#", str(i)).replace("$", str(y)))
                    resized_img = pedestrian_img.resize(
                        (int(pedestrian_img.width * (self.ped_height / pedestrian_img.height)), self.ped_height))
                    rotated_img = resized_img.rotate(90 * (int(x) - 1), expand=True)
                    ped_images[str(i + 1)][str(y)] = ImageTk.PhotoImage(rotated_img)
                pedestrian_img = Image.open(self.ped_img.replace("#", str(i)).replace("$", "st"))
                resized_img = pedestrian_img.resize(
                    (int(pedestrian_img.width * (self.ped_height / pedestrian_img.height)), self.ped_height))
                rotated_img = resized_img.rotate(90 * (int(x) - 1), expand=True)
                ped_images[str(i + 1)]["st"] = ImageTk.PhotoImage(rotated_img)
            images[x] = ped_images
        return images

    def pedestrian_creator(self):
        """Μέθοδος η οποία δημιουργεί συνεχώς ένα πεζό μετά το πέρας ενός
           συγκεκριμένου χρονικού διαστήματος"""
        if self.lights.operation_mode:
            if len(self.total_ped_list) < self.pedestrian_limit:
                rand_num = random.randint(1, 100)
                if rand_num <= 35:
                    direction = 1
                elif rand_num <= 50:
                    direction = 2
                elif rand_num <= 75:
                    direction = 3
                else:
                    direction = 4
                ped_image = random.choice(list(self.ped_images[str(direction)].values()))
                new_ped = Pedestrian(image=ped_image, direction=direction, params=self.ped_params, canvas=self.canvas,
                                     window=self.root, lights=self.lights, total_ped_list=self.total_ped_list,
                                     ped_dict=self.ped_dict, cars_dict=self.cars_dict)
                #  Καταχώριση του αντικειμένου στο λεξικό ανάλογα με την κατεύθυνσή του
                self.ped_dict[str(new_ped.direction)].append(new_ped)
                # Καταχώριση στη λίστα με όλους τους πεζούς
                self.total_ped_list.append(new_ped)
        self.root.after(4000, self.pedestrian_creator)

    def delete_ped(self):
        """Μέθοδος η οποία καλείται συνεχώς και διαγράφει τους πεζούς
           που έχουν εξέλθει από τα όρια του παραθύρου"""
        for ped in self.total_ped_list:
            if ped.x < -80 or ped.x > 1932 or ped.y < -80 or ped.y > 1150:
                self.total_ped_list.remove(ped)
                self.ped_dict[str(ped.direction)].remove(ped)
                self.canvas.delete(ped.pedestrian)
                del ped
        self.root.after(100, self.delete_ped)
