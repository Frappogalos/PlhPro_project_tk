from traffic_lights import TrafficLights, PedestrianLights
from PIL import Image, ImageTk


class LightsController:
    """Κλάση που δημιουργεί και διαχειρίζεται τους φωτεινούς σηματοδότες"""
    def __init__(self, tl_parameters, canvas, root):
        # Μεταβλητή του παραθύρου που έχει δημιουργηθεί
        self.root = root
        # Μεταβλητή του καμβά που έχει δημιουργηθεί και πάνω στην οποία θα προσθέτονται
        # τα νέα αντικείμενα
        self.canvas = canvas
        # Μεταβλητή με την τιμή του χρόνου που ξεκίνησε η τελευταία φάση
        self.central_time = 0
        # Μεταβλητή για το εάν το πρόγραμμα λειτουργεί ή
        # βρίσκεται σε παύση
        self.operation_mode = True
        # Μεταβλητή με την τρέχουσα λειτουργία των σηματοδοτών
        self.current_mode = "normal"
        # Λεξικό με τις παραμέτρους των φωτεινών σηματοδοτών ανάλογα με την
        # κατεύθυνση της κίνησης που ελέγχουν
        self.tl_params = tl_parameters
        # Λεξικό με τις παραμέτρους των φωτεινών σηματοδοτών για τους πεζούς
        self.ped_config = tl_parameters["ped_config"]
        # Λεξικό με τις εικόνες των φωτεινών σηματοδοτών για τα αυτοκίνητα
        self.car_images = self.car_lights_images_creator()
        # Λεξικό με τις εικόνες των φωτεινών σηματοδοτών για τους πεζούς
        self.ped_images = self.ped_lights_images_creator()
        # Λεξικό που αποθηκεύει τους φωτεινούς σηματοδότες ανά κατεύθυνση
        self.tr_lights_dict = {}
        # Λεξικό που αποθηκεύει ξεχωριστά τους σηματοδότες της κύριας
        # οδού με αυτούς της δευτερεύουσας
        self.tr_lights_main_sec = {"main": [], "secondary": []}
        # Λεξικό που αποθηκεύει τους φωτεινούς σηματοδότες για τους πεζούς
        # ανά κατεύθυνση
        self.ped_lights_dict = {"1": [], "2": [], "3": [], "4": []}
        # Κλήση της μεθόδου για τη δημιουργία των φωτεινών σηματοδοτών
        self.traffic_lights_creator()
        # Κλήση της μεθόδου για την αρχικοποίηση των φωτεινών σηματοδοτών
        self.initialise(self.current_mode)
        # Κλήση της μεθόδου για τη λειτουργία των φωτεινών σηματοδοτών
        self.operator()

    def initialise(self, mode):
        """Μέθοδος που αρχικοποιεί τη λειτουργία των φαναριών σε μία από τις
        δύο λειτουργίες κανονική και νυχτερινή"""
        self.current_mode = mode
        if mode == "night":
            self.pedestrian_command("main", "off", 0)
            self.car_command("main", "off")
            self.pedestrian_command("secondary", "off", 0)
            self.car_command("secondary", "orange")
        elif mode == "normal":
            self.central_time = 0
            self.pedestrian_command("main", "red", 29)
            self.car_command("main", "green")
            self.pedestrian_command("secondary", "green", 25)
            self.car_command("secondary", "red")

    def operator(self):
        """Μέθοδος που ελέγχει τη λειτουργία και το συγχρονισμό των σηματοδοτών"""
        if self.operation_mode:
            if self.current_mode == "night":
                self.light_blink("secondary")
            elif self.current_mode == "normal":
                if self.central_time > 46:
                    self.central_time = 0
                    self.initialise("normal")
                elif self.central_time == 26:
                    self.pedestrian_command("secondary", "red", 18)
                    self.car_command("main", "orange")
                elif self.central_time == 29:
                    self.car_command("main", "red")
                elif self.central_time == 30:
                    self.car_command("secondary", "green")
                    self.pedestrian_command("main", "green", 11)
                elif self.central_time == 42:
                    self.pedestrian_command("main", "red", 33)
                    self.car_command("secondary", "orange")
                elif self.central_time == 45:
                    self.car_command("secondary", "red")
                elif self.central_time == 46:
                    self.car_command("main", "green")
                    self.pedestrian_command("secondary", "green", 25)
            self.central_time += 1
        self.root.after(1000, self.operator)

    def pedestrian_command(self, street, command, seconds):
        """Μέθοδος που μεταφέρει τις εντολές στους φωτεινούς σηματοδότες των πεζών
        καθώς και το χρόνο για το χρονόμετρο που βλέπουν οι πεζοί"""
        for tr_lights in self.tr_lights_main_sec[street]:
            for ped in tr_lights.ped_lights:
                if ped.phase != command:
                    ped.command = command
                    ped.timer_seconds = seconds

    def car_command(self, street, command):
        """Μέθοδος που μεταφέρει τις εντολές στους φωτεινούς σηματοδότες των αυτοκινήτων"""
        for val in self.tr_lights_main_sec[street]:
            if command != val.command:
                val.command = command

    def light_blink(self, street):
        """Μέθοδος που μεταφέρει τις εντολές για την παλώμενη λειτουργία του σηματοδότη"""
        for val in self.tr_lights_main_sec[street]:
            if val.command != "orange":
                val.command = "orange"
            else:
                val.command = "off"

    def change_mode(self):
        """Μέθοδος που πραγματοποιεί την αλλαγή λειτουργίας των φωτεινών σηματοδοτών
        από κανονική σε νυχτερινή"""
        self.operation_mode = not self.operation_mode
        for i in self.tr_lights_dict.values():
            i.operation_mode = self.operation_mode
            for x in i.ped_lights:
                x.operation_mode = self.operation_mode

    def car_lights_images_creator(self):
        """Δημιουργία λεξικού με τις φωτογραφίες των φωτεινών σηματοδοτών ανάλογα
        με την κατεύθυνση του κάθε ενός"""
        images = {}
        for x in self.tl_params["pos"]["car_tl"][0].keys():
            dir_images = {}
            for i in TrafficLights.light_phases:
                tr_image = Image.open(self.tl_params["img"].replace("#", i))
                resized_image = tr_image.resize((int(tr_image.width * (self.tl_params["height"] / tr_image.height)),
                                                 self.tl_params["height"]))
                rotated_image = resized_image.rotate(90 * (int(x) - 2), expand=True)
                dir_images[i] = ImageTk.PhotoImage(rotated_image)
            images[x] = dir_images
        return images

    def traffic_lights_creator(self):
        """Μέθοδος η οποία δημιουργεί τους φωτεινούς σηματοδότες"""
        for x in range(0, len(self.tl_params["pos"]["car_tl"])):
            for i in self.tl_params["pos"]["car_tl"][x].keys():
                tr_light = TrafficLights(images=self.car_images[i], direction=int(i),
                                         position=self.tl_params["pos"]["car_tl"][x][i],
                                         ped_lights_parameters=self.tl_params["pos"]["ped_lights"][x],
                                         ped_config=self.tl_params["ped_config"],
                                         ped_images=self.ped_images,
                                         canvas=self.canvas, window=self.root)
                for light in tr_light.ped_lights:
                    self.ped_lights_dict[str(light.direction)].append(light)
                # Ανάλογα με την κατεύθυνση που ρυθμίζει ο σηματοδότης εισάγεται στην κατάλληλη θέση του λεξικού
                if tr_light.direction == 1 or tr_light.direction == 3:
                    self.tr_lights_main_sec["main"].append(tr_light)
                else:
                    self.tr_lights_main_sec["secondary"].append(tr_light)
                self.tr_lights_dict[str(tr_light.direction)] = tr_light

    def ped_lights_images_creator(self):
        """Δημιουργία λεξικού με τις φωτογραφίες των φωτεινών σηματοδοτών των πεζών
        ανάλογα με την κατεύθυνση του κάθε ενός"""
        images = {}
        for x in range(1, 5):
            dir_images = {}
            for i in PedestrianLights.light_phases:
                tr_image = Image.open(self.ped_config["img"].replace("#", i))
                resized_image = tr_image.resize((int(tr_image.width * (self.ped_config["height"] / tr_image.height)),
                                                 self.ped_config["height"]))
                rotated_image = resized_image.rotate(90 * x, expand=True)
                dir_images[i] = ImageTk.PhotoImage(rotated_image)
            images[x] = dir_images
        return images
