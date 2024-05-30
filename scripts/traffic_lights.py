class TrafficLights:
    """Κλάση για τη δημιουργία και τις λειτουργίες των φωτεινών σηματοδοτών"""
    # Λίστα με τις φάσεις λειτουργίας των σηματοδοτών
    light_phases = ["off", "green", "orange", "red"]

    def __init__(self, images, direction, position, ped_lights_parameters, ped_config, ped_images, canvas, window):
        # Μεταβλητή για το εάν το πρόγραμμα λειτουργεί ή
        # βρίσκεται σε παύση
        self.operation_mode = True
        # Λεξικό με τις φωτογραφίες που θα χρησιμοποιηθούν
        self.images = images
        # Μεταβλητή με την κατεύθυνση της κυκλοφορίας
        # που ρυθμίζει το φανάρι
        self.direction = direction
        # Μεταβλητή με την εντολή που λαμβάνει από την κύρια
        # συνάρτηση ελέγχου των σηματοδοτών
        self.command = "off"
        # Παράμετροι των φωτεινών σηματοδοτών των πεζών
        self.ped_lights_params = ped_lights_parameters
        # Ρυθμίσεις για τους σηματοδότες των πεζών
        self.ped_config = ped_config
        # Λεξικό με τις φωτογραφίες που θα χρησιμοποιηθούν
        # για τους φωτεινούς σηματοδότες των πεζών
        self.ped_images = ped_images
        # Μεταβλητή με την παρούσα φάση που βρίσκεται ο σηματοδότης
        self.phase = "off"
        # Μεταβλητή με τη θέση του σηματοδότη στον άξονα X
        self.x = position[0]
        # Μεταβλητή με τη θέση του σηματοδότη στον άξονα Y
        self.y = position[1]
        # Μεταβλητή του παραθύρου που έχει δημιουργηθεί
        self.root = window
        # Μεταβλητή του καμβά που έχει δημιουργηθεί και πάνω στην οποία θα προσθέτονται
        # τα νέα αντικείμενα
        self.canvas = canvas
        # Δημιουργία αντικειμένου πάνω στον καμβά
        self.tr_light = self.canvas.create_image(self.x, self.y, image=self.images[self.phase])
        # Ανάλογα με την κατεύθυνση που ρυθμίζει ο σηματοδότης εισάγονται και οι ανάλογοι σηματοδότες πεζών
        self.ped_lights = self.create_pedestrian_lights()
        self.change()

    def change(self):
        """Μέθοδος που πραγματοποιεί την αλλαγή φάσης στον κάθε φωτεινό σηματοδότη
        και ανεβάζει επίπεδο τις φωτογραφίες των φωτεινών σηματοδοτών στον καμβά"""
        if self.command != self.phase:
            self.phase = self.command
            self.canvas.itemconfig(self.tr_light, image=self.images[self.phase])
        self.canvas.tag_raise(self.tr_light)
        self.root.after(100, self.change)

    def create_pedestrian_lights(self):
        """Δημιουργία των φωτεινών σηματοδοτών των πεζών"""
        lights_list = []
        for i in self.ped_lights_params[self.direction]:
            ped_light = PedestrianLights(images=self.ped_images, direction=i["direction"],
                                         ped_config=self.ped_config, phase=i["phase"],
                                         canvas=self.canvas, window=self.root, pos=i["pos"])
            lights_list.append(ped_light)
        return lights_list


class PedestrianLights:
    """Κλάση για τη δημιουργία των φωτεινών σηματοδοτών για τους πεζούς και τις λειτουργίες τους"""
    light_phases = ["off", "green", "red"]

    def __init__(self, images, direction, ped_config, pos, phase, canvas, window):
        # Μεταβλητή με την κατεύθυνση της κυκλοφορίας
        # που ρυθμίζει το φανάρι
        self.direction = direction
        # Λεξικό με τις φωτογραφίες που θα χρησιμοποιηθούν
        self.images = images[self.direction]
        # Μεταβλητή με την παρούσα φάση που βρίσκεται ο σηματοδότης
        self.phase = phase
        # Μεταβλητή για το εάν το πρόγραμμα λειτουργεί ή
        # βρίσκεται σε παύση
        self.operation_mode = True
        # Μεταβλητή με την εντολή που λαμβάνει από την κύρια
        # συνάρτηση ελέγχου των σηματοδοτών
        self.command = phase
        # Μεταβλητή με τη θέση του σηματοδότη στον άξονα X
        self.x = pos[0]
        # Μεταβλητή με τη θέση του σηματοδότη στον άξονα Υ
        self.y = pos[1]
        # Παράμετροι των φωτεινών σηματοδοτών
        self.ped_config = ped_config
        # Μεταβλητή του παραθύρου που έχει δημιουργηθεί
        self.root = window
        # Μεταβλητή του καμβά που έχει δημιουργηθεί και πάνω στην οποία θα προσθέτονται
        # τα νέα αντικείμενα
        self.canvas = canvas
        # Μεταβλητή του χρόνου του χρονομέτρου που απομένει
        self.timer_seconds = 0
        # Δημιουργία αντικειμένου πάνω στον καμβά
        self.ped_light = self.canvas.create_image(self.x, self.y, image=self.images[self.phase])
        # Μεταβλητή με τη θέση του χρονομέτρου στον άξονα Χ
        self.t_x = self.x + self.ped_config["timer_pos"][self.direction][0]
        # Μεταβλητή με τη θέση του χρονομέτρου στον άξονα Υ
        self.t_y = self.y + self.ped_config["timer_pos"][self.direction][1]
        # Δημιουργία του χρονομέτρου πάνω στον καμβά
        self.timer_widget = self.canvas.create_text(self.t_x, self.t_y, font=("Arial", 15), text="00",
                                                    angle=90*self.direction, fill="white")
        self.change()
        self.timer()

    def timer(self):
        """Μέθοδος που διαχειρίζεται το χρονόμετρο στους φωτεινούς σηματοδότες για τους πεζούς"""
        if self.operation_mode:
            if self.timer_seconds >= 0:
                if self.timer_seconds < 10:
                    time_text = "0" + str(self.timer_seconds)
                else:
                    time_text = str(self.timer_seconds)
                self.canvas.itemconfig(self.timer_widget, text=time_text)
                self.timer_seconds -= 1
        self.root.after(1000, self.timer)

    def change(self):
        """Μέθοδος που πραγματοποιεί την αλλαγή φάσης στον κάθε φωτεινό σηματοδότη"""
        if self.command != self.phase:
            self.phase = self.command
            self.canvas.itemconfig(self.ped_light, image=self.images[self.phase])
        self.canvas.tag_raise(self.ped_light)
        self.canvas.tag_raise(self.timer_widget)
        self.root.after(100, self.change)
