# https://gist.github.com/lipis/c148134151ac57b7f5df62cba69a4ee4
# https://excalidraw.com/?addLibrary=https://gist.githubusercontent.com/lipis/c148134151ac57b7f5df62cba69a4ee4/raw/b4b9bfa27c7399ebb6e4390fdfae2162ff768b39/polygons.excalidrawlib
# https://excalidraw.com/#json=5636464553492480,cBE2J8KaCrIGGucL7UpGbg

import excalidraw
import math

scene = excalidraw.Excalidraw()

radius = 80
initial_angle = 3 * math.pi / 2

polygons = [3, 5, 6, 8, 10, 12]

for index, polygon in enumerate(polygons):
    points = []
    for point in range(polygon + 1):
        # source: https://stackoverflow.com/a/7198179/8418
        points.append(
            [
                radius * math.cos(2 * math.pi * point / polygon + initial_angle),
                radius * math.sin(2 * math.pi * point / polygon + initial_angle),
            ]
        )
    scene.add_line(
        (index % 3) * (radius * 2 + radius / 2),
        (index // 3) * (radius * 2 + radius / 2),
        points,
        strokeSharpness="sharp",
        fillStyle="solid",
        backgroundColor=excalidraw.BACKGROUND[index + 3],
    )

scene.save_as("polygons")
scene.save_as_lib("polygons")
