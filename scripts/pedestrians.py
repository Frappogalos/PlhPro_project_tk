from cars import Car


class Pedestrian(Car):
	def __init__(self, image, direction, lane, canvas, window):
		super().__init__(image, direction, lane, canvas, window)