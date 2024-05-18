from traffic_lights import TrafficLights as trl


class LightsController:
    controller = None
    # Μεταβλητή για το εάν το πρόγραμμα λειτουργεί ή
    # βρίσκεται σε παύση
    operation_mode = True
    # Μεταβλητή με την τρέχουσα λειτουργία των σηματοδοτών
    current_mode = "normal"

    def __init__(self):
        # Μεταβλητή με την τιμή του χρόνου που ξεκίνησε η τελευταία φάση
        self.central_time = 0
        LightsController.controller = self
        self.initialise("normal")
        self.operator()

    def initialise(self, mode):
        LightsController.current_mode = mode
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
        if self.operation_mode:
            if LightsController.current_mode == "night":
                self.light_blink("secondary")
            elif LightsController.current_mode == "normal":
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
        trl.tr_lights_main_sec["main"][0].root.after(1000, self.operator)

    @staticmethod
    def pedestrian_command(street, command, seconds):
        for tr_lights in trl.tr_lights_main_sec[street]:
            for ped in tr_lights.ped_lights:
                if ped.phase != command:
                    ped.command = command
                    ped.timer_seconds = seconds

    @staticmethod
    def car_command(street, command):
        for val in trl.tr_lights_main_sec[street]:
            if command != val.command:
                val.command = command

    @staticmethod
    def light_blink(street):
        for val in trl.tr_lights_main_sec[street]:
            if val.command != "orange":
                val.command = "orange"
            else:
                val.command = "off"
