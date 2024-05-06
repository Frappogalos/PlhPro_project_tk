import tkinter as tk
from itertools import cycle
from PIL import Image, ImageTk

class TrafficLightApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Traffic Light")
        self.master.geometry("1000x1000")

        self.car_images = {
            "off": "../images/traffic_lights/car_off.png",
            "red": "../images/traffic_lights/car_red.png",
            "orange": "../images/traffic_lights/car_orange.png",
            "green": "../images/traffic_lights/car_green.png"
        }
        self.pedestrian_images = {
            "off": "../images/traffic_lights/pedestrian_off.png",
            "red": "../images/traffic_lights/pedestrian_red.png",
            "green": "../images/traffic_lights/pedestrian_green.png"
        }
        self.current_car_image = cycle(self.car_images.values())
        self.current_pedestrian_image = cycle(self.pedestrian_images.values())

        self.double_intersection_image_path = "../images/double_intersection.jpg"

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # Load background image and resize
        self.bg_image_path = "../images/double_intersection.jpg"
        self.bg_image = Image.open(self.bg_image_path)
        self.bg_image_resized = self.bg_image.resize(
            (self.master.winfo_screenwidth(), self.master.winfo_screenheight()), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image_resized)

        # Add background image to label
        self.background_label = tk.Label(self.frame, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.car_canvas = tk.Canvas(self.frame, width=75, height=27, highlightthickness=0)
        self.car_canvas.grid(row=2, column=1, padx=20, pady=20)

        self.car_canvas_2= tk.Canvas(self.frame, width=75, height=27, highlightthickness=0)
        self.car_canvas_2.grid(row=3, column=1, padx=20, pady=20)

        self.car_canvas_3 = tk.Canvas(self.frame, width=100, height=100, highlightthickness=0)
        self.car_canvas_3.grid(row=4, column=2, padx=20, pady=20)

        self.car_canvas_4 = tk.Canvas(self.frame, width=100, height=100, highlightthickness=0)
        self.car_canvas_4.grid(row=4, column=3, padx=20, pady=20)

        self.car_canvas_5 = tk.Canvas(self.frame, width=150, height=80, highlightthickness=0)
        self.car_canvas_5.grid(row=2, column=4, padx=20, pady=20)

        self.car_canvas_6 = tk.Canvas(self.frame, width=150, height=80, highlightthickness=0)
        self.car_canvas_6.grid(row=3, column=4, padx=20, pady=20)

        self.car_canvas_7 = tk.Canvas(self.frame, width=150, height=105, highlightthickness=0)
        self.car_canvas_7.grid(row=1, column=2, padx=20, pady=20)

        self.car_canvas_8 = tk.Canvas(self.frame, width=150, height=105, highlightthickness=0)
        self.car_canvas_8.grid(row=1, column=3, padx=20, pady=20)


        self.pedestrian_canvas = tk.Canvas(self.frame, width=40, height=30, highlightthickness=0)
        self.pedestrian_canvas.grid(row=2, column=0, padx=20, pady=20)

        self.pedestrian_canvas_2 = tk.Canvas(self.frame, width=40, height=30, highlightthickness=0)
        self.pedestrian_canvas_2.grid(row=3, column=0, padx=20, pady=20)

        self.pedestrian_canvas_3 = tk.Canvas(self.frame, width=150, height=105, highlightthickness=0)
        self.pedestrian_canvas_3.grid(row=5, column=2, padx=20, pady=20)

        self.pedestrian_canvas_4 = tk.Canvas(self.frame, width=150, height=105, highlightthickness=0)
        self.pedestrian_canvas_4.grid(row=5, column=3, padx=20, pady=20)

        self.pedestrian_canvas_5 = tk.Canvas(self.frame, width=150, height=105, highlightthickness=0)
        self.pedestrian_canvas_5.grid(row=2, column=5, padx=20, pady=20)

        self.pedestrian_canvas_6 = tk.Canvas(self.frame, width=150, height=105, highlightthickness=0)
        self.pedestrian_canvas_6.grid(row=3, column=5, padx=20, pady=20)

        self.pedestrian_canvas_7 = tk.Canvas(self.frame, width=150, height=105, highlightthickness=0)
        self.pedestrian_canvas_7.grid(row=0, column=2, padx=20, pady=20)

        self.pedestrian_canvas_8 = tk.Canvas(self.frame, width=150, height=105, highlightthickness=0)
        self.pedestrian_canvas_8.grid(row=0, column=3, padx=20, pady=20)


        self.update_lights()

    def update_lights(self):

        car_image_path = next(self.current_car_image)
        car_image = Image.open(car_image_path)
        self.car_image_tk = ImageTk.PhotoImage(car_image)
        self.car_canvas.create_image(0, 0, anchor="nw", image=self.car_image_tk)
        self.car_canvas_2.create_image(0, 0, anchor="nw", image=self.car_image_tk)

        rotated_car_image = car_image.rotate(90, expand=True)
        self.car_image_tk_rotated = ImageTk.PhotoImage(rotated_car_image)
        self.car_canvas_3.create_image(75, 52, anchor="center", image=self.car_image_tk_rotated)
        self.car_canvas_4.create_image(75, 52, anchor="center", image=self.car_image_tk_rotated)

        rotated_car_image1 = car_image.rotate(180, expand=True)
        self.car_image_tk_rotated1 = ImageTk.PhotoImage(rotated_car_image1)
        self.car_canvas_5.create_image(75, 52, anchor="center", image=self.car_image_tk_rotated1)
        self.car_canvas_6.create_image(75, 52, anchor="center", image=self.car_image_tk_rotated1)

        rotated_car_image2 = car_image.rotate(270, expand=True)
        self.car_image_tk_rotated2 = ImageTk.PhotoImage(rotated_car_image2)
        self.car_canvas_7.create_image(75, 52, anchor="center", image=self.car_image_tk_rotated2)
        self.car_canvas_8.create_image(75, 52, anchor="center", image=self.car_image_tk_rotated2)

        pedestrian_image_path = next(self.current_pedestrian_image)
        pedestrian_image = Image.open(pedestrian_image_path)
        self.pedestrian_image_tk = ImageTk.PhotoImage(pedestrian_image)
        self.pedestrian_canvas.create_image(0, 0, anchor="nw", image=self.pedestrian_image_tk)
        self.pedestrian_canvas_2.create_image(0, 0, anchor="nw", image=self.pedestrian_image_tk)

        rotated_pedestrian_image = pedestrian_image.rotate(90, expand=True)
        self.pedestrian_image_tk_rotated = ImageTk.PhotoImage(rotated_pedestrian_image)
        self.pedestrian_canvas_3.create_image(75, 52, anchor="center", image=self.pedestrian_image_tk_rotated)
        self.pedestrian_canvas_4.create_image(75, 52, anchor="center", image=self.pedestrian_image_tk_rotated)

        rotated_pedestrian_image1 = pedestrian_image.rotate(180, expand=True)
        self.pedestrian_image_tk_rotated1 = ImageTk.PhotoImage(rotated_pedestrian_image1)
        self.pedestrian_canvas_5.create_image(75, 52, anchor="center", image=self.pedestrian_image_tk_rotated1)
        self.pedestrian_canvas_6.create_image(75, 52, anchor="center", image=self.pedestrian_image_tk_rotated1)

        rotated_pedestrian_image2 = pedestrian_image.rotate(270, expand=True)
        self.pedestrian_image_tk_rotated2 = ImageTk.PhotoImage(rotated_pedestrian_image2)
        self.pedestrian_canvas_7.create_image(75, 52, anchor="center", image=self.pedestrian_image_tk_rotated2)
        self.pedestrian_canvas_8.create_image(75, 52, anchor="center", image=self.pedestrian_image_tk_rotated2)


        current_car_state = car_image_path.split("/")[-1].split("_")[-1].split(".")[0]
        if current_car_state == "green":
            next_car_state1 = "green"
            next_pedestrian_state = "green"
            next_car_state = "red"
            next_pedestrian_state2 = "red"
        elif current_car_state == "red":
            next_car_state1 = "red"
            next_pedestrian_state = "red"
            next_car_state = "orange"
            next_pedestrian_state2 = "green"
        elif current_car_state == "orange":
            next_car_state1 = "orange"
            next_pedestrian_state = "off"
            next_car_state = "green"
            next_pedestrian_state2 = "off"
        else:
            next_car_state1 = "off"
            next_pedestrian_state = "off"
            next_car_state = "off"
            next_pedestrian_state2 = "off"



        car_image_path_rotated = self.car_images[next_car_state]
        car_image_rotated = Image.open(car_image_path_rotated)
        self.car_image_tk_rotated = ImageTk.PhotoImage(car_image_rotated.rotate(90, expand=True))
        self.car_canvas_3.create_image(75, 52, anchor="center", image=self.car_image_tk_rotated)
        self.car_canvas_4.create_image(75, 52, anchor="center", image=self.car_image_tk_rotated)

        car_image_path_rotated2 = self.car_images[next_car_state1]
        car_image_rotated2 = Image.open(car_image_path_rotated2)
        self.car_image_tk_rotated2 = ImageTk.PhotoImage(car_image_rotated2.rotate(180, expand=True))
        self.car_canvas_5.create_image(75, 52, anchor="center", image=self.car_image_tk_rotated2)
        self.car_canvas_6.create_image(75, 52, anchor="center", image=self.car_image_tk_rotated2)

        car_image_path_rotated1 = self.car_images[next_car_state]
        car_image_rotated1 = Image.open(car_image_path_rotated1)
        self.car_image_tk_rotated1 = ImageTk.PhotoImage(car_image_rotated1.rotate(270, expand=True))
        self.car_canvas_7.create_image(75, 52, anchor="center", image=self.car_image_tk_rotated1)
        self.car_canvas_8.create_image(75, 52, anchor="center", image=self.car_image_tk_rotated1)


        pedestrian_image_path = self.pedestrian_images[next_pedestrian_state]
        pedestrian_image = Image.open(pedestrian_image_path)
        self.pedestrian_image_tk = ImageTk.PhotoImage(pedestrian_image)
        self.pedestrian_canvas.create_image(0, 0, anchor="nw", image=self.pedestrian_image_tk)
        self.pedestrian_canvas_2.create_image(0, 0, anchor="nw", image=self.pedestrian_image_tk)

        rotated_pedestrian_image_path1 = self.pedestrian_images[next_pedestrian_state]  # Χρησιμοποίησε την κατάσταση του next_car_state
        rotated_pedestrian_image1 = Image.open(rotated_pedestrian_image_path1)
        self.rotated_pedestrian_image_tk1 = ImageTk.PhotoImage(rotated_pedestrian_image1.rotate(180, expand=True))
        self.pedestrian_canvas_5.create_image(75, 52, anchor="center", image=self.rotated_pedestrian_image_tk1)
        self.pedestrian_canvas_6.create_image(75, 52, anchor="center", image=self.rotated_pedestrian_image_tk1)

        rotated_pedestrian_image_path2 = self.pedestrian_images[next_pedestrian_state2]  # Χρησιμοποίησε την κατάσταση του next_car_state
        rotated_pedestrian_image2 = Image.open(rotated_pedestrian_image_path2)
        self.rotated_pedestrian_image_tk2 = ImageTk.PhotoImage(rotated_pedestrian_image2.rotate(270, expand=True))
        self.pedestrian_canvas_7.create_image(75, 52, anchor="center", image=self.rotated_pedestrian_image_tk2)
        self.pedestrian_canvas_8.create_image(75, 52, anchor="center", image=self.rotated_pedestrian_image_tk2)

        rotated_pedestrian_image_path = self.pedestrian_images[next_pedestrian_state2]  # Χρησιμοποίησε την κατάσταση του next_car_state
        rotated_pedestrian_image = Image.open(rotated_pedestrian_image_path)
        self.rotated_pedestrian_image_tk = ImageTk.PhotoImage(rotated_pedestrian_image.rotate(90, expand=True))
        self.pedestrian_canvas_3.create_image(75, 52, anchor="center", image=self.rotated_pedestrian_image_tk)
        self.pedestrian_canvas_4.create_image(75, 52, anchor="center", image=self.rotated_pedestrian_image_tk)

        self.master.after(1000, self.update_lights)

def main():
    root = tk.Tk()
    app = TrafficLightApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
# Έχω χύσει το αίμα μου αν μπορείτε συνεχίστε το
