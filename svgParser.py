from svgpathtools import svg2paths, path
import matplotlib.pyplot as plt

straight1 = r"C:\Users\alecl\De Haagse Hogeschool\Sophia Elzinga (24022772) - project 4\documenten\Code\Finmo-Non-Treble\svg\noHomo1.svg"
straight2 = r"/home/user/Documents/ProjectFinmo/Finmo-Non-Treble/svg/noHomo2.svg"
squiggly1 = r"/home/user/Documents/ProjectFinmo/Finmo-Non-Treble/svg/squiggly1.svg"
squiggly2 = r"/home/user/Documents/ProjectFinmo/Finmo-Non-Treble/svg/squiggly2.svg"
ziggert1 = r"/home/user/Documents/ProjectFinmo/Finmo-Non-Treble/svg/ziggert1.svg"
ziggert2 = r"/home/user/Documents/ProjectFinmo/Finmo-Non-Treble/svg/ziggert2.svg"

xPath1 = []
yPath1 = []
xPath2 = []
yPath2 = []

def svgToCoords(path1, path2):
    global xPath1, yPath1, xPath2, yPath2

    xPath1.clear()
    yPath1.clear()
    xPath2.clear()
    yPath2.clear()

    paths, attributes = svg2paths(path1)

    path = paths[0]
    print(path)

    for path in paths:

        for segment in path:

            for i in range(100):

                t = i / 99

                point = segment.point(t)

                x = point.real
                y = point.imag

                xPath1.append(x)
                yPath1.append(y)

    paths, attributes = svg2paths(path2)

    path = paths[0]

    for path in paths:

        for segment in path:

            for i in range(100):

                t = i / 99

                point = segment.point(t)

                x = point.real
                y = point.imag

                xPath2.append(x)
                yPath2.append(y)

svgToCoords(squiggly1, squiggly2)
print(yPath1[0])
print(yPath1[99])
print(yPath2[0])
print(yPath2[99])