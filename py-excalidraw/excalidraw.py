import json
import random
import hashlib
import copy

RND = 4

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
    return (
        round(box[1][0] - box[0][0], RND),
        round(box[1][1] - box[0][1], RND),
    )


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
            "angle": angle,
            "fillStyle": fillStyle,
            "groupIds": [],  # Libs don't work without it
            "opacity": 100,
            "roughness": roughness,
            "seed": random.randint(1_000_000, 100_000_000),
            "strokeColor": STROKE[0],
            "strokeSharpness": strokeSharpness,
            "strokeWidth": strokeWidth,
            "type": element_type,
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
        element = self.__new_element("rectangle", **kargs)
        element["x"] = x
        element["y"] = y
        element["width"] = width
        element["height"] = height
        element["strokeColor"] = strokeColor
        element["backgroundColor"] = backgroundColor
        self.add_element(element)

    def add_ellipse(
        self,
        x,
        y,
        width,
        height,
        strokeColor=STROKE[0],
        backgroundColor=BACKGROUND[0],
        **kargs,
    ):
        element = self.__new_element("ellipse", **kargs)
        element["x"] = x
        element["y"] = y
        element["width"] = width
        element["height"] = height
        element["strokeColor"] = strokeColor
        element["backgroundColor"] = backgroundColor
        self.add_element(element)

    def add_line(
        self,
        x,
        y,
        points,
        strokeColor=STROKE[0],
        backgroundColor=BACKGROUND[0],
        **kargs,
    ):
        element = self.__new_element("line", **kargs)
        element["x"] = x
        element["y"] = y
        element["points"] = points
        element["strokeColor"] = strokeColor
        element["backgroundColor"] = backgroundColor
        element["width"], element["height"] = width_height(bounding_box(points))
        self.add_element(element)

    def save_as(self, filename):
        filename = filename if filename.find(".") > -1 else f"{filename}.excalidraw"
        with open(filename, "w") as excalidraw_file:
            json.dump(self.data, excalidraw_file, indent=2, sort_keys=True)
        print(f"File saved {filename}")

    def save_as_lib(self, filename):
        filename = filename if filename.find(".") > -1 else f"{filename}.excalidrawlib"
        for element in self.data["elements"]:
            self.lib["library"].append([element])
        with open(filename, "w") as excalidraw_lib_file:
            json.dump(self.lib, excalidraw_lib_file, indent=2, sort_keys=True)
        print(f"File saved {filename}")

    def add_element(self, element):
        self.data["elements"].append(self.normalize_element(element))

    def normalize_element(self, element):
        if "width" in element:
            element["width"] = round(element["width"], RND)
        if "height" in element:
            element["height"] = round(element["height"], RND)
        if "x" in element:
            element["x"] = round(element["x"], RND)
        if "y" in element:
            element["y"] = round(element["y"], RND)
        if "points" in element:
            element["points"] = [
                [round(p[0], RND), round(p[1], RND)] for p in element["points"]
            ]

        # generate the ID based on the elements data, withouth the seed
        data = copy.copy(element)
        del data["seed"]
        element["id"] = hashlib.md5(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()

        return element
