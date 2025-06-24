import matplotlib.pyplot as plt
import numpy as np

class Map:
    def __init__(self, poles, car_position, path):
        """
        poles: list of tuples (x, y)
        car_position: ((x, y), angle) -- initial car position and direction in degrees
        path: list of tuples [(x1, y1), (x2, y2), ...]
        """
        self.Poles = poles
        self.CarPosition = car_position
        self.Path = path

        # Set up the figure
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.ax.grid(True)

        # Draw the initial content
        self._draw()

        # Show the map
        plt.ion()
        plt.show()

    def _draw(self):
        self.ax.clear()
        self.ax.set_aspect('equal')
        self.ax.grid(True)

        # Draw poles
        for (x, y) in self.Poles:
            self.ax.plot(x, y, 'ro', markersize=10)

        # Draw path
        if len(self.Path) >= 2:
            xs, ys = zip(*self.Path)
            self.ax.plot(xs, ys, 'b-', linewidth=2)

        # Draw car
        (x, y), angle = self.CarPosition
        self.ax.plot(x, y, 'go', markersize=8)

        # Draw car direction
        if angle is not None:
            self.ax.text(x, y, f'Angle: {angle}°', fontsize=10, ha='right')
            angle_rad = np.deg2rad(angle)
            dx = 0.5 * np.cos(angle_rad)
            dy = 0.5 * np.sin(angle_rad)
            self.ax.arrow(x, y, dx, dy, head_width=0.2, head_length=0.2, fc='g', ec='g')

        # Set axis limits
        all_x = [p[0] for p in self.Poles] + [p[0] for p in self.Path] + [x]
        all_y = [p[1] for p in self.Poles] + [p[1] for p in self.Path] + [y]

        if all_x and all_y:
            self.ax.set_xlim(min(all_x) - 1, max(all_x) + 1)
            self.ax.set_ylim(min(all_y) - 1, max(all_y) + 1)

        # Update the plot
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def updateCar(self, new_position):
        """
        new_position: ((x, y), angle)
        """
        self.CarPosition = new_position
        self._draw()

    def update_path(self, new_path):
        self.Path = new_path
        self._draw()

# Example usage
if __name__ == "__main__":
    poles = [(2, 3), (5, 5), (7, 2)]
    car = ((1, 1), None)
    path = [(1, 1), (2, 2), (3, 3), (6.2, 5.5)]

    map_view = Map(poles, car, path)

    # Simulate car movement (path is fixed)
    import time
    for i in range(10):
        new_pos = ((1 + i * 0.5, 1 + i * 0.3), None)
        map_view.updateCar(new_pos)
        time.sleep(0.5)
