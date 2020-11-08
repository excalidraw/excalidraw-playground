import excalidraw
import math

scene = excalidraw.Excalidraw()

inner_radius = 30
outer_radius = 80

stars = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 32]

for index, star in enumerate(stars):
    points = []
    # source: https://www.xarg.org/2019/01/drawing-an-upright-star-polygon/
    for point in range(star * 2 + 1):
        alpha = (2 * point + 2 - star % 4) / (2 * star) * math.pi
        radius = inner_radius if 0 == point % 2 else outer_radius
        points.append([math.cos(alpha) * radius, math.sin(alpha) * radius])

    scene.add_line(
        (index % 4) * (outer_radius * 2 + outer_radius / 2),
        (index // 4) * (outer_radius * 2 + outer_radius / 2),
        points,
        strokeSharpness="sharp",
        fillStyle="solid",
        backgroundColor=excalidraw.BACKGROUND[index + 3],
    )

scene.save_as("stars")
scene.save_as_lib("stars")
