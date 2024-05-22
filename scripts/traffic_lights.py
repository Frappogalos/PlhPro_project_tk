from PIL import Image, ImageTk


class TrafficLights:
    # Λίστα με τις φάσεις λειτουργίας των σηματοδοτών
    light_phases = ["off", "green", "orange", "red"]

    def __init__(self, images, direction, position, canvas, window):
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
        if self.direction == 1:
            self.ped_lights = [PedestrianLights(image=PedestrianLights.create_images(direction=4), direction=4,
                                                phase="off", canvas=self.canvas, window=self.root, pos=(680, 340)),
                               PedestrianLights(image=PedestrianLights.create_images(direction=2), direction=2,
                                                phase="off", canvas=self.canvas, window=self.root, pos=(680, 740))]
        elif self.direction == 2:
            self.ped_lights = [PedestrianLights(image=PedestrianLights.create_images(direction=1), direction=1,
                                                phase="off", canvas=self.canvas, window=self.root, pos=(760, 280)),
                               PedestrianLights(image=PedestrianLights.create_images(direction=3), direction=3,
                                                phase="off", canvas=self.canvas, window=self.root, pos=(1070, 280)),
                               PedestrianLights(image=PedestrianLights.create_images(direction=1), direction=1,
                                                phase="off", canvas=self.canvas, window=self.root, pos=(760, 800)),
                               PedestrianLights(image=PedestrianLights.create_images(direction=3), direction=3,
                                                phase="off", canvas=self.canvas, window=self.root, pos=(1070, 800))]
        elif self.direction == 3:
            self.ped_lights = [PedestrianLights(image=PedestrianLights.create_images(direction=4), direction=4,
                                                phase="off", canvas=self.canvas, window=self.root, pos=(1150, 340)),
                               PedestrianLights(image=PedestrianLights.create_images(direction=2), direction=2,
                                                phase="off", canvas=self.canvas, window=self.root, pos=(1150, 740))]
        self.change()

    def change(self):
        """Μέθοδος που πραγματοποιεί την αλλαγή φάσης στον κάθε φωτεινό σηματοδότη"""
        if self.command != self.phase:
            self.phase = self.command
            self.canvas.itemconfig(self.tr_light, image=self.images[self.phase])
        self.canvas.tag_raise(self.tr_light)
        self.root.after(100, self.change)


class PedestrianLights:
    light_phases = ["off", "green", "red"]
    light_img_file = "../images/traffic_lights/pedestrian_#.png"
    # Ύψος που πρέπει να έχει η εικόνα στο πρόγραμμα
    target_height = 110
    ped_lights_dict = {"1": [], "2": [], "3": [], "4": []}

    def __init__(self, image, direction, pos, phase, canvas, window):
        self.images = image
        self.direction = direction
        self.phase = phase
        self.operation_mode = True
        self.x = pos[0]
        self.y = pos[1]
        self.command = phase
        self.root = window
        self.canvas = canvas
        self.timer_seconds = 0
        self.ped_light = self.canvas.create_image(self.x, self.y, image=self.images[self.phase])
        if self.direction == 1:
            self.t_x = self.x - 38
            self.t_y = self.y
        elif self.direction == 2:
            self.t_x = self.x
            self.t_y = self.y + 38
        elif self.direction == 3:
            self.t_x = self.x + 38
            self.t_y = self.y
        elif self.direction == 4:
            self.t_x = self.x
            self.t_y = self.y - 38
        self.timer_widget = self.canvas.create_text(self.t_x, self.t_y, font=("Arial", 15), text="00",
                                                    angle=90*self.direction, fill="white")
        PedestrianLights.ped_lights_dict[str(self.direction)].append(self)
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

    @classmethod
    def create_images(cls, direction):
        dir_images = {}
        for i in PedestrianLights.light_phases:
            tr_image = Image.open(PedestrianLights.light_img_file.replace("#", i))
            resized_image = tr_image.resize((int(tr_image.width*(PedestrianLights.target_height/tr_image.height)),
                                             PedestrianLights.target_height))
            rotated_image = resized_image.rotate(90 * direction, expand=True)
            dir_images[i] = ImageTk.PhotoImage(rotated_image)
        return dir_images
