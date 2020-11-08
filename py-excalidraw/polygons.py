# https://gist.github.com/lipis/c148134151ac57b7f5df62cba69a4ee4
# https://excalidraw.com/?addLibrary=https://gist.githubusercontent.com/lipis/c148134151ac57b7f5df62cba69a4ee4/raw/033c8a8353db224beff34f3024e3cbe21f182c30/polygons.excalidrawlib
# https://excalidraw.com/#json=5666429063921664,h0yDjfkDndzI10H-OnNEcA

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
        fillStyle="solid",
        backgroundColor=excalidraw.BACKGROUND[index + 3],
    )

scene.save_as("polygons")
scene.save_as_lib("polygons")
