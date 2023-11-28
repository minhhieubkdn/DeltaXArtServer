import matplotlib.pyplot as plt
import json
import constant as ct

from dots_object import *

def m_round(num=0.123456):
    num = int(num * 10000)
    num = num / 10000
    return num

class DotExportor():
    def __init__(self) -> None:
        pass

    def scaleToRobotRange(self, path, x, y, w, h):
        points = []
        for (px, py) in path:
            mx = m_round(x + px / 500 * (w/2))
            my = m_round(y + py / 500 * (h/2))
            points.append((mx, my))

        return points
    
    def calculate_z_value(self, x, y):

        p1 = ct.THREE_POINTS_PLANE[0]
        p2 = ct.THREE_POINTS_PLANE[1]
        p3 = ct.THREE_POINTS_PLANE[2]

        v1 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
        v2 = [p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]]

        normal = [v1[1] * v2[2] - v1[2] * v2[1],
                  v1[2] * v2[0] - v1[0] * v2[2],
                  v1[0] * v2[1] - v1[1] * v2[0]]

        D = -(normal[0] * p1[0] + normal[1] * p1[1] + normal[2] * p1[2])

        z = (-normal[0] * x - normal[1] * y - D) / normal[2]
        return z

    def export_gcodes(self, filename="data/users/admin/SpiderMan.json"):
        with open(filename, 'r') as f:
            json_data = json.load(f)

        fig, ax = plt.subplots()

        frame_points = []
        frame_path = [(-500, 500), (500, 500),
                      (500, -500), (-500, -500), (-500, 500)]

        frame_points = self.scaleToRobotRange(frame_path, -25, -170, 200, 200)
        print("frame_points: ", frame_points)

        x, y = zip(*frame_points)
        ax.plot(x, y)

        rects = json_data['rects']
        points = []
        for rect in rects:
            points.append((rect['x'], rect['y']))

        real_points = self.scaleToRobotRange(points, -25, -170, 200, 200)

        gcodes = []
        gcodes.append("G01 X{} Y{} Z{}".format(0, -170, ct.Z_SAFE))
        
        for point in real_points:
            z = self.calculate_z_value(point[0], point[1])
            gcodes.append("G01 X{} Y{}".format(point[0], point[1]))
            gcodes.append("G01 Z{}".format(z))
            gcodes.append("G04 P100")
            gcodes.append("G01 Z{}".format(ct.Z_SAFE))

        with open(filename[0:filename.find(".json")] + '.gcode', 'w') as file:
            for gcode in gcodes:
                # print(gcode)
                file.write(gcode + '\n')

        x_coords = [point[0] for point in real_points]
        y_coords = [point[1] for point in real_points]

        # Plot the points
        plt.scatter(x_coords, y_coords, s=2)

        # Add labels and title
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Plot of Points')

        plt.show()

        return frame_points

if __name__ == "__main__":
    ex = DotExportor()
    ex.export_gcodes("data/users/admin/SpiderMan.json")
