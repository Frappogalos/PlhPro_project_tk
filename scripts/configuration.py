# Background image
# Σχετική διεύθυνση που βρίσκεται η φωτογραφία
# του φόντου
bg_image = "../images/double_intersection.jpg"
# Σχετική διεύθυνση που βρίσκεται η φωτογραφία
# που θα χρησιμοποιηθεί για το εικονίδιο του
# παραθύρου
window_icon_image = "../images/window_icon.png"

# Παράμετροι σηματοδοτών αυτοκινήτων και πεζών
light_params = {"pos": {"car_tl": [{"1": (780, 700), "2": (1030, 700), "3": (1040, 380)}],
                        "ped_lights": [{1: [{"direction": 4, "phase": "off", "pos": (680, 340)},
                                            {"direction": 2, "phase": "off", "pos": (680, 740)}
                                            ],
                                        2: [{"direction": 1, "phase": "off", "pos": (760, 280)},
                                            {"direction": 3, "phase": "off", "pos": (1070, 280)},
                                            {"direction": 1, "phase": "off", "pos": (760, 800)},
                                            {"direction": 3, "phase": "off", "pos": (1070, 800)}
                                            ],
                                        3: [{"direction": 4, "phase": "off", "pos": (1150, 340)},
                                            {"direction": 2, "phase": "off", "pos": (1150, 740)}
                                            ]
                                        }
                                       ]
                        },
                "img": "../images/traffic_lights/car_#.png",
                "height": 120,
                "ped_config": {"img": "../images/traffic_lights/pedestrian_#.png",
                               "height": 110,
                               "timer_pos": {1: (-38, 0), 2: (0, 38), 3: (38, 0), 4: (0, -38)}
                               }
                }

# Παράμετροι αυτοκινήτων
cars_params = {"pos": {"1": [(-100, 645), (-100, 570)], "2": [(870, 1180), (960, 1180)],
                       "3": [(1932, 440), (1932, 510)], "4": []},
               "cars_speed_range": (4, 8),
               "default_car_speed": 6,
               "distinct_cars": 2,
               "car_min_dist": 150,
               "dist_to_light": (150, 220),
               "img": "../images/cars/car_#.png",
               "height": 55,
               "car_limit": 10,
               "car_time_interval": 4
               }

# Παράμετροι πεζών
peds_params = {"pos": {"1": (-40, 340), "2": (760, 1130), "3": (1882, 740), "4": (1080, -40)},
               "ped_speed": 3,
               "distinct_peds": 2,
               "num_of_steps": 2,
               "ped_min_dist": 50,
               "dist_to_light": (10, 50),
               "frames_to_next_step": 9,
               "img": "../images/pedestrians/Person_#_$.png",
               "height": 36,
               "pedestrian_limit": 10,
               "ped_time_interval": 4000
               }

# Παράμετροι κουμπιών
# Κουμπί παύσης
pause_params = {"pos": (1200, 50), "img": "../images/buttons/pause_btn.png"}

# Κουμπί λειτουργίας
op_btn_params = {"pos": (1300, 50),
                 "images": ("../images/buttons/on_off_grn.png", "../images/buttons/on_off_red.png")}

# Κουμπί ελέγχου ταχύτητας οχημάτων
car_spinbox = {"pos": (1450, 80)}
