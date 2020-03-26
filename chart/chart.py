import json
import random

SOURCE = "data1.csv"
MAX_WIDTH = 600
MAX_HEIGHT = 400
COLORS = [
    "#ced4da",
    "#868e96",
    "#fa5252",
    "#e64980",
    "#be4bdb",
    "#7950f2",
    "#4c6ef5",
    "#228be6",
    "#15aabf",
    "#12b886",
    "#40c057",
    "#82c91e",
    "#fab005",
    "#fd7e14",
]

data = []

title_x = "X Axis"
title_y = "Y Axis"

excalidraw = {
    "version": 1,
    "type": "excalidraw",
    "elements": [],
    "appState": {"viewBackgroundColor": "#ffffff"},
}


def new_element(element_type):
    return {
        "type": element_type,
        "opacity": 100,
        "seed": random.randint(1000000, 100000000),
        "strokeColor": "#000000",
        "fillStyle": "hachure",
        "strokeWidth": 1,
        "roughness": 1,
        "opacity": 100,
    }


def new_arrow(x, y, width, height):
    arrow = new_element("arrow")
    arrow["x"] = x
    arrow["y"] = y
    arrow["width"] = width
    arrow["height"] = height
    arrow["points"] = [
        [x, y],
        [width, height],
    ]
    return arrow


def new_text(x, y, width, text):
    element = new_element("text")
    element["x"] = x
    element["y"] = y
    element["width"] = width
    element["height"] = 20
    element["text"] = text
    element["font"] = "16px Virgil"
    element["baseline"] = 14
    return element


def get_random_color():
    return random.choice(COLORS)


with open(SOURCE, "r") as file:
    header = False
    for line in file.readlines():
        if not header:
            title_x, title_y = line.split(",")
            header = True
        else:
            key, value = line.split(",")
            data.append([key, float(value)])

max_y = 0
max_x = len(data)

for key, value in data:
    max_y = max(max_y, value)

# Draw charts
width = MAX_WIDTH / max_x
gap = width / 8
x = 0
color = get_random_color()

for key, value in data:
    element = new_element("rectangle")
    element["x"] = x * width + gap
    element["y"] = -gap
    element["width"] = width - gap
    element["height"] = -value * (MAX_HEIGHT / max_y)
    element["backgroundColor"] = color

    excalidraw["elements"].append(element)
    excalidraw["elements"].append(new_text(x * width + gap, gap, width, key))
    x += 1


# Draw lines
excalidraw["elements"].append(new_arrow(0, 0, 0, -MAX_HEIGHT - width))
excalidraw["elements"].append(new_arrow(0, 0, MAX_WIDTH + width, 0))

with open("graph.excalidraw", "w") as excalidraw_file:
    json.dump(excalidraw, excalidraw_file, indent=2)
