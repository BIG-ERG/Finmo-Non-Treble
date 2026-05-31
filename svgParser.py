from svgpathtools import svg2paths, path
import matplotlib.pyplot as plt

straight = r"/home/user/Documents/ProjectFinmo/Finmo-Non-Treble/svg/noHomo.svg"
squiggly = r"/home/user/Documents/ProjectFinmo/Finmo-Non-Treble/svg/squiggly.svg"
ziggert = r"/home/user/Documents/ProjectFinmo/Finmo-Non-Treble/svg/ziggert.svg"


paths, attributes = svg2paths(straight)

print(paths)

path = paths[0]

points = []

for path in paths:

    for segment in path:

        for i in range(100):

            t = i / 99

            point = segment.point(t)

            x = point.real
            y = point.imag

            points.append(x)

print(paths)
