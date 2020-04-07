import excalidraw

scene = excalidraw.Excalidraw()

size = 32
width = 16

for column in range(size):
    for row in range(size):
        red = row * 256 // size
        green = column * 256 // size
        blue = column * 256 // size

        color = "#%02x%02x%02x" % (red, green, blue)
        scene.add_rectangle(
            row * size,
            column * size,
            size,
            size,
            backgroundColor=color,
            fillStyle="solid",
        )

scene.save_as("hola")
print(f"Total objects {size * size}")
