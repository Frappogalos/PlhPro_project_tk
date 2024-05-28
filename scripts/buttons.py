import tkinter as tk
from PIL import ImageTk, Image


class OpButton:
    """Κλάση για τη δημιουργία κουμπιού λειτουργίας των φαναριών της προσομοίωσης"""
    modes = ["night", "normal"]

    def __init__(self, x, y, images, window, lights_controller):
        # Θέση του κουμπιού στον άξονα Χ
        self.posx = x
        # Θέση του κουμπιού στον άξονα Υ
        self.posy = y
        # Εικόνες που θα χρησιμοποιηθούν για το κουμπί
        self.images = [ImageTk.PhotoImage(Image.open(images[0])),
                       ImageTk.PhotoImage(Image.open(images[1]))]
        # Τρέχουσα εικόνα το κουμπιού
        self.current_image = self.images[1]
        # Τρέχουσα λειτουργία
        self.operation = "normal"
        # Διαχειριστής των σηματοδοτών
        self.controller = lights_controller
        # Δημιουργία του κουμπιού στον καμβά
        self.button = tk.Button(window, image=self.current_image, command=self.btn_click)
        # Τοποθέτηση στη θέση που ορίζεται
        self.button.place(x=self.posx, y=self.posy)

    def btn_click(self):
        """Μέθοδος για τη λειτουργία του κουμπιού όταν αυτό πατηθεί"""
        # Αλλαγή εικόνας του κουμπιού λειτουργίας
        self.current_image = self.images[self.images.index(self.current_image)-1]
        self.button.config(image=self.current_image)
        # Αλλαγή της τρέχουσας λειτουργίας
        self.operation = OpButton.modes[OpButton.modes.index(self.operation)-1]
        # Αρχικοποίηση της λειτουργίας των σηματοδοτών
        self.controller.initialise(self.operation)


class PauseButton:
    """Κλάση για τη δημιουργία κουμπιού παύσης της προσομοίωσης"""
    def __init__(self, x, y, image, window, lights_controller):
        # Θέση του κουμπιού στον άξονα Χ
        self.posx = x
        # Θέση του κουμπιού στον άξονα Υ
        self.posy = y
        # Εικόνα που θα χρησιμοποιηθεί για το κουμπί
        self.image = ImageTk.PhotoImage(Image.open(image))
        # Διαχειριστής των σηματοδοτών
        self.controller = lights_controller
        # Δημιουργία του κουμπιού στον καμβά
        self.button = tk.Button(window, image=self.image, command=self.pause_unpause)
        # Τοποθέτηση στη θέση που ορίζεται
        self.button.place(x=self.posx, y=self.posy)

    def pause_unpause(self):
        """Μέθοδος για την παύση ή διακοπή της παύσης του προσομοιωτή"""
        self.controller.change_mode()


class CarsSpeedControl:
    """Κλάση για τη δημιουργία του γραφικού στοιχείου για τη ρύθμιση
    της ταχύτητας των οχημάτων"""
    def __init__(self, x, y, window, traffic_manager, default_speed, speed_range):
        # Θέση στον άξονα Χ
        self.posx = x
        # Θέση στον άξονα Χ
        self.posy = y
        # Διαχειριστής κυκλοφορίας
        self.traffic_manager = traffic_manager
        # Μεταβλητή με την προεπιλεγμένη ταχύτητα
        def_speed = tk.DoubleVar(value=default_speed)
        # Δημιουργία ετικέτας
        self.label = tk.Label(window, text="Ταχύτητα οχημάτων", bg="lightblue", font=("Arial", 16, "bold"),
                              relief=tk.RAISED)
        # Τοποθέτηση της ετικέτας στον καμβά
        self.label.place(x=self.posx-40, y=self.posy-30)
        # Δημιουργία του γραφικού στοιχείου για τη ρύθμιση
        # της ταχύτητας των οχημάτων
        self.spinbox = tk.Spinbox(window, from_=speed_range[0], to=speed_range[1], textvariable=def_speed, width=10,
                                  relief="sunken", repeatdelay=500, repeatinterval=100, font=("Arial", 12),
                                  bg="lightgrey", fg="blue", command=self.change_speed)
        self.spinbox.config(state="normal", cursor="hand2", bd=3, justify="center", wrap=True)
        # Τοποθέτηση του γραφικού στοιχείου στον καμβά
        self.spinbox.place(x=self.posx, y=self.posy)

    def change_speed(self):
        """Μέθοδος για την αλλαγή ταχύτητας των οχημάτων καλώντας την ανάλογη
        μέθοδο του διαχειριστή κυκλοφορίας"""
        value = int(self.spinbox.get())
        self.traffic_manager.change_car_speed(value)

