from svgpathtools import svg2paths, path
import matplotlib.pyplot as plt

straight = r"C:\Users\alecl\De Haagse Hogeschool\Sophia Elzinga (24022772) - project 4\documenten\Code\svg\straight.svg"
squiggly = r"C:\Users\alecl\De Haagse Hogeschool\Sophia Elzinga (24022772) - project 4\documenten\Code\svg\squiggly.svg"
ziggert = r"C:\Users\alecl\De Haagse Hogeschool\Sophia Elzinga (24022772) - project 4\documenten\Code\svg\ziggert.svg"


paths, attributes = svg2paths(ziggert)

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

for i in range(len(points)):
    print(points[i])

