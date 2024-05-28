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
        """Συνάρτηση που δημιουργεί λεξικό με τις εικόνες των αυτοκινήτων ανά κατεύθυνση
        ώστε δίνοντας την κατεύθυνση του αυτοκινήτου σαν κλειδί του λεξικού να επιστρέφεται
        η φωτογραφία του αυτοκινήτου"""
        images = {}
        for i in self.car_pos.keys():
            images[i] = []
            for x in range(0, self.distinct_cars):
                # Αντικατάσταση του συμβόλου # της συμβολοσειράς με τον αριθμό
                # της κάθε φωτογραφίας οχήματος ώστε να 'ανοίγει' την κατάλληλη
                # φωτογραφία
                car_image = Image.open(self.car_img.replace("#", str(x + 1)))
                # Μετατροπή του μεγέθους της κάθε φωτογραφίας ώστε να είναι αυτό της μεταβλητής
                # self.car_height
                resized_car = car_image.resize(
                    (int(car_image.width * (self.car_height / car_image.height)), self.car_height))
                # Περιστροφή ανάλογα με την κατεύθυνση του οχήματος
                rotated_image = resized_car.rotate(90 * (int(i) - 1), expand=True)
                images[i].append(ImageTk.PhotoImage(rotated_image))
        return images

    def car_creator(self):
        """Μέθοδος η οποία δημιουργεί συνεχώς ένα καινούριο αυτοκίνητο μετά το πέρας ενός
           συγκεκριμένου χρονικού διαστήματος"""
        if self.lights.operation_mode:
            # Με τη χρήση της random το αυτοκίνητο που δημιουργείται έχει 80% πιθανότητα
            # να δημιουργηθεί σε ένα από τα δύο ρεύματα κυκλοφορίας της κεντρικής οδού
            # όπως ζητείται από το β προαιρετικό ζητούμενο της εργασίας
            if len(self.total_car_list) < self.car_limit:
                rand_num = random.randint(1, 100)
                if rand_num <= 40:
                    direction = 1
                elif rand_num <= 60:
                    direction = 2
                else:
                    direction = 3
                lane = random.choice([0, 1])
                # Τυχαία επιλογή μίας από τις διαθέσιμες φωτογραφίες αυτοκινήτων
                car_image = random.choice(self.car_images[str(direction)])
                # Δημιουργία καινούριου αυτοκινήτου
                new_car = Car(image=car_image, direction=direction, lane=lane, params=self.car_params,
                              canvas=self.canvas, window=self.root, lights=self.lights,
                              total_car_list=self.total_car_list, cars_dict=self.cars_dict)
                #  Καταχώριση του αντικειμένου στο λεξικό ανάλογα με την κατεύθυνσή του
                #  και τη λορίδα κυκλοφορίας
                self.cars_dict[str(new_car.direction)][new_car.lane].append(new_car)
                # Καταχώριση στη λίστα με όλα τα αυτοκίνητα
                self.total_car_list.append(new_car)
        # Κλήση της ίδιας συνάρτησης μετά από 4 δευτερόλεπτα
        self.root.after(4000, self.car_creator)

    # Μέθοδος που ρυθμίζει τις ταχύτητες των αυτοκινήτων όπως ζητείται από το β προαιρετικό ζητούμενο
    def change_car_speed(self, speed):
        """Μέθοδος η οποία αλλάζει τις ταχύτητες όλων των αυτοκινήτων στον προσομοιωτή"""
        # Διαπέραση όλων των αυτοκινήτων στη λίστα
        for car in self.total_car_list:
            # Χρήση list comprehension για δημιουργία πλειάδας που περιέχει την
            # ταχύτητα κίνησης του αυτοκινήτου στον κάθε άξονα
            # πηγή: https://stackoverflow.com/questions/9987483/elif-in-list-comprehension-conditionals
            car.speed = tuple([i if i == 0 else speed if i > 0 else -speed for i in list(car.speed)])
            # Αλλαγή της προεπιλεγμένης ταχύτητας
            self.car_params["default_car_speed"] = speed
            # Αν το αυτοκίνητο κινείται αλλάζει και την τρέχουσα ταχύτητα του οχήματος
            if car.moving:
                car.cur_speed = car.speed

    def delete_car(self):
        """Μέθοδος η οποία καλείται συνεχώς και διαγράφει τα αυτοκίνητα
        που έχουν εξέλθει από τα όρια του παραθύρου"""
        # Διαπέραση όλων των αυτοκινήτων στη λίστα
        for car in self.total_car_list:
            # Εάν το όχημα εξέλθει από τα συγκεκριμένα όρια
            if (car.x < -150 or car.x > self.root.winfo_width() + 150 or car.y < -150
                    or car.y > self.root.winfo_height() + 150):
                # Διαγράφεται από τη λίστα με όλα τα αυτοκίνητα
                self.total_car_list.remove(car)
                # Διαγράφεται από το λεξικό
                self.cars_dict[str(car.direction)][car.lane].remove(car)
                # Διαγράφεται η εικόνα από τον καμβά
                self.canvas.delete(car.car)
                # Και τέλος διαγράφεται και το ίδιο το αντικείμενο
                del car
        # Μετά από 100ms καλείται πάλι η μέθοδος
        self.root.after(100, self.delete_car)

    def create_ped_images(self):
        """Συνάρτηση που δημιουργεί λεξικό με τις εικόνες των πεζών ανά κατεύθυνση"""
        images = {}
        for x in self.ped_pos.keys():
            ped_images = {}
            for i in range(0, self.distinct_peds):
                ped_images[str(i + 1)] = {}
                for y in range(0, self.num_of_steps):
                    # Αντικατάσταση των συμβόλων # και $ της συμβολοσειράς με τον αριθμό
                    # της κάθε φωτογραφίας πεζού και τον αριθμό του κάθε βήματος ώστε να
                    # 'ανοίγει' την κατάλληλη φωτογραφία
                    pedestrian_img = Image.open(self.ped_img.replace("#", str(i)).replace("$", str(y)))
                    # Μετατροπή του μεγέθους της κάθε φωτογραφίας ώστε να είναι αυτό της μεταβλητής
                    # self.ped_height
                    resized_img = pedestrian_img.resize(
                        (int(pedestrian_img.width * (self.ped_height / pedestrian_img.height)), self.ped_height))
                    # Περιστροφή της κάθε φωτογραφίας ανάλογα με την κατεύθυνση του πεζού ώστε
                    # να εμφανίζεται σωστά στον προσομοιωτή
                    rotated_img = resized_img.rotate(90 * (int(x) - 1), expand=True)
                    # Εισαγωγή στη σωστή θέση του λεξικού ανάλογα με την κατεύθυνση και τον
                    # αριθμό του πεζού
                    ped_images[str(i + 1)][str(y)] = ImageTk.PhotoImage(rotated_img)
                    # Συμπλήρωση του λεξικού με τον ίδιο τρόπο για τη φωτογραφία του
                    # πεζού σε θέση στάσης
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
            # Τυχαία εκχώρηση κατεύθυνσης σε κάθε πεζό
            if len(self.total_ped_list) < self.pedestrian_limit:
                rand_num = random.randint(1, 100)
                if rand_num <= 35:
                    direction = 1
                elif rand_num <= 50:
                    direction = 2
                elif rand_num <= 85:
                    direction = 3
                else:
                    direction = 4
                # Τυχαία επιλογή φωτογραφίας πεζού
                ped_image = random.choice(list(self.ped_images[str(direction)].values()))
                # Δημιουργία καινούριας οντότητας πεζού
                new_ped = Pedestrian(image=ped_image, direction=direction, params=self.ped_params, canvas=self.canvas,
                                     window=self.root, lights=self.lights, total_ped_list=self.total_ped_list,
                                     ped_dict=self.ped_dict, cars_dict=self.cars_dict)
                #  Καταχώριση του αντικειμένου στο λεξικό ανάλογα με την κατεύθυνσή του
                self.ped_dict[str(new_ped.direction)].append(new_ped)
                # Καταχώριση στη λίστα με όλους τους πεζούς
                self.total_ped_list.append(new_ped)
        # Κλήση εκ νέου της συνάρτησης μετά από το οριζόμενο χρονικό διάστημα
        self.root.after(4000, self.pedestrian_creator)

    def delete_ped(self):
        """Μέθοδος η οποία καλείται συνεχώς και διαγράφει τους πεζούς
           που έχουν εξέλθει από τα όρια του παραθύρου"""
        for ped in self.total_ped_list:
            # Εάν το όχημα εξέλθει από τα συγκεκριμένα όρια
            if (ped.x < -100 or ped.x > self.root.winfo_width() + 100 or ped.y < -100
                    or ped.y > self.root.winfo_height() + 100):
                # Διαγράφεται από τη λίστα με όλους τους πεζούς
                self.total_ped_list.remove(ped)
                # Διαγράφεται από το λεξικό
                self.ped_dict[str(ped.direction)].remove(ped)
                # Διαγράφεται η εικόνα του πεζού από τον καμβά
                self.canvas.delete(ped.pedestrian)
                # Και τέλος διαγράφεται το ίδιο το αντικείμενο
                del ped
        # Κλήση εκ νέου της μεθόδου μετά από το οριζόμενο
        # χρονικό διάστημα
        self.root.after(100, self.delete_ped)
