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


class SettingsBtn:
    def __init__(self, x, y, image, traffic_manager, cars_params, window):
        # Θέση του κουμπιού στον άξονα Χ
        self.posx = x
        # Θέση του κουμπιού στον άξονα Υ
        self.posy = y
        # Εικόνα που θα χρησιμοποιηθεί για το κουμπί
        self.image = ImageTk.PhotoImage(Image.open(image))
        # Δημιουργία του κουμπιού στον καμβά
        self.button = tk.Button(window, image=self.image, command=self.open_settings)
        # Τοποθέτηση στη θέση που ορίζεται
        self.button.place(x=self.posx, y=self.posy)
        # Διαχειριστής κυκλοφορίας
        self.traffic_manager = traffic_manager
        self.cars_params = cars_params
        self.popup = None
        self.speed_spinbox = None
        self.car_lim_spinbox = None
        self.car_time_inter_spinbox = None

    def open_settings(self):
        """Μέθοδος που δημιουργεί το παράθυρο των ρυθμίσεων του προγράμματος"""
        if self.popup:
            self.popup.destroy()
        win = tk.Toplevel()
        # Τίτλος παραθύρου
        win.title("Ρυθμίσεις")
        # Μέγεθος παραθύρου
        win.geometry("400x300")
        # Εικονίδιο παραθύρου
        win.wm_iconphoto(False, self.image)
        # Κλείδωμα διαστάσεων παραθύρου
        win.resizable(width=False, height=False)
        self.popup = win
        # Δημιουργία ετικέτας
        speed_label_txt = (f"Ταχύτητα οχημάτων\n{self.cars_params['cars_speed_range'][0]} - "
                           f"{self.cars_params['cars_speed_range'][1]}")
        speed_label = tk.Label(win, text=speed_label_txt, bg="lightblue", font=("Arial", 16, "bold"), relief=tk.RAISED)
        # Τοποθέτηση της ετικέτας στον καμβά
        speed_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))
        # Δημιουργία ετικέτας
        limit_label_txt = "Όριο οχημάτων\n1 - 50"
        limit_label = tk.Label(win, text=limit_label_txt, bg="lightblue", font=("Arial", 16, "bold"), relief=tk.RAISED)
        # Τοποθέτηση της ετικέτας στον καμβά
        limit_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))
        # Δημιουργία ετικέτας
        density_label_txt = "Πυκνότητα κυκλοφορίας\n1 - 7"
        density_label = tk.Label(win, text=density_label_txt, bg="lightblue", font=("Arial", 16, "bold"),
                                 relief=tk.RAISED)
        # Τοποθέτηση της ετικέτας στον καμβά
        density_label.grid(row=2, column=0, padx=(10, 10), pady=(10, 10))
        # Δημιουργία του γραφικού στοιχείου για τη ρύθμιση
        # της ταχύτητας των οχημάτων
        self.speed_spinbox = tk.Spinbox(win, from_=self.cars_params["cars_speed_range"][0],
                                        to=self.cars_params["cars_speed_range"][1],
                                        textvariable=tk.DoubleVar(value=self.cars_params["default_car_speed"]), width=10,
                                        relief="sunken", repeatdelay=500, repeatinterval=100, font=("Arial", 12),
                                        bg="lightgrey", fg="blue", command=self.change_speed)
        self.speed_spinbox.config(state="normal", cursor="hand2", bd=3, justify="center", wrap=True)
        # Τοποθέτηση του γραφικού στοιχείου στον καμβά
        self.speed_spinbox.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
        # Δημιουργία του γραφικού στοιχείου για τη ρύθμιση
        # του ορίου των οχημάτων που μπορούν να βρίσκονται στο χάρτη
        self.car_lim_spinbox = tk.Spinbox(win, from_=1, to=50,
                                          textvariable=tk.DoubleVar(value=self.traffic_manager.car_limit), width=10,
                                          relief="sunken", repeatdelay=500, repeatinterval=100, font=("Arial", 12),
                                          bg="lightgrey", fg="blue", command=self.change_car_limit)
        self.car_lim_spinbox.config(state="normal", cursor="hand2", bd=3, justify="center", wrap=True)
        # Τοποθέτηση του γραφικού στοιχείου στον καμβά
        self.car_lim_spinbox.grid(row=1, column=1, padx=(10, 10), pady=(10, 10))
        # Δημιουργία του γραφικού στοιχείου για τη ρύθμιση
        # της πυκνότητας της κυκλοφορίας
        self.car_time_inter_spinbox = tk.Spinbox(win, from_=1, to=7,
                                                 textvariable=tk.DoubleVar(
                                                     value=8 - self.traffic_manager.car_time_interval
                                                 ),
                                                 width=10, relief="sunken", repeatdelay=500, repeatinterval=100,
                                                 font=("Arial", 12), bg="lightgrey", fg="blue",
                                                 command=self.change_car_time_interval)
        self.car_time_inter_spinbox.config(state="normal", cursor="hand2", bd=3, justify="center", wrap=True)
        # Τοποθέτηση του γραφικού στοιχείου στον καμβά
        self.car_time_inter_spinbox.grid(row=2, column=1, padx=(10, 10), pady=(10, 10))

    def change_speed(self):
        """Μέθοδος για την αλλαγή ταχύτητας των οχημάτων καλώντας την ανάλογη
        μέθοδο του διαχειριστή κυκλοφορίας"""
        value = int(self.speed_spinbox.get())
        self.traffic_manager.change_car_speed(value)

    def change_car_limit(self):
        """Μέθοδος για την αλλαγή του ορίου οχημάτων που μπορούν να βρίσκονται
        στον προσομοιωτή αλλάζοντας την ανάλογη μεταβλητή του διαχειριστή κυκλοφορίας"""
        value = int(self.car_lim_spinbox.get())
        self.traffic_manager.car_limit = value

    def change_car_time_interval(self):
        """Μέθοδος για την αλλαγή της πυκνότητας των οχημάτων στον προσομοιωτή
        αλλάζοντας την ανάλογη μεταβλητή του διαχειριστή κυκλοφορίας"""
        value = int(self.car_time_inter_spinbox.get())
        self.traffic_manager.car_time_interval = 8 - value
