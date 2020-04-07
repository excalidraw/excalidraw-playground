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


class Excalidraw:
    data = {
        "version": 1,
        "type": "excalidraw",
        "source": "py-excalidraw",
        "elements": [],
        "appState": {"viewBackgroundColor": CANVAS[0]},
    }

    def __new_element(
        self, element_type, angle=0, roughness=1, strokeWidth=1, fillStyle="hachure"
    ):
        return {
            "type": element_type,
            "opacity": 100,
            "seed": random.randint(1000000, 100000000),
            "strokeColor": STROKE[0],
            "fillStyle": fillStyle,
            "strokeWidth": strokeWidth,
            "roughness": roughness,
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

    def save_as(self, filename):
        filename = filename if filename.find(".") > -1 else f"{filename}.excalidraw"
        with open(filename, "w") as excalidraw_file:
            json.dump(self.data, excalidraw_file, indent=2)
        print(f"File saved {filename}")

    def get_data(self):
        return self.data
