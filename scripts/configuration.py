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
                                "timer_pos": {1: (-38, 0), 2: (0, 38), 3: (38, 0), 4: (0, -38)}
                                }
                 }

# Παράμετροι αυτοκινήτων
cars_speed = 6
cars_params = {"pos": {"1": [(-140, 645), (-140, 570)], "2": [(870, 1130), (960, 1130)],
                       "3": [(1982, 440), (1982, 510)]},
               "direction_speed": {"1": (cars_speed, 0), "2": (0, -cars_speed), "3": (-cars_speed, 0)},
               "distinct_cars": 2,
               "car_min_dist": 150,
               "dist_to_light": (150, 220),
               "img": "../images/cars/car_#.png",
               "height": 55,
               "car_limit": 10
               }

# Παράμετροι πεζών
ped_speed = 3
peds_params = {"pos": {"1": (-40, 340), "2": (760, 1130), "3": (1882, 740), "4": (1080, -40)},
               "direction_speed": {"1": (ped_speed, 0), "2": (0, -ped_speed), "3": (-ped_speed, 0), "4": (0, ped_speed)},
               "distinct_peds": 2,
               "num_of_steps": 2,
               "ped_min_dist": 50,
               "dist_to_light": (10, 50),
               "frames_to_next_step": 9,
               "img": "../images/pedestrians/Person_#_$.png",
               "height": 36,
               "pedestrian_limit": 10
               }

# Παράμετροι κουμπιών
# Κουμπί παύσης
pause_params = {"pos": (1200, 50), "img": "../images/buttons/pause_btn.png"}

# Κουμπί λειτουργίας
op_btn_params = {"pos": (1300, 50),
                 "images": ("../images/buttons/on_off_grn.png", "../images/buttons/on_off_red.png")}
