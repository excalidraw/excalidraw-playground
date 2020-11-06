import json
import random

CANVAS = [
    "#ffffff",
    "#f8f9fa",
    "#f1f3f5",
    "#fff5f5",
    "#fff0f6",
    "#f8f0fc",
    "#f3f0ff",
    "#edf2ff",
    "#e7f5ff",
    "#e3fafc",
    "#e6fcf5",
    "#ebfbee",
    "#f4fce3",
    "#fff9db",
    "#fff4e6",
]

BACKGROUND = [
    "transparent",
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

STROKE = [
    "#000000",
    "#343a40",
    "#495057",
    "#c92a2a",
    "#a61e4d",
    "#862e9c",
    "#5f3dc4",
    "#364fc7",
    "#1864ab",
    "#0b7285",
    "#087f5b",
    "#2b8a3e",
    "#5c940d",
    "#e67700",
    "#d9480f",
]

# source: https://stackoverflow.com/a/46336730/8418
def bounding_box(points):
    x_coordinates, y_coordinates = zip(*points)
    return [
        (min(x_coordinates), min(y_coordinates)),
        (max(x_coordinates), max(y_coordinates)),
    ]


def width_height(box):
    return box[1][0] - box[0][0], box[1][1] - box[0][1]


class Excalidraw:
    data = {
        "version": 2,
        "type": "excalidraw",
        "source": "py-excalidraw",
        "elements": [],
        "appState": {"viewBackgroundColor": CANVAS[0]},
    }

    lib = {"type": "excalidrawlib", "version": 1, "library": []}

    def __new_element(
        self,
        element_type,
        angle=0,
        roughness=1,
        strokeWidth=1,
        fillStyle="hachure",
        strokeSharpness="round",
    ):
        return {
            "type": element_type,
            "opacity": 100,
            "seed": random.randint(1000000, 100000000),
            "strokeColor": STROKE[0],
            "fillStyle": fillStyle,
            "strokeWidth": strokeWidth,
            "roughness": roughness,
            "strokeSharpness": strokeSharpness,
            "angle": angle,
        }

    def add_rectangle(
        self,
        x,
        y,
        width,
        height,
        strokeColor=STROKE[0],
        backgroundColor=BACKGROUND[0],
        **kargs,
    ):
        rectangle = self.__new_element("rectangle", **kargs)
        rectangle["x"] = x
        rectangle["y"] = y
        rectangle["width"] = width
        rectangle["height"] = height
        rectangle["strokeColor"] = strokeColor
        rectangle["backgroundColor"] = backgroundColor
        self.data["elements"].append(rectangle)

    def add_line(
        self,
        x,
        y,
        points,
        strokeColor=STROKE[0],
        backgroundColor=BACKGROUND[0],
        **kargs,
    ):
        line = self.__new_element("line", **kargs)
        line["x"] = x
        line["y"] = y
        line["points"] = points
        line["strokeColor"] = strokeColor
        line["backgroundColor"] = backgroundColor
        line["width"], line["height"] = width_height(bounding_box(points))
        self.data["elements"].append(line)

    def save_as(self, filename):
        filename = filename if filename.find(".") > -1 else f"{filename}.excalidraw"
        with open(filename, "w") as excalidraw_file:
            json.dump(self.data, excalidraw_file, indent=2)
        print(f"File saved {filename}")

    def save_as_lib(self, filename):
        filename = filename if filename.find(".") > -1 else f"{filename}.excalidrawlib"
        for element in self.data["elements"]:
            self.lib["library"].append([element])
        with open(filename, "w") as excalidraw_lib_file:
            json.dump(self.lib, excalidraw_lib_file, indent=2)
        print(f"File saved {filename}")

    def get_data(self):
        return self.data
