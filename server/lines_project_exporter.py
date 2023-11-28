from lines_object import *

def m_round(num=0.123456):
    num = int(num * 10000)
    num = num / 10000
    return num


class LinesExportor():
    def __init__(self, icon_path="data/users/admin/E=mc2.json"):
        self.icon_path = icon_path

    def get_raw_path(self):
        with open(self.icon_path, 'r') as f:
            json_data = json.load(f)

        ob = lines_object_from_dict(json_data)
        m_lines = []
        for line in ob.lines:
            m_line = []

            for dot in line.line:
                m_line.append((m_round(dot.x), m_round(dot.y)))

            m_lines.append(m_line.copy())

        # print(m_lines)

        return m_lines

    def createEmc2Path(self, x=0, y=0, w=0, h=0):
        
        # emc2_path = [[(190.658, 324.655), (115.619, 324.655), (40.581, 324.655), (40.581, 398.544), (40.581, 472.434), (40.581, 546.214), (40.581, 620.214), (126, 620.214), (212.098, 620.214)],
        #               [(40.581, 470.137), (100.03, 470.137), (160.03, 470.137)],
        #               [(287.136, 516.079), (342.396, 516.079), (397.396, 516.079)],
        #                 [(276.416, 617.151), (340.053, 617.151), (405.053, 617.151)],
        #                 [(480.091, 465.543), (480.091, 538.557), (480.091, 612.557)],
        #                 [(480.091, 528.33), (507.656, 508.548), (521.439, 498.297), (533.69, 488.514), (550.535, 480.857), (567.381, 473.2), (585.758, 471.669), (601.071, 483.92), (608.728, 500.765), (611.791, 519.142), (613.323, 537.519), (613.323, 555.895), (613.323, 574.272), (613.323, 592.649), (613.323, 611.026)],
        #                 [(613.323, 520.485), (636.294, 497.234), (648.545, 485.451), (665.39, 476.263), (683.767, 474.732), (702.143, 479.326), (718.989, 488.514), (726.646, 505.359), (728.177, 523.736), (729.709, 542.113), (729.709, 560.49), (729.709, 578.866), (729.709, 597.243), (729.709, 615.62)],
        #                 [(861.408, 470.137), (843.032, 468.606), (824.655, 468.606), (807.81, 476.263), (794.027, 488.514), (781.776, 502.297), (771.056, 517.611), (767.993, 535.987), (764.931, 554.364), (764.931, 572.741), (772.588, 589.586), (789.433, 598.774), (806.278, 606.431), (824.655, 612.557), (843.032, 614.088), (861.408, 612.557), (878.254, 603.369), (895.099, 594.18)],
        #                 [(884.379, 359.877), (896.63, 346.094), (915.007, 341.5), (927.258, 355.283), (927.258, 373.66), (915.007, 387.442), (901.225, 399.693), (885.911, 410.413), (870.597, 421.133), (888.973, 421.196), (907.35, 421.664), (925.727, 421.133)]]
        
        emc2_path = self.get_raw_path()

        new_path = []
        for line in emc2_path:
            m_line = []
            for (px, py) in line:
                mx = x - (1000/2 - px) / 1000 * w
                my = y - (py - 1000/2) / 1000 * w

                m_line.append((mx, my))

            new_path.append(m_line.copy())
        return new_path

    def scaleToRobotRange(self, path, x, y, w, h):
        m_path = []
        for line in path:
            m_line = []
            for (px, py) in line:
                mx = m_round(x + px / 500 * (w/2))
                my = m_round(y + py / 500 * (h/2))
                m_line.append((mx, my))

            m_path.append(m_line.copy())

        # print(m_path)
        return m_path

    def export_gcodes(self, filename="data/users/admin/p1.json"):

        # print(filename)
        # with open("data/users/admin/" + filename + ".json", 'r') as f:
        #     json_data = json.load(f)

        with open(filename, 'r') as f:
            json_data = json.load(f)
        ob = dot_object_from_dict(json_data)
        gcodes = []

        frame_path = [[(-500, 354.5), (500, 354.5),
                       (500, -354.5), (-500, -354.5), (-500, 354.5)]]
        frame_in_ws = self.scaleToRobotRange(frame_path, 0, -170, 200, 200)
        print("frame_in_ws: ",frame_in_ws)
        fig, ax = plt.subplots()

        for line in frame_in_ws:
            x, y = zip(*line)
            ax.plot(x, y)

        gcodes.append("G01 X0 Y0 Z{0}".format(Z_SAFE))

        z = 0.0

        for i, (px, py) in enumerate(frame_in_ws[0]):
            z = m_round(self.calculate_z_value(px, py))
            gcodes.append("G01 X{0} Y{1} Z{2}".format(px, py, Z_SAFE))
            gcodes.append("G01 Z{0}".format(z))
            gcodes.append("G01 Z{0}".format(Z_SAFE))

        for rect in ob.rects:

            pirc = self.createEmc2Path(rect.x, rect.y, rect.w, rect.h)
            pirr = self.scaleToRobotRange(pirc, 0, -170, 200, 200)

            for line in pirr:
                for i, (x, y) in enumerate(line):
                    z = m_round(self.calculate_z_value(x, y))
                    if i == 0:
                        gcodes.append(
                            "G01 X{0} Y{1} Z{2}".format(x, y, Z_SAFE))
                        gcodes.append("G01 Z{0}".format(z))
                    else:
                        gcodes.append("G01 X{0} Y{1} Z{2}".format(x, y, z))

                gcodes.append("G01 Z{0}".format(Z_SAFE))

            for line in pirr:
                x, y = zip(*line)
                ax.plot(x, y)
            
        # plt.show()

        with open(filename[0:filename.find('.json')] + '.gcode', 'w') as file:
            for gcode in gcodes:
                print(gcode)
                file.write(gcode + '\n')

        # return gcodes

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


if __name__ == "__main__":

    ex = LinesExportor("data/users/admin/E=mc2.json")

    # export each part
    ex.export_gcodes("data/users/admin/p1.json")

    # # export all part
    # for i in range(9):
    #     ex.export_gcodes("data/users/admin/p{0}.json".format(i+1))
