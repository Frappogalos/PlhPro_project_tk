
class TrafficLights:
    # Λίστα με τις φάσεις λειτουργίας των σηματοδοτών
    light_phases = ["off", "green", "orange", "red"]

    def __init__(self, images, direction, position, tl_parameters, ped_images, canvas, window):
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
        self.tl_params = tl_parameters
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
        """Μέθοδος που πραγματοποιεί την αλλαγή φάσης στον κάθε φωτεινό σηματοδότη"""
        if self.command != self.phase:
            self.phase = self.command
            self.canvas.itemconfig(self.tr_light, image=self.images[self.phase])
        self.canvas.tag_raise(self.tr_light)
        self.root.after(100, self.change)

    def create_pedestrian_lights(self):
        lights_list = []
        for i in self.tl_params["pl_params"][self.direction]:
            ped_light = PedestrianLights(images=self.ped_images, direction=i["direction"],
                                         ped_config=self.tl_params["ped_config"], phase=i["phase"], canvas=self.canvas,
                                         window=self.root, pos=i["pos"])
            lights_list.append(ped_light)
        return lights_list


class PedestrianLights:
    light_phases = ["off", "green", "red"]

    def __init__(self, images, direction, ped_config, pos, phase, canvas, window):
        self.direction = direction
        self.images = images[self.direction]
        self.phase = phase
        self.operation_mode = True
        self.command = phase
        self.x = pos[0]
        self.y = pos[1]
        self.ped_config = ped_config
        self.root = window
        self.canvas = canvas
        self.timer_seconds = 0
        self.ped_light = self.canvas.create_image(self.x, self.y, image=self.images[self.phase])
        self.t_x = self.x + self.ped_config["timer_pos"][self.direction][0]
        self.t_y = self.y + self.ped_config["timer_pos"][self.direction][1]
        self.timer_widget = self.canvas.create_text(self.t_x, self.t_y, font=("Arial", 15), text="00",
                                                    angle=90*self.direction, fill="white")
        self.change()
        self.timer()

    def timer(self):
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
