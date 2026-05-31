from svgpathtools import svg2paths, path
import matplotlib.pyplot as plt

straight = r"C:\Users\alecl\De Haagse Hogeschool\Sophia Elzinga (24022772) - project 4\documenten\Code\Finmo-Non-Treble\svg\straight.svg"
straight2 = r"C:\Users\alecl\De Haagse Hogeschool\Sophia Elzinga (24022772) - project 4\documenten\Code\Finmo-Non-Treble\svg\noHomo2.svg"
squiggly1 = r"C:\Users\alecl\De Haagse Hogeschool\Sophia Elzinga (24022772) - project 4\documenten\Code\Finmo-Non-Treble\svg\squiggly1.svg"
squiggly2 = r"C:\Users\alecl\De Haagse Hogeschool\Sophia Elzinga (24022772) - project 4\documenten\Code\Finmo-Non-Treble\svg\squiggly2.svg"
ziggert1 = r"C:\Users\alecl\De Haagse Hogeschool\Sophia Elzinga (24022772) - project 4\documenten\Code\Finmo-Non-Treble\svg\ziggert1.svg"
ziggert2 = r"C:\Users\alecl\De Haagse Hogeschool\Sophia Elzinga (24022772) - project 4\documenten\Code\Finmo-Non-Treble\svg\ziggert2.svg"

lookup = []
xPath = []
yPath = []

def build_lookup(svg_file):
    global lookup, xPath, yPath
    lookup.clear()
    xPath.clear()
    yPath.clear()   
    lookup[:] = [-1] * 297

    paths, _ = svg2paths(svg_file)

    for path in paths:
        for segment in path:
            for i in range(100):
                t = i / 99
                pt = segment.point(t)
                y_mm = round(pt.imag)
                xPath.append(pt.real)
                yPath.append(pt.imag)
                if 0 <= y_mm < 297:
                    lookup[y_mm] = pt.real


build_lookup(straight)

print (lookup)
print (yPath)