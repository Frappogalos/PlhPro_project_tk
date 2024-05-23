# Background image
# Σχετική διεύθυνση που βρίσκεται η φωτογραφία
# του φόντου
bg_image = "../images/double_intersection.jpg"

# Παράμετροι σηματοδοτών αυτοκινήτων και πεζών
car_tl_params = {"pos": [{"1": (830, 600), "2": (910, 670), "3": (1010, 470)}],
                 "img": "../images/traffic_lights/car_#.png",
                 "height": 120,
                 "pl_params": {1: [{"direction": 4, "phase": "off", "pos": (680, 340)},
                                   {"direction": 2, "phase": "off", "pos": (680, 740)}],
                               2: [{"direction": 1, "phase": "off", "pos": (760, 280)},
                                   {"direction": 3, "phase": "off", "pos": (1070, 280)},
                                   {"direction": 1, "phase": "off", "pos": (760, 800)},
                                   {"direction": 3, "phase": "off", "pos": (1070, 800)}],
                               3: [{"direction": 4, "phase": "off", "pos": (1150, 340)},
                                   {"direction": 2, "phase": "off", "pos": (1150, 740)}]},
                 "ped_config": {"img": "../images/traffic_lights/pedestrian_#.png",
                                "height": 110,
                                "timer_pos": {1: (-38, 0), 2: (0, 38), 3: (38, 0), 4: (0, -38)}}}

# Παράμετροι κουμπιών
# Κουμπί παύσης
pause_params = {"pos": (1200, 50), "img": "../images/buttons/pause_btn.png"}

# Κουμπί λειτουργίας
op_btn_params = {"pos": (1300, 50),
                 "images": ("../images/buttons/on_off_grn.png", "../images/buttons/on_off_red.png")}
